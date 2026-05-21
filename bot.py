import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import subprocess

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

def get_recipe_from_book(user_query):
    try:
        result = subprocess.run(
            ['python3', '/opt/rag-recipes/rag_search.py', user_query],
            capture_output=True,
            text=True,
            timeout=90
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return "Рецепт не найден. Попробуйте другие ключевые слова."
    except Exception as e:
        return f"Ошибка поиска: {e}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я кулинарный бот. Рецепты беру из книги Похлёбкина.",
        reply_markup=menu()
    )

@bot.message_handler(func=lambda m: m.text == 'На ужин')
def dinner(m):
    bot.send_message(m.chat.id, "Ищу рецепт для ужина...")
    recipe = get_recipe_from_book("ужин")
    bot.send_message(m.chat.id, recipe)

@bot.message_handler(func=lambda m: m.text == 'Десерт')
def dessert(m):
    bot.send_message(m.chat.id, "Ищу десерт...")
    recipe = get_recipe_from_book("десерт")
    bot.send_message(m.chat.id, recipe)

@bot.message_handler(func=lambda m: m.text == 'Случайный')
def random_recipe(m):
    bot.send_message(m.chat.id, "Выбираю случайный рецепт...")
    recipe = get_recipe_from_book("случайный")
    bot.send_message(m.chat.id, recipe)

@bot.message_handler(func=lambda m: m.text == 'Ввести словами')
def ask_products(m):
    bot.send_message(m.chat.id, "Напиши блюдо или ингредиенты, например: борщ, блины, картошка")

@bot.message_handler(func=lambda m: True)
def handle_text(m):
    if m.text.startswith('/'):
        return
    if m.text in ['На ужин', 'Десерт', 'Случайный', 'Ввести словами']:
        return
    bot.send_message(m.chat.id, f"Ищу: {m.text}...")
    recipe = get_recipe_from_book(m.text)
    bot.send_message(m.chat.id, recipe)

if __name__ == '__main__':
    print("Бот запущен с RAG-поиском по книге")
    bot.polling(none_stop=True)