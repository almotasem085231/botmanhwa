import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# توكن البوت
TOKEN = "7167539511:AAHDb4Wb8ZSr9Wz4j0MXjKuSo1huxMT2Khc"

# التصنيفات (إضافية)
CATEGORIES = [
    "أكشن", "رومانسي", "مدرسي", "كوميدي", "دراما",
    "خيال", "مغامرات", "إثارة", "غموض", "فنون قتالية"
]

logging.basicConfig(level=logging.INFO)

# أزرار التصنيفات
def category_keyboard():
    buttons = [[InlineKeyboardButton(cat, callback_data=f"cat:{cat}")] for cat in CATEGORIES]
    return InlineKeyboardMarkup(buttons)

# 🔎 البحث في LekManga فقط
def search_lekmanga(query):
    search_url = f"https://lekmanga.net/lek/?s={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.select("h3.post-title a")
        if results:
            first = results[0]
            title = first.text.strip()
            link = first["href"]
            return f"🔹 <b>LekManga</b>:\n📖 {title}\n🔗 <a href='{link}'>رابط</a>"
        else:
            return "🔹 <b>LekManga</b>: لا يوجد نتائج."
    except Exception as e:
        return "🔹 <b>LekManga</b>: حدث خطأ أثناء البحث."

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل اسم المانهوا التي تريد البحث عنها 🔍", reply_markup=category_keyboard())

# عند إرسال اسم
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_html(f"⏳ يتم البحث عن:\n<b>{query}</b>")
    result = search_lekmanga(query)
    await update.message.reply_html(result, disable_web_page_preview=True)

# عند الضغط على تصنيف
async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.split(":")[1]
    await query.message.reply_text(f"أرسل اسم مانهوا من تصنيف: {category} 📚")

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_category, pattern="^cat:"))

    print("✅ Bot is running...")
    app.run_polling()
