from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Example:
    en: str
    ru: str
    note: str = ""


@dataclass
class FormulaRow:
    subject: str
    affirmative: str
    negative: str
    question: str


@dataclass
class Scenario:
    title: str
    description: str
    examples: list[Example]


@dataclass
class ExerciseItem:
    question: str
    answer: str


@dataclass
class Exercise:
    title: str
    instruction: str
    items: list[ExerciseItem]


@dataclass
class Topic:
    slug: str
    title: str
    subtitle: str
    category: str
    essence: str
    formulas: list[FormulaRow]
    formula_note: str
    scenarios: list[Scenario]
    markers: list[str]
    exercises: list[Exercise]
    order: int = 0
    level: str = "B1"


TOPICS: list[Topic] = []


def get_topic(slug: str) -> Topic | None:
    return next((t for t in TOPICS if t.slug == slug), None)


def filter_topics(q: str = "", category: str = "", level: str = "") -> list[Topic]:
    result = TOPICS
    if category:
        result = [t for t in result if t.category == category]
    if level:
        result = [t for t in result if t.level == level]
    if q:
        q_lower = q.lower()
        result = [t for t in result if q_lower in t.title.lower()]
    return result


CATEGORIES: list[tuple[str, str]] = [
    ("tenses", "Времена"),
    ("conditionals", "Условные"),
    ("modals", "Модальные"),
    ("non_finite", "Неличные формы"),
    ("reported", "Косвенная речь"),
    ("advanced", "Продвинутые"),
]


_PRESENT_SIMPLE = Topic(
    slug="present-simple",
    title="Present Simple",
    subtitle="Настоящее простое",
    category="tenses",
    order=1,
    level="A1",
    essence=(
        "Описывает то, что всегда истинно, повторяется регулярно или "
        "запланировано по расписанию. Это «карта реальности» — факты, "
        "привычки, законы природы."
    ),
    formulas=[
        FormulaRow(
            subject="I / You / We / They",
            affirmative="work",
            negative="do not (don't) work",
            question="Do you work?",
        ),
        FormulaRow(
            subject="He / She / It",
            affirmative="works",
            negative="does not (doesn't) work",
            question="Does he work?",
        ),
    ],
    formula_note=(
        "Орфография для he/she/it: go→goes, watch→watches, " "study→studies, have→has."
    ),
    scenarios=[
        Scenario(
            title="Постоянные факты и общие истины",
            description=(
                "Всё, что всегда было и будет верным — законы физики, "
                "биологии, математики."
            ),
            examples=[
                Example("Water boils at 100°C.", "Вода кипит при 100°C."),
                Example(
                    "The Earth revolves around the Sun.",
                    "Земля вращается вокруг Солнца.",
                ),
            ],
        ),
        Scenario(
            title="Привычки и регулярные действия",
            description=(
                "Действия, которые человек выполняет с определённой "
                "периодичностью. Именно здесь живут маркеры."
            ),
            examples=[
                Example(
                    "She goes to the gym every Monday.",
                    "Она ходит в зал каждый понедельник.",
                ),
                Example(
                    "I don't drink coffee after 6 PM.",
                    "Я не пью кофе после 18:00.",
                ),
            ],
        ),
        Scenario(
            title="Постоянная ситуация",
            description=(
                "Описание черт характера, профессии, места проживания — "
                "всего, что является неизменным фоном жизни."
            ),
            examples=[
                Example("He works as a surgeon.", "Он работает хирургом."),
                Example("They live in Barcelona.", "Они живут в Барселоне."),
            ],
        ),
        Scenario(
            title="Расписания и официальные планы",
            description=(
                "Фиксированное будущее — расписание поездов, самолётов, "
                "официальных мероприятий."
            ),
            examples=[
                Example(
                    "The train leaves at 7:40 tomorrow.",
                    "Поезд уходит в 7:40 завтра.",
                ),
                Example(
                    "The conference starts on Monday.",
                    "Конференция начинается в понедельник.",
                ),
            ],
        ),
        Scenario(
            title="Инструкции и пошаговые описания",
            description=(
                "Рецепты, инструкции, спортивные комментарии в реальном времени."
            ),
            examples=[
                Example(
                    "First, you add the flour, then you stir the mixture.",
                    "Сначала добавьте муку, затем перемешайте.",
                ),
                Example(
                    "He passes to Messi — Messi shoots — goal!",
                    "Он передаёт Месси — Месси бьёт — гол!",
                ),
            ],
        ),
        Scenario(
            title="Глаголы состояния (State Verbs)",
            description=(
                "Глаголы know, believe, understand, love, hate, want, "
                "prefer, seem, belong, contain НЕ используются во "
                "Continuous — только в Simple."
            ),
            examples=[
                Example("I believe you are right.", "Я считаю, ты прав."),
                Example("This bag belongs to her.", "Эта сумка принадлежит ей."),
            ],
        ),
    ],
    markers=[
        "always",
        "usually",
        "often",
        "sometimes",
        "rarely",
        "never",
        "every day / week / year",
        "on Mondays",
        "twice a week",
        "in the morning",
        "as a rule",
        "nowadays",
    ],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction=("Поставьте глагол в правильную форму Present Simple."),
            items=[
                ExerciseItem("He always ___ (read) before bed.", "reads"),
                ExerciseItem(
                    "The train ___ (depart) at 6:15 tomorrow morning.",
                    "departs",
                ),
                ExerciseItem("Butter ___ (melt) when heated.", "melts"),
                ExerciseItem("She ___ not ___ (like) loud music.", "does / like"),
                ExerciseItem(
                    "What ___ you usually ___ (eat) for breakfast?",
                    "do / eat",
                ),
                ExerciseItem("___ your sister ___ (speak) French?", "Does / speak"),
                ExerciseItem("I ___ (think) this is a great idea.", "think"),
            ],
        ),
    ],
)


_PRESENT_CONTINUOUS = Topic(
    slug="present-continuous",
    title="Present Continuous",
    subtitle="Настоящее длительное",
    category="tenses",
    order=2,
    level="A1",
    essence=(
        "Описывает действие, которое происходит прямо сейчас, вокруг "
        "момента речи, или временную ситуацию, а также намеченные "
        "личные планы на ближайшее будущее."
    ),
    formulas=[
        FormulaRow(
            subject="I",
            affirmative="am working",
            negative="am not working",
            question="Am I working?",
        ),
        FormulaRow(
            subject="He / She / It",
            affirmative="is working",
            negative="is not (isn't) working",
            question="Is he working?",
        ),
        FormulaRow(
            subject="You / We / They",
            affirmative="are working",
            negative="are not (aren't) working",
            question="Are they working?",
        ),
    ],
    formula_note=(
        "Орфография: run→running, write→writing, lie→lying, swim→swimming. "
        "Глаголы состояния (know, love, want, believe, own, seem) "
        "НЕ используются в Continuous."
    ),
    scenarios=[
        Scenario(
            title="Действие прямо сейчас",
            description=(
                "Самый очевидный сценарий — то, что происходит в момент речи. "
                "Часто сопровождается словами Look! Listen!"
            ),
            examples=[
                Example(
                    "She is talking on the phone right now.",
                    "Она сейчас разговаривает по телефону.",
                ),
                Example("Why are you laughing?", "Почему ты смеёшься?"),
            ],
        ),
        Scenario(
            title="Временная ситуация вокруг сегодняшнего периода",
            description=(
                "В отличие от Present Simple (постоянно), здесь — ситуация, "
                "которая продолжается лишь какое-то время."
            ),
            examples=[
                Example(
                    "He is staying with his parents this month.",
                    "В этом месяце он живёт у родителей (временно).",
                ),
                Example(
                    "I am working from home this week.",
                    "На этой неделе я работаю дома.",
                ),
            ],
        ),
        Scenario(
            title="Запланированное будущее — личные договорённости",
            description=(
                "Договорённости с конкретным человеком на конкретное "
                "время в ближайшем будущем."
            ),
            examples=[
                Example(
                    "We are meeting Jake at 8 PM tonight.",
                    "Сегодня вечером в 8 мы встречаемся с Джейком.",
                ),
                Example(
                    "I am flying to Rome next Friday.",
                    "В следующую пятницу я лечу в Рим.",
                ),
            ],
        ),
        Scenario(
            title="Раздражающая привычка с always",
            description=(
                "Когда always + Continuous — это НЕ обычная привычка, "
                "а выражение раздражения или недовольства."
            ),
            examples=[
                Example(
                    "He is always losing his keys!",
                    "Он вечно теряет свои ключи! (с раздражением)",
                ),
                Example(
                    "She is always interrupting me!",
                    "Она вечно меня перебивает!",
                ),
            ],
        ),
        Scenario(
            title="Изменения и тренды",
            description=("Описание процессов, которые постепенно меняются."),
            examples=[
                Example(
                    "The climate is getting warmer.",
                    "Климат становится теплее.",
                ),
                Example(
                    "More and more people are switching to electric cars.",
                    "Всё больше людей переходит на электромобили.",
                ),
            ],
        ),
    ],
    markers=[
        "now",
        "right now",
        "at the moment",
        "currently",
        "at present",
        "today",
        "this week / month",
        "still",
        "Look!",
        "Listen!",
        "tonight",
    ],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="Поставьте глагол в Present Continuous.",
            items=[
                ExerciseItem("Quiet! The child ___ (sleep).", "is sleeping"),
                ExerciseItem(
                    "This semester she ___ (take) a programming course.",
                    "is taking",
                ),
                ExerciseItem(
                    "We ___ (meet) tomorrow at 7 PM.",
                    "are meeting",
                ),
                ExerciseItem(
                    "He ___ always ___ (complain) — it's annoying!",
                    "is / complaining",
                ),
                ExerciseItem("The ocean water level ___ (rise).", "is rising"),
                ExerciseItem(
                    "I ___ (think) about your offer. (действие, не состояние)",
                    "am thinking",
                ),
            ],
        ),
    ],
)

