import json
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Файл, в котором хранятся коды и тексты
DATA_FILE = 'big_texts.json'

# Список ID администраторов
ADMINS = [8071719190]  # <-- сюда добавь свой Telegram user_id

# Загружаем тексты из файла
def load_texts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Сохраняем тексты в файл
def save_texts(texts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

# Начальное чтение
BIG_TEXTS = load_texts()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне код и я выдам данные от аккаунта."
    )

# /add код | текст
async def add_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("У тебя нет прав для этой команды.")
        return

    parts = update.message.text[len('/add '):].split('|', 1)
    if len(parts) != 2:
        await update.message.reply_text("Неверный формат. Используй: /add код | текст")
        return

    code = parts[0].strip()
    text = parts[1].strip()

    BIG_TEXTS[code] = text
    save_texts(BIG_TEXTS)

    await update.message.reply_text(f"Код '{code}' успешно добавлен.")

# Обработка сообщений с кодами
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    big_text = BIG_TEXTS.get(code)

    if big_text:
        await update.message.reply_text(big_text)
    else:
        await update.message.reply_text(
            "Код не найден. Попробуй другой или обратись к администратору."
        )

def main():
    token = "7991629839:AAGcAnk54U3ubjgcAa6qfGF5pizaqfHo-CM"  # <-- сюда свой токен
    app = ApplicationBuilder().token(token).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_code))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск
    app.run_polling()

if __name__ == "__main__":
    main()
