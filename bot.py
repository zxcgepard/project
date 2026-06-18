# Бот переведён на GigaChat
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GIGACHAT_AUTH_KEY = os.getenv('GIGACHAT_AUTH_KEY') # Новый ключ для GigaChat

bot = telebot.TeleBot(BOT_TOKEN)

# Инициализация клиента GigaChat
giga = GigaChat(
    credentials=GIGACHAT_AUTH_KEY,
    scope="GIGACHAT_API_PERS",  # Для физических лиц
    model="GigaChat",           # Можно также использовать "GigaChat-Pro" или "GigaChat-Max"
    verify_ssl_certs=False      # Отключаем проверку SSL, если возникают ошибки
)

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton('На ужин'),
        KeyboardButton('Десерт'),
        KeyboardButton('Случайный'),
        KeyboardButton('Ввести словами')
    )
    return kb

def get_recipe(query):
    try:
        # Формируем запрос для GigaChat
        prompt = f"Напиши рецепт на русском языке: {query}. Название, ингредиенты, шаги."
        response = giga.chat(prompt)
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка при обращении к GigaChat: {e}"

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, f"Привет, {msg.from_user.first_name}! Я кулинарный бот на GigaChat.", reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == 'На ужин')
def dinner(m):
    bot.send_message(m.chat.id, "Готовлю рецепт ужина...")
    bot.send_message(m.chat.id, get_recipe("ужин из простых продуктов"))

@bot.message_handler(func=lambda m: m.text == 'Десерт')
def dessert(m):
    bot.send_message(m.chat.id, "Готовлю десерт...")
    bot.send_message(m.chat.id, get_recipe("простой десерт"))

@bot.message_handler(func=lambda m: m.text == 'Случайный')
def random_recipe(m):
    bot.send_message(m.chat.id, "Генерирую случайный рецепт...")
    bot.send_message(m.chat.id, get_recipe("любое блюдо"))

@bot.message_handler(func=lambda m: m.text == 'Ввести словами')
def ask_products(m):
    bot.send_message(m.chat.id, "Напиши продукты через запятую, например: картошка, лук, яйца")

@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    if msg.text.startswith('/'):
        return
    if msg.text in ['На ужин', 'Десерт', 'Случайный', 'Ввести словами']:
        return
    bot.send_message(msg.chat.id, f"Ищу рецепт из: {msg.text}...")
    bot.send_message(msg.chat.id, get_recipe(msg.text))

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)