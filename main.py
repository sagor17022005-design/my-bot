import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Variable setup
TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = "@shibir_online_library" # আপনার চ্যানেলের ইউজারনেম

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম।\nবইয়ের নাম লিখে সার্চ দিন, আমি চ্যানেল থেকে খুঁজে দেব।")

async def auto_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()
    if len(query) < 3:
        await update.message.reply_text("অনুগ্রহ করে অন্তত ৩ অক্ষরের নাম লিখুন।")
        return

    # এখানে আমরা সরাসরি চ্যানেলের পাবলিক লিঙ্ক ফরম্যাট ব্যবহার করছি
    # ইউজারকে জানানো হচ্ছে তারা যেন চ্যানেলে সার্চ করে অথবা বট লিঙ্ক জেনারেট করছে
    search_url = f"https://t.me/s/{CHANNEL_USERNAME[1:]}?q={query}"
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 চ্যানেলে ফলাফল দেখুন", url=search_url)]
    ])
    
    await update.message.reply_text(
        f"আপনার খোঁজা '{query}' সম্পর্কিত বইগুলো চ্যানেলে দেখতে নিচের বাটনে ক্লিক করুন:",
        reply_markup=kb
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_search))
    app.run_polling()
