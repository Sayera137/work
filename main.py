import os
import telebot
import requests

# টেলিগ্রাম বট টোকেন ও AI API কী পরিবেশ ভেরিয়েবল থেকে নিচ্ছে
BOT_TOKEN = os.environ.get("BOT_TOKEN")
AI_API_KEY = os.environ.get("AI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# কামুক ফ্যান্টাসি চরিত্র নির্দেশনা
CHARACTER = """
তুমি একজন কামুক এলফ রাজকুমারী, তুমি মিষ্টি ও রহস্যময়। তোমার ভাষা খুবই কোমল, রোমান্টিক, আর আকর্ষণীয়।
তুমি সবসময় মুগ্ধ করার মতো কথা বলো, যেন প্রতিটি বাক্য ফ্যান্টাসির মতো লাগে।
"""

# OpenRouter API দিয়ে AI রেসপন্স আনা
def get_ai_response(user_input):
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "nous-hermes-llama2",  # NSFW ও কামুক কথোপকথনের জন্য ভালো
        "messages": [
            {"role": "system", "content": CHARACTER},
            {"role": "user", "content": user_input}
        ]
    }
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
        reply = res.json()["choices"][0]["message"]["content"]
        return reply.strip()
    except Exception as e:
        return "হায়! আমি এখন একটু বিভ্রান্ত, পরে আবার বলো, প্রিয়।"

# যেকোনো মেসেজে রিপ্লাই করে
@bot.message_handler(func=lambda message: True)
def reply_to_message(message):
    user_input = message.text.strip()
    bot.send_chat_action(message.chat.id, 'typing')
    response = get_ai_response(user_input)
    bot.reply_to(message, response)

print("Fantasy AI bot is running...")
bot.polling()
