import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Variable setup
TOKEN = os.environ.get("BOT_TOKEN")
# আপনার চ্যানেলের ইউজারনেম (অবশ্যই @ থাকতে হবে)
CHANNEL_USERNAME = "@shibir_online_library" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "আসসালামু আলাইকুম।\n"
        "বইয়ের নাম লিখে সার্চ দিন। আমি সরাসরি চ্যানেল থেকে খুঁজে দেব।\n\n"
        "যেমন: কর্মপদ্ধতি"
    )

async def auto_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    if len(query) < 2:
        await update.message.reply_text("অনুগ্রহ করে বইয়ের নামটি একটু বিস্তারিত লিখুন।")
        return

    # টেলিগ্রাম চ্যানেলের ভেতরে সার্চ করার লিঙ্ক তৈরি
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://t.me/s/{CHANNEL_USERNAME[1:]}?q={encoded_query}"
    
    # ইনলাইন বাটন তৈরি
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔍 '{query}' এর ফলাফল দেখুন", url=search_url)]
    ])
    
    await update.message.reply_text(
        f"আপনার খোঁজা বইটির জন্য নিচের বাটনে ক্লিক করুন। এটি সরাসরি আপনাকে আমাদের চ্যানেলের ওই বইটিতে নিয়ে যাবে:",
        reply_markup=kb
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_search))
    print("Auto-indexing bot is running...")
    app.run_polling()