_PRESENT_PERFECT = Topic(
    slug="present-perfect",
    title="Present Perfect",
    subtitle="Настоящее совершённое",
    category="tenses",
    order=3,
    level="A2",
    essence=(
        "Мост между прошлым и настоящим. Действие произошло в прошлом, "
        "но его результат важен сейчас или оно связано с незавершённым "
        "периодом времени. Конкретное время НЕ указывается."
    ),
    formulas=[
        FormulaRow(
            subject="I / You / We / They",
            affirmative="have + V³  (I've worked)",
            negative="have not (haven't) + V³",
            question="Have you worked?",
        ),
        FormulaRow(
            subject="He / She / It",
            affirmative="has + V³  (He's worked)",
            negative="has not (hasn't) + V³",
            question="Has he worked?",
        ),
    ],
    formula_note=(
        "V³ = третья форма глагола (Participle II). "
        "Правильные глаголы: work→worked. "
        "Неправильные: go→gone, see→seen, break→broken, write→written. "
        "КЛЮЧЕВОЕ ОТЛИЧИЕ от Past Simple: если время указано "
        "(yesterday, in 2010, last year) — Past Simple. "
        "Если время не указано или не важно — Present Perfect."
    ),
    scenarios=[
        Scenario(
            title="Жизненный опыт",
            description=(
                "Важен сам факт опыта — когда именно, неважно. "
                "Часто с ever / never / before / once / twice."
            ),
            examples=[
                Example(
                    "I have been to Japan twice.",
                    "Я был в Японии дважды.",
                ),
                Example(
                    "Have you ever tried sushi?",
                    "Ты когда-нибудь пробовал суши?",
                ),
                Example(
                    "She has never flown first class.",
                    "Она никогда не летала первым классом.",
                ),
            ],
        ),
        Scenario(
            title="Действие в прошлом — результат виден сейчас",
            description=(
                "Прошлое действие, и его последствия видны или важны "
                "прямо сейчас. Акцент на ТЕКУЩЕМ СОСТОЯНИИ."
            ),
            examples=[
                Example(
                    "He has broken his leg.",
                    "Он сломал ногу.",
                    "(= его нога сломана сейчас)",
                ),
                Example(
                    "I have lost my wallet.",
                    "Я потерял кошелёк.",
                    "(= у меня его нет сейчас)",
                ),
                Example(
                    "Someone has eaten my sandwich!",
                    "Кто-то съел мой бутерброд!",
                    "(= его нет, результат налицо)",
                ),
            ],
        ),
        Scenario(
            title="Незавершённый период времени",
            description=(
                "Период, в котором произошло действие, ещё не закончился. "
                "Часто с today, this week, this year, this morning."
            ),
            examples=[
                Example(
                    "I have drunk three coffees this morning.",
                    "Сегодня утром я выпил три чашки кофе.",
                    "(утро ещё не закончилось)",
                ),
                Example(
                    "She has called me twice today.",
                    "Сегодня она звонила мне дважды.",
                ),
                Example(
                    "We haven't had a holiday this year.",
                    "В этом году у нас не было отпуска.",
                ),
            ],
        ),
        Scenario(
            title="Только что завершённое действие — just",
            description="just ставится между have/has и V³.",
            examples=[
                Example(
                    "I have just finished my report.",
                    "Я только что закончил отчёт.",
                ),
                Example(
                    "The film has just started.",
                    "Фильм только что начался.",
                ),
            ],
        ),
        Scenario(
            title="already и yet",
            description=(
                "already — в утверждениях (раньше ожидаемого). "
                "yet — в отрицаниях и вопросах (ожидаем, но не случилось)."
            ),
            examples=[
                Example(
                    "She has already submitted the application.",
                    "Она уже подала заявку.",
                ),
                Example(
                    "Have you read the report yet?",
                    "Ты уже прочитал отчёт?",
                ),
                Example(
                    "He hasn't called me yet.",
                    "Он ещё не звонил.",
                ),
            ],
        ),
        Scenario(
            title="for и since — длящееся до сих пор состояние",
            description=(
                "Ситуация началась в прошлом и ПРОДОЛЖАЕТСЯ до настоящего. "
                "for + период (for two years), since + точка начала (since 2010)."
            ),
            examples=[
                Example(
                    "I have known her for ten years.",
                    "Я знаю её десять лет.",
                    "(и сейчас знаю)",
                ),
                Example(
                    "They have lived here since 2015.",
                    "Они живут здесь с 2015 года.",
                ),
                Example(
                    "He hasn't eaten anything since this morning.",
                    "Он ничего не ел с утра.",
                ),
            ],
        ),
        Scenario(
            title="lately / recently / so far",
            description=("Обобщение событий за последнее время или на данный момент."),
            examples=[
                Example(
                    "I haven't been feeling well lately.",
                    "В последнее время я чувствую себя неважно.",
                ),
                Example(
                    "So far, we have sold 500 units.",
                    "На данный момент мы продали 500 единиц.",
                ),
            ],
        ),
    ],
    markers=[
        "just",
        "already",
        "yet",
        "ever",
        "never",
        "recently",
        "lately",
        "so far",
        "before",
        "since",
        "for",
        "today",
        "this week / month / year",
        "up to now",
        "it's the first time",
    ],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="Поставьте глагол в Present Perfect.",
            items=[
                ExerciseItem("Have you ever ___ (eat) lobster?", "eaten"),
                ExerciseItem(
                    "Careful! The floor ___ just ___ (wash).",
                    "has / been washed",
                ),
                ExerciseItem(
                    "She ___ (work) at this company for 5 years.",
                    "has worked",
                ),
                ExerciseItem(
                    "I ___ not ___ (watch) this film yet.",
                    "have / watched",
                ),
                ExerciseItem(
                    "They ___ already ___ (send) the parcel.",
                    "have / sent",
                ),
                ExerciseItem(
                    "It's the first time he ___ (visit) London.",
                    "has visited",
                ),
                ExerciseItem(
                    "The weather ___ (be) terrible lately.",
                    "has been",
                ),
            ],
        ),
    ],
)


_PAST_SIMPLE = Topic(
    slug="past-simple",
    title="Past Simple",
    subtitle="Прошедшее простое",
    category="tenses",
    order=5,
    level="A1",
    essence=(
        "Описывает завершённое действие в конкретный момент или период "
        "в прошлом. Время ВСЕГДА указано или подразумевается. "
        "В отличие от Present Perfect — действие изолировано в прошлом, "
        "без связи с настоящим."
    ),
    formulas=[
        FormulaRow(
            subject="I / You / He / She / It / We / They",
            affirmative="V²  (worked, went)",
            negative="did not (didn't) + V¹  (didn't work)",
            question="Did you work? / Did he go?",
        ),
    ],
    formula_note=(
        "V² = вторая форма глагола. Правильные глаголы: +ed (work→worked, "
        "play→played). Неправильные: go→went, see→saw, buy→bought, "
        "take→took, write→wrote. "
        "Глагол to be: was (I/he/she/it), were (you/we/they)."
    ),
    scenarios=[
        Scenario(
            title="Завершённое действие в конкретное время",
            description=(
                "Главный сценарий: действие закончено, время указано явно "
                "или контекстом (yesterday, last year, in 2010, ago)."
            ),
            examples=[
                Example(
                    "I visited Rome last summer.",
                    "Прошлым летом я посетил Рим.",
                ),
                Example(
                    "She called me an hour ago.",
                    "Она позвонила мне час назад.",
                ),
            ],
        ),
        Scenario(
            title="Серия последовательных действий в прошлом",
            description=("Несколько действий, которые произошли одно за другим."),
            examples=[
                Example(
                    "He woke up, had breakfast and left for work.",
                    "Он проснулся, позавтракал и ушёл на работу.",
                ),
                Example(
                    "She opened the door, saw the letter and smiled.",
                    "Она открыла дверь, увидела письмо и улыбнулась.",
                ),
            ],
        ),
        Scenario(
            title="Привычки или повторяющиеся действия в прошлом",
            description=(
                "То, что происходило регулярно в прошлом, но больше не происходит. "
                "Часто с every day, always, used to."
            ),
            examples=[
                Example(
                    "We always spent our summers at the lake.",
                    "Мы всегда проводили лето на озере.",
                ),
                Example(
                    "He smoked a pack a day for twenty years.",
                    "Он курил пачку в день двадцать лет.",
                ),
            ],
        ),
        Scenario(
            title="Условие в реальном прошлом",
            description="В нарративе — фоновый контекст или объяснение.",
            examples=[
                Example(
                    "When I was a student, I lived in a tiny flat.",
                    "Когда я был студентом, я жил в крошечной квартире.",
                ),
            ],
        ),
    ],
    markers=[
        "yesterday",
        "last week / month / year",
        "ago",
        "in 2010",
        "in the morning (вчера)",
        "once",
        "when I was...",
        "at that time",
        "then",
        "the other day",
        "in those days",
    ],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="Поставьте глагол в Past Simple.",
            items=[
                ExerciseItem("She ___ (move) to Paris three years ago.", "moved"),
                ExerciseItem("___ you ___ (see) the match yesterday?", "Did / see"),
                ExerciseItem("He ___ not ___ (come) to the party.", "did / come"),
                ExerciseItem("We ___ (spend) a week in Scotland.", "spent"),
                ExerciseItem("They ___ (not / know) the answer.", "didn't know"),
                ExerciseItem(
                    "What time ___ the train ___ (arrive)?",
                    "did / arrive",
                ),
                ExerciseItem(
                    "I ___ (wake) up late and ___ (miss) the bus.",
                    "woke / missed",
                ),
            ],
        ),
    ],
)

_PAST_CONTINUOUS = Topic(
    slug="past-continuous",
    title="Past Continuous",
    subtitle="Прошедшее длительное",
    category="tenses",
    order=6,
    level="A2",
    essence=(
        "Описывает действие, которое было В ПРОЦЕССЕ в конкретный момент "
        "в прошлом, или служит фоном для другого, более короткого действия."
    ),
    formulas=[
        FormulaRow(
            subject="I / He / She / It",
            affirmative="was + V-ing  (was working)",
            negative="was not (wasn't) + V-ing",
            question="Was he working?",
        ),
        FormulaRow(
            subject="You / We / They",
            affirmative="were + V-ing  (were working)",
            negative="were not (weren't) + V-ing",
            question="Were they working?",
        ),
    ],
    formula_note=(
        "Чаще всего используется в паре с Past Simple: "
        "длительное действие (was doing) = фон, "
        "короткое (did) = событие на этом фоне."
    ),
    scenarios=[
        Scenario(
            title="Действие в процессе в определённый момент прошлого",
            description="Что происходило в конкретный момент вчера/тогда.",
            examples=[
                Example(
                    "At 9 PM yesterday I was watching a film.",
                    "Вчера в 9 вечера я смотрел фильм.",
                ),
                Example(
                    "What were you doing at midnight?",
                    "Что ты делал в полночь?",
                ),
            ],
        ),
        Scenario(
            title="Фон + событие (Past Continuous + Past Simple)",
            description=(
                "Past Continuous описывает длительный фон, Past Simple — "
                "короткое событие, которое прервало или произошло на этом фоне. "
                "Союзы: when, while, as."
            ),
            examples=[
                Example(
                    "I was cooking dinner when the phone rang.",
                    "Я готовил ужин, когда зазвонил телефон.",
                ),
                Example(
                    "While she was reading, the lights went out.",
                    "Пока она читала, погас свет.",
                ),
            ],
        ),
        Scenario(
            title="Два параллельных действия в прошлом",
            description="Два длительных действия, происходивших одновременно.",
            examples=[
                Example(
                    "While I was studying, my brother was playing guitar.",
                    "Пока я учился, брат играл на гитаре.",
                ),
            ],
        ),
    ],
    markers=[
        "at 9 PM yesterday",
        "at that moment",
        "when",
        "while",
        "as",
        "all day long",
        "the whole morning",
    ],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="Используйте Past Simple или Past Continuous.",
            items=[
                ExerciseItem(
                    "She ___ (sleep) when I ___ (call) her.",
                    "was sleeping / called",
                ),
                ExerciseItem("At 8 AM they ___ (have) breakfast.", "were having"),
                ExerciseItem(
                    "While he ___ (drive), his tyre ___ (burst).",
                    "was driving / burst",
                ),
                ExerciseItem(
                    "What ___ you ___ (do) at this time yesterday?",
                    "were / doing",
                ),
            ],
        ),
    ],
)


_PAST_PERFECT = Topic(
    slug="past-perfect",
    title="Past Perfect",
    subtitle="Прошедшее совершённое",
    category="tenses",
    order=7,
    level="B1",
    essence=(
        "«Прошлое до прошлого». Описывает действие, которое завершилось "
        "ДО другого момента или события в прошлом. "
        "Это способ выразить хронологию в рамках прошлого."
    ),
    formulas=[
        FormulaRow(
            subject="I / You / He / She / It / We / They",
            affirmative="had + V³  (had worked, had gone)",
            negative="had not (hadn't) + V³",
            question="Had you finished?",
        ),
    ],
    formula_note=(
        "Часто используется в паре с Past Simple: "
        "had done (более раннее) + did (позднее). "
        "Союзы: before, after, when, by the time, already, just, never."
    ),
    scenarios=[
        Scenario(
            title="Действие до другого прошлого действия",
            description=("Чётко показывает, что одно завершилось раньше другого."),
            examples=[
                Example(
                    "By the time I arrived, the film had already started.",
                    "К тому времени как я пришёл, фильм уже начался.",
                ),
                Example(
                    "She had never seen snow before she moved to Canada.",
                    "Она никогда не видела снег до переезда в Канаду.",
                ),
            ],
        ),
        Scenario(
            title="Причина прошлого состояния",
            description=("Объясняет, почему в прошлом что-то было именно так."),
            examples=[
                Example(
                    "He was tired because he had worked all night.",
                    "Он устал, потому что работал всю ночь.",
                ),
                Example(
                    "They couldn't find the keys — they had left them in the car.",
                    "Они не могли найти ключи — оставили их в машине.",
                ),
            ],
        ),
        Scenario(
            title="После after, when, before, by the time",
            description=(
                "После этих союзов Past Perfect показывает "
                "первое из двух прошлых действий."
            ),
            examples=[
                Example(
                    "After she had finished the report, she went home.",
                    "После того как она закончила отчёт, она пошла домой.",
                ),
            ],
        ),
    ],
    markers=[
        "before",
        "after",
        "when",
        "by the time",
        "already",
        "just",
        "never... before",
        "by 2020",
        "as soon as",
    ],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="Используйте Past Simple или Past Perfect.",
            items=[
                ExerciseItem(
                    "When I arrived, she ___ already ___ (leave).",
                    "had / left",
                ),
                ExerciseItem(
                    "He ___ (not / eat) because he ___ (have) lunch earlier.",
                    "didn't eat / had had",
                ),
                ExerciseItem(
                    "By the time the ambulance ___ (arrive), he ___ (recover).",
                    "arrived / had recovered",
                ),
                ExerciseItem(
                    "___ you ever ___ (try) sushi before you went to Japan?",
                    "Had / tried",
                ),
            ],
        ),
    ],
)


