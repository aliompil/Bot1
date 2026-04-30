import os
import asyncio
import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread

# --- 1. إعداد سيرفر الويب (ضروري جداً لـ Render) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run_flask():
    # هنا استخدمنا PORT النظام الذي يطلبه Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- 2. إعدادات البوت ---
ALLOWED_USER_ID = 1358008461522108416
TOKEN = "MTQ5OTMzNTIzMzgxNDc5MDI0NA.GSXzO2.Va4zsiiHBlu3sPuOZ72JJiIjeOWlydRMZCFdys"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def bc(ctx, *, message: str):
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("❌ ما عندك صلاحية.")
        return

    await ctx.send("🚀 جاري البدء بالإرسال السريع...")  

    success = 0  
    failed = 0  
    members = [m for m in ctx.guild.members if not m.bot]  
    total = len(members)  

    batch_size = 10  
    for i in range(0, total, batch_size):  
        batch = members[i:i+batch_size]
        tasks_list = [member.send(message) for member in batch]
        
        results = await asyncio.gather(*tasks_list, return_exceptions=True)
        
        for res in results:
            if isinstance(res, (discord.HTTPException, Exception)):
                failed += 1
            else:
                success += 1
        
        await asyncio.sleep(1.5)

    await ctx.send(f"✅ تم الانتهاء:\n👥 الإجمالي: {total}\n✅ نجح: {success}\n❌ فشل: {failed}")

@bot.event
async def on_ready():
    print(f"✅ سجل الدخول باسم: {bot.user}")

# --- 3. تشغيل سيرفر الويب ثم البوت ---
if __name__ == "__main__":
    keep_alive()  # تشغيل Flask في الخلفية
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"⚠️ خطأ: {e}")
      
