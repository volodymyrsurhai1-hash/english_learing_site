# English Learning Platform — Implementation Plan

  

Полная копия **dop.votetoang.com** — образовательная платформа для изучения английского.

  

---

  

## Что представляет из себя сайт (анализ)

  

Тёмная тема, единый дизайн с маскотом-собакой в разных образах под каждый раздел.

Навбар: **Каталог · Словарь · Таблицы · Книги · Сегодня · Кино · Скролл · Качалка · Кабинет · Курсы**

  

---

  

## Технологический стек

  

| Слой | Технология | Почему |

|---|---|---|

| **Backend** | **Django 5.x** | ORM, admin, auth, middleware, sessions — всё из коробки |

| **REST API** | **Django REST Framework** | AJAX-запросы (клик на слово, прогресс, карточки) |

| **БД** | **PostgreSQL** | JSON-поля (субтитры, таблицы), FTS для словаря |

| **Кэш / очереди** | **Redis + Celery** | OTP-коды, AI-батчи, email |

| **AI** | **OpenAI GPT-4o-mini** | Дёшево, быстро; или Gemini Flash — бесплатная квота |

| **Субтитры** | **pysrt + WebVTT** | Парсинг SRT/VTT → JSON |

| **Книги** | **ebooklib (EPUB)** | Парсинг глав и параграфов |

| **Фронтенд** | **Django Templates + Vanilla JS** | SSR + интерактивность, никакого JS-фреймворка |

| **Медиа** | **Cloudflare R2 / S3** | Видео, аудио, постеры |

| **Деплой** | **Docker + Nginx + Gunicorn** | Продакшн |

  

---

  

## Структура Django-приложений

  

```

english_platform/

├── manage.py

├── config/

│   ├── settings/

│   │   ├── base.py

│   │   ├── dev.py

│   │   └── prod.py

│   ├── urls.py

│   └── celery.py

│

├── apps/

│   ├── accounts/      # OTP-авторизация (email → 6-значный код)

│   ├── dictionary/    # Словарь: поиск слова → полный разбор

│   ├── grammar/       # Таблицы + упражнения + тренажёр

│   ├── books/         # Читалка: EPUB → главы → параграфы EN+RU

│   ├── kino/          # Плеер с двойными субтитрами (Intersub-стиль)

│   ├── scroll/        # TikTok-формат коротких клипов

│   ├── kachalka/      # Карточки (SM-2) + питомец-собака (30 уровней)

│   ├── subscriptions/ # Подписки + платёжный шлюз

│   ├── ai_pipeline/   # Celery-задачи для AI API

│   └── core/          # Утилиты, middleware

│

├── templates/

├── static/            # CSS, JS, иконки

└── media/             # Локальные медиа (dev)

```

  

---

  

## Детали каждого модуля

  

---

  

### 🔑 `accounts` — OTP-авторизация

  

**Что на сайте:** только email, без пароля. Вводишь email → получаешь 6-значный код → вводишь → сессия.

  

```python

class User(AbstractUser):

    email = models.EmailField(unique=True)

    username = None  # только email

    subscription_until = models.DateTimeField(null=True)

    days_streak = models.IntegerField(default=0)

    last_study_date = models.DateField(null=True)

  

class OTPCode(models.Model):

    email = models.EmailField()

    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()  # +5 минут

    is_used = models.BooleanField(default=False)

```

  

**Flow:** `POST /api/auth/send-otp/` → Celery отправляет письмо → `POST /api/auth/verify-otp/` → Django session.

  

---

  

### 🗂️ `catalog` — Каталог выпусков

  

**Что на сайте:** 710+ карточек видео-разборов. Каждая карточка = разбор к YouTube-ролику.

Теги: Карточки · Текст · Тетрадь · Упражнения · Уровень (A1–C2).

Поиск по выпускам + фильтры по уровню.

  

```python

class Episode(models.Model):

    title = models.CharField(max_length=300)

    title_en = models.CharField(max_length=300)

    youtube_id = models.CharField(max_length=20)

    poster = models.ImageField(upload_to='episodes/posters/')

    level = models.CharField(max_length=2)  # A1, A2, B1, B2, C1, C2

    series = models.CharField(max_length=100)  # "Английский по мультикам"

    published_at = models.DateField()

    is_premium = models.BooleanField(default=True)

    has_cards = models.BooleanField(default=False)

    has_text = models.BooleanField(default=False)

    has_notebook = models.BooleanField(default=False)

    has_exercises = models.BooleanField(default=False)

  

class EpisodeTranscript(models.Model):

    episode = models.OneToOneField(Episode, on_delete=models.CASCADE)

    content = models.TextField()

  

class EpisodeWord(models.Model):

    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)

    word = models.ForeignKey('dictionary.Word', on_delete=models.CASCADE)

    order = models.IntegerField()

```

  

