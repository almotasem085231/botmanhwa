import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ✅ توكن البوت
TOKEN = "7167539511:AAHDb4Wb8ZSr9Wz4j0MXjKuSo1huxMT2Khc"

logging.basicConfig(level=logging.INFO)

# 🔎 البحث في موقع LekManga
def search_lekmanga(query):
    search_url = f"https://lekmanga.net/lek/?s={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        result = soup.select_one("h3.post-title a")
        if result:
            title = result.text.strip()
            link = result["href"]

            # جلب الصفحة الخاصة بالمانهوا للحصول على التصنيفات
            page = requests.get(link, headers=headers, timeout=10)
            page_soup = BeautifulSoup(page.text, "html.parser")
            genres = page_soup.select(".genres a")

            if genres:
                genre_list = [g.text.strip() for g in genres]
                genres_text = "، ".join(genre_list)
            else:
                genres_text = "غير محددة"

            return f"""🔹 <b>LekManga</b>:
📖 <b>{title}</b>
📚 <b>التصنيفات:</b> {genres_text}
🔗 <a href="{link}">رابط المانهوا</a>"""
        else:
            return "🔹 <b>LekManga</b>: لا يوجد نتائج."

    except Exception:
        return "🔹 <b>LekManga</b>: حدث خطأ أثناء البحث."

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل اسم المانهوا التي تريد البحث عنها 🔍")

# الرسائل العادية (اسم المانهوا)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_html(f"⏳ يتم البحث عن:\n<b>{query}</b>")
    result = search_lekmanga(query)
    await update.message.reply_html(result, disable_web_page_preview=True)

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()
