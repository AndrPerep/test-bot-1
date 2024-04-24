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
def get_keyboard(message, answer):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if answer["type"] != "main":
        keyboard.add("Назад")
    for button in answer["buttons"]:
        keyboard.add(button)
    return keyboard


# Отправка шпаргалок
def send_picture(message):
    try:
        with open(f'pictures/{message.text}.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.reply_to(message, "Этой шпаргалки пока нет")


# Обработчик команды /start или текста "Привет"
@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: message.text.lower() == 'привет')
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот. Чем могу помочь?", reply_markup=get_keyboard(message, answer=ANSWERS[message.text]))


# Обработчик команды Назад
@bot.message_handler(func=lambda message: message.text.lower() == 'назад')
def handle_back(message):
    bot.reply_to(message, "Вы вернулись в главное меню.", reply_markup=get_keyboard(message, answer=ANSWERS[message.text]))

# Обработчик нажатия на кнопки главного меню
@bot.message_handler(func=lambda message: True)
def handle_main_menu(message):
    if message.text in ANSWERS.keys():
        answer = ANSWERS[message.text]
        message_type = answer['type']
        if message_type == 'keyboard':
            bot.reply_to(
                message,
                "Выберите пункт меню:",
                reply_markup=get_keyboard(message, answer=answer)
            )
        elif message_type == 'texts':
            for text in answer["texts"]:
                bot.send_message(message.chat.id, text, parse_mode='Markdown')
    elif "📝" in message.text:
        send_picture(message)
    else:
        bot.reply_to(message, "Я вас не понимаю. Используйте кнопки на клавиатуре")

# Запуск бота
bot.polling()
