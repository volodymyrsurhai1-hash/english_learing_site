from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SubtitleConfig:
    languages: list[str] = field(default_factory=lambda: ["en", "ru"])
    format: str = "srt"
    write_auto: bool = True
    embed: bool = False


@dataclass(frozen=True)
class DownloadConfig:
    output_dir: Path = Path("downloads")
    video_format: str = "mp4"
    subtitle_config: SubtitleConfig | None = None
    no_playlist: bool = True
    task_id: str | None = None


@dataclass
class DownloadResult:
    title: str
    filepath: Path
    subtitle_files: list[Path] = field(default_factory=list)
    success: bool = True
    error: str | None = None


@dataclass
class ProgressState:
    status: str = "pending"
    percent: float = 0.0
    speed: str = ""
    eta: str = ""
    message: str = "Starting download..."
    film_id: int | None = None
    error: str | None = None