---

  

### 📖 `dictionary` — Словарь

  

**Что на сайте:** Вводишь слово → полный разбор:

- **Что значит:** перевод (несколько вариантов)

- **Как выглядит:** картинка

- **Как звучит:** транскрипция `/lʌv/` + аудио-кнопка

- **Как в речи:** словосочетания (love letter, love song)

- Фильтры уровня: A1 / A2 / B1 / B2 / C1 / C2 / EN→RU

- ❤️ Добавить в избранное → попадает в Качалку

  

```python

class Word(models.Model):

    english = models.CharField(max_length=200, unique=True)

    translation = models.TextField()

    translations_list = models.JSONField()     # ["любовь", "любить", "нравиться"]

    transcription = models.CharField(max_length=100)  # /lʌv/

    cefr_level = models.CharField(max_length=2)

    part_of_speech = models.CharField(max_length=20)

    audio = models.FileField(upload_to='words/audio/', blank=True)

    image = models.ImageField(upload_to='words/images/', blank=True)

    collocations = models.JSONField(default=list)  # ["love letter", "love song"]

    example_en = models.TextField(blank=True)

    example_ru = models.TextField(blank=True)

    synonyms = models.JSONField(default=list)

    ai_enriched = models.BooleanField(default=False)

  

class UserFavoriteWord(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    source = models.CharField(max_length=50)  # 'dictionary', 'scroll', 'kino', 'book'

    added_at = models.DateTimeField(auto_now_add=True)

```

  

**API:** `GET /api/dictionary/lookup/?q=love` → если слова нет → Celery → AI → кэш.

  

---

  

### 📋 `grammar` — Таблицы

  

**Что на сайте:** Список тем с аккордеоном (Части речи 1, Существительные 4...).

Каждая тема — модальное окно с 3 вкладками:

1. **Таблица** — грамматическая таблица, клик на слово → произношение

2. **Упражнение** — вписать форму (1/5, 2/5...), результат 5/5 ✓ Отлично!

3. **Тренажёр** — повторение в стиле карточек

  

```python

class GrammarCategory(models.Model):

    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    order = models.IntegerField()

  

class GrammarTable(models.Model):

    category = models.ForeignKey(GrammarCategory, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)         # "Глагол to be"

    subtitle = models.CharField(max_length=200, blank=True)  # "am / is / are — was / were"

    content = models.JSONField()                     # структура таблицы

    audio_map = models.JSONField(default=dict)       # {"am": "/audio/am.mp3", ...}

    order = models.IntegerField()

    number = models.IntegerField()                   # 15 из 101

  

class GrammarExercise(models.Model):

    table = models.ForeignKey(GrammarTable, on_delete=models.CASCADE)

    prompt = models.CharField(max_length=300)

    questions = models.JSONField()   # [{prompt: "I →", answer: "am"}, ...]

  

class UserGrammarProgress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    table = models.ForeignKey(GrammarTable, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    score = models.IntegerField(default=0)

    completed_at = models.DateTimeField(null=True)

```

  

---

  

### 📚 `books` — Читалка

  

**Что на сайте:** "Классика в оригинале". 6 книг + 13 историй, 76 глав.

К каждой главе — текст с подстрочником + карточки слов + рабочая тетрадь.

  

```python

class Book(models.Model):

    title = models.CharField(max_length=300)

    title_en = models.CharField(max_length=300)

    author = models.CharField(max_length=200)

    cover = models.ImageField(upload_to='books/covers/')

    level = models.CharField(max_length=2)

    is_premium = models.BooleanField(default=True)

    book_type = models.CharField(max_length=10)  # 'book' или 'story'

    source_file = models.FileField(upload_to='books/sources/', blank=True)

    import_status = models.CharField(max_length=20, default='pending')

  

class Chapter(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    number = models.IntegerField()

    title = models.CharField(max_length=300)

  

class Paragraph(models.Model):

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    english_text = models.TextField()

    russian_text = models.TextField()   # AI-перевод (подстрочник)

    order = models.IntegerField()

    translation_status = models.CharField(max_length=20, default='pending')

```

  

