import os
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- কনফিগারেশন ---
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6232195536  # আপনার আইডি
CHANNEL_ID = "@shibir_online_library"

# ইউজার লিস্ট সেভ করার জন্য একটি সেট (ব্রডকাস্টের জন্য)
# নোট: বড় পরিসরে ব্যবহারের জন্য ডাটাবেস (যেমন MongoDB) প্রয়োজন, আপাতত এটি মেমোরিতে কাজ করবে।
user_list = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_list.add(user.id) # ইউজারকে লিস্টে যোগ করা
    
    # সাবস্ক্রিপশন চেক
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
        if member.status in ['left', 'kicked']:
            keyboard = [[InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন", url="https://t.me/shibir_online_library")]]
            await update.message.reply_text("বটটি ব্যবহার করতে আমাদের চ্যানেলে জয়েন করুন।", reply_markup=InlineKeyboardMarkup(keyboard))
            return
    except: pass

    keyboard = [
        [InlineKeyboardButton("📝 বইয়ের রিকোয়েস্ট করুন", callback_data='request_book')],
        [InlineKeyboardButton("📢 আমাদের লাইব্রেরি", url="https://t.me/shibir_online_library")],
        [InlineKeyboardButton("👨‍💻 অ্যাডমিন সাপোর্ট", url="https://t.me/Sagor_Islam_id_")]
    ]
    await update.message.reply_text(f"আসসালামু আলাইকুম {user.first_name}! বইয়ের নাম লিখে মেসেজ দিন।", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    user = update.effective_user

    # ১. ব্রডকাস্ট ফিচার (অ্যাডমিন যদি /broadcast লিখে কিছু পাঠান)
    if query.startswith("/broadcast") and user.id == ADMIN_ID:
        msg = query.replace("/broadcast", "").strip()
        if not msg: return await update.message.reply_text("মেসেজটি লিখুন। উদা: /broadcast হ্যালো")
        count = 0
        for uid in user_list:
            try:
                await context.bot.send_message(chat_id=uid, text=f"📢 **নোটিশ:**\n\n{msg}", parse_mode="Markdown")
                count += 1
            except: continue
        return await update.message.reply_text(f"✅ {count} জন ইউজারের কাছে মেসেজ পাঠানো হয়েছে।")

    # ২. বই রিকোয়েস্ট হ্যান্ডলিং
    if context.user_data.get('awaiting_request'):
        await context.bot.send_message(ADMIN_ID, f"🆕 **বই রিকোয়েস্ট:**\n\nবই: {query}\nথেকে: {user.first_name}\nID: `{user.id}`", parse_mode="Markdown")
        await update.message.reply_text("✅ আপনার রিকোয়েস্টটি অ্যাডমিনের কাছে পাঠানো হয়েছে।")
        context.user_data['awaiting_request'] = False
        return

    # ৩. সাধারণ সার্চ
    encoded_query = urllib.parse.quote(query)
    keyboard = [
        [InlineKeyboardButton("📚 আমাদের লাইব্রেরি", url=f"https://t.me/s/shibir_online_library?q={encoded_query}")],
        [InlineKeyboardButton("🌐 পুরো টেলিগ্রাম", url=f"tg://search?text={encoded_query}")],
        [InlineKeyboardButton("🔍 গুগল (PDF) সার্চ", url=f"https://www.google.com/search?q=filetype:pdf+{encoded_query}+bangla")]
    ]
    await update.message.reply_text(f"🔎 **'{query}'** এর জন্য ফলাফল:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'request_book':
        await query.message.reply_text("বই ও লেখকের নাম লিখে মেসেজ দিন।")
        context.user_data['awaiting_request'] = True

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()
