import os
from pathlib import Path
from typing import Any

from django.conf import settings
import yt_dlp

from apps.films.dataclasses import DownloadConfig, DownloadResult, SubtitleConfig
from apps.films.interfaces import VideoDownloader
from apps.films.progress import progress_tracker


class YtDlpDownloader(VideoDownloader):
    def __init__(self) -> None:
        self._ensure_environment_path()

    def _ensure_environment_path(self) -> None:
        persistent_path = (
            os.environ.get("Path", "")
            + ";"
            + (
                os.getenv("LOCALAPPDATA", "")
                + r"\Microsoft\WinGet\Packages\DenoLand.Deno_Microsoft.Winget.Source_8wekyb3d8bbwe"
            )
            + ";"
            + (
                os.getenv("LOCALAPPDATA", "")
                + r"\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
            )
        )
        os.environ["PATH"] = persistent_path

    def _create_progress_hook(self, task_id: str) -> Any:
        def hook(d: dict[str, Any]) -> None:
            status = d.get("status")
            if status == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes", 0)
                percent = round((downloaded / total * 100), 1) if total else 0.0
                speed = d.get("_speed_str", "").strip()
                eta = d.get("_eta_str", "").strip()
                progress_tracker.update_task(
                    task_id=task_id,
                    status="downloading",
                    percent=percent,
                    speed=speed,
                    eta=eta,
                    message=f"Downloading video: {percent}%",
                )
            elif status == "finished":
                progress_tracker.update_task(
                    task_id=task_id,
                    status="processing",
                    percent=99.0,
                    message="Merging audio and video...",
                )

        return hook

    def _create_postprocessor_hook(self, task_id: str) -> Any:
        def hook(d: dict[str, Any]) -> None:
            status = d.get("status")
            if status == "started":
                progress_tracker.update_task(
                    task_id=task_id,
                    status="processing",
                    percent=99.0,
                    message="Processing video formats...",
                )

        return hook

    def _build_options(self, config: DownloadConfig) -> dict[str, Any]:
        opts: dict[str, Any] = {
            "format": (
                f"bestvideo[ext={config.video_format}]+bestaudio[ext=m4a]"
                f"/best[ext={config.video_format}]/best"
            ),
            "merge_output_format": config.video_format,
            "outtmpl": str(config.output_dir / "%(title)s.%(ext)s"),
            "noplaylist": config.no_playlist,
            "quiet": False,
            "no_color": True,
            "ignoreerrors": True,
            "windowsfilenames": True,
            "postprocessor_args": {"ffmpeg": ["-movflags", "+faststart"]},
            "extractor_args": {"youtube": {"player_client": ["ios", "web", "mweb"]}},
        }

        cookie_candidates: list[str] = [
            os.environ.get("YOUTUBE_COOKIES_PATH", ""),
            "/app/cookies/cookies.txt",
            "/app/cookies/youtube.txt",
            str(Path(settings.BASE_DIR) / "cookies.txt"),
            str(Path(settings.BASE_DIR).parent / "cookies.txt"),
            str(Path(settings.MEDIA_ROOT) / "cookies.txt"),
        ]
        for candidate in cookie_candidates:
            if candidate and Path(candidate).is_file():
                opts["cookiefile"] = candidate
                break

        proxy: str = os.environ.get("YOUTUBE_PROXY", "")
        if proxy:
            opts["proxy"] = proxy

        if config.task_id is not None:
            opts["progress_hooks"] = [self._create_progress_hook(config.task_id)]
            opts["postprocessor_hooks"] = [
                self._create_postprocessor_hook(config.task_id)
            ]

        if config.subtitle_config is not None:
            opts.update(self._build_subtitle_options(config.subtitle_config))

        return opts

    def _build_subtitle_options(self, sub_config: SubtitleConfig) -> dict[str, Any]:
        opts: dict[str, Any] = {
            "writesubtitles": True,
            "writeautomaticsub": sub_config.write_auto,
            "subtitleslangs": sub_config.languages,
            "subtitlesformat": sub_config.format,
        }

        if sub_config.embed:
            opts["postprocessors"] = [{"key": "FFmpegEmbedSubtitle"}]

        return opts

    def _has_subtitles(self, info: dict[str, Any]) -> bool:
        manual_subs: dict[str, Any] = info.get("subtitles") or {}
        auto_subs: dict[str, Any] = info.get("automatic_captions") or {}
        all_langs: set[str] = set(manual_subs.keys()) | set(auto_subs.keys())
        return any(
            lang == "en"
            or lang.startswith("en-")
            or lang.startswith("en.")
            or lang.startswith("en_")
            for lang in all_langs
        )

    def _collect_subtitle_files(
        self,
        info: dict[str, Any],
        prepared_base: Path,
        sub_format: str,
    ) -> list[Path]:
        subtitle_files: list[Path] = []
        output_dir = prepared_base.parent
        stem = prepared_base.stem

        if output_dir.exists():
            for file_path in output_dir.iterdir():
                if (
                    file_path.is_file()
                    and file_path.name.startswith(stem)
                    and file_path.suffix in [".srt", ".vtt"]
                ):
                    subtitle_files.append(file_path)

        return subtitle_files

    def download(self, url: str, config: DownloadConfig) -> DownloadResult:
        config.output_dir.mkdir(parents=True, exist_ok=True)
        opts = self._build_options(config)

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info: dict[str, Any] = ydl.extract_info(url, download=False)
                if info is None:
                    return DownloadResult(
                        title="",
                        filepath=Path(),
                        success=False,
                        error="Failed to extract video info",
                    )

                if not self._has_subtitles(info):
                    error_msg = (
                        "Видео не поддерживается: у этого видео отсутствуют субтитры."
                    )
                    if config.task_id is not None:
                        progress_tracker.update_task(
                            task_id=config.task_id,
                            status="error",
                            error=error_msg,
                            message=error_msg,
                        )
                    return DownloadResult(
                        title=info.get("title", ""),
                        filepath=Path(),
                        success=False,
                        error=error_msg,
                    )

                info = ydl.extract_info(url, download=True)
                if info is None:
                    return DownloadResult(
                        title="",
                        filepath=Path(),
                        success=False,
                        error="Failed to download video",
                    )

                title: str = info.get("title", "Unknown")
                prepared_filename: str = ydl.prepare_filename(info)
                prepared_path = Path(prepared_filename)
                filepath = prepared_path.with_suffix(f".{config.video_format}")

                if not filepath.exists() and config.output_dir.exists():
                    for file_path in config.output_dir.iterdir():
                        if (
                            file_path.is_file()
                            and file_path.name.startswith(prepared_path.stem)
                            and file_path.suffix in [".mp4", ".mkv", ".webm"]
                        ):
                            filepath = file_path
                            break

                sub_format = (
                    config.subtitle_config.format if config.subtitle_config else "srt"
                )
                subtitle_files = self._collect_subtitle_files(
                    info, prepared_path, sub_format
                )

                if not subtitle_files:
                    if filepath.exists():
                        filepath.unlink(missing_ok=True)
                    error_msg = (
                        "Видео не поддерживается: у этого видео отсутствуют субтитры."
                    )
                    if config.task_id is not None:
                        progress_tracker.update_task(
                            task_id=config.task_id,
                            status="error",
                            error=error_msg,
                            message=error_msg,
                        )
                    return DownloadResult(
                        title=title,
                        filepath=Path(),
                        success=False,
                        error=error_msg,
                    )

                return DownloadResult(
                    title=title,
                    filepath=filepath,
                    subtitle_files=subtitle_files,
                )
        except yt_dlp.utils.DownloadError as exc:
            return DownloadResult(
                title="",
                filepath=Path(),
                success=False,
                error=str(exc),
            )
