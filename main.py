import telebot  # імпорт бібліотки для роботи з телеграм ботами
from config import bot_token  # імпорт токена телеграм бота
from response import Response

# ініціалізація класу для відповіді
city = Response()  # створення нового об'єкту класу Response()

# ініціалізація функції для пошуку користувача в файлі
def find_user(id, name):
    f = open('users_info.txt', 'r+')  # відкриття файлу для оновлення
    found = False  # ініціалізація змінної і надання значення
    for lines in f:  # для кожного рядка в файлі
        strings = lines.split('/')  # розділит рядок на частини при зустрічі /
        if strings[0] == str(id):  # якщо перша частина дорівнює id типу string
            found = True  # змінити значення змінної
            # повернути повідомлення про останній візит користувача
            return f"{name}🦖, last time you were on {strings[2]} and asked for a ☔️weather☀️ in <b>{strings[1]}</b>🌉"
    if not found:  # якщо змінна так і залишилась зі значенням False
        return f"{name}🦭 , this is your first visit👣🌥️"  # повернути повідомлення про перший візит


# передання токена телеграм бота в функцію
bot = telebot.TeleBot(bot_token)


# ініціалізація команди старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Weather report for which city would you like to know?')  # вивід повідомлення в чат


# ініціалізація команди допомоги
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Input the name of the city and I will show you weather report')  # вивід повідомлення в чат


# ініціалізація команди перегляду візитів
@bot.message_handler(commands=['visit'])
def visit(message):
    bot.send_message(message.chat.id, find_user(message.from_user.id, message.from_user.first_name), parse_mode='html')  # вивід повідомлення в чат


# ініціалізація функції для обробки текстових повідомлень
@bot.message_handler(content_types=['text'])
def get(message):
    city_name = str(message.text)  # надання змінній значення введеного з повідомлення
    bot.send_message(message.chat.id, city.weather_report(city_name, message.from_user.id), parse_mode='html')  # виклик функції weather_report для об'єкту city і вивід результату в форматі html


# ініціалізація функції для обробки всіх інших типів повідомлень
@bot.message_handler(
    content_types=['audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'video_note', 'voice',
                   'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment', 'connected_website', 'poll',
                   'passport_data', 'web_app_data'])
def answer(message):
    bot.send_message(message.chat.id, 'Actually, it is not the name of the city🤓')  # вивід повідомлення про помилку


# функція запуску боту, яка відтворює його весь час
bot.polling(none_stop=True)
