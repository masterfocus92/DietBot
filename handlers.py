from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
import logging


logger = logging.getLogger(__name__)

GENDER, AGE, WEIGHT, HEIGHT = range(4)

class UserParams:
    def set_gender(self, user_answer: str):
        if user_answer == "Мальчик": setattr(self, 'is_male', True)
        else: setattr(self, 'is_male', False)

    def set_age(self, str_age: str):
        age = int(str_age)
        setattr(self, 'age', age)

    def set_height(self, str_height: str):
        height = int(str_height)
        setattr(self, 'height', height)

    def set_weight(self, str_weight: str):
        weight = int(str_weight)
        setattr(self, 'weight', weight)


user_params = UserParams()

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот помогающий тебе освоить разумное питание!\n\nЯ еще очень маленький, и умею только считать нужную тебе для выживания калорийность питания. Введи команду /bmr чтобы я посчитал твой базовый уровень метаболизма.")

def base_metabolic_rate(is_male, age: int, height: int, weight: int):
    if is_male:
        r = 66.5 + (13.7 * weight) + (5 * height) - (6.8 * age)
        return int(r)
    else:
        r = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
        return int(r)

def bmr(update: Update, context: CallbackContext):
    reply_keyboard = [['Мальчик', 'Девочка']]
    update.message.reply_text(
        'Давай посчитаем сколько калорий требует твой базовый уровень метаболизма '
        'Отправь /cancel чтобы прекратить разговор.\n\n'
        'Ты мальчик или девочка?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='мальчик или девочка?'
        ),
    )

    return GENDER

def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    user_params.set_gender(update.message.text)
    update.message.reply_text(
        'Сколько тебе полных лет?',
        reply_markup=ReplyKeyboardRemove(),
    )

    return AGE


def age(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_params.set_age(update.message.text)
    update.message.reply_text(
        'Сколько ты весишь в килограмммах?',
    )

    return WEIGHT


def weight(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_params.set_weight(update.message.text)
    update.message.reply_text(
        'Сколько твой рост в сантиметрах?',
    )

    return HEIGHT


def height(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_params.set_height(update.message.text)

    user_bmr = base_metabolic_rate(user_params.is_male, user_params.age, user_params.height, user_params.weight)
    reply = "Твой расчетный базовый уровень метаболизма равен:\n\n", user_bmr
    update.message.reply_text(
        f"Твой расчетный базовый уровень метаболизма равен:\n\n {user_bmr}"
    )

    return ConversationHandler.END



def cancel(update: Update, context: CallbackContext) -> int:    
    """Cancels and ends the conversation."""
    user = update.message.from_user
    update.message.reply_text(
        'Надеюсь мы продолжим позже! Хорошего дня:)', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END 
