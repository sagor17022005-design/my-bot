import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন সংগ্রহ
TOKEN = os.environ.get("BOT_TOKEN")

# আপনার চ্যানেল এবং অ্যাডমিন লিঙ্ক
MY_CHANNEL_LINK = "https://t.me/shibir_online_library"
ADMIN_SUPPORT_LINK = "http://t.me/shibir_online_library?direct"
OFFICIAL_WEBSITE = "https://shibirlibrary.org"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    
    keyboard = [
        [InlineKeyboardButton("📢 আমাদের চ্যানেলে জয়েন করুন", url=MY_CHANNEL_LINK)],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট (যোগাযোগ)", url=ADMIN_SUPPORT_LINK)]
    ]
    
    welcome_text = (
        f"আসসালামু আলাইকুম {user_name}! 👋\n\n"
        "📖 আমি Shibir Online Library Bot বলছি।\n\n"
        "বইয়ের নাম লিখে আমাকে মেসেজ দিন, আমি সরাসরি ওয়েবসাইট ও চ্যানেল থেকে আপনাকে বই খুঁজে দেব। 🔍"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    if len(query) < 2:
        await update.message.reply_text("⚠️ দয়া করে বইয়ের সঠিক এবং পূর্ণ নাম লিখুন।")
        return

    # কি-ওয়ার্ড এনকোড করা
    encoded_query = urllib.parse.quote(query)
    
    # অফিসিয়াল ওয়েবসাইটের সার্চ লিঙ্ক
    website_search_url = f"{OFFICIAL_WEBSITE}/?s={encoded_query}"
    
    # আপনার চ্যানেলের ব্রাউজিং সার্চ লিঙ্ক
    channel_search_url = f"https://t.me/s/shibir_online_library?q={encoded_query}"
    
    # বাটন মেনু
    keyboard = [
        [InlineKeyboardButton(f"🌐 ওয়েবসাইট থেকে ডাউনলোড করুন", url=website_search_url)],
        [InlineKeyboardButton(f"📚 আমাদের চ্যানেলে খুঁজুন", url=channel_search_url)],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট (যোগাযোগ)", url=ADMIN_SUPPORT_LINK)],
        [InlineKeyboardButton("📢 আমাদের লাইব্রেরি চ্যানেল", url=MY_CHANNEL_LINK)]
    ]
    
    response_text = (
        f"🔎 '{query}' বই এর জন্য নিচের বাটনে ক্লিক করুন।\n\n"
        "যদি বইটি খুঁজে না পান তাহলে আবার সঠিক নাম লিখে পুনরায় চেষ্টা করুন অথবা অ্যাডমিন এর সাথে যোগাযোগ করুন। 📝"
    )
    
    await update.message.reply_text(
        response_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
        print("Bot is running with Website & Channel Search...")
        app.run_polling()
