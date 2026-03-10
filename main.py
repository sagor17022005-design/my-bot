import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- কনফিগারেশন ---
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_USERNAME = "@Sagor_Islam_id" # আপনার ইউজারনেম

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user.first_name}!\n"
        "আমি **Shibir Online Library Bot**।\n\n"
        "যেকোনো বইয়ের নাম লিখে আমাকে মেসেজ দিন, আমি আমাদের লাইব্রেরি থেকে সরাসরি লিঙ্ক খুঁজে দেব।"
    )

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if len(text) < 2:
        await update.message.reply_text("বইয়ের নামটি অন্তত ২ অক্ষরে লিখুন।")
        return

    # সার্চ ইউআরএল তৈরি (আপনার চ্যানেল থেকে সরাসরি রেজাল্ট দেখাবে)
    encoded_query = urllib.parse.quote(text)
    search_url = f"https://t.me/s/shibir_online_library?q={encoded_query}"
    
    # বাটন সেটআপ (সার্চ লিঙ্ক + অ্যাডমিন সাপোর্ট)
    keyboard = [
        [InlineKeyboardButton("📖 বইটি এখানে ডাউনলোড করুন", url=search_url)],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট (যোগাযোগ)", url=f"https://t.me/{ADMIN_USERNAME[1:]}")]
    ]
    
    await update.message.reply_text(
        f"🔎 **'{text}'** এর জন্য নিচের বাটনে ক্লিক করুন। বই না পেলে সরাসরি অ্যাডমিনকে জানাতে পারেন।",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
    
    print("Bot is live! No join required...")
    app.run_polling()