_FUTURE_SIMPLE = Topic(
    slug="future-simple-will",
    title="Future Simple (will)",
    subtitle="Будущее простое",
    category="tenses",
    order=9,
    level="A1",
    essence=(
        "Will используется для спонтанных решений, предсказаний, "
        "обещаний и предложений. Не путать с going to — "
        "там речь о заранее запланированных действиях."
    ),
    formulas=[
        FormulaRow(
            subject="I / You / He / She / It / We / They",
            affirmative="will + V¹  (will work, 'll work)",
            negative="will not (won't) + V¹",
            question="Will you work?",
        ),
    ],
    formula_note=(
        "Will vs Going to: "
        "WILL — спонтанное решение в момент речи, предсказание без доказательств. "
        "GOING TO — заранее принятое решение, предсказание на основе видимых признаков. "
        "'The phone is ringing.' — 'I'll get it!' (спонтанно = will). "
        "'I'm going to call him tonight.' (запланировано = going to)."
    ),
    scenarios=[
        Scenario(
            title="Спонтанное решение в момент речи",
            description=(
                "Решение принято только что, в процессе разговора, "
                "а не заранее. Это главное применение will."
            ),
            examples=[
                Example(
                    "'We've run out of milk.' — 'I'll go and buy some.'",
                    "«Молоко кончилось.» — «Я схожу куплю.»",
                ),
                Example(
                    "'It's cold in here.' — 'I'll close the window.'",
                    "«Здесь холодно.» — «Я закрою окно.»",
                ),
            ],
        ),
        Scenario(
            title="Предсказания и прогнозы",
            description=(
                "Мнение или ожидание о будущем, основанное на личных "
                "убеждениях, а не на конкретных признаках."
            ),
            examples=[
                Example(
                    "I think it will rain tomorrow.",
                    "Я думаю, завтра будет дождь.",
                ),
                Example(
                    "She will be a great doctor one day.",
                    "Когда-нибудь она станет отличным врачом.",
                ),
            ],
        ),
        Scenario(
            title="Обещания, угрозы, клятвы",
            description="Will используется для торжественных заверений.",
            examples=[
                Example("I will always love you.", "Я всегда буду тебя любить."),
                Example("I won't tell anyone.", "Я никому не скажу."),
            ],
        ),
        Scenario(
            title="Предложения и просьбы",
            description="Will you...? — вежливая просьба. I'll... — предложение помощи.",
            examples=[
                Example(
                    "Will you help me with this?",
                    "Ты поможешь мне с этим?",
                ),
                Example(
                    "I'll carry your bags for you.",
                    "Я понесу ваши сумки.",
                ),
            ],
        ),
    ],
    markers=[
        "tomorrow",
        "next week / year",
        "soon",
        "in the future",
        "one day",
        "I think / I'm sure / probably / definitely",
        "I promise",
        "I'm afraid",
    ],
    exercises=[
        Exercise(
            title="will или going to?",
            instruction=("Выберите правильную форму: will + V или going to + V."),
            items=[
                ExerciseItem(
                    "Look at those clouds — it ___ (rain).", "is going to rain"
                ),
                ExerciseItem(
                    "'The bags are heavy.' — 'Don't worry, I ___ (help) you.'",
                    "will help",
                ),
                ExerciseItem(
                    "They ___ (get) married in June. (already planned)",
                    "are going to get",
                ),
                ExerciseItem("I ___ not ___ (tell) anyone your secret.", "will / tell"),
                ExerciseItem("I think prices ___ (rise) next year.", "will rise"),
            ],
        ),
    ],
)


_ZERO_CONDITIONAL = Topic(
    slug="zero-conditional",
    title="Zero Conditional",
    subtitle="Нулевое условное",
    category="conditionals",
    order=1,
    level="A2",
    essence=(
        "Выражает общие истины, научные факты и закономерности — "
        "то, что ВСЕГДА происходит при данном условии. "
        "Обе части предложения в Present Simple."
    ),
    formulas=[
        FormulaRow(
            subject="If / When + условие",
            affirmative="If + Present Simple, + Present Simple",
            negative="If you don't water plants, they die.",
            question="What happens if water reaches 100°C?",
        ),
    ],
    formula_note=(
        "If и when взаимозаменяемы в Zero Conditional. "
        "Если → when, смысл не меняется."
    ),
    scenarios=[
        Scenario(
            title="Научные факты и законы природы",
            description="Абсолютные истины, не зависящие от человека.",
            examples=[
                Example(
                    "If you heat ice, it melts.",
                    "Если нагреть лёд, он тает.",
                ),
                Example(
                    "When the tide comes in, the beach disappears.",
                    "Когда приходит прилив, пляж исчезает.",
                ),
            ],
        ),
        Scenario(
            title="Инструкции и советы (всегда верные)",
            description="Что всегда нужно делать при данных обстоятельствах.",
            examples=[
                Example(
                    "If the alarm goes off, leave the building immediately.",
                    "Если сработает сигнализация, немедленно покиньте здание.",
                ),
            ],
        ),
    ],
    markers=["always", "every time", "when", "if"],
    exercises=[
        Exercise(
            title="Составьте Zero Conditional",
            instruction="Поставьте глаголы в нужную форму.",
            items=[
                ExerciseItem(
                    "If you ___ (mix) red and blue, you ___ (get) purple.",
                    "mix / get",
                ),
                ExerciseItem(
                    "Plants ___ (die) if they ___ (not / get) sunlight.",
                    "die / don't get",
                ),
            ],
        ),
    ],
)


_FIRST_CONDITIONAL = Topic(
    slug="first-conditional",
    title="First Conditional",
    subtitle="Первое условное (реальное)",
    category="conditionals",
    order=2,
    level="B1",
    essence=(
        "Описывает реальные, вероятные ситуации в будущем. "
        "Условие выполнимо — это не фантазия, а реальная возможность."
    ),
    formulas=[
        FormulaRow(
            subject="Структура",
            affirmative="If + Present Simple, + will + V¹",
            negative="If it doesn't rain, we'll have a picnic.",
            question="If you come, will you help?",
        ),
    ],
    formula_note=(
        "ВАЖНО: после if НЕ используется will! "
        "Неверно: If it will rain... "
        "Верно: If it rains, I will... "
        "Вместо will можно: can, may, might, should, must + V."
    ),
    scenarios=[
        Scenario(
            title="Реальное возможное условие в будущем",
            description="Говорящий считает, что условие вполне может выполниться.",
            examples=[
                Example(
                    "If she studies hard, she will pass the exam.",
                    "Если она будет усердно учиться, она сдаст экзамен.",
                ),
                Example(
                    "We will miss the train if we don't hurry.",
                    "Мы опоздаем на поезд, если не поторопимся.",
                ),
            ],
        ),
        Scenario(
            title="Предупреждения и угрозы",
            description="Реальные последствия, которые наступят.",
            examples=[
                Example(
                    "If you touch that, you will burn yourself.",
                    "Если ты это тронешь, обожжёшься.",
                ),
            ],
        ),
        Scenario(
            title="Обещания и предложения",
            description="Реальное обещание, зависящее от условия.",
            examples=[
                Example(
                    "If you help me move, I'll cook dinner.",
                    "Если поможешь мне переехать, я приготовлю ужин.",
                ),
            ],
        ),
    ],
    markers=["if", "unless (= if not)", "as long as", "provided that", "in case"],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="First Conditional: If + Present Simple, + will + V.",
            items=[
                ExerciseItem(
                    "If it ___ (rain), we ___ (stay) at home.",
                    "rains / will stay",
                ),
                ExerciseItem(
                    "She ___ (not / come) unless you ___ (invite) her.",
                    "won't come / invite",
                ),
                ExerciseItem(
                    "If he ___ (study) harder, he ___ (get) better grades.",
                    "studies / will get",
                ),
                ExerciseItem(
                    "___ you ___ (help) me if I ___ (need) you?",
                    "Will / help / need",
                ),
            ],
        ),
    ],
)


_SECOND_CONDITIONAL = Topic(
    slug="second-conditional",
    title="Second Conditional",
    subtitle="Второе условное (нереальное настоящее/будущее)",
    category="conditionals",
    order=3,
    level="B1",
    essence=(
        "Описывает гипотетические, маловероятные или нереальные ситуации "
        "в настоящем или будущем. Говорящий НЕ ожидает, что условие выполнится."
    ),
    formulas=[
        FormulaRow(
            subject="Структура",
            affirmative="If + Past Simple, + would + V¹",
            negative="If I didn't have a car, I would take the bus.",
            question="What would you do if you won the lottery?",
        ),
    ],
    formula_note=(
        "После if be всегда = were (для всех лиц): "
        "'If I were you...' (не 'was'). "
        "Вместо would можно: could, might + V¹. "
        "Сравнение: "
        "1st Conditional: If it rains, I will stay. (реально, вероятно) "
        "2nd Conditional: If it rained, I would stay. (маловероятно / гипотетически)"
    ),
    scenarios=[
        Scenario(
            title="Гипотетическое условие в настоящем или будущем",
            description="Воображаемая ситуация, которой нет и вряд ли будет.",
            examples=[
                Example(
                    "If I had a million dollars, I would travel the world.",
                    "Если бы у меня был миллион долларов, я бы объездил весь мир.",
                ),
                Example(
                    "She would be happier if she changed her job.",
                    "Она была бы счастливее, если бы сменила работу.",
                ),
            ],
        ),
        Scenario(
            title="Советы с If I were you",
            description="Устойчивая конструкция для дачи совета.",
            examples=[
                Example(
                    "If I were you, I would apologise.",
                    "На твоём месте я бы извинился.",
                ),
                Example(
                    "If I were in your situation, I wouldn't sign the contract.",
                    "На твоём месте я бы не подписывал контракт.",
                ),
            ],
        ),
    ],
    markers=[
        "if I were you",
        "imagine",
        "what if",
        "suppose",
        "in your position / place",
    ],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="Second Conditional: If + Past Simple, + would + V.",
            items=[
                ExerciseItem(
                    "If I ___ (be) taller, I ___ (play) basketball.",
                    "were / would play",
                ),
                ExerciseItem(
                    "What ___ you ___ (do) if you ___ (lose) your job?",
                    "would / do / lost",
                ),
                ExerciseItem(
                    "She ___ (travel) more if she ___ (have) more holidays.",
                    "would travel / had",
                ),
                ExerciseItem(
                    "If I ___ (be) you, I ___ (not / accept) that offer.",
                    "were / wouldn't accept",
                ),
            ],
        ),
    ],
)


