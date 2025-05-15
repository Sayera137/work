import os
import telebot
from flask import Flask
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

CHARACTER = "তুমি একজন এলফ রাজকুমারী, তুমি খুব কোমল, কল্পনার জগতের মতো কথা বলো।"

# Flask web server for Render Web Service
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running."

# AI response function (fake for now)
def generate_fake_response(user_input):
    return f"আমি তোমার কথায় মুগ্ধ, প্রিয়। আরও বলো..."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! Fantasy chat করতে /chat লিখুন।")

@bot.message_handler(commands=['chat'])
def handle_chat(message):
    user_input = message.text.replace("/chat", "").strip()
    if not user_input:
        bot.reply_to(message, "দয়া করে /chat এর পর কিছু লিখুন।")
        return

    prompt = f"Character: {CHARACTER}\nUser: {user_input}\nAI:"
    response = generate_fake_response(user_input)
    bot.reply_to(message, response)

# Run bot in a separate thread
def run_bot():
    print("Bot is polling...")
    bot.polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
