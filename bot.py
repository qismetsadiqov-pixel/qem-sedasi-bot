import telebot
import os
from gtts import gTTS
from telebot import types
import google.generativeai as genai

# Açarın gizli olması üçün mühit dəyişənlərindən oxuyuruq
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        text_content = response.text
        bot.reply_to(message, text_content)
        
        # Səs faylı yaratmaq üçün düymə
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("MP3 kimi göndər", callback_data="audio")
        markup.add(btn)
        
        bot.last_text = text_content
        bot.send_message(message.chat.id, "Səsli dinləmək istəyirsiniz?", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, "Xəta: " + str(e))

@bot.callback_query_handler(func=lambda call: call.data == "audio")
def callback_query(call):
    tts = gTTS(text=bot.last_text, lang='az')
    tts.save("ses.mp3")
    with open("ses.mp3", "rb") as audio:
        bot.send_audio(call.message.chat.id, audio)
    os.remove("ses.mp3")

bot.polling()
