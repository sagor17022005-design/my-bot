import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# লগিং সেটআপ যাতে কোনো ভুল হলে রেলওয়ে ড্যাশবোর্ডে দেখা যায়
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# আপনার বট টোকেন এখানে দিন (অথবা রেলওয়ে এনভায়রনমেন্ট ভেরিয়েবল ব্যবহার করুন)
TOKEN = "YOUR_BOT_TOKEN_HERE" 
CHANNEL_LINK = "https://t.me/shibir_online_library"
CHANNEL_USERNAME = "shibir_online_library"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user_name}!\n"
        f"বইয়ের নাম লিখে মেসেজ দিন, আমি সেটি আমাদের লাইব্রেরিতে খুঁজে দেব।"
    )

async def search_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    
    # ২ অক্ষরের কম সার্চ করলে রেজাল্ট ভালো আসে না
    if len(query) < 2:
        await update.message.reply_text("অনুগ্রহ করে বইয়ের নাম পূর্ণাঙ্গভাবে লিখুন।")
        return

    # টেলিগ্রামের পাবলিক সার্চ ইউআরএল তৈরি
    # এটি ইউজারকে সরাসরি আপনার চ্যানেলের ঐ নির্দিষ্ট সার্চ রেজাল্টে নিয়ে যাবে
    search_url = f"https://t.me/s/{CHANNEL_USERNAME}?q={query.replace(' ', '+')}"
    
    response = (
        f"📚 *সার্চ রেজাল্ট:* {query}\n\n"
        f"আপনার কাঙ্ক্ষিত বইটি নিচে দেওয়া লিঙ্কে ক্লিক করে খুঁজে নিন:\n"
        f"🔗 [বইটি এখানে দেখুন]({search_url})\n\n"
        f"ধন্যবাদ আমাদের সাথে থাকার জন্য।"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=False)

def main():
    # বট তৈরি
    application = Application.builder().token(TOKEN).build()

    # কমান্ড ও মেসেজ হ্যান্ডলার
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_books))

    # বট চালু করা
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
