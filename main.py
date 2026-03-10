import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- কনফিগারেশন ---
TOKEN = os.environ.get("BOT_TOKEN")
# আপনার দেওয়া নতুন ডিরেক্ট লিঙ্ক
ADMIN_SUPPORT_LINK = "http://t.me/shibir_online_library?direct"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # আপনার দেওয়া নির্দিষ্ট টেক্সট ইমোজি সহ
    welcome_text = (
        f"আসসালামু আলাইকুম {user.first_name}! 👋\n\n"
        "📖 আমি Shibir Online Library Bot বলছি।\n\n"
        "বাংলাদেশ ইসলামী ছাত্রশিবিরের যেকোনো বইয়ের নাম লিখে আমাকে মেসেজ দিন, আমি বইটি আপনাকে খুঁজে দেব। 🔍"
    )
    await update.message.reply_text(welcome_text)

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if len(text) < 2:
        await update.message.reply_text("⚠️ দয়া করে বইয়ের সঠিক এবং পূর্ণ নাম লিখুন।")
        return

    # আপনার চ্যানেলের ইন-চ্যানেল সার্চ ইউআরএল
    encoded_query = urllib.parse.quote(text)
    search_url = f"https://t.me/s/shibir_online_library?q={encoded_query}"
    
    # বাটন সেটআপ
    keyboard = [
        [InlineKeyboardButton("📚 বইটি এখানে ডাউনলোড করুন", url=search_url)],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট (যোগাযোগ)", url=ADMIN_SUPPORT_LINK)]
    ]
    
    # রিপ্লাই মেসেজ
    await update.message.reply_text(
        f"🔎 '{text}' এর জন্য নিচের বাটনে ক্লিক করুন।\n\n"
        "যদি কাঙ্ক্ষিত বইটি না পান, তবে সঠিক নাম লিখে পুনরায় চেষ্টা করুন অথবা অ্যাডমিনকে জানান। 📝",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
    
    print("Bot is running with New Admin Link and Emojis...")
    app.run_polling()