_THIRD_CONDITIONAL = Topic(
    slug="third-conditional",
    title="Third Conditional",
    subtitle="Третье условное (нереальное прошлое)",
    category="conditionals",
    order=4,
    level="B2",
    essence=(
        "Описывает воображаемые ситуации в прошлом — то, чего НЕ произошло. "
        "Часто выражает сожаление, критику или упрёк: "
        "'Если бы тогда... то сейчас...'"
    ),
    formulas=[
        FormulaRow(
            subject="Структура",
            affirmative="If + Past Perfect, + would have + V³",
            negative="If she hadn't been late, she wouldn't have missed it.",
            question="Would you have come if I had invited you?",
        ),
    ],
    formula_note=(
        "Сжатые формы: 'd have done = would have done. "
        "Вместо would: could have, might have + V³. "
        "Порядок частей можно менять: "
        "'I would have called you if I had known.' = "
        "'If I had known, I would have called you.'"
    ),
    scenarios=[
        Scenario(
            title="Нереальное прошлое — сожаление",
            description="Ситуация в прошлом, которая сложилась иначе. Выражает сожаление.",
            examples=[
                Example(
                    "If I had studied harder, I would have passed the exam.",
                    "Если бы я усерднее учился, я бы сдал экзамен.",
                ),
                Example(
                    "She would have got the job if she had arrived on time.",
                    "Она бы получила работу, если бы пришла вовремя.",
                ),
            ],
        ),
        Scenario(
            title="Упрёк и критика в прошлом",
            description="Что должно было быть сделано иначе.",
            examples=[
                Example(
                    "If you had told me the truth, I wouldn't have been so angry.",
                    "Если бы ты сказал мне правду, я бы не был так зол.",
                ),
            ],
        ),
    ],
    markers=["if only", "I wish", "had known / done / gone earlier"],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="Third Conditional: If + Past Perfect, + would have + V³.",
            items=[
                ExerciseItem(
                    "If he ___ (listen) to the doctor, he ___ (recover) faster.",
                    "had listened / would have recovered",
                ),
                ExerciseItem(
                    "They ___ (not / lose) if they ___ (play) better.",
                    "wouldn't have lost / had played",
                ),
                ExerciseItem(
                    "If I ___ (know) you were coming, I ___ (bake) a cake.",
                    "had known / would have baked",
                ),
                ExerciseItem(
                    "___ you ___ (come) if I ___ (invite) you?",
                    "Would / have come / had invited",
                ),
            ],
        ),
    ],
)


_MODALS_MUST = Topic(
    slug="modals-must-have-to",
    title="Must / Have to / Should",
    subtitle="Обязательство, необходимость, совет",
    category="modals",
    order=2,
    level="A2",
    essence=(
        "Три уровня обязательства: must (внутреннее / субъективное), "
        "have to (внешнее / объективное), should (рекомендация, совет). "
        "Must не имеет прошедшего — используется had to."
    ),
    formulas=[
        FormulaRow(
            subject="must",
            affirmative="must + V¹  (внутренняя необходимость)",
            negative="must not (mustn't) + V¹  (категорический запрет)",
            question="Must I...? (редко; чаще Do I have to...?)",
        ),
        FormulaRow(
            subject="have to",
            affirmative="have to / has to + V¹  (внешняя необходимость)",
            negative="don't / doesn't have to + V¹  (не нужно, необязательно)",
            question="Do / Does + subject + have to + V¹?",
        ),
        FormulaRow(
            subject="should",
            affirmative="should + V¹  (совет, рекомендация)",
            negative="should not (shouldn't) + V¹",
            question="Should I...?",
        ),
    ],
    formula_note=(
        "КЛЮЧЕВОЕ РАЗЛИЧИЕ must vs have to: "
        "'I must go to the gym.' — сам хочу/считаю нужным. "
        "'I have to go to the gym.' — доктор сказал/правило требует. "
        "РАЗЛИЧИЕ mustn't vs don't have to: "
        "mustn't = запрещено (You mustn't smoke here). "
        "don't have to = необязательно (You don't have to come — your choice)."
    ),
    scenarios=[
        Scenario(
            title="Внутренняя обязанность (must)",
            description="Говорящий сам решил, что это необходимо сделать.",
            examples=[
                Example(
                    "I must call my parents today.",
                    "Мне нужно сегодня позвонить родителям.",
                ),
                Example(
                    "You must try this restaurant!",
                    "Тебе обязательно нужно попробовать этот ресторан!",
                ),
            ],
        ),
        Scenario(
            title="Внешняя обязанность (have to)",
            description="Правила, законы, требования других людей.",
            examples=[
                Example(
                    "I have to wear a uniform at work.",
                    "Мне приходится носить форму на работе.",
                ),
                Example(
                    "You have to show your passport at the border.",
                    "На границе нужно показать паспорт.",
                ),
            ],
        ),
        Scenario(
            title="Запрет (mustn't) vs Необязательность (don't have to)",
            description="Самая частая ошибка — смешение этих двух форм.",
            examples=[
                Example(
                    "You mustn't park here. (запрещено!)",
                    "Здесь нельзя парковаться.",
                ),
                Example(
                    "You don't have to come. (необязательно, твой выбор)",
                    "Ты не обязан приходить.",
                ),
            ],
        ),
        Scenario(
            title="Совет и рекомендация (should)",
            description="Говорящий считает это правильным или полезным.",
            examples=[
                Example(
                    "You should see a doctor about that.",
                    "Тебе стоит показаться врачу.",
                ),
                Example(
                    "They shouldn't work so late every day.",
                    "Им не стоит работать допоздна каждый день.",
                ),
            ],
        ),
    ],
    markers=["must", "have to", "should", "ought to", "had to (прошедшее must)"],
    exercises=[
        Exercise(
            title="must / mustn't / have to / don't have to / should",
            instruction="Выберите правильный модальный глагол.",
            items=[
                ExerciseItem(
                    "You ___ touch that wire — it's live! (запрет)",
                    "mustn't",
                ),
                ExerciseItem(
                    "She ___ wear glasses since her operation. (внешняя необходимость)",
                    "has to",
                ),
                ExerciseItem(
                    "You ___ bring food — we have plenty. (необязательно)",
                    "don't have to",
                ),
                ExerciseItem(
                    "I really ___ tidy my room today. (внутреннее решение)",
                    "must",
                ),
                ExerciseItem(
                    "You look tired. You ___ take a break.",
                    "should",
                ),
            ],
        ),
    ],
)


_MODALS_DEDUCTION = Topic(
    slug="modals-deduction-past",
    title="Модальные глаголы: дедукция (прошедшее)",
    subtitle="must have done / can't have done / might have done",
    category="modals",
    order=5,
    level="B2",
    essence=(
        "Выражают предположение или вывод о прошлом на основании "
        "имеющихся фактов. Степень уверенности: "
        "must have done (почти уверен) > might/could have done (возможно) > "
        "can't/couldn't have done (почти уверен, что нет)."
    ),
    formulas=[
        FormulaRow(
            subject="Уверен: это было",
            affirmative="must have + V³",
            negative="—",
            question="—",
        ),
        FormulaRow(
            subject="Уверен: этого не было",
            affirmative="can't / couldn't have + V³",
            negative="—",
            question="—",
        ),
        FormulaRow(
            subject="Возможно / не уверен",
            affirmative="might / could / may have + V³",
            negative="might not have + V³",
            question="—",
        ),
        FormulaRow(
            subject="Упрёк / необходимость в прошлом",
            affirmative="should have + V³  (нужно было, но не сделал)",
            negative="shouldn't have + V³  (не нужно было, но сделал)",
            question="—",
        ),
    ],
    formula_note=(
        "Сравнение с настоящим: "
        "He must be tired. (сейчас) → He must have been tired. (тогда). "
        "She can't be lying. (сейчас) → She can't have lied. (тогда)."
    ),
    scenarios=[
        Scenario(
            title="must have done — почти уверен, что это было",
            description="Логичный вывод из очевидных фактов.",
            examples=[
                Example(
                    "She knows every street here — she must have lived in this city.",
                    "Она знает каждую улицу — она наверняка жила в этом городе.",
                ),
                Example(
                    "He looks exhausted — he must have worked all night.",
                    "Он выглядит измотанным — наверное, работал всю ночь.",
                ),
            ],
        ),
        Scenario(
            title="can't have done — почти уверен, что этого не было",
            description="Отрицательный вывод на основании фактов.",
            examples=[
                Example(
                    "He can't have stolen it — he was with me all evening.",
                    "Он не мог этого украсть — он был со мной весь вечер.",
                ),
                Example(
                    "She can't have forgotten — I reminded her twice.",
                    "Она не могла забыть — я напоминал ей дважды.",
                ),
            ],
        ),
        Scenario(
            title="might / could have done — возможно",
            description="Неуверенность, несколько вариантов объяснения.",
            examples=[
                Example(
                    "He might have missed the bus.",
                    "Возможно, он опоздал на автобус.",
                ),
                Example(
                    "She could have taken a different route.",
                    "Возможно, она поехала другой дорогой.",
                ),
            ],
        ),
        Scenario(
            title="should have done — нужно было, но не сделано (упрёк)",
            description="Упрёк в адрес себя или других за прошлые действия.",
            examples=[
                Example(
                    "You should have told me earlier.",
                    "Тебе нужно было сказать мне раньше.",
                    "(но ты не сказал)",
                ),
                Example(
                    "I shouldn't have eaten so much.",
                    "Мне не нужно было столько есть.",
                    "(но я съел)",
                ),
            ],
        ),
    ],
    markers=[
        "must have",
        "can't have",
        "couldn't have",
        "might have",
        "may have",
        "could have",
        "should have",
        "shouldn't have",
        "ought to have",
    ],
    exercises=[
        Exercise(
            title="Выразите дедукцию о прошлом",
            instruction=(
                "Используйте: must have / can't have / might have / "
                "should have + V³."
            ),
            items=[
                ExerciseItem(
                    "The ground is wet. It ___ (rain) during the night.",
                    "must have rained",
                ),
                ExerciseItem(
                    "He looks pale. He ___ (sleep) well. (= очевидно, не спал)",
                    "can't have slept",
                ),
                ExerciseItem(
                    "I'm not sure where she is. She ___ (go) to the library.",
                    "might have gone",
                ),
                ExerciseItem(
                    "You ___ (tell) her the truth — she's upset now. (упрёк)",
                    "shouldn't have told",
                ),
                ExerciseItem(
                    "He ___ (leave) already — his coat is gone.",
                    "must have left",
                ),
            ],
        ),
    ],
)

