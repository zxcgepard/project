import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('8172308599:AAGeUzhSVSlSbUzMJjmXTCETxedCmZO6YcQ')
bot = telebot.TeleBot(BOT_TOKEN)
def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton('На ужин'),
        KeyboardButton('Десерт'),
        KeyboardButton('Случайный'),
        KeyboardButton('Ввести словами')
    )
    return kb

food = ['лук', 'картошка', 'морковь', 'свекла', 'капуста', 'мясо', 'курица',
        'яйца', 'молоко', 'сыр', 'масло', 'мука', 'сахар', 'соль', 'помидоры',
        'огурцы', 'чеснок', 'рыба', 'гречка', 'рис', 'макароны']

def has_food(text):
    text = text.lower()
    for item in food:
        if item in text:
            return True
        return False

def get_recipe(q):
    try:
        r = requests.post('http://localhost:11434/api/generate', json={
            "model": "qwen2.5:3b",
            "prompt": f"Напиши рецепт на русском языке: {q}. Название, ингредиенты, шаги.",
            "stream": False
        })
        raw_recipe = r.json()['response']
        return clean_markdown(raw_recipe)
    except Exception as e:
        return f"Ошибка: {e}"

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, f"Привет, {msg.from_user.first_name}! Я кулинарный бот.", reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == 'На ужин')
def dinner(m):
    bot.send_message(m.chat.id, "Секунду, процесс может занять где-то 1 минуты")
    bot.send_message(m.chat.id, get_recipe("ужин из простых продуктов"))

@bot.message_handler(func=lambda m: m.text == 'Десерт')
def dessert(m):
    bot.send_message(m.chat.id, "Секунду, процесс может занять где-то 1 минуты")
    bot.send_message(m.chat.id, get_recipe("простой десерт"))

@bot.message_handler(func=lambda m: m.text == 'Случайный')
def random_recipe(m):
    bot.send_message(m.chat.id, "Секунду, процесс может занять где-то 1 минуты")
    bot.send_message(m.chat.id, get_recipe("любое блюдо"))

@bot.message_handler(func=lambda m: m.text == 'Ввести словами')
def ask_products(m):
    bot.send_message(m.chat.id, "Напиши продукты через запятую, например: картошка, лук, яйца")

@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    if msg.text.startswith('/'):
        return
    if has_food(msg.text):
        bot.send_message(msg.chat.id, f"Секунду, процесс может занять где-то 1 минуты .Ищу рецепт из: {msg.text}...")
        bot.send_message(msg.chat.id, get_recipe(msg.text))
    else:
        bot.send_message(msg.chat.id, "Я понимаю только продукты. Пример: картошка, лук, яйца", reply_markup=menu())




import re

def clean_recipe(text):
    text = text.replace('*', '')
    english_words = ['Dill', 'Bay leaf', 'sour cream', 'épaissit', 'chicken', 'beef', 'apple', 'pepper', 'salt', 'sugar', 'milk', 'butter', 'egg', 'cheese', 'cream', 'water', 'pimienta', 'Olivenöl', 'Oliven', 'öl']
    for word in english_words:
       text = text.replace(word, '')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


import re

def clean_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    text = re.sub(r'^\*\s+', '- ', text, flags=re.MULTILINE)
    return text

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)