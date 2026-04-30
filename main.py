import os
import asyncio
import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread

# --- 1. سيرفر الويب لـ Render ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- 2. إعدادات البوت ---
ALLOWED_USER_ID = 1358008461522108416
TOKEN = "MTQ5OTMzNTIzMzgxNDc5MDI0NA.G1V0Nu.FG1hQQ8OoN0-4CkHclvZ31bY1aobOIXtDhXYRA"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- أمر البث (Broadcast) ---
@bot.command()
async def bc(ctx, *, message: str):
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("❌ ما عندك صلاحية.")
        return

    await ctx.send("🚀 جاري البدء بالإرسال...")  

    success = 0  
    failed = 0  
    members = [m for m in ctx.guild.members if not m.bot]  
    total = len(members)  

    for i in range(0, total, 10):  
        batch = members[i:i+10]
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

# --- 3. التشغيل ---
if __name__ == "__main__":
    keep_alive()
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"⚠️ خطأ: {e}")
      
