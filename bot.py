import telebot
import os
from gtts import gTTS
from telebot import types
import google.generativeai as genai

# Mühit dəyişənlərindən tokenləri oxuyuruq
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# İstifadəçi mətnlərini yadda saxlamaq üçün lüğət
user_texts = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salam! Mənə bir mövzu yaz (şeir, mərsiyə), mən onu hazırlayım.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        text_content = response.text
        
        # Mətni həmin istifadəçinin ID-si ilə yadda saxlayırıq
        user_texts[message.chat.id] = text_content
        
        # "MP3 kimi göndər" düyməsini yaradırıq
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("MP3 kimi göndər", callback_data="audio")
        markup.add(btn)
        
        bot.send_message(message.chat.id, text_content, reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"Xəta baş verdi: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data == "audio")
def callback_query(call):
    chat_id = call.message.chat.id
    if chat_id in user_texts:
        text = user_texts[chat_id]
        tts = gTTS(text=text, lang='az')
        filename = f"audio_{chat_id}.mp3"
        tts.save(filename)
        with open(filename, 'rb') as audio:
            bot.send_audio(chat_id, audio)
        os.remove(filename) # İş bitəndə faylı silirik
    else:
        bot.answer_callback_query(call.id, "Əvvəlcə mətn yaratmalısan!")

bot.polling()