**AI-импорт (Celery):**

1. Admin загружает EPUB → `ebooklib` разбивает на главы/параграфы

2. Celery батчами по 20 параграфов → Gemini API переводит EN→RU

3. `import_status` → `'done'`

  

---

  

### 🎬 `kino` — Плеер с двойными субтитрами

  

**Что на сайте:** Фильмы с субтитрами EN+RU. Ключевая фича: **наводишься на слово → попап с полным разбором** (транскрипция + перевод + примеры + кнопка "В карточки").

  

```python

class Film(models.Model):

    title = models.CharField(max_length=300)

    poster = models.ImageField(upload_to='films/posters/')

    video_file = models.FileField(upload_to='films/videos/', blank=True)

    youtube_id = models.CharField(max_length=20, blank=True)

    level = models.CharField(max_length=2)

    is_premium = models.BooleanField(default=True)

  

class SubtitleTrack(models.Model):

    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    language = models.CharField(max_length=5)  # 'en', 'ru'

    srt_file = models.FileField(upload_to='films/subtitles/')

    parsed = models.JSONField()  # [{id, start_ms, end_ms, text}, ...]

  

class UserFilmProgress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    last_position_ms = models.IntegerField(default=0)

```

  

**Синхронизация субтитров (JS):**

```javascript

video.addEventListener('timeupdate', () => {

  const ms = video.currentTime * 1000 + offset;

  const en = subtitlesEN.find(s => ms >= s.start_ms && ms <= s.end_ms);

  const ru = subtitlesRU.find(s => ms >= s.start_ms && ms <= s.end_ms);

  subtitleEN.innerHTML = en ? wrapWords(en.text) : '';

  subtitleRU.textContent = ru ? ru.text : '';

});

  

function wrapWords(text) {

  return text.split(' ').map(w =>

    `<span class="word" data-word="${clean(w)}">${w}</span>`

  ).join(' ');

}

// Клик → AJAX → /api/dictionary/lookup/?q=word → попап

```

  

---

  

### 📱 `scroll` — TikTok-формат

  

**Что на сайте:** Вертикальные видео 9:16 с двойными субтитрами EN+RU.

Сложные слова выделены жёлтым. Клик на слово → mini-попап (слово + транскрипция + перевод + кнопка "Открыть в словаре").

Кнопка **A→Я** — скрыть/показать RU субтитры.

  

```python

class VideoClip(models.Model):

    title = models.CharField(max_length=300, blank=True)

    video_file = models.FileField(upload_to='scroll/videos/')

    source = models.CharField(max_length=200)  # "Hot Ones"

    subtitles_en = models.JSONField()  # [{start_ms, end_ms, text, highlighted_words:[...]}]

    subtitles_ru = models.JSONField()  # [{start_ms, end_ms, text}]

    level = models.CharField(max_length=2, blank=True)

    order = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

```

  

Intersection Observer для автоплея следующего клипа при прокрутке.

  

---

  

### 💪 `kachalka` — Карточки + Питомец

  

**Что на сайте:** Собака-питомец от Щенка (ур. 1) до Легенды (ур. 30).

Статистика: слов выучено / в работе / ответов / точность / освоено.

График активности за 5 недель.

Разделы: **Колоды** / **Избранное** (❤️ из любого раздела) / **Повторение** (SM-2).

Заморозки стрика (2 штуки — пропуск дня не ломает серию).

  

```python

class Pet(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    level = models.IntegerField(default=1)

    experience = models.IntegerField(default=0)

  

class Deck(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    is_favorite = models.BooleanField(default=False)

  

class UserWordProgress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    word = models.ForeignKey('dictionary.Word', on_delete=models.CASCADE)

    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, null=True)

    # SM-2

    ease_factor = models.FloatField(default=2.5)

    interval = models.IntegerField(default=1)

    repetitions = models.IntegerField(default=0)

    next_review = models.DateTimeField()

    total_answers = models.IntegerField(default=0)

    correct_answers = models.IntegerField(default=0)

    is_mastered = models.BooleanField(default=False)

  

class StudySession(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()

    cards_reviewed = models.IntegerField(default=0)

    correct = models.IntegerField(default=0)

    xp_earned = models.IntegerField(default=0)

```

  

