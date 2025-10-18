from pyrogram import Client, filters
import subprocess
import os

# ضع التوكن هنا بعد التحميل
BOT_TOKEN = "8336417843:AAHU9GYRBD_2rV8pTJngYdUZLzRCiQLdWYg"
API_ID = 1234567  # من my.telegram.org
API_HASH = "YOUR_API_HASH_HERE"

OWNER_ID = 8414665703  # معرف المطور
CREDITS = "@z_t_t_j"

bot = Client(
    "python_host_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        f"👋 أهلاً {message.from_user.first_name}!\n"
        f"أنا بوت استضافة وتشغيل ملفات بايثون.\n"
        f"أرسل لي ملف Python (.py) وسأقوم بتشغيله لك 🔥\n\n"
        f"حقوق: {CREDITS}"
    )

@bot.on_message(filters.document & filters.private)
async def run_python_file(_, message):
    file = await message.download()
    if not file.endswith(".py"):
        await message.reply_text("📁 أرسل فقط ملفات Python (.py)")
        os.remove(file)
        return

    await message.reply_text("⚙️ جاري تشغيل الملف...")

    try:
        result = subprocess.run(
            ["python3", file],
            capture_output=True,
            text=True,
            timeout=15
        )
        output = result.stdout or result.stderr
        if len(output) > 4000:
            with open("output.txt", "w") as f:
                f.write(output)
            await message.reply_document("output.txt", caption="📄 ناتج التنفيذ")
            os.remove("output.txt")
        else:
            await message.reply_text(f"✅ النتيجة:\n```\n{output}\n```", quote=True)
    except subprocess.TimeoutExpired:
        await message.reply_text("⏱️ انتهى الوقت! الملف أخذ وقتًا طويلًا للتنفيذ.")
    except Exception as e:
        await message.reply_text(f"❌ خطأ أثناء التشغيل:\n`{e}`")

    os.remove(file)

@bot.on_message(filters.command("owner"))
async def owner(_, message):
    await message.reply_text(f"👑 المطور: {CREDITS}\n🆔 {OWNER_ID}")

print("✅ البوت يعمل الآن ...")
bot.run()
