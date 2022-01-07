from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
import logging


logger = logging.getLogger(__name__)
START_MESSAGE = ("Привет! Я бот помогающий тебе освоить разумное питание!\n\n"
                "Я еще очень маленький, и умею только считать нужную тебе для" 
                "выживания калорийность питания. " 
                "Введи команду /bmr чтобы я посчитал твой базовый "
                "уровень метаболизма.")

BMR_MESSAGE =("Давай посчитаем сколько калорий требует " 
            "твой базовый уровень метаболизма. \n"
            "Отправь /cancel чтобы прекратить разговор.\n\n"
            "Ты мальчик или девочка?")

GENDER, AGE, WEIGHT, HEIGHT = range(4)

class User:
    def set_gender(self, user_answer: str):
        if user_answer == "Мальчик": setattr(self, "is_male", True)
        else: setattr(self, "is_male", False)

    def set_age(self, user_answer: str):
        age = int(user_answer)
        setattr(self, "age", age)

    def set_height(self, user_answer: str):
        height = int(user_answer)
        setattr(self, "height", height)

    def set_weight(self, user_answer: str):
        weight = int(user_answer)
        setattr(self, "weight", weight)


user_params = User()

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
            text=START_MESSAGE) 

def calculate_female_bmr(user: User) -> int:
    rate = 655 + (9.6*user.weight) + (1.8*user.height) - (4.7*user.age)
    return int(rate)

def calculate_male_bmr(user: User) -> int:
    rate = 66.5 + (13.7*user.weight) + (5*user.height) - (6.8*user.age)
    return int(rate)

def base_metabolic_rate(user: User) -> int:
    if user.is_male:
        return calculate_male_bmr(user)
    else:
        return calculate_female_bmr(user)

def bmr(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [["Мальчик", "Девочка"]]
    update.message.reply_text(BMR_MESSAGE,        
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, 
            one_time_keyboard=True, 
            input_field_placeholder = "мальчик или девочка?"
        ),
    )
    return GENDER

def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    user_params.set_gender(update.message.text)
    update.message.reply_text(
        "Сколько тебе полных лет?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return AGE


def age(update: Update, context: CallbackContext) -> int:
    user_params.set_age(update.message.text)
    update.message.reply_text(
        "Сколько ты весишь в килограмммах?",
    )
    return WEIGHT


def weight(update: Update, context: CallbackContext) -> int:
    user_params.set_weight(update.message.text)
    update.message.reply_text(
        "Сколько твой рост в сантиметрах?",
    )

    return HEIGHT


def height(update: Update, context: CallbackContext) -> int:
    user_params.set_height(update.message.text)

    user_bmr = base_metabolic_rate(user_params)

    update.message.reply_text(
        f"Твой расчетный базовый уровень метаболизма равен:\n\n {user_bmr}"
    )

    return ConversationHandler.END



def cancel(update: Update, context: CallbackContext) -> int:    
    """Cancels and ends the conversation."""
    update.message.reply_text(
        "Надеюсь мы продолжим позже! Хорошего дня:)",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END 
