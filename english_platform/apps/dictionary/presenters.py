from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class CuratedExample:
    en: str
    ru: str


@dataclass(frozen=True)
class CuratedSense:
    index: int
    ru: str
    context: Optional[str]
    examples: list[CuratedExample]
    show_header: bool


@dataclass(frozen=True)
class CuratedSlot:
    name: str
    grammatical_form: Optional[str]
    description: str
    tokens: list[str]
    examples: list[CuratedExample]
    sentences: list[str]


@dataclass(frozen=True)
class CuratedVariation:
    pattern: str
    note: str
    example: Optional[CuratedExample] = None


@dataclass(frozen=True)
class CuratedDictionaryEntry:
    english: str
    transcription: Optional[str]
    part_of_speech: Optional[str]
    cefr: Optional[str]
    frequency: Optional[str]
    style: Optional[str]
    primary_translation: str
    english_definition: Optional[str]
    pattern: Optional[str]
    grammar_note: Optional[str]
    what_it_means: Optional[str]
    senses: list[CuratedSense]
    senses_title: str
    slots: list[CuratedSlot]
    variations: list[CuratedVariation]
    synonyms_by_level: list[dict[str, Any]]
    collocations: list[str]
    word_family: list[str]
    entry_type: str


class DictionaryPresenter:
    @staticmethod
    def present(result: dict[str, Any], query: str) -> CuratedDictionaryEntry:
        english: str = str(result.get("english") or query).strip()
        transcription: Optional[str] = result.get("transcription")
        part_of_speech: Optional[str] = result.get("part_of_speech")
        cefr: Optional[str] = result.get("cefr")
        frequency: Optional[str] = result.get("frequency")
        style: Optional[str] = result.get("style")

        english_def_raw: Optional[str] = result.get("english_definition")
        english_definition: Optional[str] = None
        if english_def_raw:
            cleaned_def: str = str(english_def_raw).strip()
            if cleaned_def.lower() != english.lower():
                english_definition = cleaned_def

        pattern_raw: Optional[str] = result.get("pattern")
        pattern: Optional[str] = None
        if pattern_raw:
            cleaned_pat: str = str(pattern_raw).strip()
            normalized_pat: str = cleaned_pat.lower().strip("\"'`")
            normalized_eng: str = english.lower().strip()
            normalized_query: str = query.lower().strip()
            if normalized_pat not in (normalized_eng, normalized_query):
                pattern = cleaned_pat

        meanings_raw: Any = result.get("meanings")
        uses_raw: Any = result.get("uses")
        raw_senses: list[Any] = []
        senses_title: str = "Примеры"

        if isinstance(meanings_raw, list) and len(meanings_raw) > 0:
            raw_senses = meanings_raw
            senses_title = "Значения и примеры"
        elif isinstance(uses_raw, list) and len(uses_raw) > 0:
            raw_senses = uses_raw
            senses_title = "Применения и примеры"

        primary_translation: str = ""
        explicit_primary: Optional[str] = result.get("primary_translation")
        if explicit_primary:
            cleaned_primary: str = str(explicit_primary).strip().rstrip(".")
            if cleaned_primary:
                primary_translation = cleaned_primary

        if not primary_translation:
            if raw_senses and isinstance(raw_senses[0], dict):
                primary_translation = str(raw_senses[0].get("ru") or "").strip()
            elif result.get("what_it_means"):
                primary_translation = str(result.get("what_it_means") or "").strip()

        if len(primary_translation) > 100 and "." in primary_translation:
            first_sentence: str = primary_translation.split(".")[0].strip()
            if len(first_sentence) >= 10:
                primary_translation = first_sentence

        what_it_means_raw: Optional[str] = result.get("what_it_means")
        what_it_means: Optional[str] = None
        if what_it_means_raw:
            cleaned_wim: str = str(what_it_means_raw).strip()
            if cleaned_wim.lower() != primary_translation.lower() and (
                not english_definition
                or cleaned_wim.lower() != english_definition.lower()
            ):
                what_it_means = cleaned_wim

        curated_senses: list[CuratedSense] = []
        is_single_sense: bool = len(raw_senses) == 1

        for idx, sense in enumerate(raw_senses, start=1):
            if not isinstance(sense, dict):
                continue
            ru_text: str = str(sense.get("ru") or "").strip()
            context_val: Optional[str] = sense.get("context")
            cleaned_context: Optional[str] = (
                str(context_val).strip() if context_val else None
            )

            raw_examples: Any = sense.get("examples")
            curated_examples: list[CuratedExample] = []
            if isinstance(raw_examples, list):
                for ex in raw_examples[:2]:
                    if isinstance(ex, dict):
                        en_val: str = str(ex.get("en") or "").strip()
                        ru_val: str = str(ex.get("ru") or "").strip()
                        if " - " in en_val and any(
                            "\u0400" <= c <= "\u04ff" for c in en_val.split(" - ", 1)[1]
                        ):
                            en_val = en_val.split(" - ", 1)[0].strip()
                        if en_val:
                            curated_examples.append(
                                CuratedExample(en=en_val, ru=ru_val)
                            )

            show_header: bool = not (
                is_single_sense
                and primary_translation
                and ru_text.lower() == primary_translation.lower()
            )
            curated_senses.append(
                CuratedSense(
                    index=idx,
                    ru=ru_text,
                    context=cleaned_context,
                    examples=curated_examples,
                    show_header=show_header,
                )
            )

        if is_single_sense and curated_senses and not curated_senses[0].show_header:
            senses_title = "Примеры употребления"

        grammar_note_raw: Optional[str] = result.get("grammar_note")
        grammar_note: Optional[str] = None
        if grammar_note_raw:
            cleaned_gn: str = str(grammar_note_raw).strip()
            if cleaned_gn:
                grammar_note = cleaned_gn

        raw_slots: Any = result.get("slots")
        curated_slots: list[CuratedSlot] = []
        if isinstance(raw_slots, list):
            for slot in raw_slots:
                if not isinstance(slot, dict):
                    continue
                name: str = str(slot.get("name") or "").strip().strip("[]")
                grammatical_form_raw: Optional[str] = slot.get("grammatical_form")
                grammatical_form: Optional[str] = (
                    str(grammatical_form_raw).strip() if grammatical_form_raw else None
                )
                description: str = str(slot.get("description") or "").strip()
                tokens: list[str] = []
                sentences: list[str] = []
                curated_slot_examples: list[CuratedExample] = []

                raw_tokens: Any = slot.get("tokens")
                if isinstance(raw_tokens, list):
                    for tok in raw_tokens:
                        s_tok: str = str(tok).strip()
                        if s_tok and s_tok not in tokens:
                            tokens.append(s_tok)

                examples_val: Any = slot.get("examples")
                if isinstance(examples_val, list):
                    for item in examples_val:
                        if isinstance(item, dict):
                            en_str: str = str(item.get("en") or "").strip()
                            ru_str: str = str(item.get("ru") or "").strip()
                            if en_str:
                                curated_slot_examples.append(
                                    CuratedExample(en=en_str, ru=ru_str)
                                )
                                sentences.append(en_str)
                        elif isinstance(item, str):
                            s_item: str = item.strip()
                            if not s_item:
                                continue
                            if len(s_item) <= 35 and not (
                                s_item.endswith(".") or s_item.endswith("!")
                            ):
                                if s_item not in tokens:
                                    tokens.append(s_item)
                            else:
                                sentences.append(s_item)
                                curated_slot_examples.append(
                                    CuratedExample(en=s_item, ru="")
                                )

                curated_slots.append(
                    CuratedSlot(
                        name=name,
                        grammatical_form=grammatical_form,
                        description=description,
                        tokens=tokens,
                        examples=curated_slot_examples,
                        sentences=sentences,
                    )
                )

        raw_variations: Any = result.get("variations")
        curated_variations: list[CuratedVariation] = []
        if isinstance(raw_variations, list):
            for var in raw_variations:
                if isinstance(var, dict):
                    pattern_val: str = str(var.get("pattern") or "").strip()
                    note_val: str = str(var.get("note") or "").strip()
                    ex_val: Any = var.get("example")
                    curated_var_ex: Optional[CuratedExample] = None
                    if isinstance(ex_val, dict):
                        en_ex: str = str(ex_val.get("en") or "").strip()
                        ru_ex: str = str(ex_val.get("ru") or "").strip()
                        if en_ex:
                            curated_var_ex = CuratedExample(en=en_ex, ru=ru_ex)
                    elif isinstance(ex_val, str) and ex_val.strip():
                        curated_var_ex = CuratedExample(en=ex_val.strip(), ru="")
                    if pattern_val:
                        curated_variations.append(
                            CuratedVariation(
                                pattern=pattern_val,
                                note=note_val,
                                example=curated_var_ex,
                            )
                        )

        synonyms_by_level: list[dict[str, Any]] = (
            result.get("synonyms_by_level")
            if isinstance(result.get("synonyms_by_level"), list)
            else []
        )
        collocations: list[str] = (
            result.get("collocations")
            if isinstance(result.get("collocations"), list)
            else []
        )
        word_family: list[str] = (
            result.get("word_family")
            if isinstance(result.get("word_family"), list)
            else []
        )
        entry_type: str = str(result.get("entry_type") or "word").strip()

        return CuratedDictionaryEntry(
            english=english,
            transcription=transcription,
            part_of_speech=part_of_speech,
            cefr=cefr,
            frequency=frequency,
            style=style,
            primary_translation=primary_translation,
            english_definition=english_definition,
            pattern=pattern,
            grammar_note=grammar_note,
            what_it_means=what_it_means,
            senses=curated_senses,
            senses_title=senses_title,
            slots=curated_slots,
            variations=curated_variations,
            synonyms_by_level=synonyms_by_level,
            collocations=collocations,
            word_family=word_family,
            entry_type=entry_type,
        )