_GERUND_INFINITIVE = Topic(
    slug="gerund-infinitive",
    title="Gerund vs Infinitive",
    subtitle="Герундий или инфинитив?",
    category="non_finite",
    order=1,
    level="B1",
    essence=(
        "После некоторых глаголов мы должны использовать герундий (V-ing), "
        "а после других — инфинитив (to V). Герундий чаще выражает реальный "
        "опыт, процесс или завершённое действие. Инфинитив — цель, намерение "
        "или нереализованное действие."
    ),
    formulas=[
        FormulaRow(
            subject="Герундий (Gerund)",
            affirmative="V + V-ing  (enjoy reading)",
            negative="V + not + V-ing",
            question="—",
        ),
        FormulaRow(
            subject="Инфинитив (Infinitive)",
            affirmative="V + to + V¹  (want to read)",
            negative="V + not to + V¹",
            question="—",
        ),
    ],
    formula_note=(
        "Список глаголов, после которых ТОЛЬКО герундий: "
        "enjoy, mind, suggest, avoid, finish, consider, deny, risk, miss, can't help. "
        "Список глаголов, после которых ТОЛЬКО инфинитив: "
        "want, decide, hope, expect, promise, agree, refuse, afford, seem, manage."
    ),
    scenarios=[
        Scenario(
            title="Глаголы, после которых ставится Герундий (V-ing)",
            description="Обычно это глаголы, выражающие предпочтения, завершение действия или избегание.",
            examples=[
                Example(
                    "I enjoy reading in bed.",
                    "Мне нравится читать в постели.",
                ),
                Example(
                    "He suggested going to the cinema.",
                    "Он предложил пойти в кино.",
                ),
            ],
        ),
        Scenario(
            title="Глаголы, после которых ставится Инфинитив (to V)",
            description="Глаголы, выражающие намерения, планы, обещания.",
            examples=[
                Example(
                    "She decided to quit her job.",
                    "Она решила уволиться.",
                ),
                Example(
                    "We hope to see you again.",
                    "Мы надеемся увидеть вас снова.",
                ),
            ],
        ),
        Scenario(
            title="Предлоги + Герундий",
            description="После ЛЮБОГО предлога (in, on, at, for, about, without) ВСЕГДА ставится V-ing.",
            examples=[
                Example(
                    "He is good at playing tennis.",
                    "Он хорошо играет в теннис.",
                ),
                Example(
                    "She left without saying goodbye.",
                    "Она ушла, не попрощавшись.",
                ),
            ],
        ),
        Scenario(
            title="Глаголы, меняющие смысл (remember, stop, try)",
            description=(
                "С этими глаголами можно использовать и то, и другое, но "
                "смысл кардинально меняется."
            ),
            examples=[
                Example(
                    "I stopped to smoke. (остановился, ЧТОБЫ покурить)",
                    "Я остановился покурить.",
                ),
                Example(
                    "I stopped smoking. (бросил сам процесс курения)",
                    "Я бросил курить.",
                ),
                Example(
                    "I remember locking the door. (помню, как делал это в прошлом)",
                    "Я помню, как запирал дверь.",
                ),
                Example(
                    "Remember to lock the door! (не забудь сделать это в будущем)",
                    "Не забудь запереть дверь!",
                ),
            ],
        ),
    ],
    markers=["to", "-ing", "enjoy", "want", "stop", "remember"],
    exercises=[
        Exercise(
            title="Герундий или Инфинитив?",
            instruction="Раскройте скобки, выбрав правильную форму (to V или V-ing).",
            items=[
                ExerciseItem(
                    "I avoid ___ (drive) in the rush hour.",
                    "driving",
                ),
                ExerciseItem(
                    "She promised ___ (help) me with the project.",
                    "to help",
                ),
                ExerciseItem(
                    "He stopped ___ (buy) a newspaper on his way home.",
                    "to buy",
                ),
                ExerciseItem(
                    "Have you finished ___ (paint) the room?",
                    "painting",
                ),
                ExerciseItem(
                    "I am looking forward to ___ (see) you.",
                    "seeing",
                ),
            ],
        ),
    ],
)

_REPORTED_SPEECH = Topic(
    slug="reported-speech",
    title="Reported Speech",
    subtitle="Косвенная речь",
    category="reported",
    order=1,
    level="B1",
    essence=(
        "Используется для передачи чужих слов. Главное правило — "
        "«шаг назад во времени» (согласование времён), если глагол, "
        "вводящий косвенную речь, стоит в прошедшем времени (said, told)."
    ),
    formulas=[
        FormulaRow(
            subject="Present Simple → Past Simple",
            affirmative="'I work' → He said he worked",
            negative="—",
            question="—",
        ),
        FormulaRow(
            subject="Present Continuous → Past Continuous",
            affirmative="'I am working' → He said he was working",
            negative="—",
            question="—",
        ),
        FormulaRow(
            subject="Past Simple / Present Perfect → Past Perfect",
            affirmative="'I worked / I have worked' → He said he had worked",
            negative="—",
            question="—",
        ),
        FormulaRow(
            subject="will → would",
            affirmative="'I will work' → He said he would work",
            negative="—",
            question="—",
        ),
    ],
    formula_note=(
        "say vs tell: "
        "He said (that) he was tired. (без указания кому) "
        "He told me (that) he was tired. (ОБЯЗАТЕЛЬНО указать кому: tell me, tell us). "
        "Вопросы: порядок слов становится прямым (без do/does/did). "
        "'Where do you live?' → He asked where I lived."
    ),
    scenarios=[
        Scenario(
            title="Утверждения",
            description="Прямая речь переводится в косвенную с «шагом назад».",
            examples=[
                Example(
                    "'I like coffee.' → She said she liked coffee.",
                    "Она сказала, что любит кофе.",
                ),
                Example(
                    "'I have finished.' → He told me he had finished.",
                    "Он сказал мне, что закончил.",
                ),
            ],
        ),
        Scenario(
            title="Специальные вопросы (Wh-questions)",
            description="Вопросительное слово сохраняется, порядок слов — прямой.",
            examples=[
                Example(
                    "'Where are you going?' → He asked where I was going.",
                    "Он спросил, куда я иду.",
                ),
            ],
        ),
        Scenario(
            title="Общие вопросы (Yes/No questions)",
            description="Используется if или whether, порядок слов — прямой.",
            examples=[
                Example(
                    "'Are you cold?' → She asked if I was cold.",
                    "Она спросила, холодно ли мне.",
                ),
            ],
        ),
        Scenario(
            title="Приказы и просьбы",
            description="Используется tell / ask + to V.",
            examples=[
                Example(
                    "'Open the door.' → He told me to open the door.",
                    "Он велел мне открыть дверь.",
                ),
                Example(
                    "'Don't shout.' → She asked me not to shout.",
                    "Она попросила меня не кричать.",
                ),
            ],
        ),
    ],
    markers=["said", "told", "asked", "if", "whether", "to"],
    exercises=[
        Exercise(
            title="Переведите в косвенную речь",
            instruction="Переделайте предложение, начав с 'He said/asked...'",
            items=[
                ExerciseItem(
                    "'I am tired.' → He said he ___ tired.",
                    "was",
                ),
                ExerciseItem(
                    "'Do you speak English?' → She asked me ___ I ___ English.",
                    "if / spoke",
                ),
                ExerciseItem(
                    "'Where did you go?' → He asked where I ___.",
                    "had gone",
                ),
                ExerciseItem(
                    "'Don't touch this.' → She told me ___ touch that.",
                    "not to",
                ),
            ],
        ),
    ],
)

_CAUSATIVE = Topic(
    slug="causative",
    title="Causative (have something done)",
    subtitle="Каузативная форма",
    category="advanced",
    order=1,
    level="B2",
    essence=(
        "Используется, когда мы не сами делаем работу, а кто-то другой "
        "(обычно профессионал) делает её для нас за деньги или по нашей просьбе."
    ),
    formulas=[
        FormulaRow(
            subject="have / get",
            affirmative="have / get + объект + V³",
            negative="don't have + объект + V³",
            question="Do you have + объект + V³?",
        ),
    ],
    formula_note=(
        "Форма меняется по временам: I am having my car washed (сейчас), "
        "I had my hair cut (вчера), I will get my house painted (завтра)."
    ),
    scenarios=[
        Scenario(
            title="Услуги, оказанные кем-то другим",
            description="Организация процесса, где физическую работу выполняет кто-то другой.",
            examples=[
                Example(
                    "I had my car repaired yesterday. (Не я чинил, а механик)",
                    "Мне вчера починили машину.",
                ),
                Example(
                    "She is getting her hair cut tomorrow.",
                    "Завтра она идёт стричься. (её постригут)",
                ),
            ],
        ),
        Scenario(
            title="Неприятный опыт (жертва обстоятельств)",
            description="Тоже causative, но в негативном ключе — с нами что-то сделали.",
            examples=[
                Example(
                    "He had his wallet stolen.",
                    "У него украли кошелёк.",
                ),
            ],
        ),
    ],
    markers=["have", "get", "done"],
    exercises=[
        Exercise(
            title="Составьте causative",
            instruction="Используйте have/get + объект + V³.",
            items=[
                ExerciseItem(
                    "I didn't fix the roof myself. I ___ it ___ (fix).",
                    "had / fixed",
                ),
                ExerciseItem(
                    "We need to ___ our windows ___ (clean).",
                    "have / cleaned",
                ),
            ],
        ),
    ],
)


_PASSIVE_VOICE = Topic(
    slug="passive-voice",
    title="Passive Voice",
    subtitle="Пассивный залог",
    category="advanced",
    order=2,
    level="B1",
    essence=(
        "Пассивный залог используется, когда нам важнее само действие или объект, "
        "над которым оно совершается, а не тот, кто его выполняет. Исполнитель часто "
        "неизвестен, не важен или очевиден."
    ),
    formulas=[
        FormulaRow(
            subject="Present Simple Passive",
            affirmative="am/is/are + V³",
            negative="am/is/are not + V³",
            question="Am/Is/Are + объект + V³?",
        ),
        FormulaRow(
            subject="Past Simple Passive",
            affirmative="was/were + V³",
            negative="was/were not + V³",
            question="Was/Were + объект + V³?",
        ),
        FormulaRow(
            subject="Future Simple Passive",
            affirmative="will be + V³",
            negative="will not be + V³",
            question="Will + объект + be + V³?",
        ),
        FormulaRow(
            subject="Present Perfect Passive",
            affirmative="have/has been + V³",
            negative="have/has not been + V³",
            question="Have/Has + объект + been + V³?",
        ),
    ],
    formula_note=(
        "Если нам всё-таки нужно указать, кем выполнено действие, "
        "используется предлог 'by' (by Shakespeare, by the police). "
        "Если указываем инструмент/орудие — предлог 'with' (with a knife)."
    ),
    scenarios=[
        Scenario(
            title="Исполнитель неизвестен или не важен",
            description="Мы не знаем или нам всё равно, кто сделал это действие.",
            examples=[
                Example(
                    "My car was stolen last night.",
                    "Мою машину украли прошлой ночью.",
                ),
                Example(
                    "The house was built in 1920.",
                    "Дом был построен в 1920 году.",
                ),
            ],
        ),
        Scenario(
            title="Исполнитель очевиден из контекста",
            description="Нет смысла уточнять, так как это и так понятно.",
            examples=[
                Example(
                    "The thief was arrested.",
                    "Вор был арестован. (очевидно, что полицией)",
                ),
            ],
        ),
        Scenario(
            title="Формальный стиль и инструкции",
            description="Пассив часто используется в новостях, отчётах и инструкциях.",
            examples=[
                Example(
                    "Passengers are asked not to leave their bags unattended.",
                    "Пассажиров просят не оставлять сумки без присмотра.",
                ),
                Example(
                    "The results will be published next week.",
                    "Результаты будут опубликованы на следующей неделе.",
                ),
            ],
        ),
    ],
    markers=["by", "with", "is made", "was written", "will be done"],
    exercises=[
        Exercise(
            title="Актив или Пассив?",
            instruction="Раскройте скобки, выбрав правильный залог (Active или Passive).",
            items=[
                ExerciseItem(
                    "The letter ___ (send) two days ago.",
                    "was sent",
                ),
                ExerciseItem(
                    "Millions of people ___ (use) the internet every day.",
                    "use",
                ),
                ExerciseItem(
                    "This room ___ (clean) every morning.",
                    "is cleaned",
                ),
                ExerciseItem(
                    "A new bridge ___ (build) next year.",
                    "will be built",
                ),
            ],
        ),
    ],
)


