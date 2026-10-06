from pathlib import Path
from tempfile import NamedTemporaryFile
from django.test import SimpleTestCase

from apps.films.subtitle_parser import (
    SubtitleEntry,
    SubtitleGrouper,
    clean_subtitle_text,
    load_bilingual_subtitles,
    parse_srt,
    parse_timestamp,
)


class SubtitleParserTests(SimpleTestCase):
    def test_parse_timestamp_three_parts(self) -> None:
        self.assertEqual(parse_timestamp("01:02:03,456"), 3723.456)
        self.assertEqual(parse_timestamp("00:00:05.500"), 5.5)

    def test_parse_timestamp_two_parts(self) -> None:
        self.assertEqual(parse_timestamp("01:30,000"), 90.0)

    def test_clean_subtitle_text(self) -> None:
        raw: str = "<font color='red'>Hello &amp; <b>World</b></font>\nsecond line"
        cleaned: str = clean_subtitle_text(raw)
        self.assertEqual(cleaned, "Hello & World second line")

    def test_parse_srt_empty_or_missing(self) -> None:
        self.assertEqual(parse_srt(Path("non_existent_file.srt")), [])

    def test_parse_srt_success(self) -> None:
        content: str = (
            "1\n"
            "00:00:01,000 --> 00:00:03,000\n"
            "First line\n\n"
            "2\n"
            "00:00:03,500 --> 00:00:05,000\n"
            "Second line\n"
        )
        with NamedTemporaryFile(
            mode="w", suffix=".srt", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)

        try:
            entries: list[SubtitleEntry] = parse_srt(tmp_path)
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0].index, 1)
            self.assertEqual(entries[0].start_seconds, 1.0)
            self.assertEqual(entries[0].end_seconds, 3.0)
            self.assertEqual(entries[0].text, "First line")
            self.assertEqual(entries[1].text, "Second line")
        finally:
            tmp_path.unlink(missing_ok=True)


class SubtitleGrouperTests(SimpleTestCase):
    def test_group_empty(self) -> None:
        grouper = SubtitleGrouper()
        self.assertEqual(grouper.group([]), [])

    def test_group_single_entry(self) -> None:
        grouper = SubtitleGrouper()
        entry = SubtitleEntry(
            index=1, start_seconds=1.0, end_seconds=3.0, text="Only entry."
        )
        grouped: list[SubtitleEntry] = grouper.group([entry])
        self.assertEqual(len(grouped), 1)
        self.assertEqual(grouped[0].text, "Only entry.")
        self.assertEqual(grouped[0].start_seconds, 1.0)
        self.assertEqual(grouped[0].end_seconds, 3.0)

    def test_group_combines_short_entries(self) -> None:
        grouper = SubtitleGrouper(target_words=10, max_words=15)
        entries: list[SubtitleEntry] = [
            SubtitleEntry(
                index=1,
                start_seconds=0.0,
                end_seconds=2.0,
                text="Today I want to",
            ),
            SubtitleEntry(
                index=2,
                start_seconds=1.5,
                end_seconds=4.0,
                text="show you a pattern",
            ),
            SubtitleEntry(
                index=3,
                start_seconds=3.5,
                end_seconds=6.0,
                text="that works very well.",
            ),
        ]
        grouped: list[SubtitleEntry] = grouper.group(entries)
        self.assertEqual(len(grouped), 1)
        self.assertEqual(
            grouped[0].text,
            "Today I want to show you a pattern that works very well.",
        )
        self.assertEqual(grouped[0].start_seconds, 0.0)
        self.assertEqual(grouped[0].end_seconds, 6.0)

    def test_group_breaks_on_pause(self) -> None:
        grouper = SubtitleGrouper(pause_threshold=2.0)
        entries: list[SubtitleEntry] = [
            SubtitleEntry(
                index=1, start_seconds=1.0, end_seconds=2.5, text="First phrase"
            ),
            SubtitleEntry(
                index=2,
                start_seconds=5.0,
                end_seconds=6.5,
                text="Second phrase after silence",
            ),
        ]
        grouped: list[SubtitleEntry] = grouper.group(entries)
        self.assertEqual(len(grouped), 2)
        self.assertEqual(grouped[0].text, "First phrase")
        self.assertEqual(grouped[0].end_seconds, 2.5)
        self.assertEqual(grouped[1].text, "Second phrase after silence")
        self.assertEqual(grouped[1].start_seconds, 5.0)

    def test_group_breaks_on_max_words(self) -> None:
        grouper = SubtitleGrouper(max_words=6)
        entries: list[SubtitleEntry] = [
            SubtitleEntry(
                index=1, start_seconds=0.0, end_seconds=2.0, text="One two three four"
            ),
            SubtitleEntry(
                index=2, start_seconds=1.5, end_seconds=3.5, text="five six seven eight"
            ),
        ]
        grouped: list[SubtitleEntry] = grouper.group(entries)
        self.assertEqual(len(grouped), 2)
        self.assertEqual(grouped[0].text, "One two three four")
        self.assertEqual(grouped[1].text, "five six seven eight")

    def test_load_bilingual_subtitles(self) -> None:
        en_content: str = (
            "1\n00:00:00,000 --> 00:00:02,000\nHello world\n\n"
            "2\n00:00:01,500 --> 00:00:04,000\nwelcome here\n"
        )
        ru_content: str = (
            "1\n00:00:00,000 --> 00:00:02,000\nПривет мир\n\n"
            "2\n00:00:01,500 --> 00:00:04,000\nдобро пожаловать сюда\n"
        )
        with NamedTemporaryFile(
            mode="w", suffix=".en.srt", delete=False, encoding="utf-8"
        ) as en_f:
            en_f.write(en_content)
            en_path = Path(en_f.name)

        with NamedTemporaryFile(
            mode="w", suffix=".ru.srt", delete=False, encoding="utf-8"
        ) as ru_f:
            ru_f.write(ru_content)
            ru_path = Path(ru_f.name)

        try:
            result = load_bilingual_subtitles(en_path, ru_path)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["en"], "Hello world welcome here")
            self.assertIn("Привет мир", str(result[0]["ru"]))
        finally:
            en_path.unlink(missing_ok=True)
            ru_path.unlink(missing_ok=True)
