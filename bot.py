import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = "9020872784:AAEqaZG8HveIWtd23Qi9tRhNynUv-Glac-A"
FRIEND_CHAT_ID = 8345797413  # የጓደኛዎን የቻት ID እዚህ ያስገቡ

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ተጠቃሚዎችን ለመለየት State እንጠቀማለን
class ChatState(StatesGroup):
    waiting_for_reply = State()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("ሰላም! መልእክትዎን የስቀምጡ!")

@dp.message()
async def forward_to_friend(message: types.Message):
    # መልእክቱ የመጣው ከባለቤቱ (Friend) ከሆነ እና በቦቱ ላይ Reply የተደረገ ከሆነ
    if message.from_user.id == FRIEND_CHAT_ID and message.reply_to_message:
        replied_text = message.reply_to_message.text
        # ከተላከው መልእክት ውስጥ የተጠቃሚውን ዩዘርናም ወይም መታወቂያ እንፈልጋለን
        try:
            # ከቀድሞው መልእክት ውስጥ የዩዘር 🆔 ወይም ስም እንወስዳለን
            if "👤 ከ:" in replied_text:
                # ሪፕላይ የተደረገበትን ሰው ቻት አይዲ ለማግኘት እንሞክራለን
                lines = replied_text.split("\n")
                for line in lines:
                    if "ID:" in line:
                        target_user_id = int(line.split("ID:")[1].strip())
                        await bot.send_message(chat_id=target_user_id, text=message.text)
                        await message.reply("✅ መልእክቱ ለተጠቃሚው ተልኳል!")
                        return
        except Exception as e:
            print(f"Reply የማድረግ ስህተት: {e}")

        # መደበኛ ምላሽ መስጫ
        await message.answer("❌ መልእክቱን ለተጠቃሚው መላክ አልተቻለም። እባክዎ በትክክል Reply ያደርጉ።")
        return

    # ከተለመዱ ተጠቃሚዎች የሚመጣ መልእክት ወደ ባለቤቱ (Friend) መላኪያ
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_username = f"@{message.from_user.username}" if message.from_user.username else "ዩዘርናም የለውም"
    
    text = f"📩 አዲስ መልእክት መጥቷል!\n\n👤 ከ: {user_name} ({user_username})\n🆔 ID: {user_id}\n💬 መልእክት:\n{message.text}"
    
    try:
        await bot.send_message(chat_id=FRIEND_CHAT_ID, text=text)
    except Exception as e:
        print(f"ስህተት ተፈጥሯል: {e}")

async def main():
    print("ቦቱ በመስራት ላይ ነው...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
