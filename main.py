import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# .env fayldan tokenni o'qish
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Loggingni sozlash
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Vaqtinchalik soxta baza (Kelgusida buni Supabase yoki PostgreSQL bilan almashtirasiz)
MOCK_DATABASE = {
    "7241299350": {
        "username": "namuna_user",
        "groups_count": 5,
        "last_activity": "2026-09-27 12:00",
        "status": "Faol"
    }
}

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Assalomu alaykum! Botga Telegram ID yuboring, men bazadan o'sha ID bo'yicha ma'lumotlarni qidirib topaman."
    )

@dp.message(F.text.isdigit())
async def search_by_id(message: Message):
    user_id = message.text
    
    # Bazadan qidirish
    user_data = MOCK_DATABASE.get(user_id)
    
    if user_data:
        response_text = (
            f"🔍 **Topilgan ma'lumot:**\n\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"👤 **Username:** @{user_data['username']}\n"
            f"📊 **Qatnashgan guruhlar:** {user_data['groups_count']} ta\n"
            f"⏰ **Oxirgi faollik:** {user_data['last_activity']}\n"
            f"🟢 **Holati:** {user_data['status']}"
        )
    else:
        response_text = f"❌ `ID: {user_id}` bo'yicha bazada hech qanday ma'lumot topilmadi."
        
    await message.answer(response_text, parse_mode="Markdown")

@dp.message()
async def incorrect_input(message: Message):
    await message.answer("Iltimos, faqat raqamli **Telegram ID** kiriting (masalan: `7241299350`).")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
