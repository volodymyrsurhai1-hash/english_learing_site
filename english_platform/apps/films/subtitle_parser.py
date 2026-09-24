import html
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SubtitleEntry:
    index: int
    start_seconds: float
    end_seconds: float
    text: str


def parse_timestamp(timestamp: str) -> float:
    normalized = timestamp.strip().replace(",", ".")
    parts = normalized.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    if len(parts) == 2:
        minutes, seconds = parts
        return float(minutes) * 60 + float(seconds)
    return float(parts[0])


def clean_subtitle_text(raw_text: str) -> str:
    without_tags = re.sub(r"<[^>]+>", "", raw_text)
    unescaped = html.unescape(without_tags)
    lines = [line.strip() for line in unescaped.splitlines() if line.strip()]
    return " ".join(lines)


def parse_srt(filepath: Path) -> list[SubtitleEntry]:
    entries: list[SubtitleEntry] = []
    if not filepath.exists():
        return entries

    content: str = filepath.read_text(encoding="utf-8-sig", errors="ignore")
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    blocks: list[str] = re.split(r"\n\s*\n", content.strip())

    auto_index: int = 1
    for block in blocks:
        lines: list[str] = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines or lines[0].startswith("WEBVTT") or lines[0].startswith("NOTE"):
            continue

        time_line_idx: int = -1
        for i, line in enumerate(lines[:3]):
            if "-->" in line:
                time_line_idx = i
                break

        if time_line_idx == -1:
            continue

        time_range: str = lines[time_line_idx]
        raw_text: str = "\n".join(lines[time_line_idx + 1 :])
        cleaned_text: str = clean_subtitle_text(raw_text)
        if not cleaned_text:
            continue

        try:
            start_str, end_str = time_range.split(" --> ")
            start_seconds: float = parse_timestamp(start_str)
            end_seconds: float = parse_timestamp(end_str.split()[0])
            idx: int = auto_index
            if time_line_idx > 0 and lines[0].isdigit():
                idx = int(lines[0])

            entries.append(
                SubtitleEntry(
                    index=idx,
                    start_seconds=start_seconds,
                    end_seconds=end_seconds,
                    text=cleaned_text,
                )
            )
            auto_index += 1
        except (ValueError, IndexError):
            continue

    return sorted(entries, key=lambda x: x.start_seconds)


def load_bilingual_subtitles(
    en_path: Path, ru_path: Path | None
) -> list[dict[str, str | float]]:
    en_entries: list[SubtitleEntry] = parse_srt(en_path)
    ru_entries: list[SubtitleEntry] = []

    if ru_path is not None and ru_path.exists():
        ru_entries = parse_srt(ru_path)

    ru_map_by_index: dict[int, SubtitleEntry] = {e.index: e for e in ru_entries}

    result: list[dict[str, str | float]] = []

    for en_entry in en_entries:
        ru_text: str = ""
        ru_entry: SubtitleEntry | None = ru_map_by_index.get(en_entry.index)

        if ru_entry is not None:
            ru_text = ru_entry.text
        elif ru_entries:
            for entry in ru_entries:
                overlap_start: float = max(en_entry.start_seconds, entry.start_seconds)
                overlap_end: float = min(en_entry.end_seconds, entry.end_seconds)
                if overlap_end > overlap_start:
                    ru_text = entry.text
                    break

        result.append(
            {
                "start": en_entry.start_seconds,
                "end": en_entry.end_seconds,
                "en": en_entry.text,
                "ru": ru_text,
            }
        )

    return result