---

  

### 📅 `daily` — Сегодня

  

Лента выпусков по датам. Разбор = YouTube-плеер + транскрипт + карточки слов выпуска.

  

---

  

### 💳 `subscriptions` — Подписка

  

97 ₽/мес. Закрывает: Кино, Книги, Колоды, Избранное, Повторение.

  

```python

class SubscriptionPlan(models.Model):

    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    duration_days = models.IntegerField()  # 30, 90, 365

  

class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20)  # pending / success / failed

    external_id = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

```

  

---

  

## API-эндпоинты (DRF)

  

```

POST /api/auth/send-otp/

POST /api/auth/verify-otp/

  

GET  /api/catalog/

GET  /api/catalog/<id>/

  

GET  /api/dictionary/lookup/?q=

POST /api/dictionary/favorite/

  

GET  /api/grammar/

POST /api/grammar/<id>/complete/

GET  /api/grammar/<id>/exercise/

  

GET  /api/books/

GET  /api/books/<id>/chapter/<n>/

POST /api/books/import/           # [Admin]

  

GET  /api/kino/

GET  /api/kino/<id>/subtitles/

POST /api/kino/<id>/progress/

  

GET  /api/scroll/feed/

  

GET  /api/kachalka/queue/

POST /api/kachalka/answer/

POST /api/kachalka/mine/

  

POST /api/subscriptions/pay/

POST /api/subscriptions/webhook/

```

  

---

  

## Дизайн-система

  

- Тёмный фон `#0d1117` / `#111827`

- Акценты: синий (Каталог), зелёный (Таблицы), жёлтый (Книги), фиолетовый (Качалка)

- Маскот-собака в разных образах под каждый раздел

- Glassmorphism-карточки, Inter / Roboto Mono для транскрипций

  

---

  

## Порядок разработки

  

### Этап 1 — Фундамент (1 нед.)

- [ ] Django + PostgreSQL + Redis + Celery + Docker Compose

- [ ] `accounts`: OTP через email

- [ ] `core`: базовый шаблон, navbar, дизайн-система

- [ ] `subscriptions`: модели + middleware

  

### Этап 2 — Словарь + AI (1 нед.)

- [ ] `dictionary`: поиск + разбор слова (4 блока)

- [ ] `ai_pipeline`: Celery → AI-обогащение слов

- [ ] `kachalka`: SM-2 + питомец + базовый UI

- [ ] Admin-панель для контента

  

### Этап 3 — Таблицы (3-4 дня)

- [ ] `grammar`: аккордеон → модалка → таблица + упражнение + тренажёр

- [ ] Прогресс пользователя (N/101 пройдено)

  

### Этап 4 — Скролл (1 нед.)

- [ ] `scroll`: вертикальный TikTok-плеер

- [ ] Двойные субтитры EN/RU + клик на слово → попап

- [ ] Intersection Observer для автоплея

  

### Этап 5 — Каталог + Daily (4-5 дней)

- [ ] `catalog`: сетка 710+ выпусков + поиск + фильтры

- [ ] `daily`: лента по датам + страница разбора

  

### Этап 6 — Книги (1-2 нед.)

- [ ] `books`: читалка с двойным подстрочником

- [ ] Celery-импорт EPUB → AI-перевод параграфов

  

### Этап 7 — Кино (1-2 нед.)

- [ ] `kino`: видеоплеер + двойные субтитры SRT

- [ ] Клик на слово → попап + "В карточки"

- [ ] Resume позиции, сдвиг субтитров, скорость

  

### Этап 8 — Деплой

- [ ] Docker + Nginx + Gunicorn

- [ ] Cloudflare R2 для медиа

- [ ] CI/CD (GitHub Actions)

  

---

  

## Открытые вопросы

  

> [!IMPORTANT]

> **AI API:** OpenAI GPT-4o-mini или Gemini Flash (бесплатная квота для разработки)?

  

> [!IMPORTANT]

> **Платёжная система:** YooKassa (97 ₽/мес как на сайте) или Stripe?

  

> [!NOTE]

> **Видео для Кино:** MP4 сам или YouTube-embed + отдельный SRT?

  

> [!NOTE]

> **Книги:** Есть EPUB-файлы или берём с Project Gutenberg (публичное достояние)?

  

> [!NOTE]

> **С какого модуля начнём?** Рекомендую: Фундамент → Словарь → Таблицы → Скролл.