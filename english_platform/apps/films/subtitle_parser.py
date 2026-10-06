from dataclasses import dataclass
import html
from pathlib import Path
import re


@dataclass(frozen=True)
class SubtitleEntry:
    index: int
    start_seconds: float
    end_seconds: float
    text: str


class SubtitleGrouper:
    def __init__(
        self,
        target_words: int = 12,
        max_words: int = 20,
        max_duration: float = 7.0,
        pause_threshold: float = 3.5,
        min_sentence_words: int = 8,
    ) -> None:
        self._target_words: int = target_words
        self._max_words: int = max_words
        self._max_duration: float = max_duration
        self._pause_threshold: float = pause_threshold
        self._min_sentence_words: int = min_sentence_words

    def group(self, entries: list[SubtitleEntry]) -> list[SubtitleEntry]:
        if not entries:
            return []

        merged: list[SubtitleEntry] = []
        i: int = 0
        total_entries: int = len(entries)
        auto_index: int = 1

        while i < total_entries:
            group: list[SubtitleEntry] = [entries[i]]
            word_count: int = len(entries[i].text.split())
            start_seconds: float = entries[i].start_seconds
            j: int = i + 1

            while j < total_entries:
                next_entry: SubtitleEntry = entries[j]
                next_words: int = len(next_entry.text.split())
                gap: float = next_entry.start_seconds - entries[j - 1].start_seconds

                if gap > self._pause_threshold:
                    break

                duration: float = next_entry.start_seconds - start_seconds
                if duration > self._max_duration:
                    break

                prev_has_terminal_punct: bool = (
                    group[-1].text.rstrip().endswith((".", "?", "!"))
                )
                if prev_has_terminal_punct and word_count >= self._min_sentence_words:
                    break

                if word_count + next_words > self._max_words:
                    break

                group.append(next_entry)
                word_count += next_words

                current_has_terminal_punct: bool = next_entry.text.rstrip().endswith(
                    (".", "?", "!")
                )
                if word_count >= self._target_words and current_has_terminal_punct:
                    j += 1
                    break

                j += 1

            group_text: str = " ".join(e.text for e in group)
            group_start: float = group[0].start_seconds
            last_entry: SubtitleEntry = group[-1]

            if j < total_entries:
                next_start: float = entries[j].start_seconds
                if next_start > last_entry.end_seconds:
                    group_end: float = last_entry.end_seconds
                else:
                    group_end = next_start
            else:
                group_end = last_entry.end_seconds

            if group_end <= group_start:
                group_end = max(last_entry.end_seconds, group_start + 1.0)

            merged.append(
                SubtitleEntry(
                    index=auto_index,
                    start_seconds=round(group_start, 2),
                    end_seconds=round(group_end, 2),
                    text=group_text,
                )
            )
            auto_index += 1
            i = j

        return merged


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
    en_path: Path,
    ru_path: Path | None,
    grouper: SubtitleGrouper | None = None,
) -> list[dict[str, str | float]]:
    en_entries: list[SubtitleEntry] = parse_srt(en_path)
    ru_entries: list[SubtitleEntry] = []

    if ru_path is not None and ru_path.exists():
        ru_entries = parse_srt(ru_path)

    active_grouper: SubtitleGrouper = grouper or SubtitleGrouper()
    grouped_en: list[SubtitleEntry] = active_grouper.group(en_entries)

    result: list[dict[str, str | float]] = []

    for en_entry in grouped_en:
        ru_text: str = ""
        if ru_entries:
            matched_ru: list[str] = [
                ru.text
                for ru in ru_entries
                if min(en_entry.end_seconds, ru.end_seconds)
                > max(en_entry.start_seconds, ru.start_seconds)
            ]
            ru_text = " ".join(dict.fromkeys(matched_ru))

        result.append(
            {
                "start": en_entry.start_seconds,
                "end": en_entry.end_seconds,
                "en": en_entry.text,
                "ru": ru_text,
            }
        )

    return result
