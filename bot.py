import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import subprocess
import random
import re

BOT_TOKEN = '8172308599:AAEuJ9Zd3vVETx18Ozi6fGuEMJ60cGWDmvk'
bot = telebot.TeleBot(BOT_TOKEN)

def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton('На ужин'),
        KeyboardButton('Десерт'),
        KeyboardButton('Случайный'),
        KeyboardButton('Ввести словами')
    )
    return keyboard

def get_recipe_from_book(user_query):
    try:
        result = subprocess.run(
            ['python3', '/opt/simple-rag-script/rag.py', '--query', user_query],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return "Рецепт не найден. Попробуйте другие ключевые слова."
    except Exception as error:
        return f"Ошибка поиска: {error}"

def get_random_recipe():
    try:
        with open('/opt/simple-rag-script/documents/pokhlebkin.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        recipes = content.split('\n\n')
        random_recipe = random.choice(recipes).strip()
        return random_recipe if random_recipe else "Не удалось найти случайный рецепт"
    except Exception as error:
        return f"Ошибка: {error}"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я кулинарный бот. Рецепты беру из книги Похлёбкина.", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == 'На ужин')
def dinner(message):
    bot.send_message(message.chat.id, "Ищу рецепт для ужина...")
    recipe = get_recipe_from_book("ужин")
    bot.send_message(message.chat.id, recipe)

@bot.message_handler(func=lambda message: message.text == 'Десерт')
def dessert(message):
    bot.send_message(message.chat.id, "Ищу десерт...")
    recipe = get_recipe_from_book("десерт")
    bot.send_message(message.chat.id, recipe)

@bot.message_handler(func=lambda message: message.text == 'Случайный')
def random_recipe(message):
    bot.send_message(message.chat.id, "Выбираю случайный рецепт...")
    recipe = get_random_recipe()
    bot.send_message(message.chat.id, recipe)

@bot.message_handler(func=lambda message: message.text == 'Ввести словами')
def ask_ingredients(message):
    bot.send_message(message.chat.id, "Напиши блюдо или ингредиенты, например: борщ, блины, картошка")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.startswith('/'):
        return
    if message.text in ['На ужин', 'Десерт', 'Случайный', 'Ввести словами']:
        return
    
    bot.send_message(message.chat.id, f"Ищу: {message.text}...")
    recipe = get_recipe_from_book(message.text)
    bot.send_message(message.chat.id, recipe)

if __name__ == '__main__':
    print("Бот запущен и работает с книгой рецептов")
    bot.polling(none_stop=True)
