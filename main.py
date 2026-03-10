import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- কনফিগারেশন ---
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6232195536  # আপনার আইডি
CHANNEL_USERNAME = "@shibir_online_library" # আপনার চ্যানেল ইউজারনেম

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # ১. সাবস্ক্রিপশন চেক (Force Join)
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
        if member.status in ['left', 'kicked']:
            keyboard = [[InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন", url="https://t.me/shibir_online_library")]]
            await update.message.reply_text(
                f"আসসালামু আলাইকুম {user.first_name}!\n\nবটটি ব্যবহার করতে আপনাকে অবশ্যই আমাদের চ্যানেলে জয়েন থাকতে হবে। জয়েন করে আবার /start দিন।",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
    except Exception as e:
        print(f"Error checking member: {e}")

    # ২. মেইন মেনু
    keyboard = [
        [InlineKeyboardButton("📝 বইয়ের রিকোয়েস্ট", callback_data='request_book')],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট", url="https://t.me/Sagor_Islam_id_")],
        [InlineKeyboardButton("📢 আমাদের লাইব্রেরি চ্যানেল", url="https://t.me/shibir_online_library")]
    ]
    
    await update.message.reply_text(
        f"স্বাগতম {user.first_name}!\n\nযেকোনো বইয়ের নাম লিখে আমাকে মেসেজ দিন, আমি আমাদের লাইব্রেরি থেকে সরাসরি লিঙ্ক খুঁজে দেব। ইনশাআল্লাহ।",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()

    # চ্যানেল জয়েন চেক (আবার চেক করা হচ্ছে যাতে কেউ লিভ নিলে কাজ না করে)
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
        if member.status in ['left', 'kicked']:
            await update.message.reply_text("দয়া করে আগে আমাদের চ্যানেলে জয়েন করুন।")
            return
    except: pass

    # যদি ইউজার রিকোয়েস্ট মোডে থাকে
    if context.user_data.get('awaiting_request'):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 **নতুন বইয়ের রিকোয়েস্ট:**\n\nবই: {text}\nইউজার: {user.first_name}\nID: `{user.id}`",
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ আপনার রিকোয়েস্টটি অ্যাডমিনের কাছে পাঠানো হয়েছে।")
        context.user_data['awaiting_request'] = False
        return

    # বই সার্চ এবং সরাসরি লিঙ্ক জেনারেশন
    if len(text) < 2:
        await update.message.reply_text("বইয়ের নামটি অন্তত ২ অক্ষরে লিখুন।")
        return

    encoded_query = urllib.parse.quote(text)
    # আপনার চ্যানেলের ইন-চ্যানেল সার্চ লিঙ্ক
    search_url = f"https://t.me/s/shibir_online_library?q={encoded_query}"
    
    keyboard = [
        [InlineKeyboardButton("📖 বইটি এখানে ডাউনলোড করুন", url=search_url)],
        [InlineKeyboardButton("📝 বই না পেলে রিকোয়েস্ট করুন", callback_data='request_book')]
    ]
    
    await update.message.reply_text(
        f"🔎 **'{text}'** এর জন্য আমাদের লাইব্রেরিতে নিচের লিঙ্কে ক্লিক করুন:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'request_book':
        await query.message.reply_text("বইয়ের নাম এবং লেখকের নাম লিখে মেসেজ দিন। আপনার মেসেজটি সরাসরি অ্যাডমিনের কাছে চলে যাবে।")
        context.user_data['awaiting_request'] = True

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
