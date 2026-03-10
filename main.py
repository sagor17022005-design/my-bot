import os
import urllib.parse
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- কনফিগারেশন ---
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_SUPPORT_LINK = "http://t.me/shibir_online_library?direct"
CHANNEL_LINK = "https://t.me/shibir_online_library"
CHANNEL_USERNAME = "shibir_online_library"

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

    # সার্চ রেজাল্ট চেক করা হচ্ছে
    search_url_web = f"https://t.me/s/{CHANNEL_USERNAME}?q={urllib.parse.quote(query)}"
    
    try:
        response = requests.get(search_url_web, timeout=10)
        # রেজাল্ট না থাকলে টেলিগ্রাম 'No messages found' দেখায়
        if "No messages found" in response.text or "tgme_widget_message_error" in response.text:
            found = False
        else:
            found = True
    except:
        found = True # এরর হলে আমরা ধরে নেব রেজাল্ট থাকতে পারে

    if found:
        # বই পাওয়া গেলে
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://t.me/s/{CHANNEL_USERNAME}?q={encoded_query}"
        
        keyboard = [
            [InlineKeyboardButton("📚 বইটি এখানে ডাউনলোড করুন", url=search_url)],
            [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট (যোগাযোগ)", url=ADMIN_SUPPORT_LINK)]
        ]
        
        await update.message.reply_text(
            f"🔎 '{query}' এর জন্য নিচের বাটনে ক্লিক করুন।\n\n"
            f"📢 আমাদের বই এর চ্যানেলে যুক্ত থাকুন: {CHANNEL_LINK}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
    else:
        # বই না পাওয়া গেলে আপনার দেওয়া নির্দিষ্ট মেসেজ
        error_text = (
            "❌ বইটি খুঁজে পাওয়া যাচ্ছে না।\n\n"
            "দয়া করে বই এর সঠিক নাম লিখুন অথবা অ্যাডমিন এর সাথে সরাসরি যোগাযোগ করুন। 📝\n\n"
            f"📢 আমাদের বই এর চ্যানেলে যুক্ত থাকুন: {CHANNEL_LINK}"
        )
        keyboard = [[InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট", url=ADMIN_SUPPORT_LINK)]]
        
        await update.message.reply_text(
            error_text, 
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN variable is missing!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
        print("Bot is starting...")
        app.run_polling()