_ARTICLES = Topic(
    slug="articles",
    title="Articles (a, an, the)",
    subtitle="Артикли",
    category="advanced",
    order=3,
    level="A2",
    essence=(
        "Артикли определяют, говорим ли мы о чём-то конкретном и известном "
        "собеседнику (the), или о чём-то неопределённом, одном из многих (a/an). "
        "Также существует нулевой артикль (его отсутствие)."
    ),
    formulas=[
        FormulaRow(
            subject="A / An (Неопределённый)",
            affirmative="a + согласный звук (a book), an + гласный звук (an apple)",
            negative="Только для исчисляемых в ед. числе!",
            question="—",
        ),
        FormulaRow(
            subject="The (Определённый)",
            affirmative="the + любое существительное (ед. и мн. число)",
            negative="Когда собеседник понимает, о каком именно предмете речь.",
            question="—",
        ),
        FormulaRow(
            subject="Zero Article (Нулевой)",
            affirmative="Без артикля (вообще, в целом)",
            negative="Для неисчисляемых или мн. числа при обобщении.",
            question="—",
        ),
    ],
    formula_note=(
        "Обратите внимание на ЗВУК, а не букву. "
        "an hour (начинается с гласного звука 'ауэр'), a university (согласный 'ю')."
    ),
    scenarios=[
        Scenario(
            title="A/An — впервые упоминаем, один из многих",
            description="Собеседник ещё не знает, о чём речь. Это не уникальный предмет.",
            examples=[
                Example(
                    "I bought a car.",
                    "Я купил машину. (какую-то одну машину)",
                ),
                Example(
                    "She is a doctor.",
                    "Она врач. (одна из профессии)",
                ),
            ],
        ),
        Scenario(
            title="The — конкретный, уже упомянутый, уникальный",
            description="И мы, и собеседник понимаем, о чём конкретно речь.",
            examples=[
                Example(
                    "I bought a car. The car is red.",
                    "Я купил машину. (Эта) машина — красная.",
                ),
                Example(
                    "Could you close the door?",
                    "Можешь закрыть дверь? (очевидно, какую именно)",
                ),
                Example(
                    "The sun is shining.",
                    "Солнце светит. (оно уникально)",
                ),
            ],
        ),
        Scenario(
            title="Обобщение (Zero Article)",
            description="Когда мы говорим о вещах в целом (неисчисляемые или множественное число).",
            examples=[
                Example(
                    "I love coffee.",
                    "Я люблю кофе. (вообще, любой кофе)",
                ),
                Example(
                    "Apples are healthy.",
                    "Яблоки полезны. (яблоки вообще)",
                ),
            ],
        ),
    ],
    markers=["a", "an", "the"],
    exercises=[
        Exercise(
            title="Вставьте артикль",
            instruction="Используйте a, an, the или — (ничего).",
            items=[
                ExerciseItem(
                    "I have ___ dog and ___ cat. ___ dog is very friendly.",
                    "a / a / The",
                ),
                ExerciseItem(
                    "Can you turn off ___ light, please?",
                    "the",
                ),
                ExerciseItem(
                    "___ water freezes at 0 degrees Celsius.",
                    "—",
                ),
                ExerciseItem(
                    "She works as ___ accountant in ___ hospital.",
                    "an / a",
                ),
            ],
        ),
    ],
)


_USED_TO = Topic(
    slug="used-to",
    title="used to / be used to / get used to",
    subtitle="Привычки в прошлом и настоящем",
    category="advanced",
    order=4,
    level="B1",
    essence=(
        "Эти три конструкции звучат похоже, но означают совершенно разное. "
        "'used to do' — это то, что было раньше, но больше не происходит. "
        "'be used to doing' — привычка в настоящем (я привык к этому). "
        "'get used to doing' — процесс привыкания."
    ),
    formulas=[
        FormulaRow(
            subject="used to (Прошлая привычка)",
            affirmative="used to + V¹",
            negative="didn't use to + V¹",
            question="Did you use to + V¹?",
        ),
        FormulaRow(
            subject="be used to (Привык к...)",
            affirmative="am/is/are used to + V-ing (или существительное)",
            negative="am/is/are not used to + V-ing",
            question="Are you used to + V-ing?",
        ),
        FormulaRow(
            subject="get used to (Привыкаю к...)",
            affirmative="get / got / will get used to + V-ing",
            negative="haven't got used to + V-ing",
            question="Have you got used to + V-ing?",
        ),
    ],
    formula_note=(
        "ВАЖНО: после 'be used to' и 'get used to' ставится V-ing, а не начальная форма глагола! "
        "I am used to getting up early (а не to get up)."
    ),
    scenarios=[
        Scenario(
            title="used to do — было раньше, но не сейчас",
            description="Регулярные действия или состояния в прошлом, которые больше не актуальны.",
            examples=[
                Example(
                    "I used to smoke, but I gave up five years ago.",
                    "Раньше я курил, но бросил 5 лет назад.",
                ),
                Example(
                    "There used to be a cinema here.",
                    "Раньше здесь был кинотеатр.",
                ),
            ],
        ),
        Scenario(
            title="be used to doing — привычное, нормальное состояние",
            description="Для вас это не ново, вы к этому адаптировались.",
            examples=[
                Example(
                    "I am used to living alone.",
                    "Я привык жить один. (меня это не напрягает)",
                ),
                Example(
                    "She isn't used to the cold weather.",
                    "Она не привыкла к холодной погоде.",
                ),
            ],
        ),
        Scenario(
            title="get used to doing — процесс привыкания",
            description="Переход из состояния 'непривычно' в состояние 'привычно'.",
            examples=[
                Example(
                    "I can't get used to this new software.",
                    "Я никак не могу привыкнуть к этой новой программе.",
                ),
                Example(
                    "He will soon get used to working night shifts.",
                    "Вскоре он привыкнет работать в ночные смены.",
                ),
            ],
        ),
    ],
    markers=["used to", "be used to", "get used to"],
    exercises=[
        Exercise(
            title="Выберите правильную конструкцию",
            instruction="Вставьте used to, be used to или get used to в нужной форме.",
            items=[
                ExerciseItem(
                    "I ___ (live) in a flat, but now I live in a house.",
                    "used to live",
                ),
                ExerciseItem(
                    "I have lived in London for 10 years, so I ___ (drive) on the left.",
                    "am used to driving",
                ),
                ExerciseItem(
                    "It's difficult at first, but you will ___ (it).",
                    "get used to it",
                ),
                ExerciseItem(
                    "___ you ___ (play) football when you were young?",
                    "Did / use to play",
                ),
            ],
        ),
    ],
)


_PRESENT_PERFECT_CONTINUOUS = Topic(
    slug="present-perfect-continuous",
    title="Present Perfect Continuous",
    subtitle="Настоящее совершённо-длительное",
    category="tenses",
    order=4,
    level="B1",
    essence=(
        "Описывает действие, которое началось в прошлом и ПРОДОЛЖАЕТСЯ вплоть "
        "до момента речи (или только что завершилось, оставив видимый результат). "
        "Главный акцент — на длительности процесса (как долго это происходит?)."
    ),
    formulas=[
        FormulaRow(
            subject="I / You / We / They",
            affirmative="have been + V-ing",
            negative="have not been + V-ing",
            question="Have you been + V-ing?",
        ),
        FormulaRow(
            subject="He / She / It",
            affirmative="has been + V-ing",
            negative="has not been + V-ing",
            question="Has she been + V-ing?",
        ),
    ],
    formula_note=(
        "В отличие от Present Perfect (I have painted the wall — стена покрашена), "
        "Continuous подчёркивает процесс (I have been painting the wall — я весь в краске, "
        "и возможно, ещё не закончил). "
        "С глаголами состояния (know, like, belong) НЕ используется — берем обычный Present Perfect."
    ),
    scenarios=[
        Scenario(
            title="Действие началось в прошлом и всё ещё продолжается",
            description="Обязательно указано КАК ДОЛГО (for, since, all day).",
            examples=[
                Example(
                    "I have been learning English for three years.",
                    "Я изучаю английский уже три года. (и продолжаю)",
                ),
                Example(
                    "It has been raining since morning.",
                    "С утра идёт дождь.",
                ),
            ],
        ),
        Scenario(
            title="Действие только что завершилось (видимый результат)",
            description="Сам процесс объясняет результат в настоящем.",
            examples=[
                Example(
                    "Why are your hands dirty? — I have been repairing the car.",
                    "Почему у тебя грязные руки? — Я чинил машину.",
                ),
                Example(
                    "You look exhausted. Have you been running?",
                    "Ты выглядишь измотанным. Ты бегал?",
                ),
            ],
        ),
    ],
    markers=[
        "for",
        "since",
        "how long",
        "all day",
        "all morning",
        "lately",
        "recently",
    ],
    exercises=[
        Exercise(
            title="Present Perfect или Present Perfect Continuous?",
            instruction="Раскройте скобки в правильном времени.",
            items=[
                ExerciseItem(
                    "She ___ (read) that book all day.",
                    "has been reading",
                ),
                ExerciseItem(
                    "I ___ (read) 50 pages of that book.",
                    "have read",
                ),
                ExerciseItem(
                    "How long ___ you ___ (wait)?",
                    "have / been waiting",
                ),
                ExerciseItem(
                    "I ___ (know) him for ten years. (know - глагол состояния)",
                    "have known",
                ),
            ],
        ),
    ],
)


_MIXED_CONDITIONALS = Topic(
    slug="mixed-conditionals",
    title="Mixed Conditionals",
    subtitle="Смешанные условные предложения",
    category="conditionals",
    order=5,
    level="B2",
    essence=(
        "Смешанные условные предложения используются, когда условие и следствие "
        "относятся к разным временам. Например: условие было в прошлом, а результат "
        "влияет на настоящее (Past → Present), или наоборот (Present → Past)."
    ),
    formulas=[
        FormulaRow(
            subject="Past → Present (Type 3 + 2)",
            affirmative="If + Past Perfect, + would + V¹",
            negative="If I hadn't stayed up late, I wouldn't be tired now.",
            question="—",
        ),
        FormulaRow(
            subject="Present → Past (Type 2 + 3)",
            affirmative="If + Past Simple, + would have + V³",
            negative="If I were you, I would have told him.",
            question="—",
        ),
    ],
    formula_note=(
        "Type 3+2: Сожаление о прошлом, которое влияет на то, что происходит СЕЙЧАС. "
        "Type 2+3: Постоянное условие (характер, факт), которое повлияло на событие В ПРОШЛОМ."
    ),
    scenarios=[
        Scenario(
            title="Прошлое действие → Результат в настоящем",
            description="То, что мы сделали (или не сделали) в прошлом, привело к ситуации сейчас.",
            examples=[
                Example(
                    "If I had studied medicine, I would be a doctor now.",
                    "Если бы я учился на врача (тогда), я был бы врачом сейчас.",
                ),
                Example(
                    "If she had caught the flight, she would be here by now.",
                    "Если бы она успела на рейс (вчера), она была бы уже здесь (сейчас).",
                ),
            ],
        ),
        Scenario(
            title="Постоянное состояние → Результат в прошлом",
            description="Неизменный факт (настоящее) повлиял на ситуацию в прошлом.",
            examples=[
                Example(
                    "If I spoke French, I would have translated that document for you.",
                    "Если бы я (вообще) говорил по-французски, я бы перевел тебе тот документ (вчера).",
                ),
                Example(
                    "If he weren't so afraid of heights, he would have climbed the mountain.",
                    "Если бы он не боялся высоты (вообще), он бы поднялся на гору (тогда).",
                ),
            ],
        ),
    ],
    markers=["if", "would", "would have", "had done", "now"],
    exercises=[
        Exercise(
            title="Выберите правильную комбинацию",
            instruction="Определите, к какому времени относится условие, а к какому - результат.",
            items=[
                ExerciseItem(
                    "If I ___ (not/lose) my passport yesterday, I ___ (not/sit) in the embassy now.",
                    "hadn't lost / wouldn't be sitting",
                ),
                ExerciseItem(
                    "If he ___ (be) a faster runner, he ___ (win) the race last week.",
                    "were / would have won",
                ),
            ],
        ),
    ],
)


