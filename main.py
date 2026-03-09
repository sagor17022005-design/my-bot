# Filename: shibir_library_bot.py
# Python 3.10+
# Dependencies: python-telegram-bot v20.x, fuzzywuzzy
# pip install python-telegram-bot==20.3 fuzzywuzzy[speedup]

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from fuzzywuzzy import process
import os

# Bot token
TOKEN = os.environ.get("BOT_TOKEN", "8746638213:AAHgZWc-rp4_h1Vnld2IGN2WHQ_CiWHPoOY")

# বইয়ের নাম → চ্যানেল লিংক (post URL)
books = {
    "কর্মী সিলেবাস": "https://t.me/shibir_online_library/12",
    "সাথী সিলেবাস": "https://t.me/shibir_online_library/25",
    "সদস্য সিলেবাস": "https://t.me/shibir_online_library/30",
    "সকল বই": "https://t.me/shibir_online_library",
    # আরও বই যোগ করা যাবে
}

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "আসসালামু আলাইকুম।\n"
        "বইয়ের নাম লিখে সার্চ করুন। ছাত্রশিবিরের বইয়ের PDF লিংক পাবেন।\n\n"
        "উদাহরণ: কর্মী সিলেবাস, সাথী সিলেবাস, সদস্য সিলেবাস"
    )

# Keyword search function
async def search_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        return

    # Fuzzy search (partial match)
    matches = process.extract(query, books.keys(), limit=5)  # Top 5 matches
    results = [m for m in matches if m[1] >= 60]  # Only 60%+ similarity

    if results:
        for name, score in results:
            link = books[name]
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("📄 দেখুন", url=link)]])
            await update.message.reply_text(f"📚 {name}", reply_markup=kb)
    else:
        await update.message.reply_text("দুঃখিত, কোনো মিল পাওয়া যায়নি।")

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_book))
    print("Shibir Library Bot is running...")
    app.run_polling()
