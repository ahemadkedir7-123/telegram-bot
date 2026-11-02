import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "9264749757:AAGfIyXpU79XHbGdFiDr_zWAJrTVx99-3kM"
 # የቦቱን ቶከን እዚህ ያስገቡ
FRIEND_CHAT_ID = 8345797413
 # የጓደኛዎን Chat ID እዚህ ያስገቡ

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
await message.answer("ሰላም! መልእክትዎን ለባለቤቱ ልኬዋለሁ። በተቻለ ፍጥነት ይመልስልዎታል!")

@dp.message()
async def forward_to_friend(message: types.Message):
user_name = message.from_user.full_name
user_username = f"@{message.from_user.username}" if message.from_user.username else "ዩዘርናም የለውም"

text = f"📩 አዲስ መልእክት መጥቷል!\n\n👤 ከ: {user_name} ({user_username})\n💬 መልእክት:\n{message.text}"

try:
await bot.send_message(chat_id=FRIEND_CHAT_ID, text=text)
except Exception as e:
print(f"ስህተት ተፈጥሯል: {e}")

async def main():
print("ቦቱ በመስራት ላይ ነው...")
await dp.start_polling(bot)

if name == "main":
logging.basicConfig(level=logging.INFO)
asyncio.run(main())


