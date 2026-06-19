import telebot
import google.generativeai as genai
import os

# Telegram Bot Tokenin
TELEGRAM_TOKEN = "8620051118:AAH59PC86q3yv--9SFHnue7q6ejEb0xLIf0"

# Gemini API Açarın (Bunu aistudio.google.com-dan alıb aşağıya yapışdır)
GEMINI_API_KEY = "8620051118:AAH59PC86q3yv--9SFHnue7q6ejEb0xLIf0"


bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Bir xəta baş verdi: " + str(e))

bot.polling()
