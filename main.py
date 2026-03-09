import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from fuzzywuzzy import process

# Bot token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")

# Function to load books from txt file
def load_books():
    book_dict = {}
    try:
        with open("books.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line:
                    name, link = line.strip().split("|")
                    book_dict[name] = link
    except FileNotFoundError:
        print("Error: books.txt file not found!")
    return book_dict

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "আসসালামু আলাইকুম।\n"
        "বইয়ের নাম লিখে সার্চ করুন। আমি আপনাকে PDF লিঙ্ক খুঁজে দেব।\n\n"
        "যেমন: কর্মী সিলেবাস"
    )

# Search function
async def search_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        return

    # Reload books every time to get new updates from txt file
    all_books = load_books()
    
    # Fuzzy search logic
    matches = process.extract(query, all_books.keys(), limit=5)
    results = [m for m in matches if m[1] >= 50] # Similarity score 50%

    if results:
        for name, score in results:
            link = all_books[name]
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("📖 বইপিডিএফ দেখুন", url=link)]])
            await update.message.reply_text(f"📚 {name}", reply_markup=kb)
    else:
        await update.message.reply_text("দুঃখিত, এই নামে কোনো বই খুঁজে পাওয়া যায়নি। সঠিক নাম লিখে চেষ্টা করুন।")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN not found in environment variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_book))
        print("Bot is running with txt database...")
        app.run_polling()
