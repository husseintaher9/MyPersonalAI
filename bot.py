import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# سيرفر Render الصغير
app = Flask('')
@app.route('/')
def home(): return "AI Iraqi Bot is Live!"

def run(): app.run(host='0.0.0.0', port=8080)

# --- المعلومات الخاصة بك ---
TELEGRAM_TOKEN = "8759282929:AAFKcbklqSOHX_MIF5zluvyr0o7-PZebAqI"
GROQ_API_KEY = "هنا_حط_كود_الـ_gsk_الذي_نسخته"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

def get_ai_reply(user_message):
    try:
        # هنا نعطي التعليمات للهجة العراقية والمنطق
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "أنت مساعد ذكي ومنطقي جداً. جاوب على كل الأسئلة بذكاء وباللهجة العراقية (بغدادية) حصراً، خلي كلامك قريب للقلب ومفيد كأنك صديق عراقي حكيم."
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "والله يا غالي حالياً عندي ضغط، ثواني وارجعلك!"

@bot.business_message_handler(func=lambda message: True)
def handle_business_message(message):
    if message.from_user.id == bot.get_me().id:
        return
    
    user_text = message.text
    if user_text:
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            reply = get_ai_reply(user_text)
            
            bot.send_message(
                message.chat.id, 
                reply, 
                business_connection_id=message.business_connection_id
            )
        except:
            pass

if __name__ == "__main__":
    Thread(target=run).start()
    print("البوت العراقي المنطقي يعمل الآن...")
    bot.infinity_polling()
