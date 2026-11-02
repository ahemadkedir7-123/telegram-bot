import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "9020872784:AAEqaZG8HveIWtd23Qi9tRhNynUv-Glac-A"
FRIEND_CHAT_ID = 8345797413  # የጓደኛዎን ትክክለኛ የቻት ID እዚህ ያስገቡ

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("ሰላም! መልእክትዎን የስቀምጡ!!")

@dp.message()
async def forward_to_friend(message: types.Message):
    # መልእክቱ የመጣው ከባለቤቱ (Friend) ከሆነ እና ሪፕላይ ከተደረገ
    if message.from_user.id == FRIEND_CHAT_ID and message.reply_to_message:
        replied_text = message.reply_to_message.text or message.reply_to_message.caption
        try:
            if replied_text and "👤 ከ:" in replied_text:
                # ከቀድሞው መልእክት ውስጥ የተጠቃሚውን ዩዘር 🆔 በድብቅ እንወስዳለን (ለስክሪኑ ንጽህና አይታይም)
                for line in replied_text.split("\n"):
                    if "🆔 ID:" in line:
                        target_user_id = int(line.split("🆔 ID:")[1].strip())
                        
                        # ፎቶ፣ ቪዲዮ፣ ዶክመንት ወይም የድምጽ መልእክት ከሆነ ፋይሉን እንልካለን
                        if message.photo:
                            await bot.send_photo(chat_id=target_user_id, photo=message.photo[-1].file_id, caption=message.caption)
                        elif message.video:
                            await bot.send_video(chat_id=target_user_id, video=message.video.file_id, caption=message.caption)
                        elif message.voice:
                            await bot.send_voice(chat_id=target_user_id, voice=message.voice.file_id)
                        elif message.audio:
                            await bot.send_audio(chat_id=target_user_id, audio=message.audio.file_id, caption=message.caption)
                        elif message.document:
                            await bot.send_document(chat_id=target_user_id, document=message.document.file_id, caption=message.caption)
                        else:
                            # የፅሁፍ መልእክት ከሆነ
                            await bot.send_message(chat_id=target_user_id, text=message.text)
                            
                        await message.reply("✅ መልእክቱ ተልኳል!")
                        return
        except Exception as e:
            print(f"Reply ስህተት: {e}")
        
        await message.answer("❌ መልእክቱን መላክ አልተቻለም። እባክዎ በትክክል Reply ያድርጉ።")
        return

    # ከተጠቃሚዎች የሚመጣ ማንኛውንም ነገር (ጽሁፍ፣ ፎቶ፣ ቮይስ፣ ወዘተ) ወደ ባለቤቱ ማስተላለፊያ
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_username = f"@{message.from_user.username}" if message.from_user.username else "ዩዘርናም የለውም"
    
    # ስክሪኑ እንዳይበላሽ ጽሁፉን አጠር እና ጥንቅቅ አድርገነዋል (ID በድብቅ ይያዛል)
    header_text = f"📩 <b>{user_name}</b> ({user_username})\n🆔 ID: {user_id}"

    try:
        if message.photo:
            await bot.send_photo(chat_id=FRIEND_CHAT_ID, photo=message.photo[-1].file_id, caption=f"{header_text}\n\n💬 {message.caption or ''}")
        elif message.video:
            await bot.send_video(chat_id=FRIEND_CHAT_ID, video=message.video.file_id, caption=f"{header_text}\n\n💬 {message.caption or ''}")
        elif message.voice:
            await bot.send_voice(chat_id=FRIEND_CHAT_ID, voice=message.voice.file_id, caption=header_text)
        elif message.audio:
            await bot.send_audio(chat_id=FRIEND_CHAT_ID, audio=message.audio.file_id, caption=f"{header_text}\n\n💬 {message.caption or ''}")
        elif message.document:
            await bot.send_document(chat_id=FRIEND_CHAT_ID, document=message.document.file_id, caption=f"{header_text}\n\n💬 {message.caption or ''}")
        else:
            # መደበኛ የፅሁፍ መልእክት
            full_text = f"{header_text}\n\n💬 <b>መልእክት:</b>\n{message.text}"
            await bot.send_message(chat_id=FRIEND_CHAT_ID, text=full_text, parse_mode="HTML")
    except Exception as e:
        print(f"ማስተላለፍ ስህተት: {e}")

async def main():
    print("ቦቱ በመስራት ላይ ነው...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
