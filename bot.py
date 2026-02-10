import os
import telebot
from telebot import types
import json

# ========= ТОКЕН ИЗ RAILWAY VARIABLES =========
TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@INTERIOR_DESIGN_KRASNODAR"
WEBAPP_URL = "https://karlitomasterini-dotcom.github.io/interior-mini-app/"

# Проверка токена
if not TOKEN:
    print("❌ TOKEN НЕ НАЙДЕН! Проверь Variables в Railway")
    exit()

bot = telebot.TeleBot(TOKEN)

# ========= КНОПКА =========
def get_inline_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text="📝 Оставить заявку",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
        )
    )
    return markup

# ========= /start =========
@bot.message_handler(commands=['start'])
def start(message):
    print("▶ /start от", message.chat.id)

    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\n"
        "Нажмите кнопку ниже, чтобы оставить заявку 👇",
        reply_markup=get_inline_keyboard()
    )

# ========= ПРИЕМ ЗАЯВКИ =========
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app(message):
    print("🔥 Получены web_app_data")

    try:
        raw = message.web_app_data.data
        print("RAW:", raw)

        data = json.loads(raw)

        name = data.get("name", "Не указано")
        phone = data.get("phone", "Не указан")
        comment = data.get("comment", "—")

        text = (
            "📩 Новая заявка\n\n"
            f"👤 Имя: {name}\n"
            f"📞 Телефон: {phone}\n"
            f"💬 Комментарий: {comment}"
        )

        # 👉 В КАНАЛ
        bot.send_message(CHANNEL_ID, text)

        # 👉 Пользователю
        bot.send_message(
            message.chat.id,
            "✅ Спасибо за заявку!\n\n"
            "Мы скоро свяжемся с вами 😊\n\n"
            "Можно оставить ещё одну заявку 👇",
            reply_markup=get_inline_keyboard()
        )

        print("✅ Заявка отправлена")

    except Exception as e:
        print("❌ ОШИБКА:", e)
        bot.send_message(message.chat.id, "Ошибка при обработке заявки 😢")

# ========= FALLBACK =========
@bot.message_handler(func=lambda m: True)
def fallback(message):
    print("ℹ️ Обычное сообщение:", message.text)

# ========= ЗАПУСК =========
print("🤖 Бот запущен")
bot.infinity_polling(timeout=20, long_polling_timeout=20)
