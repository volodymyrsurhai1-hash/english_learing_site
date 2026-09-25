import json
import re
import threading
import uuid
from pathlib import Path
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View


from apps.subscriptions.models import ActionType
from apps.subscriptions.services import QuotaService
from apps.dictionary.services import (
    get_or_generate_word,
    is_word_saved,
    save_word_for_user,
)
from apps.films.downloader import download_video
from apps.films.models import Film
from apps.films.progress import progress_tracker
from apps.films.subtitle_parser import load_bilingual_subtitles


def _execute_download_task(task_id: str, url: str, user: Any = None) -> None:
    try:
        result = download_video(url, task_id=task_id)

        if not result.success:
            clean_error = re.sub(
                r"\x1b\[[0-9;]*m", "", result.error or "Download failed"
            )
            progress_tracker.update_task(
                task_id=task_id,
                status="error",
                error=clean_error,
                message=clean_error,
            )
            return

        media_root = Path(settings.MEDIA_ROOT)
        video_rel = result.filepath.relative_to(media_root).as_posix()

        en_rel = ""
        ru_rel = ""
        for sub_file in result.subtitle_files:
            rel_path = sub_file.relative_to(media_root).as_posix()
            if ".en." in rel_path:
                en_rel = rel_path
            elif ".ru." in rel_path:
                ru_rel = rel_path

        film = Film.objects.create(
            title=result.title,
            youtube_url=url,
            video_file=video_rel,
            subtitle_en=en_rel,
            subtitle_ru=ru_rel,
        )

        if user and user.is_authenticated:
            QuotaService.consume(user, ActionType.VIDEO_DOWNLOAD)

        progress_tracker.update_task(
            task_id=task_id,
            status="completed",
            percent=100.0,
            film_id=film.pk,
            message="Download completed successfully!",
        )
    except Exception as exc:
        clean_error = re.sub(r"\x1b\[[0-9;]*m", "", str(exc))
        progress_tracker.update_task(
            task_id=task_id,
            status="error",
            error=clean_error,
            message=clean_error,
        )
    finally:
        connection.close()


class FilmListView(LoginRequiredMixin, ListView):
    model = Film
    template_name = "films/film_list.html"
    context_object_name = "films"


class FilmWatchView(LoginRequiredMixin, DetailView):
    model = Film
    template_name = "films/film_watch.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        film: Film = self.object

        media_root: Path = Path(settings.MEDIA_ROOT)
        en_path: Path = media_root / film.subtitle_en if film.subtitle_en else Path()
        ru_path: Path | None = (
            media_root / film.subtitle_ru if film.subtitle_ru else None
        )

        subtitles: list[dict[str, str | float]] = load_bilingual_subtitles(
            en_path, ru_path
        )

        has_ru: bool = any(bool(sub.get("ru")) for sub in subtitles)
        context["has_ru_subtitles"] = has_ru
        context["film"] = film
        context["other_films"] = Film.objects.all()
        context["media_url"] = settings.MEDIA_URL
        context["subtitles_json"] = json.dumps(subtitles, ensure_ascii=False)
        return context


class FilmDownloadView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not QuotaService.can_consume(request.user, ActionType.VIDEO_DOWNLOAD):
            messages.error(
                request,
                "Daily video download limit reached for your subscription plan.",
            )
            return redirect("films:list")

        url: str = request.POST.get("url", "").strip()
        if not url:
            messages.error(request, "YouTube URL is required.")
            return redirect("films:list")

        result = download_video(url)

        if not result.success:
            clean_error = re.sub(r"\x1b\[[0-9;]*m", "", result.error or "")
            messages.error(request, clean_error)
            return redirect("films:list")

        media_root: Path = Path(settings.MEDIA_ROOT)
        video_rel: str = result.filepath.relative_to(media_root).as_posix()

        en_rel: str = ""
        ru_rel: str = ""
        for sub_file in result.subtitle_files:
            rel_path: str = sub_file.relative_to(media_root).as_posix()
            if ".en." in rel_path:
                en_rel = rel_path
            elif ".ru." in rel_path:
                ru_rel = rel_path

        film: Film = Film.objects.create(
            title=result.title,
            youtube_url=url,
            video_file=video_rel,
            subtitle_en=en_rel,
            subtitle_ru=ru_rel,
        )
        QuotaService.consume(request.user, ActionType.VIDEO_DOWNLOAD)
        return redirect("films:watch", pk=film.pk)


