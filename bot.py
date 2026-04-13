import logging
import random
import os
import asyncio
from typing import Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8656288335:AAFbnpGy3STW92pwymqEviuZuxtFZ0NMQKM"

# Базовая директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(BASE_DIR, "audio")
PIC_PATH = os.path.join(BASE_DIR, "pic")

# Задержка между сообщениями (секунды)
MESSAGE_DELAY = 5

# Состояния для ConversationHandler
(
    SELECTING_REACTION,
    SELECTING_SATAN_RESPONSE,
    SELECTING_FEATURE,
    SELECTING_SUBFEATURE,
    ROLLING_DICE,
    CONFIRM_FAIL,
    KPI_DISPLAY,
    GAME_OVER,
) = range(8)

# Классы сложности (уменьшены на 1)
DC = {
    "hr_interviews": 5,
    "ai_reject": 5,
    "jira_comment": 6,
    "jira_notifications": 6,
    "code_review": 4,
    "pink_floyd": 4,
    "ganvest": 11,
    "lynch": 13,
    "neuroslop": 7,
    "temperature": 6,
    "deprivation": 8,
}

# Тексты фич для концовок
FAIL_TEXTS = {
    "code_review": "без код-ревью",
    "jira_comment": "без Жиры",
    "jira_notifications": "без Жиры",
    "hr_interviews": "без нудных собеседований",
    "ai_reject": "без ИИ-отказов",
    "pink_floyd": "под караоке-версию Пинк Флойд",
    "ganvest": "под Ганвеста",
    "lynch": "среди кинолюбителей",
    "neuroslop": "среди эскапистов",
    "temperature": "в тёплом джакузи",
    "deprivation": "среди просветлённых соседей",
}

FAIL_GROUPS = {
    "code_review": 1,
    "jira_comment": 1,
    "jira_notifications": 1,
    "hr_interviews": 1,
    "ai_reject": 1,
    "pink_floyd": 2,
    "ganvest": 2,
    "lynch": 3,
    "neuroslop": 3,
    "temperature": 4,
    "deprivation": 4,
}


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.success_count = 0
        self.fail_count = 0
        self.played_stages = []
        self.available_helpers = ["procrastinator", "exaggerator", "slacker"]
        self.current_feature = None
        self.current_subfeature = None
        self.current_dc = None
        self.rolled_value = None
        self.used_helpers_in_turn = []
        self.failed_features = []
        self.songs_played = False
        self.knew_satan = False

    def get_fail_text(self):
        if not self.failed_features:
            return ""
        sorted_fails = sorted(self.failed_features, key=lambda x: FAIL_GROUPS[x])
        parts = []
        has_cinema = False
        for fail in sorted_fails:
            text = FAIL_TEXTS[fail]
            if fail == "deprivation" and has_cinema:
                parts.append("и просветлённых соседей")
            else:
                parts.append(text)
            if fail in ["lynch", "neuroslop"]:
                has_cinema = True
        if len(parts) == 1:
            return parts[0] + "."
        else:
            return ", ".join(parts[:-1]) + ", " + parts[-1] + "."


user_states: Dict[int, GameState] = {}


def get_user_state(user_id: int) -> GameState:
    if user_id not in user_states:
        user_states[user_id] = GameState()
    return user_states[user_id]


