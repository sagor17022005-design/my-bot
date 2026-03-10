import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- কনফিগারেশন ---
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_SUPPORT_LINK = "http://t.me/shibir_online_library?direct"
CHANNEL_LINK = "https://t.me/shibir_online_library"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"আসসালামু আলাইকুম {user.first_name}! 👋\n\n"
        "📖 আমি Shibir Online Library Bot বলছি।\n\n"
        "বাংলাদেশ ইসলামী ছাত্রশিবিরের যেকোনো বইয়ের নাম লিখে আমাকে মেসেজ দিন, আমি বইটি আপনাকে খুঁজে দেব। 🔍\n\n"
        f"📢 আমাদের বই এর চ্যানেলে যুক্ত থাকুন: {CHANNEL_LINK}"
    )
    await update.message.reply_text(welcome_text, disable_web_page_preview=True)

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    if len(query) < 2:
        await update.message.reply_text("⚠️ দয়া করে বইয়ের সঠিক এবং পূর্ণ নাম লিখুন।")
        return

    # সরাসরি ইন-চ্যানেল সার্চ ইউআরএল তৈরি
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://t.me/s/shibir_online_library?q={encoded_query}"
    
    # বাটন মেনু সেটআপ (বই লিঙ্ক + অ্যাডমিন + চ্যানেল)
    keyboard = [
        [InlineKeyboardButton("📚 বইটি এখানে ডাউনলোড করুন", url=search_url)],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট (যোগাযোগ)", url=ADMIN_SUPPORT_LINK)],
        [InlineKeyboardButton("📢 আমাদের লাইব্রেরি চ্যানেল", url=CHANNEL_LINK)]
    ]
    
    # রিপ্লাই মেসেজ
    response_text = (
        f"🔎 '{query}' এর জন্য নিচের বাটনে ক্লিক করুন।\n\n"
        "❌ বইটি খুঁজে পাওয়া যাচ্ছে না? তবে সঠিক নাম লিখে পুনরায় চেষ্টা করুন অথবা সরাসরি অ্যাডমিনকে জানান। 📝\n\n"
        f"📢 আমাদের বই এর চ্যানেলে যুক্ত থাকুন: {CHANNEL_LINK}"
    )
    
    await update.message.reply_text(
        response_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
        print("Bot is running perfectly...")
        app.run_polling()