class StartDownloadView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        if not request.user.is_authenticated:
            return JsonResponse(
                {"status": "error", "message": "Authentication required"},
                status=401,
            )

        if not QuotaService.can_consume(request.user, ActionType.VIDEO_DOWNLOAD):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Daily video download limit reached for your subscription plan.",
                },
                status=429,
            )

        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)
                url = data.get("url", "").strip()
            else:
                url = request.POST.get("url", "").strip()
        except Exception:
            url = ""

        if not url:
            return JsonResponse(
                {"status": "error", "message": "YouTube URL is required"},
                status=400,
            )

        task_id = str(uuid.uuid4())
        progress_tracker.start_task(task_id)

        thread = threading.Thread(
            target=_execute_download_task,
            args=(task_id, url, request.user),
            daemon=True,
        )
        thread.start()

        return JsonResponse({"status": "started", "task_id": task_id})


class DownloadProgressView(View):
    def get(self, request: HttpRequest, task_id: str) -> JsonResponse:
        state = progress_tracker.get_task(task_id)
        if state is None:
            return JsonResponse(
                {"status": "not_found", "message": "Task not found"},
                status=404,
            )

        return JsonResponse(
            {
                "status": state.status,
                "percent": state.percent,
                "speed": state.speed,
                "eta": state.eta,
                "message": state.message,
                "film_id": state.film_id,
                "error": state.error,
            }
        )


class TranslateWordView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        raw_word: str = request.GET.get("word", "").strip()

        if (
            "http://" in raw_word
            or "https://" in raw_word
            or "www." in raw_word
            or "/" in raw_word
        ):
            return JsonResponse(
                {"error": "Please enter an English word or phrase, not a URL."},
                status=400,
            )

        word_query: str = re.sub(r"^[^\w]+|[^\w]+$", "", raw_word).lower()
        if not word_query:
            return JsonResponse({"error": "Word is required"}, status=400)

        try:
            data: dict[str, Any] = get_or_generate_word(word_query)

            translation: str = ""
            meanings: list[Any] = data.get("meanings", [])
            if meanings and isinstance(meanings, list) and "ru" in meanings[0]:
                translation = str(meanings[0]["ru"]).strip()
            elif data.get("uses") and isinstance(data["uses"], list):
                translation = str(data["uses"][0].get("ru", "")).strip()

            if not translation or translation.lower() == "no translation":
                return JsonResponse(
                    {"error": f"No translation found for '{word_query}'"},
                    status=404,
                )

            is_saved: bool = False
            if request.user.is_authenticated:
                is_saved = is_word_saved(word_query, request.user)

            return JsonResponse(
                {
                    "word": word_query,
                    "translation": translation,
                    "transcription": data.get("transcription", ""),
                    "cefr": data.get("cefr", ""),
                    "is_saved": is_saved,
                }
            )
        except Exception as exc:
            err_str = str(exc)
            if "503" in err_str or "UNAVAILABLE" in err_str or "high demand" in err_str:
                msg = "AI translation service is temporarily busy. Please try again in a moment."
            elif "not found" in err_str.lower() or "не является" in err_str:
                msg = f"Word '{word_query}' was not recognized as a valid English word."
            else:
                msg = "Translation temporarily unavailable. Please try again."
            return JsonResponse({"error": msg}, status=503)


class SaveWordFromFilmView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        if not request.user.is_authenticated:
            return JsonResponse(
                {"status": "error", "message": "Authentication required"},
                status=401,
            )

        try:
            data: dict[str, Any] = json.loads(request.body)
            raw_word: str = data.get("word", "").strip()
            word_str: str = re.sub(r"^[^\w]+|[^\w]+$", "", raw_word).lower()

            if not word_str:
                return JsonResponse(
                    {"status": "error", "message": "Word is required"},
                    status=400,
                )

            get_or_generate_word(word_str)
            save_word_for_user(word_str, request.user)

            return JsonResponse({"status": "saved", "word": word_str})
        except Exception as exc:
            return JsonResponse(
                {"status": "error", "message": str(exc)},
                status=400,
            )
