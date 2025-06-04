import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# ✅ التوكن الخاص بك
token = "7167539511:AAHDb4Wb8ZSr9Wz4j0MXjKuSo1huxMT2Khc"

# التصنيفات
CATEGORIES = [
    "أكشن", "رومانسي", "مدرسي", "كوميدي", "دراما",
    "خيال", "مغامرات", "إثارة", "غموض", "فنون قتالية"
]

# إعداد اللوج
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# أزرار التصنيفات
def category_keyboard():
    buttons = [[InlineKeyboardButton(cat, callback_data=f"cat:{cat}")] for cat in CATEGORIES]
    return InlineKeyboardMarkup(buttons)

# البحث في المواقع
def search_manhwa(query):
    results = []

    sites = {
        "Mangalek": f"https://mangalek.net/?s={query}",
        "ArabManga": f"https://arab-manga.com/?s={query}",
        "MangaSwat": f"https://mangaswat.com/?s={query}",
        "AreaScan": f"https://areascans.com/?s={query}"
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    for name, url in sites.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            first_link = soup.find("a", href=True)
            if first_link:
                results.append(f"🔹 <b>{name}</b>: <a href='{first_link['href']}'>رابط</a>")
            else:
                results.append(f"🔹 <b>{name}</b>: لا يوجد نتائج.")
        except Exception:
            results.append(f"🔹 <b>{name}</b>: خطأ أثناء البحث.")

    return "\n".join(results)

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل اسم المانهوا التي تريد البحث عنها 🔍", reply_markup=category_keyboard())

# رسالة البحث
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_html("⏳ يتم البحث عن:\n<b>{}</b>".format(query))
    result = search_manhwa(query)
    await update.message.reply_html(result, disable_web_page_preview=True)

# عند الضغط على تصنيف
async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.split(":")[1]
    await query.message.reply_text(f"أرسل اسم مانهوا من تصنيف: {category} 📚")

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_category, pattern="^cat:"))

    print("✅ Bot is running...")
    app.run_polling()
