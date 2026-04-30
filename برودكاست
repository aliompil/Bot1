import os
import sys
import asyncio
import discord
from discord.ext import commands, tasks

# --- إعدادات البوت ---
# آيديك الوحيد الذي يمكنه استخدام الأمر
ALLOWED_USER_ID = 1358008461522108416
# التوكن الخاص بك
TOKEN = "MTQ5OTMzNTIzMzgxNDc5MDI0NA.GSXzO2.Va4zsiiHBlu3sPuOZ72JJiIjeOWlydRMZCFdys"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- أمر البث السريع (Broadcast) ---
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
            if isinstance(res, discord.HTTPException) or isinstance(res, Exception):
                failed += 1
            else:
                success += 1
        
        await asyncio.sleep(1.5)  # وقت أمان لتجنب حظر ديسكورد

    await ctx.send(f"✅ تم الانتهاء:\n👥 الإجمالي: {total}\n✅ نجح: {success}\n❌ فشل: {failed}")

# --- ميزة الحفاظ على التشغيل ---
@tasks.loop(minutes=5)
async def keep_alive_log():
    print("💡 البوت مستمر في العمل بدون توقف...")

@bot.event
async def on_ready():
    print(f"✅ سجل الدخول باسم: {bot.user}")
    if not keep_alive_log.is_running():
        keep_alive_log.start()

# --- تشغيل البوت ---
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"⚠️ خطأ: {e}")