_WISHES_REGRETS = Topic(
    slug="wishes-regrets",
    title="I wish / If only",
    subtitle="Желания и сожаления",
    category="advanced",
    order=5,
    level="B2",
    essence=(
        "Используется для выражения сожаления о том, что ситуация не такова, "
        "как нам хотелось бы. Работает по принципу условных предложений: "
        "делаем 'шаг назад' во времени."
    ),
    formulas=[
        FormulaRow(
            subject="Желание в настоящем",
            affirmative="I wish / If only + Past Simple (или were)",
            negative="I wish I had a car.",
            question="—",
        ),
        FormulaRow(
            subject="Сожаление о прошлом",
            affirmative="I wish / If only + Past Perfect",
            negative="I wish I had studied harder.",
            question="—",
        ),
        FormulaRow(
            subject="Жалоба / раздражение",
            affirmative="I wish / If only + would + V¹",
            negative="I wish you would stop talking.",
            question="—",
        ),
    ],
    formula_note=(
        "'If only' звучит более эмоционально, чем 'I wish'. "
        "Мы НЕ используем 'would' для своих собственных действий (нельзя: I wish I would...)."
    ),
    scenarios=[
        Scenario(
            title="Недовольство ситуацией в настоящем",
            description="Хочу, чтобы прямо сейчас или вообще всё было иначе.",
            examples=[
                Example(
                    "I wish I were taller.",
                    "Жаль, что я не выше. (Хотел бы я быть выше.)",
                ),
                Example(
                    "If only we didn't have to work today.",
                    "Ах, если бы нам не нужно было сегодня работать.",
                ),
            ],
        ),
        Scenario(
            title="Сожаление о прошлом",
            description="Поздно что-то менять, мы лишь сожалеем.",
            examples=[
                Example(
                    "I wish I hadn't eaten so much cake.",
                    "Жаль, что я съел так много торта.",
                ),
                Example(
                    "If only I had known you were coming!",
                    "Если бы я только знал, что ты придёшь!",
                ),
            ],
        ),
        Scenario(
            title="Раздражение чьим-то поведением",
            description="Хотим, чтобы кто-то другой изменил своё поведение в будущем.",
            examples=[
                Example(
                    "I wish he would stop complaining.",
                    "Хоть бы он перестал жаловаться.",
                ),
                Example(
                    "I wish it would stop raining.",
                    "Хоть бы дождь прекратился.",
                ),
            ],
        ),
    ],
    markers=["I wish", "If only"],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="Сделайте 'шаг назад' во времени.",
            items=[
                ExerciseItem(
                    "I wish I ___ (speak) Italian. (but I don't)",
                    "spoke",
                ),
                ExerciseItem(
                    "I wish I ___ (not/say) that to him yesterday.",
                    "hadn't said",
                ),
                ExerciseItem(
                    "If only she ___ (call) me earlier!",
                    "had called",
                ),
                ExerciseItem(
                    "I wish you ___ (stop) making that noise! (раздражение)",
                    "would stop",
                ),
            ],
        ),
    ],
)


_FUTURE_CONTINUOUS = Topic(
    slug="future-continuous-perfect",
    title="Future Continuous & Perfect",
    subtitle="Длительное и завершённое будущее",
    category="tenses",
    order=10,
    level="B2",
    essence=(
        "Future Continuous показывает процесс в определенный момент в будущем. "
        "Future Perfect показывает действие, которое завершится К определенному моменту в будущем."
    ),
    formulas=[
        FormulaRow(
            subject="Future Continuous",
            affirmative="will be + V-ing",
            negative="will not (won't) be + V-ing",
            question="Will you be + V-ing?",
        ),
        FormulaRow(
            subject="Future Perfect",
            affirmative="will have + V³",
            negative="will not (won't) have + V³",
            question="Will you have + V³?",
        ),
    ],
    formula_note=(
        "Маркер Future Perfect — предлог 'by' (к какому-то времени): by 5 PM, by next week. "
        "Маркер Future Continuous — точное время в будущем: at 5 PM tomorrow, this time next week."
    ),
    scenarios=[
        Scenario(
            title="Future Continuous: Процесс в будущем",
            description="Мы будем находиться в середине действия.",
            examples=[
                Example(
                    "This time tomorrow, I will be flying to Paris.",
                    "Завтра в это же время я буду лететь в Париж.",
                ),
                Example(
                    "Don't call me at 8. I will be having dinner.",
                    "Не звони мне в 8. Я буду ужинать.",
                ),
            ],
        ),
        Scenario(
            title="Future Perfect: Результат К моменту в будущем",
            description="Действие уже полностью завершится ДО наступления дедлайна.",
            examples=[
                Example(
                    "I will have finished the report by Friday.",
                    "Я закончу отчет к пятнице.",
                ),
                Example(
                    "By the time you arrive, we will have eaten all the pizza.",
                    "К тому моменту как ты приедешь, мы съедим всю пиццу.",
                ),
            ],
        ),
    ],
    markers=["by", "at 5 PM", "this time tomorrow", "by the time"],
    exercises=[
        Exercise(
            title="Continuous или Perfect?",
            instruction="Раскройте скобки в правильном будущем времени.",
            items=[
                ExerciseItem(
                    "By the end of the year, she ___ (save) $5000.",
                    "will have saved",
                ),
                ExerciseItem(
                    "At 10 AM tomorrow, we ___ (write) an exam.",
                    "will be writing",
                ),
                ExerciseItem(
                    "Don't come around 6 PM. I ___ (work) out.",
                    "will be working",
                ),
                ExerciseItem(
                    "I ___ (read) this book by next Monday.",
                    "will have read",
                ),
            ],
        ),
    ],
)


_PAST_PERFECT_CONTINUOUS = Topic(
    slug="past-perfect-continuous",
    title="Past Perfect Continuous",
    subtitle="Прошедшее совершённо-длительное",
    category="tenses",
    order=8,
    level="B2",
    essence=(
        "Описывает действие, которое длилось в прошлом в течение какого-то времени ДО другого "
        "момента в прошлом. Акцент делается на самом процессе и его длительности."
    ),
    formulas=[
        FormulaRow(
            subject="Все лица",
            affirmative="had been + V-ing",
            negative="had not (hadn't) been + V-ing",
            question="Had + subject + been + V-ing?",
        ),
    ],
    formula_note="С глаголами состояния (know, like) используем обычный Past Perfect (had known).",
    scenarios=[
        Scenario(
            title="Процесс ДО другого действия в прошлом",
            description="Подчеркивает, как долго продолжалось действие до того, как случилось что-то еще.",
            examples=[
                Example(
                    "I had been waiting for an hour when the bus finally arrived.",
                    "Я прождал час, когда наконец приехал автобус.",
                ),
                Example(
                    "They had been talking for 2 hours before the boss walked in.",
                    "Они разговаривали 2 часа, прежде чем вошел босс.",
                ),
            ],
        ),
        Scenario(
            title="Причина видимого результата в прошлом",
            description="Объясняет причину состояния в прошлом через длительный процесс.",
            examples=[
                Example(
                    "He was tired because he had been working all day.",
                    "Он устал, потому что работал весь день.",
                ),
                Example(
                    "The ground was wet. It had been raining.",
                    "Земля была мокрой. Шел дождь (до этого).",
                ),
            ],
        ),
    ],
    markers=["for", "since", "all day", "before", "when"],
    exercises=[
        Exercise(
            title="Past Perfect или Past Perfect Continuous?",
            instruction="Раскройте скобки.",
            items=[
                ExerciseItem(
                    "She was exhausted because she ___ (study) all night.",
                    "had been studying",
                ),
                ExerciseItem(
                    "When I arrived, they ___ (already/eat) dinner.",
                    "had already eaten",
                ),
            ],
        )
    ],
)


_FUTURE_PERFECT_CONTINUOUS = Topic(
    slug="future-perfect-continuous",
    title="Future Perfect Continuous",
    subtitle="Будущее совершённо-длительное",
    category="tenses",
    order=11,
    level="B2",
    essence=(
        "Описывает действие, которое будет длиться вплоть до определенного момента в будущем. "
        "Мы смотрим из будущего назад и подчеркиваем, сколько времени уже займет процесс."
    ),
    formulas=[
        FormulaRow(
            subject="Все лица",
            affirmative="will have been + V-ing",
            negative="will not (won't) have been + V-ing",
            question="Will + subject + have been + V-ing?",
        ),
    ],
    formula_note="Очень редкое время. Обязательно нужны два обстоятельства: 'к какому моменту' (by) и 'как долго' (for).",
    scenarios=[
        Scenario(
            title="Длительность к моменту в будущем",
            description="",
            examples=[
                Example(
                    "By next month, I will have been living here for 5 years.",
                    "К следующему месяцу будет 5 лет, как я здесь живу.",
                ),
                Example(
                    "By 6 PM, she will have been working for ten hours straight.",
                    "К 6 вечера она будет работать 10 часов подряд.",
                ),
            ],
        )
    ],
    markers=["by...", "for..."],
    exercises=[
        Exercise(
            title="Раскройте скобки",
            instruction="",
            items=[
                ExerciseItem(
                    "By December, we ___ (work) on this project for a year.",
                    "will have been working",
                )
            ],
        )
    ],
)


_COMPLEX_PASSIVE = Topic(
    slug="complex-passive",
    title="Complex Passive (It is said...)",
    subtitle="Сложный пассив и глаголы мнения",
    category="advanced",
    order=4,
    level="B2",
    essence=(
        "Используется для передачи слухов, общих мнений, новостей. Вместо 'People say that he is rich' "
        "мы используем формальные пассивные конструкции."
    ),
    formulas=[
        FormulaRow(
            subject="Безличная (It is...)",
            affirmative="It is said/believed/thought + that...",
            negative="It is not thought that...",
            question="—",
        ),
        FormulaRow(
            subject="Личная (He is...)",
            affirmative="Subject + is said/believed + to V (или to have V³)",
            negative="He is not believed to be...",
            question="—",
        ),
    ],
    formula_note="Если действие относится к прошлому (случилось ДО мнения), используем Perfect Infinitive (to have done).",
    scenarios=[
        Scenario(
            title="Передача новостей и фактов",
            description="Типично для журналистики и формального стиля.",
            examples=[
                Example(
                    "It is reported that the president will resign.",
                    "Сообщают, что президент уйдет в отставку.",
                ),
                Example(
                    "He is known to be a hard worker.", "Известно, что он трудоголик."
                ),
            ],
        ),
        Scenario(
            title="Отношение к прошлому (to have done)",
            description="О действии, которое уже произошло.",
            examples=[
                Example(
                    "The company is believed to have lost millions.",
                    "Считается, что компания потеряла миллионы.",
                )
            ],
        ),
        Scenario(
            title="Пассив с двумя дополнениями",
            description="Глаголы give, send, show. Можно сделать пассив двумя способами.",
            examples=[
                Example(
                    "They gave him a reward. → He was given a reward. (Предпочтительно)",
                    "Ему дали награду.",
                ),
                Example("→ A reward was given to him.", "Награда была дана ему."),
            ],
        ),
    ],
    markers=["it is said", "is expected to", "is believed to"],
    exercises=[
        Exercise(
            title="Перефразируйте",
            instruction="Начните предложение с указанного слова.",
            items=[
                ExerciseItem(
                    "People think he is hiding in Brazil. → He...",
                    "is thought to be hiding in Brazil",
                ),
                ExerciseItem(
                    "They say she stole the money. → She...",
                    "is said to have stolen the money",
                ),
            ],
        )
    ],
)


_REPORTING_VERBS = Topic(
    slug="reporting-verbs",
    title="Reporting Verbs",
    subtitle="Глаголы косвенной речи",
    category="reported",
    order=2,
    level="B2",
    essence=(
        "В косвенной речи мы не обязаны всегда использовать 'say' или 'tell'. "
        "Гораздо точнее передать смысл с помощью глаголов-рефлеквов (advise, promise, apologize, deny)."
    ),
    formulas=[
        FormulaRow(
            subject="Verb + to V",
            affirmative="agree, promise, refuse, offer, threaten + to V",
            negative="He refused to help.",
            question="—",
        ),
        FormulaRow(
            subject="Verb + Object + to V",
            affirmative="advise, ask, invite, order, warn + sb + to V",
            negative="She warned me not to go.",
            question="—",
        ),
        FormulaRow(
            subject="Verb + V-ing",
            affirmative="deny, recommend, suggest, admit + V-ing",
            negative="He denied stealing the car.",
            question="—",
        ),
    ],
    formula_note="Некоторые глаголы требуют предлога перед герундием: apologize FOR doing, accuse sb OF doing, blame sb FOR doing.",
    scenarios=[
        Scenario(
            title="Передача намерений",
            description="",
            examples=[
                Example(
                    "'I'll help you' → He promised to help me.", "Он пообещал помочь."
                ),
                Example(
                    "'You should see a doctor' → She advised me to see a doctor.",
                    "Она посоветовала обратиться к врачу.",
                ),
            ],
        ),
        Scenario(
            title="Передача извинений и обвинений",
            description="",
            examples=[
                Example(
                    "'I'm sorry I broke it' → He apologized for breaking it.",
                    "Он извинился за то, что сломал это.",
                ),
                Example(
                    "'You took the money!' → They accused him of taking the money.",
                    "Они обвинили его в краже денег.",
                ),
            ],
        ),
    ],
    markers=["promise", "refuse", "advise", "suggest", "deny"],
    exercises=[
        Exercise(
            title="Выберите правильную конструкцию",
            instruction="",
            items=[
                ExerciseItem("She suggested ___ (go) to the cinema.", "going"),
                ExerciseItem(
                    "They warned us ___ (not/touch) the wire.", "not to touch"
                ),
                ExerciseItem("He apologized for ___ (be) late.", "being"),
            ],
        )
    ],
)


