from pathlib import Path

from django.conf import settings

from apps.films.dataclasses import DownloadConfig, DownloadResult, SubtitleConfig
from apps.films.interfaces import VideoDownloader
from apps.films.services import YtDlpDownloader


def download_video(
    url: str,
    output_dir: Path | None = None,
    languages: list[str] | None = None,
    downloader: VideoDownloader | None = None,
    task_id: str | None = None,
) -> DownloadResult:
    if output_dir is None:
        output_dir = Path(settings.MEDIA_ROOT) / "films"

    if languages is None:
        languages = ["en", "ru"]

    subtitle_config = SubtitleConfig(languages=languages)
    download_config = DownloadConfig(
        output_dir=output_dir,
        subtitle_config=subtitle_config,
        task_id=task_id,
    )

    active_downloader: VideoDownloader = downloader or YtDlpDownloader()
    return active_downloader.download(url, download_config)
