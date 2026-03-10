import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন সংগ্রহ
TOKEN = os.environ.get("BOT_TOKEN")

# আপনার চ্যানেল এবং অ্যাডমিন লিঙ্ক
MY_CHANNEL_LINK = "https://t.me/shibir_online_library"
ADMIN_SUPPORT_LINK = "http://t.me/shibir_online_library?direct"
CHANNEL_USERNAME = "shibir_online_library"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    
    keyboard = [
        [InlineKeyboardButton("📢 আমাদের চ্যানেলে জয়েন করুন", url=MY_CHANNEL_LINK)],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট (যোগাযোগ)", url=ADMIN_SUPPORT_LINK)]
    ]
    
    welcome_text = (
        f"আসসালামু আলাইকুম {user_name}! 👋\n\n"
        "📖 আমি Shibir Online Library Bot বলছি।\n\n"
        "বাংলাদেশ ইসলামী ছাত্রশিবিরের যেকোনো বইয়ের নাম লিখে আমাকে মেসেজ দিন, আমি বইটি আপনাকে খুঁজে দেব। 🔍"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    if len(query) < 2:
        await update.message.reply_text("⚠️ দয়া করে বইয়ের সঠিক এবং পূর্ণ নাম লিখুন।")
        return

    # কি-ওয়ার্ড এনকোড করা
    encoded_query = urllib.parse.quote(query)
    
    # আপনার চাওয়া ব্রাউজিং লিঙ্ক (Web View)
    web_search_url = f"https://t.me/s/{CHANNEL_USERNAME}?q={encoded_query}"
    
    # বিকল্প শক্তিশালী সার্চ লিঙ্ক (যদি ব্রাউজারে কাজ না করে, এটি সরাসরি অ্যাপে খুঁজবে)
    app_search_url = f"tg://search?text=@{CHANNEL_USERNAME}%20{encoded_query}"
    
    # বাটন মেনু
    keyboard = [
        [InlineKeyboardButton(f"🌐 ব্রাউজারে ফলাফল দেখুন", url=web_search_url)],
        [InlineKeyboardButton(f"📲 সরাসরি অ্যাপে খুঁজুন", url=app_search_url)],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট (যোগাযোগ)", url=ADMIN_SUPPORT_LINK)],
        [InlineKeyboardButton("📢 আমাদের লাইব্রেরি চ্যানেল", url=MY_CHANNEL_LINK)]
    ]
    
    response_text = (
        f"🔎 '{query}' বই এর জন্য নিচের বাটনে ক্লিক করুন।\n\n"
        "যদি বইটি খুঁজে না পান তাহলে আবার সঠিক নাম লিখে পুনরায় চেষ্টা করুন অথবা অ্যাডমিন এর সাথে যোগাযোগ করুন। 📝"
    )
    
    try:
        await update.message.reply_text(
            response_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
        print("Bot is running with Multi-Search Options...")
        app.run_polling()
