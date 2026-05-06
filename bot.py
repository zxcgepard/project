import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

bot = telebot.TeleBot('8172308599:AAEuJ9Zd3vVETx18Ozi6fGuEMJ60cGWDmvk')

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
            "prompt": f"""Ты профессиональный повар. Напиши настоящий рецепт на русском языке.
Запрещено: выдумывать странные ингредиенты, писать бессмысленный текст.
Требования: рецепт должен быть реальным, ингредиенты настоящими, шаги понятными.
Не задавай уточняющих вопросов. Просто дай рецепт.
Формат ответа:
НАЗВАНИЕ: ...
ИНГРЕДИЕНТЫ: ...
ПРИГОТОВЛЕНИЕ: ...

Запрос пользователя: {q}""",
            "stream": False
        })
        return r.json()['response']
    except:
        return "Ошибка! Ollama не запущена"

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, f"Привет, {msg.from_user.first_name}!",
        reply_markup=menu()
    )

@bot.message_handler(func=lambda m: m.text == 'На ужин')
def din(m):
    bot.send_message(m.chat.id, "Секунду, процесс может занять где-то 2 минуты")
    bot.send_message(m.chat.id, get_recipe("ужин"))

@bot.message_handler(func=lambda m: m.text == 'Десерт')
def des(m):
    bot.send_message(m.chat.id, "Секунду, процесс может занять где-то 2 минуты")
    bot.send_message(m.chat.id, get_recipe("десерт"))

@bot.message_handler(func=lambda m: m.text == 'Случайный')
def ran(m):
    bot.send_message(m.chat.id, "Секунду, процесс может занять где-то 2 минуты")
    bot.send_message(m.chat.id, get_recipe("любое блюдо"))

@bot.message_handler(func=lambda m: m.text == 'Ввести словами')
def ask(m):
    bot.send_message(m.chat.id, "Напиши продукты через запятую")

@bot.message_handler(func=lambda m: True)
def text(msg):
    if msg.text.startswith('/'):
        return

    if has_food(msg.text):
        bot.send_message(msg.chat.id, f"Ищу: {msg.text}...")
        bot.send_message(msg.chat.id, get_recipe(msg.text))
    else:
        bot.send_message(
            msg.chat.id,
            "Я понимаю только продукты. Пример: картошка, лук, яйца",
            reply_markup=menu()
        )


bot.polling(none_stop=True)
