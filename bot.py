import telebot
from telebot import types
import json
import os

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@INTERIOR_DESIGN_KRASNODAR"
WEBAPP_URL = "https://karlitomasterini-dotcom.github.io/interior-mini-app/"

bot = telebot.TeleBot(TOKEN)

def get_inline_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text="📝 Оставить заявку",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
        )
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    print("▶ /start от", message.chat.id)
    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\nНажмите кнопку ниже 👇",
        reply_markup=get_inline_keyboard()
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    print("🔥 web_app_data ПОЛУЧЕН")

    try:
        raw = message.web_app_data.data
        print("RAW:", raw)

        data = json.loads(raw)

        name = data.get("name", "Не указано")
        phone = data.get("phone", "Не указан")
        comment = data.get("comment", "—")

        text = f"""
📩 Новая заявка

👤 Имя: {name}
📞 Телефон: {phone}
💬 Комментарий: {comment}
"""

        bot.send_message(CHANNEL_ID, text)

        bot.send_message(
            message.chat.id,
            "✅ Спасибо! Заявка отправлена 😊",
            reply_markup=get_inline_keyboard()
        )

    except Exception as e:
        print("❌ ОШИБКА:", e)

print("🤖 Бот запущен")
bot.infinity_polling()

