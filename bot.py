import os
import telebot
import requests
from flask import Flask
from threading import Thread

# سيرفر صغير لإبقاء البوت حياً على Render
app = Flask('')
@app.route('/')
def home(): return "I'm alive!"

def run(): app.run(host='0.0.0.0', port=8080)

# بياناتك الخاصة
TOKEN = "8759282929:AAFKcbklqSOHX_MIF5zluvyr0o7-PZebAqI"
HF_TOKEN = "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"

bot = telebot.TeleBot(TOKEN)

def get_ai_reply(msg):
    url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "x-wait-for-model": "true"}
    system = "أنت مساعد ذكي، منطقي، ومثقف. تجيب بدقة ولباقة."
    prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{msg}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    try:
        r = requests.post(url, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 500}}, timeout=20)
        return r.json()[0]['generated_text'].split("assistant")[-1].strip()
    except: return "أهلاً! أنا ذكاء اصطناعي، كيف أساعدك؟"

@bot.business_message_handler(func=lambda m: True)
def handle(m):
    if m.from_user.id == bot.get_me().id: return
    reply = get_ai_reply(m.text)
    if reply:
        bot.send_message(m.chat.id, reply, business_connection_id=m.business_connection_id)

if __name__ == "__main__":
    Thread(target=run).start()
    print("الذكاء الاصطناعي يعمل...")
    bot.infinity_polling()
