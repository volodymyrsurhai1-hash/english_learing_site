# 🇬🇧 English Learning Platform (AI-Powered)

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg?style=flat&logo=django)](https://www.djangoproject.com/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%203.7%20Flash-orange.svg?style=flat&logo=google)](https://ai.google.dev/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Cache-Redis-red.svg?style=flat&logo=redis)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An advanced, interactive web platform for English learners featuring dual-subtitle video playback, a bilingual reader, TikTok-style short clips (Reels), and deep AI-driven linguistic analysis of words and grammatical constructions.

---

## ✨ Key Features

### 🎬 Cinema (Interactive Dual-Subtitle Player)
- Fullscreen video player with **dual synchronized subtitles** (EN + RU).
- Tap or click any English word in the subtitles for an instant contextual breakdown modal without interrupting video playback.
- One-click addition of unfamiliar words to personal decks for spaced repetition.

### 📱 Scroll (Reels / Shorts Feed)
- Vertical video feed optimized for short learning clips (TikTok/Instagram Reels format).
- Synchronized dual subtitles with auto-highlighting of complex vocabulary.
- Quick toggle button (`A→Я`) to show or hide Russian translations.

### 📖 Dictionary & AI Linguistic Engine
- **Deep Word Analysis:** All distinct meanings, grammatical context, IPA phonetics, CEFR difficulty levels (A1–C2), and conversational examples for each definition.
- **Idiom & Construction Breakdown:** Structural patterns (e.g., `brush + sth + off`), placeholder slots, word order variations, and real-world usage scenarios.
- **Zero-Latency Autocomplete:** Client-side 5,000-word core index (0 ms response time) with typo correction.
- **Voice Search:** Integrated microphone input using native browser Web Speech API.

### 📚 Books (Bilingual Reader)
- Original classic literature organized by chapters.
- Parallel line-by-line Russian translations for every paragraph.
- Asynchronous batch translation of uploaded EPUB books via Celery workers and Gemini AI.

### 📋 Grammar Lab (Tables & Exercises)
- Interactive grammar tables with cell audio pronunciation.
- Embedded exercises with scoring, instant validation, and interactive review trainers.

### 💪 Workout / Kachalka (Spaced Repetition & Gamification)
- **SM-2 (SuperMemo)** spaced repetition algorithm for optimal vocabulary retention.
- **Pet Companion Gamification:** 30 levels of progression (from "Puppy" to "Legend") powered by earned study XP.
- Activity heatmaps (5-week view), custom decks, and Duolingo-style **Streak Freezes**.

---

## 🛠 Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.12+, Django 5.x |
| **AI Engine** | Google Gemini 3.7 Flash, Pydantic v2 (Strict Structured Outputs) |
| **Database** | PostgreSQL (JSONField, Trigram fuzzy search) |
| **Cache & Queue** | Redis, Celery (background book translation & dictionary enrichment) |
| **Frontend** | Django Templates, Vanilla JavaScript, CSS3 (Modern Glassmorphism & Dark Mode) |
| **Subtitle Parsing** | `pysrt`, `webvtt-py` |

---

## 📁 Project Architecture