async def send_photo_safe(chat_id, file_name, context):
    file_path = os.path.join(PIC_PATH, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)
        return True
    else:
        logger.error(f"Файл не найден: {file_path}")
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    state = get_user_state(user_id)
    state.reset()
    logger.info(f"User {user_id} started game")

    await update.message.reply_text(
        "_Сегодня твой день рождения. Алиса прислала тебе загадочный тег тг-бота вместе с поздравлением, и ты перешёл по ссылке и нажал «START»._",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "_И тут — огненная вспышка. БДЫЩЬ, как будто кто-то взорвал петарду прямо у тебя в голове. На секунду ты увидел свой скелет на просвет в оранжевых оттенках._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await send_photo_safe(update.effective_chat.id, "вспышка.png", context)
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "_Ты оглядываешься и видишь обычный офисный кабинет с панельным потолком, только вот жарко, как в бане, освещение в красных тонах, и пахнет серой._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "_Из темноты выходит демон. Рога, хвост, красная кожа, в руке лист бумаги. На бейдже написано «Валефар — тимлид проекта по модернизации IT-круга»._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "*Валефар:* О, явился. Да ты не волнуйся, сейчас всё объясню. Да, с днюхой, кстати, и добро пожаловать в Ад.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "*Валефар:* Короче, слушай: ты, конечно, грешник редкий, но нам не до твоих развлечений. У нас аврал. Слышал, скоро 2000 лет как Иисус того? Ну умер, воскрес, не важно. Короче, юбилей.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "*Валефар:* Ждём проверку из ГлавРайКонтроля, а у нас тут... сам увидишь. Технологии времен царя Гороха, а клиенты, то есть души, уже и из ваших появляются, из зумеров.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "*Валефар:* У нас тут есть специальный филиал — круг Ада для айтишников. Система пыток устарела на сотню лет. Нам нужен современный подход, так что ты будешь проходить у нас исправительные работы — управлять модернизацией, а я, Валефар, буду тимлидом.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "*Валефар:* Сделаешь — отправишься домой наживать новые грехи. Не сделаешь — останешься здесь навечно тестировщиком этих самых изменений. Будешь сидеть в котле и проверять, как работают твои же косяки. Ирония, правда?",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "*Валефар:* А, вот приказ, по которому тебя сюда направили отрабатывать.\n\n_Демон протягивает тебе лист бумаги._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await send_photo_safe(update.effective_chat.id, "prikaz.jpg", context)
    await asyncio.sleep(MESSAGE_DELAY)

    buttons = [
        [KeyboardButton("БЛЯТЬ")],
        [KeyboardButton("ПИЗДЕЦ")],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "*Валефар:* Вопросы?\n\n_Твоя реакция:_",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    return SELECTING_REACTION


async def handle_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.effective_user.id
    logger.info(f"User {user_id} selected reaction: {text}")

    if text not in ["БЛЯТЬ", "ПИЗДЕЦ"]:
        return SELECTING_REACTION

    await update.message.reply_text(
        "*Валефар:* Да-да, класс. Теперь — к главному.",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "_Тебя ведут в большой зал. «Главный» демон сидит на троне из костей. Ты замечаешь на его руке плавящиеся, стекающие по руке часы. На стене — портрет, где он позирует в обнимку с Колей Редькиным._\n\n"
        "_На стойке рядом — виниловый проигрыватель и колонки в форме овечьих черепов. Играет бодрый джазец, и в такт музыке раскрываются челюсти мертвых животных._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "_Демон встаёт и потирает ладони друг об друга в нетерпении._\n\n"
        "*Демон:* Косоруков, мой милый грешник! Выдаю тебе ТЗ: заставь айтишников в Аду страдать по-современному. Сроки горят... и ты будешь, если не поторопишься.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    buttons = [
        [KeyboardButton("КТО ТЫ")],
        [KeyboardButton("УЙТИ")],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "_Твой ответ:_",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    return SELECTING_SATAN_RESPONSE


async def handle_satan_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    state = get_user_state(user_id)
    logger.info(f"User {user_id} selected satan response: {text}")

    if text not in ["КТО ТЫ", "УЙТИ"]:
        return SELECTING_SATAN_RESPONSE

    if text == "КТО ТЫ":
        state.knew_satan = True
        await update.message.reply_text(
            "*Демон:* Чтобы ты мог произнести некоторые из моих имён, придётся вырвать тебе язык. Но если мы хотим обойтись без крови, то можешь называть меня просто Сатана.",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(MESSAGE_DELAY)
        satan_name = "*Сатана:*"
    else:
        state.knew_satan = False
        await update.message.reply_text(
            "*Демон:* Перед тем, как ты уйдешь, возьми это, чтобы работалось веселее.",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(MESSAGE_DELAY)
        satan_name = "*Демон:*"

    await update.message.reply_text(
        f"{satan_name} А это тебе чтоб работалось веселее.\n\n"
        "_В твоей руке материализуются два предмета — они будто сгорают, но в обратной перемотке. Это наушники и плеер._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await send_photo_safe(chat_id, "рука.png", context)
    await asyncio.sleep(MESSAGE_DELAY)

    if text == "КТО ТЫ":
        await update.message.reply_text(
            "*Сатана:* Всё, Валефар, приступайте.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "*Демон:* Всё, Валефар, приступайте.",
            parse_mode="Markdown"
        )
    await asyncio.sleep(MESSAGE_DELAY)

    if not state.songs_played:
        song_files = ["1.m4a", "2.m4a"]
        for i, song_file in enumerate(song_files, 1):
            file_path = os.path.join(AUDIO_PATH, song_file)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as audio:
                    await context.bot.send_audio(
                        chat_id=chat_id,
                        audio=audio,
                        title=f"Песня {i}",
                        performer="Адская звукозапись"
                    )
            else:
                await update.message.reply_text(
                    f"_Песня {i} (аудиофайл не найден)_",
                    parse_mode="Markdown"
                )
            await asyncio.sleep(MESSAGE_DELAY)
        state.songs_played = True

    await update.message.reply_text(
        "_Валефар щёлкает пальцами — и вы уже в другом помещении. Лава, каменные стены, на одной из них надпись костями: «ОТДЕЛ HR». Если после визита к их «главному» у тебя ещё были сомнения, то теперь они развеялись окончательно. Это Ад._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "_Валефар подзывает к себе трёх мелких демонов._\n\n"
        "*Валефар:* Вот твои подопечные. Ты можешь воспользоваться их помощью только один раз.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    helpers_text = (
        "*ТВОИ ПОМОЩНИКИ:*\n\n"
        "*Демон-прокрастинатор*\n"
        "Вечно всё откладывает.\n"
        "Функция: переброс дайса после неудачи.\n\n"
        "*Демон-преувеличитель*\n"
        "Если у него спросить, сколько раз он забавлялся с чьей-то мамой, он ответит «десять», хотя было-то всего разок.\n"
        "Функция: +3 к броску дайса.\n\n"
        "*Демон-раздолбай*\n"
        "Вечно делает два дела одновременно и оба через жопу. Но иногда случайно получается круто.\n"
        "Функция: бросок с преимуществом (два дайса, лучший результат)"
    )
    await update.message.reply_text(helpers_text, parse_mode="Markdown")
    await asyncio.sleep(MESSAGE_DELAY)

    await update.message.reply_text(
        "*Валефар:* Ну вот и всё, приступай. Можешь начинать с любой задачи. Я автоматически узнаю о твоих решениях и вернусь с фидбэком. По результатам внедрения каждой фичи ты будешь получать балл в свой KPI, если внедришь пять фич успешно, то выиграешь, а если провалишься хотя бы дважды... ну, ты понял.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    return await show_main_menu(update, context)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    state = get_user_state(user_id)

    if state.fail_count >= 2:
        return await game_over_fail(update, context)
    if state.success_count >= 5:
        return await game_over_win(update, context)

    all_stages = [
        ("no_offer", "НИКАКОГО ОФФЕРА"),
        ("music", "АУДИОПЫТКИ"),
        ("jira", "JIRA-ПЫТОЧНАЯ"),
        ("code_review", "РЕВЬЮ КОДА"),
        ("cinema", "КИНОПЫТКИ"),
        ("cauldrons", "НОВЫЕ КОТЛЫ"),
    ]

    filtered_buttons = []
    for stage_id, stage_name in all_stages:
        if stage_id not in state.played_stages:
            filtered_buttons.append([KeyboardButton(stage_name)])

    if not filtered_buttons:
        return await final_score(update, context)

    reply_markup = ReplyKeyboardMarkup(filtered_buttons, resize_keyboard=True, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Выбери задачу:_",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    if update.callback_query:
        await update.callback_query.answer()

    return SELECTING_FEATURE


async def handle_stage_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.effective_user.id
    state = get_user_state(user_id)
    logger.info(f"User {user_id} selected stage: {text}")

    stage_map = {
        "НИКАКОГО ОФФЕРА": "no_offer",
        "JIRA-ПЫТОЧНАЯ": "jira",
        "РЕВЬЮ КОДА": "code_review",
        "АУДИОПЫТКИ": "music",
        "КИНОПЫТКИ": "cinema",
        "НОВЫЕ КОТЛЫ": "cauldrons",
    }

    if text not in stage_map:
        return SELECTING_FEATURE

    stage = stage_map[text]
    state.current_feature = stage
    state.used_helpers_in_turn = []

    stage_titles = {
        "no_offer": "НИКАКОГО ОФФЕРА",
        "jira": "JIRA-ПЫТОЧНАЯ",
        "code_review": "РЕВЬЮ КОДА",
        "music": "АУДИОПЫТКИ",
        "cinema": "КИНОПЫТКИ",
        "cauldrons": "НОВЫЕ КОТЛЫ",
    }

    stage_descriptions = {
        "no_offer": "_Задача: сделать так, чтобы разработчики не получили оффер даже в Аду._",
        "jira": "_Задача: Превратить Jira в инструмент морального уничтожения. Ну, в смысле, больше._",
        "code_review": "_Задача: Заставить демонов делать невыносимое ревью._",
        "music": "_Задача: Заставить грешников мечтать оглохнуть._",
        "cinema": "_Задача: Превратить визуальный контент в мучение._",
        "cauldrons": "_Задача: Модернизировать старые котлы._",
    }

    await update.message.reply_text(
        f"*{stage_titles[stage]}*\n\n"
        f"{stage_descriptions[stage]}",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(MESSAGE_DELAY)

    if stage == "code_review":
        state.current_subfeature = "code_review"
        state.current_dc = DC["code_review"]
        # Одно сообщение: название, задача и класс сложности
        await update.message.reply_text(
            f"*{stage_titles[stage]}*\n\n"
            f"{stage_descriptions[stage]}\n\n"
            f"_Класс сложности: {state.current_dc}_",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        return await show_roll_options(update, context, state)

    sub_keyboard = []
    if stage == "no_offer":
        sub_keyboard = [
            [InlineKeyboardButton("БЕСКОНЕЧНЫЕ СОБЕСЫ", callback_data="sub_hr_interviews")],
            [InlineKeyboardButton("ИИ-ОТКАЗЫ ПО РЕЗЮМЕ", callback_data="sub_ai_reject")],
        ]
    elif stage == "jira":
        sub_keyboard = [
            [InlineKeyboardButton("ДАВАЙ ПЕРЕДЕЛАЕМ", callback_data="sub_jira_comment")],
            [InlineKeyboardButton("БЕСКОНЕЧНЫЕ УВЕДОМЛЕНИЯ", callback_data="sub_jira_notifications")],
        ]
    elif stage == "music":
        sub_keyboard = [
            [InlineKeyboardButton("ПИНК ФЛОЙД — ТОЛЬКО ХУЙНЯ", callback_data="sub_pink_floyd")],
            [InlineKeyboardButton("ГАНВЕСТ", callback_data="sub_ganvest")],
        ]
    elif stage == "cinema":
        sub_keyboard = [
            [InlineKeyboardButton("ТАРКОВСКИЙ И ЛИНЧ", callback_data="sub_lynch")],
            [InlineKeyboardButton("НЕЙРОСЛОП", callback_data="sub_neuroslop")],
        ]
    elif stage == "cauldrons":
        sub_keyboard = [
            [InlineKeyboardButton("КОНТРАСТНАЯ ТЕМПЕРАТУРА", callback_data="sub_temperature")],
            [InlineKeyboardButton("СЕНСОРНАЯ ДЕПРЕВАЦИЯ", callback_data="sub_deprivation")],
        ]

    if sub_keyboard:
        reply_markup = InlineKeyboardMarkup(sub_keyboard)
        await update.message.reply_text(
            "_Выбери вариант:_",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return SELECTING_SUBFEATURE

    return SELECTING_FEATURE


async def handle_subfeature_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    state = get_user_state(user_id)

    state.current_subfeature = query.data.replace("sub_", "")
    logger.info(f"User {user_id} selected subfeature: {state.current_subfeature}")

    dc_map = {
        "hr_interviews": DC["hr_interviews"],
        "ai_reject": DC["ai_reject"],
        "jira_comment": DC["jira_comment"],
        "jira_notifications": DC["jira_notifications"],
        "pink_floyd": DC["pink_floyd"],
        "ganvest": DC["ganvest"],
        "lynch": DC["lynch"],
        "neuroslop": DC["neuroslop"],
        "temperature": DC["temperature"],
        "deprivation": DC["deprivation"],
    }

    sub_titles = {
        "hr_interviews": "БЕСКОНЕЧНЫЕ СОБЕСЫ",
        "ai_reject": "ИИ-ОТКАЗЫ ПО РЕЗЮМЕ",
        "jira_comment": "ДАВАЙ ПЕРЕДЕЛАЕМ",
        "jira_notifications": "БЕСКОНЕЧНЫЕ УВЕДОМЛЕНИЯ",
        "pink_floyd": "ПИНК ФЛОЙД — ТОЛЬКО ХУЙНЯ",
        "ganvest": "ГАНВЕСТ",
        "lynch": "ТАРКОВСКИЙ И ЛИНЧ",
        "neuroslop": "НЕЙРОСЛОП",
        "temperature": "КОНТРАСТНАЯ ТЕМПЕРАТУРА",
        "deprivation": "СЕНСОРНАЯ ДЕПРЕВАЦИЯ",
    }

    description_map = {
        "hr_interviews": "_Бесконечные этапы собеседований._",
        "ai_reject": "_Система на базе адского ИИ присылает всем автоотказы._",
        "jira_comment": "_Задача: добавить комментарии к тикетам вроде «давай переделаем» и «а если попробовать по-другому?»_",
        "jira_notifications": "_Система тегает всех в комментариях к тикетам._",
        "pink_floyd": "_Задача: включить грешникам ремикс из хуйни Флойдов._",
        "ganvest": "_«Фа пэпэ шнейне ватафа» Ганвеста на репите. Бесконечный цикл одной фразы._",
        "lynch": "_Тарковский, Триер, Линч, Бергман. Бесконечный марафон интеллектуального кино. Без объяснений._",
        "neuroslop": "_Бесконечный поток сгенерированного контента: китайские тикток-дорамы с котами, нейрофото с иконами, которые выгрызли бобры, карточки товаров для маркетплейсов._",
        "temperature": "_Переменная температура: то кипяток, то лёд._",
        "deprivation": "_Котёл с сенсорной депривацией: полная тишина, темнота, невесомость. Грешник один на один с собой. Навечно._",
    }

    state.current_dc = dc_map.get(state.current_subfeature, 10)

    await query.edit_message_text(
        f"*{sub_titles[state.current_subfeature]}*\n\n"
        f"{description_map.get(state.current_subfeature, '')}\n\n"
        f"_Класс сложности: {state.current_dc}_",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    return await show_roll_options(update, context, state)


async def show_roll_options(update: Update, context: ContextTypes.DEFAULT_TYPE, state: GameState) -> int:
    keyboard = []

    if state.available_helpers:
        if "exaggerator" in state.available_helpers:
            keyboard.append([InlineKeyboardButton("+3 К БРОСКУ", callback_data="help_exaggerator")])
        if "slacker" in state.available_helpers:
            keyboard.append([InlineKeyboardButton("БРОСОК С ПРЕИМУЩЕСТВОМ", callback_data="help_slacker")])

    keyboard.append([InlineKeyboardButton("БРОСИТЬ КУБИК D20", callback_data="roll_dice")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Выбери действие:_",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    return ROLLING_DICE


async def handle_help_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    state = get_user_state(user_id)

    helper = query.data.replace("help_", "")
    if helper == "exaggerator":
        state.used_helpers_in_turn.append("exaggerator")
        state.available_helpers.remove("exaggerator")
        await query.edit_message_text("_Ты призвал демона-преувеличителя._", parse_mode="Markdown")
    elif helper == "slacker":
        state.used_helpers_in_turn.append("slacker")
        state.available_helpers.remove("slacker")
        await query.edit_message_text("_Ты призвал демона-раздолбая._", parse_mode="Markdown")

    await asyncio.sleep(MESSAGE_DELAY)
    return await show_roll_options(update, context, state)


async def handle_roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    state = get_user_state(user_id)

    bonus = 0
    if "exaggerator" in state.used_helpers_in_turn:
        bonus = 3

    roll_type = "normal"
    if "slacker" in state.used_helpers_in_turn:
        roll_type = "advantage"

    if roll_type == "advantage":
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        roll = max(roll1, roll2)
        roll_text = f"Выпало: {roll1} и {roll2} (лучший: {roll})"
    else:
        roll = random.randint(1, 20)
        roll_text = f"Выпало: {roll}"

    is_success = (roll + bonus) >= state.current_dc

    result_text = f"{roll_text}"
    if bonus > 0:
        result_text += f"\nС бонусом +{bonus}: {roll + bonus}"
    result_text += f"\n\nНужно было: {state.current_dc}"
    result_text += f"\n\n{'✅ УСПЕХ' if is_success else '❌ ПРОВАЛ'}"

    await query.edit_message_text(result_text)

    if is_success:
        state.success_count += 1
        state.played_stages.append(state.current_feature)
        await show_success_feedback(update, context, state)
        return KPI_DISPLAY
    else:
        if "procrastinator" in state.available_helpers:
            keyboard = [
                [InlineKeyboardButton("ПЕРЕБРОСИТЬ КУБИК", callback_data="reroll")],
                [InlineKeyboardButton("ДАЛЬШЕ (ПРОВАЛ)", callback_data="accept_fail")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="_У тебя есть демон-прокрастинатор. Призвать?_",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            return CONFIRM_FAIL
        else:
            state.fail_count += 1
            state.failed_features.append(state.current_subfeature)
            state.played_stages.append(state.current_feature)
            await show_fail_feedback(update, context, state)
            await show_kpi(update, context, state)
            return KPI_DISPLAY


async def handle_reroll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    state = get_user_state(user_id)

    state.available_helpers.remove("procrastinator")

    roll = random.randint(1, 20)
    bonus = 3 if "exaggerator" in state.used_helpers_in_turn else 0
    is_success = (roll + bonus) >= state.current_dc

    result_text = f"Переброс: {roll}"
    if bonus > 0:
        result_text += f"\nС бонусом +{bonus}: {roll + bonus}"
    result_text += f"\n\nНужно было: {state.current_dc}"
    result_text += f"\n\n{'✅ УСПЕХ' if is_success else '❌ ПРОВАЛ'}"

    await query.edit_message_text(result_text)

    if is_success:
        state.success_count += 1
        state.played_stages.append(state.current_feature)
        await show_success_feedback(update, context, state)
    else:
        state.fail_count += 1
        state.failed_features.append(state.current_subfeature)
        state.played_stages.append(state.current_feature)
        await show_fail_feedback(update, context, state)
        await show_kpi(update, context, state)

    return KPI_DISPLAY


async def accept_fail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    state = get_user_state(user_id)

    state.fail_count += 1
    state.failed_features.append(state.current_subfeature)
    state.played_stages.append(state.current_feature)

    await show_fail_feedback(update, context, state)
    await show_kpi(update, context, state)
    return KPI_DISPLAY


async def show_success_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE, state: GameState) -> None:
    feedback_map = {
        "hr_interviews": "*Валефар:* Ну что, собеседования запустили — скрининг, тестовое, пять этапов собеседований с одинаковыми вопросами, отказ, снова скрининг. Грешники сидят в цикле уже по десятому кругу. Сеньоры в сотый раз рассказывают про свои достижения, некоторые уже начинают плакать прямо на скрининге, а один девопс вообще словил галлюцинацию, что он — Иона в животе у кита, когда в очередной раз рассказывал, что такое докер. Молодец, Собака.",
        "ai_reject": "*Валефар:* Зачёт. ИИ работает как часы. Грешники откликаются и автоматически получают отказ. Откликаются снова — снова отказ. Один парень успел за день 150 раз откликнуться, получил 150 отказов и теперь сидит и просто смотрит в стену. Грешники ловят вьетнамские флешбеки по жизни и бесятся от несправедливости рынка — уровень страданий возрос.",
        "jira_comment": "*Валефар:* Ну что, Никита, Жира теперь просто бомба. Грешники открывают тикет, а там комментарий «давай переделаем». Они переделывают — новый комментарий «а если по-другому?». Они делают по-другому — «верни как было».",
        "jira_notifications": "*Валефар:* Вот это вещь. Система тегает всех во всех комментариях. Уведомления приходят даже тогда, когда ничего не происходит, и их невозможно отключить. Грешники тонут в уведомлениях.",
        "code_review": "*Валефар:* Я сначала сомневался, но демоны реально втянулись. Наши работники освоили корпоративный диалект, и теперь на любой код они пишут: «Это же элементарно, тут на 15 минут работы», «Просто сделай, как я сказал», «Я погуглил, там по-другому пишут», «Я знаю, уже вечер пятницы, но надо переделать сегодня». Разработчики плачут кровью.",
        "pink_floyd": "*Валефар:* Косоруков, это жестоко даже по меркам ада. Мы включили им какую-то внатуре адскую смесь из всей хуйни Дарксайда — дробящий черепа звон часов, бесконечный луп звуков кассового аппарата, безумный смех. Они в ужасе.",
        "ganvest": "*Валефар:* Это успех. Я сам не могу выкинуть это из головы. Один парень пытался молиться, но вместо «Отче наш» повторял «Пэпэ шнейне ватафа», протыкая себе барабанные перепонки.",
        "lynch": "*Валефар:* Грешники пытаются понять сюжет, строят теории, сходят с ума от непонимания и терпят невозможно длинные паузы.",
        "neuroslop": "*Валефар:* Никита, это жесть. Грешники в ужасе от эстетической ущербности. Глаза кровоточат, мозг плавится.",
        "temperature": "*Валефар:* Твоя идея о контрастных страданиях зашла. Грешники в хроническом стрессе от неопределённости.",
        "deprivation": "*Валефар:* Это реально жестоко. Грешники сходят с ума от одиночества и экзистенциального ужаса.",
    }
    text = feedback_map.get(state.current_subfeature, "Успех!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode="Markdown")
    await asyncio.sleep(MESSAGE_DELAY)
    await show_kpi(update, context, state)


async def show_fail_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE, state: GameState) -> None:
    feedback_map = {
        "hr_interviews": "*Валефар:* Твои собеседования... Короче, HR-демоны вошли во вкус и начали собеседовать демонов из соседних отделов вместо грешников.",
        "ai_reject": "*Валефар:* Твой ИИ, он... Короче, он настолько умный, что начал отказывать демонам, которые пытаются его настраивать.",
        "jira_comment": "*Валефар:* В общем, Jira рухнула под нагрузкой. Это провал.",
        "jira_notifications": "*Валефар:* Система тегает всех во всех комментариях. Уведомления приходят даже тогда, когда ничего не происходит, и их невозможно отключить. Сатана орёт, что его тоже тэгают. Он сказал, что если это не прекратится, он лично проверит, как работают котлы. На тебе.",
        "code_review": "*Валефар:* Демонам лень. Они ставят везде эмодзи 🔥 и уходят пить лаву. Разработчики счастливы.",
        "pink_floyd": "*Валефар:* Я сначала подумал, что грешники орут из-за страданий от нашей новой фичи, но оказалось, что они устроили артхаусное караоке. Они считают адскую смесь из всей хуйни Дарксайда новым, гениальным жанром.",
        "ganvest": "*Валефар:* Твой Ганвест... Он стал новым Святым. Грешники впали в транс и перестали реагировать на другие пытки. Они просто покачиваются и бормочут «ватафа... ватафа...». Им хорошо.",
        "lynch": "*Валефар:* Они... вошли во вкус. Стали нишевыми, открыли киноклуб. Грешники записывают подкасты и ведут лекции, обсуждают символизм и смотрят на чертей с надменностью: «Вы просто не понимаете, Тарковский гений». Скажи спасибо, что мы не вычитаем баллы из твоего KPI.",
        "neuroslop": "*Валефар:* Грешники сломали глазные распорки и убежали от слопа в мир фантазий.",
        "temperature": "*Валефар:* Система сломалась и залипла на «приятно тепло». Ты сделал им джакузи, они раскайфовываются!",
        "deprivation": "*Валефар:* Грешники ловят дзен. В тишине и темноте они познают себя, преисполняются, становятся просветлённым. Теперь они не страдают, а медитируют и учат других. У нас тут уже группа любителей Пелевина по средам собирается. Сатана в ярости от их лекции «страдание — это иллюзия». Короче, ты открыл буддийский храм в Аду.",
    }
    text = feedback_map.get(state.current_subfeature, "Провал...")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode="Markdown")
    await asyncio.sleep(MESSAGE_DELAY)


async def show_kpi(update: Update, context: ContextTypes.DEFAULT_TYPE, state: GameState) -> None:
    kpi_text = f"📊 Твой KPI: {state.success_count}/5 успехов, провалов: {state.fail_count}/2"
    keyboard = [[InlineKeyboardButton("ДАЛЬШЕ", callback_data="after_kpi")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=kpi_text,
        reply_markup=reply_markup
    )


async def after_kpi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    state = get_user_state(user_id)

    if state.fail_count >= 2:
        return await game_over_fail(update, context)
    if state.success_count >= 5:
        return await game_over_win(update, context)
    return await show_main_menu(update, context)


async def game_over_fail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    state = get_user_state(user_id)
    fail_text = state.get_fail_text()
    logger.info(f"User {user_id} game over (fail)")

    if update.callback_query:
        await update.callback_query.message.reply_text(
            "_Валефар обжигающе сжимает твоё плечо._",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            "_Валефар обжигающе сжимает твоё плечо._",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
    await asyncio.sleep(MESSAGE_DELAY)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Валефар:* Ну что, Косоруков, два провала. Пошли к Сатане.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Ты в главном зале. Сатана встаёт с трона._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Сатана:* Никита... Ты серьёзно? Я создал для тебя все условия, а результат... Ты сделал этот ад терпимым, избавил грешников от страданий.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Сатана:* Ты остаёшься.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Сатана щелчком пальцев отправляет тебя на круг ада для айтишников, выпуская искры из-под подушечек._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"_Ты проиграл. Но ад, который ты создал, оказался вполне комфортным. Теперь ты будешь вечно тусоваться здесь, {fail_text}_",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_С днём рождения. Увидимся в Аду!_",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    bad_end_path = os.path.join(AUDIO_PATH, "BAD END.m4a")
    if os.path.exists(bad_end_path):
        with open(bad_end_path, 'rb') as audio:
            await context.bot.send_audio(
                chat_id=update.effective_chat.id,
                audio=audio,
                title="BAD END",
                performer="Адская звукозапись"
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_BAD END (аудиофайл не найден)_",
            parse_mode="Markdown"
        )
    await asyncio.sleep(MESSAGE_DELAY)

    # Вместо кнопки "НОВАЯ ИГРА" отправляем текст
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Чтобы начать игру заново, используй команду /start._",
        parse_mode="Markdown"
    )

    return GAME_OVER


async def game_over_win(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    logger.info(f"User {user_id} game over (win)")

    if update.callback_query:
        await update.callback_query.message.reply_text(
            "_Валефар обжигающе хлопает тебя по плечу._",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            "_Валефар обжигающе хлопает тебя по плечу._",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
    await asyncio.sleep(MESSAGE_DELAY)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Валефар:* Красава, Собака. Ты сделал это. Пошли к Сатане.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Ты в главном зале. Сатана встаёт с трона._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Сатана:* Косоруков. Я в восторге от твоей работы. Ты свободен. Можешь отправляться домой и наживать новые грехи.",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Сатана:* Но...",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Сатана хитро щурится._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Сатана:* У меня есть предложение. Оставайся. Мы предложим тебе лучшие условия, чем на твоей новой работе — вот и будешь главным по IT-кругу. Свой котёл-джакузи, подчинённые — суккубы, концерты всех твоих любимых музыкантов и встречи с известными политиками. Ну, из числа тех, кто уже мёртв, само собой. Что скажешь?",
        parse_mode="Markdown"
    )
    await asyncio.sleep(MESSAGE_DELAY)

    keyboard = [
        [InlineKeyboardButton("ВЕРНУТЬСЯ ДОМОЙ", callback_data="win_leave")],
        [InlineKeyboardButton("СОГЛАСИТЬСЯ", callback_data="win_stay")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Твой выбор:_",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

    return GAME_OVER


async def handle_win_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    logger.info(f"User {user_id} made win choice: {query.data}")

    if query.data == "win_stay":
        await query.edit_message_text(
            "*Сатана:* Добро пожаловать в команду.",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_Теперь ты — Главный по IT-Аду. У тебя свой кабинет с видом на котлы тех, кто не оставлял комментариев в коде. На стене висит льняное кимоно, в углу стоит пульт — по пятницам ты устраиваешь сеты для демонов в котельной, вот это реальная Boiler room. Говорят, у тебя самая большая коллекция винила во Вселенной._",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_С днём рождения, босс._",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)

        hell_end_path = os.path.join(AUDIO_PATH, "HELL END.mp3")
        if os.path.exists(hell_end_path):
            with open(hell_end_path, 'rb') as audio:
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=audio,
                    title="HELL END",
                    performer="Адская звукозапись"
                )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="_HELL END (аудиофайл не найден)_",
                parse_mode="Markdown"
            )
        await asyncio.sleep(MESSAGE_DELAY)

    else:
        await query.edit_message_text(
            "*Сатана вздыхает и щёлкает пальцами, выпуская искры из-под подушечек. Ты чувствуешь странное покалывание.*",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Сатана:* Это удача. От нас, адских, подарок. Будешь общаться с людьми — любой скрывающийся демон почувствует в тебе родную душу... Ну, или риэлтор. Не демон-риэлтор, просто риэлтор.",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Сатана:* А, да, ещё: загляни к брату, тебя там ждёт ещё кое-какая плюшка.",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Сатана:* Ну, бывай.",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_Ты снова видишь огненную вспышку и мгновенно приходишь в себя с телефоном в руках. Воспоминания о твоем приключении в Аду искажаются, и с каждым мгновением у тебя уменьшается уверенность в том, что всё это было на самом деле._",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_Вскоре ты уже совершенно уверен, что это всё было просто игрой, однако ощущение приобретённой удачливости остаётся где-то внутри. Может зайти к Малому?_",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_С днём рождения, Адский Пёс._",
            parse_mode="Markdown"
        )
        await asyncio.sleep(MESSAGE_DELAY)

        true_end_path = os.path.join(AUDIO_PATH, "TRUE END.mp3")
        if os.path.exists(true_end_path):
            with open(true_end_path, 'rb') as audio:
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=audio,
                    title="TRUE END",
                    performer="Адская звукозапись"
                )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="_TRUE END (аудиофайл не найден)_",
                parse_mode="Markdown"
            )
        await asyncio.sleep(MESSAGE_DELAY)

    # Вместо кнопки "НОВАЯ ИГРА" отправляем текст
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="_Чтобы начать игру заново, используй команду /start._",
        parse_mode="Markdown"
    )

    return GAME_OVER


async def final_score(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    state = get_user_state(user_id)
    if state.success_count >= 5:
        return await game_over_win(update, context)
    if state.fail_count >= 2:
        return await game_over_fail(update, context)
    return await game_over_fail(update, context)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок — перехватывает TimedOut и не даёт боту упасть"""
    from telegram.error import TimedOut, NetworkError, RetryAfter
    
    error = context.error
    
    if isinstance(error, (TimedOut, NetworkError)):
        logger.warning(f"Сетевая ошибка (бот продолжает работу): {error}")
        await asyncio.sleep(5)
        return
    
    elif isinstance(error, RetryAfter):
        logger.warning(f"Flood control, ждём {error.retry_after} секунд")
        await asyncio.sleep(error.retry_after)
        return
    
    else:
        logger.error(f"Необработанная ошибка: {error}", exc_info=True)


def main() -> None:
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .pool_timeout(30.0)
        .build()
    )
    
    application.add_error_handler(error_handler)
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_REACTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reaction),
            ],
            SELECTING_SATAN_RESPONSE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_satan_response),
            ],
            SELECTING_FEATURE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_stage_selection),
            ],
            SELECTING_SUBFEATURE: [
                CallbackQueryHandler(handle_subfeature_selection, pattern="^sub_"),
            ],
            ROLLING_DICE: [
                CallbackQueryHandler(handle_help_selection, pattern="^help_"),
                CallbackQueryHandler(handle_roll, pattern="^roll_dice$"),
            ],
            CONFIRM_FAIL: [
                CallbackQueryHandler(handle_reroll, pattern="^reroll$"),
                CallbackQueryHandler(accept_fail, pattern="^accept_fail$"),
            ],
            KPI_DISPLAY: [
                CallbackQueryHandler(after_kpi, pattern="^after_kpi$"),
            ],
            GAME_OVER: [
                CallbackQueryHandler(handle_win_choice, pattern="^(win_stay|win_leave)$"),
                CommandHandler("start", start),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    application.add_handler(conv_handler)
    
    application.run_polling(
        poll_interval=1.0,
        timeout=30,
        bootstrap_retries=-1,
        read_timeout=30,
        write_timeout=30,
        connect_timeout=30,
        pool_timeout=30,
        drop_pending_updates=False
    )


if __name__ == "__main__":
    main()