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


# Стандартный ответ на сообщение
def get_keyboard(answer):
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


# Обработчик приветствия
@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: message.text.lower() == 'привет')
def send_welcome(message):
    answer = ANSWERS['Меню']
    for text in answer['texts']:
        bot.reply_to(message, text=text, reply_markup=get_keyboard(answer=ANSWERS['Меню']))


# Обработчик команды Назад
@bot.message_handler(func=lambda message: message.text.lower() == 'назад')
def handle_back(message):
    answer = ANSWERS[message.text]
    for text in answer['texts']:
        bot.reply_to(message, text=text, reply_markup=get_keyboard(answer=ANSWERS[message.text]))


# Обработчик остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_main_menu(message):
    if message.text == "test":
        with open('pictures/test.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    if message.text in ANSWERS.keys():
        answer = ANSWERS[message.text]
        message_type = answer['type']
        if message_type == 'keyboard':
            bot.reply_to(
                message,
                "Выберите пункт меню:",
                reply_markup=get_keyboard(answer=answer)
            )
        elif message_type == 'texts':
            for text in answer["texts"]:
                bot.send_message(message.chat.id, text, parse_mode='Markdown')
        elif message_type == "picture":
            try:
                name = ANSWERS[f"{message.text}"]["name"]
                with open(f'pictures/{name}.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo)
            except FileNotFoundError:
                bot.reply_to(message, "Этой шпаргалки пока нет")
            except KeyError:
                print('KeyError', message.text)
    else:
        bot.reply_to(message, "Я вас не понимаю. Используйте кнопки на клавиатуре")


# Запуск бота
bot.infinity_polling(timeout=10, long_polling_timeout=5)
