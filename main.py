import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- কনফিগারেশন ---
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6232195536  # আপনার আইডি সরাসরি এখানে বসিয়ে দিলাম
CHANNEL_ID = "@shibir_online_library" # আপনার চ্যানেল ইউজারনেম

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # ১. সাবস্ক্রিপশন চেক (Force Join)
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
        if member.status in ['left', 'kicked']:
            keyboard = [[InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন", url="https://t.me/shibir_online_library")]]
            await update.message.reply_text(
                "বটটি ব্যবহার করতে আমাদের চ্যানেলে জয়েন থাকা জরুরি। জয়েন করার পর আবার /start দিন।",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
    except Exception as e:
        print(f"Join Check Error: {e}")

    # ২. মেইন মেনু বাটন
    keyboard = [
        [InlineKeyboardButton("📝 বইয়ের রিকোয়েস্ট করুন", callback_data='request_book')],
        [InlineKeyboardButton("📢 আমাদের লাইব্রেরি চ্যানেল", url="https://t.me/shibir_online_library")],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট", url="https://t.me/Sagor_Islam_id_")]
    ]
    
    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user.first_name}!\n\n"
        "আমি **Shibir Online Library Bot**। বইয়ের নাম লিখে মেসেজ দিন অথবা নিচের অপশন ব্যবহার করুন।",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_search_and_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    user = update.effective_user

    # বই রিকোয়েস্ট হ্যান্ডলিং
    if context.user_data.get('awaiting_request'):
        # আপনার ইনবক্সে রিকোয়েস্ট পাঠানো
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 **নতুন বইয়ের রিকোয়েস্ট:**\n\nবই: {query}\nইউজার: {user.first_name}\nআইডি: `{user.id}`\nইউজারনেম: @{user.username}",
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ আপনার রিকোয়েস্টটি অ্যাডমিনের কাছে পাঠানো হয়েছে। ধন্যবাদ!")
        context.user_data['awaiting_request'] = False
        return

    # সাধারণ বই সার্চ
    if len(query) < 2:
        await update.message.reply_text("বইয়ের নামটি অন্তত ২ অক্ষরে লিখুন।")
        return

    encoded_query = urllib.parse.quote(query)
    keyboard = [
        [InlineKeyboardButton("📚 আমাদের লাইব্রেরিতে খুঁজুন", url=f"https://t.me/s/shibir_online_library?q={encoded_query}")],
        [InlineKeyboardButton("🌐 পুরো টেলিগ্রামে খুঁজুন", url=f"tg://search?text={encoded_query}")],
        [InlineKeyboardButton("🔍 গুগল (PDF) সার্চ", url=f"https://www.google.com/search?q=filetype:pdf+{encoded_query}+bangla")]
    ]
    
    await update.message.reply_text(
        f"🔎 **'{query}'** এর ফলাফল দেখতে নিচের বাটনে ক্লিক করুন:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'request_book':
        await query.message.reply_text("বইয়ের নাম এবং লেখকের নাম লিখে মেসেজ দিন (যেমন: প্যারাডক্সিক্যাল সাজিদ - আরিফ আজাদ)।")
        context.user_data['awaiting_request'] = True

# ব্রডকাস্ট কমান্ড (শুধুমাত্র আপনি /broadcast লিখে মেসেজ দিলে সবার কাছে যাবে)
# এটি করার জন্য ডাটাবেস প্রয়োজন, তবে আপাতত এটি আপনার রিকোয়েস্ট ফিচারের সাথে থাকছে।

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_and_request))
    
    print("Bot is fully updated with Request Feature and Admin ID!")
    app.run_polling()
