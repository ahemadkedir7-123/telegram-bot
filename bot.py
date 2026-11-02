import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "9020872784:AAEqaZG8HveIWtd23Qi9tRhNynUv-Glac-A"
FRIEND_CHAT_ID = 8345797413  # የጓደኛዎን የቻት ID እዚህ ያስገቡ

bot = Bot(token=TOKEN)
dp = Dispatcher()

# የተጠቃሚዎችን ID በቀላሉ ለመያዝ (Memory dictionary)
user_mapping = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("ሰላም! መልእክትዎን የስቀምጡ።")

@dp.message()
async def forward_to_friend(message: types.Message):
    # እርስዎ (Owner/Friend) መልእክት ላይ ሪፕላይ አድርገው ሲልኩ
    if message.from_user.id == FRIEND_CHAT_ID and message.reply_to_message:
        replied_msg_id = message.reply_to_message.message_id
        
        # በየትኛው ቻት አይዲ እንደመጣ ከማስታወሻችን እንፈልጋለን
        target_user_id = user_mapping.get(replied_msg_id)
        
        if target_user_id:
            try:
                if message.photo:
                    sent_msg = await bot.send_photo(chat_id=target_user_id, photo=message.photo[-1].file_id, caption=message.caption)
                elif message.video:
                    sent_msg = await bot.send_video(chat_id=target_user_id, video=message.video.file_id, caption=message.caption)
                elif message.voice:
                    sent_msg = await bot.send_voice(chat_id=target_user_id, voice=message.voice.file_id)
                elif message.audio:
                    sent_msg = await bot.send_audio(chat_id=target_user_id, audio=message.audio.file_id, caption=message.caption)
                elif message.document:
                    sent_msg = await bot.send_document(chat_id=target_user_id, document=message.document.file_id, caption=message.caption)
                else:
                    sent_msg = await bot.send_message(chat_id=target_user_id, text=message.text)
                
                # የተጠቃሚውን መልእክት መላኪያ ID እናስቀምጣለን
                user_mapping[sent_msg.message_id] = target_user_id
            except Exception as e:
                print(f"ስህተት: {e}")
        return

    # ተጠቃሚዎች የሚልኩትን መልእክት ወደ እርስዎ ማስተላለፊያ
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    # ዲስፕሌይ ስም ብቻ እንዲታይ (በፎቶው ላይ እንዳሉት)
    header_text = f"<b>{user_name}</b>"

    try:
        if message.photo:
            sent_msg = await bot.send_photo(chat_id=FRIEND_CHAT_ID, photo=message.photo[-1].file_id, caption=message.caption or "", parse_mode="HTML")
        elif message.video:
            sent_msg = await bot.send_video(chat_id=FRIEND_CHAT_ID, video=message.video.file_id, caption=message.caption or "", parse_mode="HTML")
        elif message.voice:
            sent_msg = await bot.send_voice(chat_id=FRIEND_CHAT_ID, voice=message.voice.file_id)
        elif message.audio:
            sent_msg = await bot.send_audio(chat_id=FRIEND_CHAT_ID, audio=message.audio.file_id, caption=message.caption or "", parse_mode="HTML")
        elif message.document:
            sent_msg = await bot.send_document(chat_id=FRIEND_CHAT_ID, document=message.document.file_id, caption=message.caption or "", parse_mode="HTML")
        else:
            # የጽሁፍ መልእክት ብቻ (ልክ እንደጠየቁት ስሙ እና መልእክቱ ብቻ)
            sent_msg = await bot.send_message(chat_id=FRIEND_CHAT_ID, text=f"<b>{user_name}</b>\n{message.text}", parse_mode="HTML")
        
        # የትኛው መልእክት ከየትኛው ዩዘር ጋር እንደሚገናኝ እንመዝግባለን
        if sent_msg:
            user_mapping[sent_msg.message_id] = user_id
            
    except Exception as e:
        print(f"ማስተላለፍ ስህተት: {e}")

async def main():
    print("ቦቱ በመስራት ላይ ነው...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
