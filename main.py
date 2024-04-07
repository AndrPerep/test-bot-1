from dotenv import load_dotenv
from json import load
from os import getenv
from telebot import types, TeleBot

# Загрузка переменных окружения из файла .env
load_dotenv()

# Создание объекта бота
bot = TeleBot(getenv('TOKEN'))

# Загрузка сообщений из json файла
with open("messages.json", "r", encoding="utf-8") as file:
    ANSWERS = load(file)


# Ответ на сообщение
def get_keyboard(message, menu):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if menu["type"] != "Назад":
        keyboard.add("Назад")
    for button in menu["buttons"]:
        keyboard.add(button)
    return keyboard


# Обработчик команды /start или текста "Привет"
@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: message.text.lower() == 'привет')
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот. Чем могу помочь?", reply_markup=get_keyboard(message, menu=ANSWERS[message.text]))


# Обработчик команды Назад
@bot.message_handler(func=lambda message: message.text.lower() == 'назад')
def handle_back(message):
    bot.reply_to(message, "Вы вернулись в главное меню.", reply_markup=get_keyboard(message, menu=ANSWERS[message.text]))

# Обработчик нажатия на кнопки главного меню
@bot.message_handler(func=lambda message: True)
def handle_main_menu(message):
    if message.text in ANSWERS.keys():
        answer = ANSWERS[message.text]
        if answer.get('buttons'):
            bot.reply_to(
                message,
                "Выберите пункт меню:",
                reply_markup=get_keyboard(message, menu=ANSWERS[message.text])
            )
        else:
            bot.reply_to(message, answer["text"])
    else:
        bot.reply_to(message, "Я вас не понимаю. Используйте кнопки на клавиатуре")

# Запуск бота
bot.polling()