_COMPLEX_OBJECT = Topic(
    slug="complex-object",
    title="Complex Object",
    subtitle="Сложное дополнение",
    category="non_finite",
    order=2,
    level="B2",
    essence=(
        "Конструкция 'Verb + Object + Infinitive/V-ing'. Мы используем её, когда хотим, "
        "чтобы кто-то другой совершил действие, или когда мы воспринимаем чужое действие."
    ),
    formulas=[
        FormulaRow(
            subject="С глаголами желания (want, expect)",
            affirmative="I want him to go.",
            negative="I don't want him to go.",
            question="—",
        ),
        FormulaRow(
            subject="С глаголами let / make (без to)",
            affirmative="make/let sb do sth (He makes me laugh).",
            negative="Don't let him go.",
            question="—",
        ),
        FormulaRow(
            subject="С глаголами чувств (see, hear, notice)",
            affirmative="see sb do (весь процесс) / see sb doing (часть процесса)",
            negative="—",
            question="—",
        ),
    ],
    formula_note="В пассивном залоге после make инфинитив возвращает частицу 'to': I was made TO clean the room.",
    scenarios=[
        Scenario(
            title="Желание или ожидание",
            description="",
            examples=[
                Example(
                    "I want you to help me.",
                    "Я хочу, чтобы ты помог мне. (Не 'I want that you help')",
                ),
                Example("We expect them to win.", "Мы ожидаем, что они победят."),
            ],
        ),
        Scenario(
            title="Принуждение и разрешение (make/let)",
            description="ОБЯЗАТЕЛЬНО без частицы to.",
            examples=[
                Example(
                    "My parents let me stay out late.",
                    "Родители разрешают мне гулять допоздна.",
                ),
                Example(
                    "The boss made him rewrite the report.",
                    "Босс заставил его переписать отчет.",
                ),
            ],
        ),
        Scenario(
            title="Восприятие (see/hear)",
            description="Infinitive = видел всё от начала до конца. V-ing = видел в процессе.",
            examples=[
                Example(
                    "I saw him cross the road.",
                    "Я видел, как он перешел дорогу. (полностью)",
                ),
                Example(
                    "I saw him crossing the road.",
                    "Я видел, как он переходил дорогу. (шел в процессе)",
                ),
            ],
        ),
    ],
    markers=["want sb to", "make sb do", "let sb do"],
    exercises=[
        Exercise(
            title="Вставьте глагол",
            instruction="Используйте V, to V или V-ing.",
            items=[
                ExerciseItem("She made me ___ (cry).", "cry"),
                ExerciseItem("I want you ___ (be) careful.", "to be"),
                ExerciseItem(
                    "I heard them ___ (argue) when I walked past their room.", "arguing"
                ),
            ],
        )
    ],
)


_RELATIVE_CLAUSES = Topic(
    slug="relative-clauses",
    title="Relative Clauses",
    subtitle="Относительные придаточные",
    category="advanced",
    order=5,
    level="B2",
    essence=(
        "Предложения, которые определяют существительное (который, чей, где). "
        "Бывают Defining (обязательная информация, без запятых) и Non-defining (добавочная, выделяется запятыми)."
    ),
    formulas=[
        FormulaRow(
            subject="Люди",
            affirmative="who (который) / whose (чей) / whom (кого)",
            negative="—",
            question="—",
        ),
        FormulaRow(
            subject="Вещи / Животные",
            affirmative="which (который)",
            negative="—",
            question="—",
        ),
        FormulaRow(
            subject="That",
            affirmative="Заменяет who/which, НО только в Defining clauses (без запятых).",
            negative="—",
            question="—",
        ),
    ],
    formula_note="Если who/which/that является ДОПОЛНЕНИЕМ (отвечает на вопрос 'кого/что?'), его можно вообще пропустить: The book (that) I read was good.",
    scenarios=[
        Scenario(
            title="Defining Relative Clauses (Определительные)",
            description="Без них непонятно, о ком речь. Запятых нет.",
            examples=[
                Example(
                    "The man who lives next door is a doctor.",
                    "Мужчина, который живет по соседству — врач.",
                ),
                Example(
                    "The car (which) I bought is very fast.",
                    "Машина, которую я купил, очень быстрая.",
                ),
            ],
        ),
        Scenario(
            title="Non-defining Relative Clauses (Описательные)",
            description="Просто дополнительная инфа. Обязательны запятые. Нельзя использовать that!",
            examples=[
                Example(
                    "My brother, who lives in London, is a doctor.",
                    "Мой брат, который (кстати) живет в Лондоне, врач.",
                ),
                Example(
                    "Paris, which is the capital of France, is beautiful.",
                    "Париж, который является столицей Франции, прекрасен.",
                ),
            ],
        ),
    ],
    markers=["who", "which", "that", "whose", "whom"],
    exercises=[
        Exercise(
            title="Выберите союз",
            instruction="",
            items=[
                ExerciseItem(
                    "The woman ___ car was stolen went to the police.", "whose"
                ),
                ExerciseItem(
                    "My car, ___ is 10 years old, broke down yesterday.",
                    "which (нельзя that!)",
                ),
                ExerciseItem(
                    "The girl ___ I met yesterday is from Spain.", "who/that/ничего"
                ),
            ],
        )
    ],
)


_LINKING_WORDS = Topic(
    slug="linking-words",
    title="Linking Words (Contrast & Purpose)",
    subtitle="Придаточные уступки и цели",
    category="advanced",
    order=6,
    level="B2",
    essence=(
        "Союзы для противопоставления (хотя, несмотря на) и для выражения цели (чтобы)."
    ),
    formulas=[
        FormulaRow(
            subject="Хотя",
            affirmative="although / even though / though + подлежащее + сказуемое",
            negative="Although it was raining, we went out.",
            question="—",
        ),
        FormulaRow(
            subject="Несмотря на",
            affirmative="in spite of / despite + сущ. или V-ing",
            negative="Despite the rain, we went out.",
            question="—",
        ),
        FormulaRow(
            subject="Чтобы (Цель)",
            affirmative="to / in order to / so as to + V",
            negative="so that + подлежащее + can/could/will/would",
            question="—",
        ),
    ],
    formula_note="Нельзя говорить 'despite OF'. In spite OF — да. Despite — нет (просто despite the rain).",
    scenarios=[
        Scenario(
            title="Противопоставление (Контраст)",
            description="Разница в грамматике после союза.",
            examples=[
                Example(
                    "Although he was ill, he went to work.",
                    "Хотя он был болен, он пошел на работу.",
                ),
                Example(
                    "Despite being ill, he went to work.",
                    "Несмотря на болезнь, он пошел на работу.",
                ),
            ],
        ),
        Scenario(
            title="Цель (Для чего?)",
            description="",
            examples=[
                Example(
                    "I set the alarm to wake up early.",
                    "Я поставил будильник, чтобы проснуться рано.",
                ),
                Example(
                    "I set the alarm so that I wouldn't oversleep.",
                    "Я поставил будильник, чтобы не проспать.",
                ),
            ],
        ),
    ],
    markers=["although", "despite", "in spite of", "so that", "in order to"],
    exercises=[
        Exercise(
            title="Выберите правильный союз",
            instruction="",
            items=[
                ExerciseItem(
                    "___ having a headache, she kept working.", "Despite / In spite of"
                ),
                ExerciseItem(
                    "___ it was cold, we didn't wear jackets.", "Although / Even though"
                ),
                ExerciseItem("I wrote it down ___ I wouldn't forget.", "so that"),
            ],
        )
    ],
)


_INVERSION = Topic(
    slug="inversion",
    title="Inversion & Emphasis",
    subtitle="Инверсия и Эмфаза",
    category="advanced",
    order=7,
    level="B2",
    essence=(
        "Стилевой прием для усиления эмоций (эмфазы) и создания литературного, формального тона. "
        "Мы ставим вспомогательный глагол ПЕРЕД подлежащим, как в вопросе."
    ),
    formulas=[
        FormulaRow(
            subject="Отрицательные наречия в начале",
            affirmative="Never / Seldom / Rarely / Hardly / No sooner + Вспомогательный глагол + Subject",
            negative="Never have I seen such a mess.",
            question="—",
        ),
        FormulaRow(
            subject="Cleft Sentences (It is... that)",
            affirmative="It is/was + [то, что выделяем] + that/who",
            negative="It was John who broke the window.",
            question="—",
        ),
    ],
    formula_note="Инверсия происходит ТОЛЬКО если отрицательное слово стоит В САМОМ НАЧАЛЕ предложения.",
    scenarios=[
        Scenario(
            title="Усиление отрицания (Never, Seldom, Rarely)",
            description="Звучит очень драматично.",
            examples=[
                Example(
                    "Never have I felt so insulted!",
                    "Никогда я не чувствовал себя таким оскорбленным!",
                ),
                Example(
                    "Seldom do we see such dedication.",
                    "Редко мы видим такую преданность.",
                ),
            ],
        ),
        Scenario(
            title="Едва... как... (Hardly / No sooner)",
            description="Означает, что одно действие произошло сразу за другим.",
            examples=[
                Example(
                    "Hardly had I sat down when the phone rang.",
                    "Едва я сел, как зазвонил телефон.",
                ),
                Example(
                    "No sooner had she left than it started raining.",
                    "Не успела она уйти, как пошел дождь.",
                ),
            ],
        ),
        Scenario(
            title="Эмфаза (Cleft Sentences)",
            description="Выделяем конкретное слово в предложении.",
            examples=[
                Example(
                    "It was Mary that I saw yesterday (not Jane).",
                    "Именно Мэри я видел вчера.",
                ),
                Example(
                    "What I need is a cup of coffee.",
                    "Что мне нужно, так это чашка кофе.",
                ),
            ],
        ),
    ],
    markers=["never", "seldom", "hardly", "no sooner", "it is... that"],
    exercises=[
        Exercise(
            title="Сделайте инверсию",
            instruction="Перепишите, начав с отрицательного слова.",
            items=[
                ExerciseItem(
                    "I have never seen such a beautiful sunset. → Never...",
                    "have I seen such a beautiful sunset.",
                ),
                ExerciseItem(
                    "He had hardly arrived when she left. → Hardly...",
                    "had he arrived when she left.",
                ),
            ],
        )
    ],
)
TOPICS = [
    _PAST_PERFECT_CONTINUOUS,
    _FUTURE_PERFECT_CONTINUOUS,
    _COMPLEX_PASSIVE,
    _REPORTING_VERBS,
    _COMPLEX_OBJECT,
    _RELATIVE_CLAUSES,
    _LINKING_WORDS,
    _INVERSION,
    _MIXED_CONDITIONALS,
    _WISHES_REGRETS,
    _FUTURE_CONTINUOUS,
    _PASSIVE_VOICE,
    _ARTICLES,
    _USED_TO,
    _PRESENT_PERFECT_CONTINUOUS,
    _PRESENT_SIMPLE,
    _PRESENT_CONTINUOUS,
    _PRESENT_PERFECT,
    _PAST_SIMPLE,
    _PAST_CONTINUOUS,
    _PAST_PERFECT,
    _FUTURE_SIMPLE,
    _ZERO_CONDITIONAL,
    _FIRST_CONDITIONAL,
    _SECOND_CONDITIONAL,
    _THIRD_CONDITIONAL,
    _MODALS_MUST,
    _MODALS_DEDUCTION,
    _GERUND_INFINITIVE,
    _REPORTED_SPEECH,
    _CAUSATIVE,
]
