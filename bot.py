import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from downloader import download_video, download_audio

BOT_TOKEN = os.getenv("8612057206:AAFmZaXijTtP5eSbOiZy-YiowwgFCjhW_a4")

url_pattern = re.compile(r'https?://\S+')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    urls = url_pattern.findall(text)

    if not urls:
        return

    url = urls[0]
    context.user_data["url"] = url

    keyboard = [
        [InlineKeyboardButton("HD Video", callback_data="hd")],
        [InlineKeyboardButton("SD Video", callback_data="sd")],
        [InlineKeyboardButton("Audio", callback_data="audio")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Choose download type:",
        reply_markup=reply_markup
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    url = context.user_data.get("url")

    await query.edit_message_text("Downloading...")

    if query.data == "audio":
        file_path = download_audio(url)

    elif query.data == "sd":
        file_path = download_video(url, quality="sd")

    else:
        file_path = download_video(url, quality="hd")

    if not file_path:
        await query.message.reply_text("Download failed.")
        return

    try:
        await query.message.reply_video(video=open(file_path, "rb"))
    except:
        await query.message.reply_document(document=open(file_path, "rb"))

    os.remove(file_path)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.add_handler(CallbackQueryHandler(button_click))

app.run_polling()