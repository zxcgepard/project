import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

BOT_TOKEN = '8172308599:AAEuJ9Zd3vVETx18Ozi6fGuEMJ60cGWDmvk'
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

def get_recipe(q):
    try:
        r = requests.post('http://localhost:11434/api/generate', json={
            "model": "qwen2.5:3b",
            "prompt": f"Ты шеф-повар. Напиши рецепт на русском языке: {q}. Название, ингредиенты, шаги.",
            "stream": False
        })
        return r.json()['response']
    except:
        return "Ошибка! Проверь, запущена ли Ollama"

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, f"Привет, {msg.from_user.first_name}! Я кулинарный бот.", reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == 'На ужин')
def dinner(m):
    bot.send_message(m.chat.id, get_recipe("ужин из простых продуктов"))

@bot.message_handler(func=lambda m: m.text == 'Десерт')
def dessert(m):
    bot.send_message(m.chat.id, get_recipe("простой десерт"))

@bot.message_handler(func=lambda m: m.text == 'Случайный')
def random_recipe(m):
    bot.send_message(m.chat.id, get_recipe("любое блюдо"))

@bot.message_handler(func=lambda m: m.text == 'Ввести словами')
def ask_products(m):
    bot.send_message(m.chat.id, "Напиши продукты через запятую")

@bot.message_handler(func=lambda m: True)
def handle_text(m):
    if m.text.startswith('/'):
        return
    if m.text in ['На ужин', 'Десерт', 'Случайный', 'Ввести словами']:
        return
    bot.send_message(m.chat.id, get_recipe(m.text))

if __name__ == '__main__':
    print("Бот запущен")
    bot.polling(none_stop=True)