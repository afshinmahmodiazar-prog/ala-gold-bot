import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🪙 به ربات قیمت طلای ئالا خوش آمدید.\n\n"
        "ربات با موفقیت فعال است. ✅"
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("ALA GOLD BOT IS RUNNING...")
    app.run_polling()


if __name__ == "__main__":
    main()
