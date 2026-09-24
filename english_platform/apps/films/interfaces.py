from typing import Protocol

from apps.films.dataclasses import DownloadConfig, DownloadResult


class VideoDownloader(Protocol):
    def download(self, url: str, config: DownloadConfig) -> DownloadResult: ...
