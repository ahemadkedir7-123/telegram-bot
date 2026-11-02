import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "9020872784:AAEqaZG8HveIWtd23Qi9tRhNynUv-Glac-A"
FRIEND_CHAT_ID = 8865319773  # የጓደኛዎን የቻት ID እዚህ ያስገቡ


bot = Bot(token=TOKEN)
dp = Dispatcher()

user_mapping = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("ሰላም! መልእክትዎን የስቀምጡ።")

@dp.message()
async def forward_to_friend(message: types.Message):
    if message.from_user.id == FRIEND_CHAT_ID and message.reply_to_message:
        replied_msg_id = message.reply_to_message.message_id
        target_user_id = user_mapping.get(replied_msg_id)
        
        if target_user_id:
            try:
                if message.photo:
                    sent_msg = await bot.send_photo(chat_id=target_user_id, photo=message.photo[-1].file_id, caption=message.caption)
                elif message.video:
                    sent_msg = await bot.send_video(chat_id=target_user_id, video=message.video.file_id, caption=message.caption)
                elif message.sticker:
                    sent_msg = await bot.send_sticker(chat_id=target_user_id, sticker=message.sticker.file_id)
                elif message.voice:
                    sent_msg = await bot.send_voice(chat_id=target_user_id, voice=message.voice.file_id)
                elif message.audio:
                    sent_msg = await bot.send_audio(chat_id=target_user_id, audio=message.audio.file_id, caption=message.caption)
                elif message.document:
                    sent_msg = await bot.send_document(chat_id=target_user_id, document=message.document.file_id, caption=message.caption)
                else:
                    sent_msg = await bot.send_message(chat_id=target_user_id, text=message.text)
                
                user_mapping[sent_msg.message_id] = target_user_id
            except Exception as e:
                print(f"ስህተት: {e}")
        return

    user_id = message.from_user.id
    user_name = message.from_user.full_name

    try:
        if message.photo:
            sent_msg = await bot.send_photo(chat_id=FRIEND_CHAT_ID, photo=message.photo[-1].file_id, caption=message.caption or "", parse_mode="HTML")
        elif message.video:
            sent_msg = await bot.send_video(chat_id=FRIEND_CHAT_ID, video=message.video.file_id, caption=message.caption or "", parse_mode="HTML")
        elif message.sticker:
            await bot.send_message(chat_id=FRIEND_CHAT_ID, text=f"<b>{user_name}</b> (ስቲከር ልኳል)", parse_mode="HTML")
            sent_msg = await bot.send_sticker(chat_id=FRIEND_CHAT_ID, sticker=message.sticker.file_id)
        elif message.voice:
            sent_msg = await bot.send_voice(chat_id=FRIEND_CHAT_ID, voice=message.voice.file_id)
        elif message.audio:
            sent_msg = await bot.send_audio(chat_id=FRIEND_CHAT_ID, audio=message.audio.file_id, caption=message.caption or "", parse_mode="HTML")
        elif message.document:
            sent_msg = await bot.send_document(chat_id=FRIEND_CHAT_ID, document=message.document.file_id, caption=message.caption or "", parse_mode="HTML")
        else:
            sent_msg = await bot.send_message(chat_id=FRIEND_CHAT_ID, text=f"<b>{user_name}</b>\n{message.text}", parse_mode="HTML")
        
        if sent_msg:
            user_mapping[sent_msg.message_id] = user_id
            
    except Exception as e:
        print(f"ማስተላለፍ ስህተት: {e}")

# Render Web Service ፖርት እንዲያይ የሚያስችል ቀላል ድር ሰርቨር
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    print("ቦቱ በመስራት ላይ ነው...")
    # የድር ሰርቨሩን እና የቴሌግራም ፖሊንግ በአንድ ላይ እናስኬዳለን
    await asyncio.gather(web_server(), dp.start_polling(bot))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
