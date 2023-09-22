import telebot
import requests
from geopy.geocoders import Nominatim

# Ключ доступу до Telegram бота
TELEGRAM_TOKEN = '6133522056:AAFRLOCGa2OskL_nmFmjez_Ns3TjgPxSKTM'
# Ключ доступу до OpenWeatherMap API
OPENWEATHERMAP_API_KEY = '0edf7c9aa6fe7e01627bc2cbcda0b9d6'

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)
geolocator = Nominatim(user_agent="geoapiExercises")

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Введіть назву міста або напишіть 'Поточний', щоб дізнатися поточну погоду.")

@bot.message_handler(func=lambda message: message.text.lower() == 'поточний')
def get_current_location(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Давайте визначимо вашу поточну локацію. Будь ласка, надайте доступ до вашої геолокації.")
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = telebot.types.KeyboardButton(text="Надіслати геолокацію", request_location=True)
    markup.add(button)
    bot.send_message(chat_id, "Натисніть кнопку 'Надіслати геолокацію', щоб поділитися вашою локацією.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    latitude = message.location.latitude
    longitude = message.location.longitude
    location = geolocator.reverse(f"{latitude}, {longitude}")
    print(location)
    city = location.address.split(", ")[1]
    
    weather_data = get_weather(city)
    if weather_data['cod'] == 200:
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        message = f"Погода в місті {city}: {description}, Температура: {temperature}°C"
    else:
        message = "Не вдалося отримати погоду для цього міста."
    
    bot.send_message(chat_id, message)

@bot.message_handler(func=lambda message: True)
def weather_by_city(message):
    city = message.text
    weather_data = get_weather(city)
    if weather_data['cod'] == 200:
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        message = f"Погода в місті {city}: {description}, Температура: {temperature}°C"
    else:
        message = "Не вдалося отримати погоду для цього міста."
    bot.send_message(message.chat.id, message)

if __name__ == '__main__':
    bot.polling(none_stop=True)