
import telebot, os, google.generativeai as genai
from flask import Flask
from threading import Thread
from telebot import types
from elevenlabs.client import ElevenLabs

TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

app = Flask(__name__)
@app.route('/')
def home(): return "Bot aktivdir!"

# Səs ID-ləri (Bura ElevenLabs-dan götürdüyün ID-ləri yaz)
voices = {
    "Qız1": "ID1", "Qız2": "ID2", "Qız3": "ID3", "Qız4": "ID4", "Qız5": "ID5",
    "Oğlan1": "ID6", "Oğlan2": "ID7", "Oğlan3": "ID8", "Oğlan4": "ID9", "Oğlan5": "ID10"
}

user_texts = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if "şeir" in message.text.lower(): prompt = f"Şeir yaz: {message.text}"
    elif "mərsiyə" in message.text.lower(): prompt = f"Mərsiyə yaz: {message.text}"
    elif "mahnı" in message.text.lower(): prompt = f"Mahnı sözləri yaz: {message.text}"
    else: prompt = message.text
    
    response = model.generate_content(prompt)
    user_texts[message.chat.id] = response.text
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    for name in voices.keys():
        markup.add(types.InlineKeyboardButton(name, callback_data=name))
    markup.add(types.InlineKeyboardButton("Duet", callback_data="duet"))
    
    bot.send_message(message.chat.id, f"Mətn hazırdır:\n\n{response.text}\n\nSəs seçin:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "duet":
        bot.answer_callback_query(call.id, "Duet funksiyası aktivdir.")
    else:
        bot.answer_callback_query(call.id, f"{call.data} ilə oxunur...")
        audio = client.generate(text=user_texts[call.message.chat.id], voice=voices[call.data])
        bot.send_audio(call.message.chat.id, audio)

if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

    # bot.polling()
