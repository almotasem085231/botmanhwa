import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# تحميل المتغيرات من ملف .env
load_dotenv()
token = os.environ.get("BOT_TOKEN")

# دوال البحث (ترجع tuple: (نص، رابط الصورة))
def search_mangalek(query):
    url = f"https://mangalek.com/?s={query}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find('div', class_='bsx')
    if result:
        title = result.find('a')['title']
        link = result.find('a')['href']
        img = result.find('img')['src']
        text = f"📚 {title}\n🔗 {link}"
        return (text, img)
    return None

def search_arabmanga(query):
    url = f"https://arabmanga.net/?s={query}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find('div', class_='utao styletwo')
    if result:
        title = result.find('a')['title']
        link = result.find('a')['href']
        img = result.find('img')['src']
        text = f"📚 {title}\n🔗 {link}"
        return (text, img)
    return None

def search_mangaswat(query):
    url = f"https://mangaswat.com/?s={query}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find('div', class_='bs')
    if result:
        title = result.find('a')['title']
        link = result.find('a')['href']
        img = result.find('img')['src']
        text = f"📚 {title}\n🔗 {link}"
        return (text, img)
    return None

def search_areascans(query):
    url = f"https://areascans.net/?s={query}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find('div', class_='bsx')
    if result:
        title = result.find('a')['title']
        link = result.find('a')['href']
        img = result.find('img')['src']
        text = f"📚 {title}\n🔗 {link}"
        return (text, img)
    return None

def search_all_sites(query):
    results = []
    for func in [search_mangalek, search_arabmanga, search_mangaswat, search_areascans]:
        try:
            result = func(query)
            if result:
                results.append(result)
        except:
            continue
    return results if results else [("🚫 لم يتم العثور على نتائج.", None)]

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً! أرسل اسم مانهوا للبحث أو استخدم /categories لاختيار تصنيف.")

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚔️ أكشن", callback_data='genre_action')],
        [InlineKeyboardButton("💘 رومانسي", callback_data='genre_romance')],
        [InlineKeyboardButton("🧙‍♂️ خيالي", callback_data='genre_fantasy')],
        [InlineKeyboardButton("🎭 دراما", callback_data='genre_drama')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📂 اختر تصنيفًا:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    genre = query.data.split('_')[1]
    await query.edit_message_text(text=f"📌 تم اختيار التصنيف: {genre} (ميزة التصفية حسب التصنيف تحت التطوير)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("🔍 جاري البحث...")
    results = search_all_sites(query)
    for text, img_url in results:
        if img_url:
            await update.message.reply_photo(photo=img_url, caption=text)
        else:
            await update.message.reply_text(text)

# تشغيل البوت
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("categories", categories))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()