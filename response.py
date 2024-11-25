import requests  # імпорт бібліотеки запросів
import datetime  # імпорт бібліотеки для роботи з часом
from config import weather_token  # імпорт токена звіта про погоду

# ініціалізація словника з погодними умовами і порадами
weather_description = {
    'Thunderstorm': 'Hide under the bed today🛏',
    'Ash': 'Maybe it is time to move?✈',
    'Squall': 'Wear lead shoes to stay on feet🎈',
    'Drizzle': "It is so good at home under the covers with a cup of cocoa☕",
    'Rain': "Time for romantic walks☔",
    'Snow': 'Let it snow, let it snow, let it snow☃',
    'Mist': "Can you see your nose? I'm not👀",
    'Fog': "Can you see your nose? I'm not👀",
    'Haze': 'This is what smoking leads to🚬',
    'Smoke': 'This is what smoking leads to🚬',
    'Dust': 'Apchi💦',
    'Sand': "When everything is over, let's make a sandcastle🏰",
    'Tornado': 'Hopefully, you have a very cozy basement🚪',
    'Clear': "Don't forget your sunglasses🕶",
    'Clouds': "I am a cloud, a cloud, a cloud. I'm not a bear at all🐻"
}

# ініціалізація словника зі смайликами
weather_smile = {
    'Thunderstorm': '⚡',
    'Ash': '🌋',
    'Squall': '🌬',
    'Drizzle': "🌧",
    'Rain': "🌧",
    'Snow': '🌨',
    'Mist': "🌁",
    'Fog': "🌁",
    'Haze': '🌫',
    'Smoke': '🌫',
    'Dust': '🌫',
    'Sand': "🏝",
    'Tornado': '🌪',
    'Clear': "☀",
    'Clouds': "⛅"
}
# ініціалізація класу
class Response_Default:
    name = None  # поле назви міста
    temp = None  # поле температури
    weather_condition = None  # поле погодних умов
    humidity = None  # поле вологості
    pressure = None  # поле тиску
    wind_speed = None  # поле швидкості вітру
    sunrise = None  # поле часу світанку
    sunset = None  # поле часу заходу сонця

    # ініціалізація методу заповнення полів класу
    def weather_report(self, city_name, user_id):  # метод приймає назву міста та id користувача
        # виконати наступні дії
        try:
            # запрос даних з ресурсу openweather, передаючи два аргументи: назва міста та погодний токен
            weather_request = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_token}&units=metric")
            # зберігання результатів запросу в змінній
            data = weather_request.json()
            self.name = data['name']  # надання полю класа значення назви міста
            self.temp = data['main']['temp']  # надання полю класа значення температури з обраного міста
            self.weather_condition = data['weather'][0]['main']  # надання полю класа значення погодної умови з обраного міста
            self.humidity = data['main']['humidity']  # надання полю класа значення вологості з обраного міста
            self.pressure = data['main']['pressure']  # надання полю класа значення тиску з обраного міста
            self.wind_speed = data['wind']['speed']  # надання полю класа значення швидкості вітру з обраного міста
            self.sunrise = datetime.datetime.fromtimestamp(
                data['sys']['sunrise'])  # надання полю класа значення світанку з обраного міста
            self.sunset = datetime.datetime.fromtimestamp(
                data['sys']['sunset'])  # надання полю класа значення заходу сонця з обраного міста
            self.save_info(user_id)  # виклик методу для зберігання даних про користувача
            return self.weather_message() # виклик наступного методу для формування повідомлення
        # якщо сталася помилка
        except:
            return "This city does not exist☠"  # повернення повідомлення про помилку

    # ініціалізація методу виводу повыдомлення
    def weather_message(self):
        if self.weather_condition in weather_description:  # якщо погодна умова є в словнику порад
            advice = weather_description[self.weather_condition]  # надання змінній значення з словника
        else:  # в інших випадках
            advice = 'Have a nice day'  # надання змінній значення поради

        if self.weather_condition in weather_smile:  # якщо погодна умова є в словнику смайлів
            smile = weather_smile[self.weather_condition]  # надання змінній значення з словника
        else:  # в інших випадках
            smile = '✨'  # надання змінній значення смайлика
        # повернення повідомлення з погодою
        return f"🏙<b>Weather report for {self.name}</b>🏙\n📆Date: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n🌡Temperature: {self.temp}°C {self.weather_condition}{smile}\n💦Humidity: {self.humidity}%\n〽Pressure: {self.pressure} mmHg\n💨Wind speed: {self.wind_speed} m/s\n🌅Sunrise time: {self.sunrise}\n🌇Sunset time: {self.sunset}\n{advice}"

    # ініціалізація методу зберігання даних про користувача
    def save_info(self, user_id):  # метод приймає id користувача
        # ініціалізація змінної і створення рядка для запису в файл
        line = str(user_id) + "/" + str(self.name) + "/" + str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M')) + "/ \n"
        with open('users_info.txt', "r+") as f:  # відкриття файлу для оновлення
            content = f.read()  # ініціалізація змінної і надання їй значення вмісту файлу
            f.seek(0, 0)  # встановлення вказівника на початок файлу
            f.write(line)  # запис нового рядка
            f.write(content)  # запис попередньої інформації
            f.close()  # закриття файлу

class Response(Response_Default):
    pass