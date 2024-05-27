import logging
import sys
import asyncio
import os
from time import sleep

from aiogram import Bot, Dispatcher, html
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types
from aiogram import enums

from aiogram.types import ReplyKeyboardRemove

from keyboards.default.keyboards import keyboard

from dotenv import load_dotenv, dotenv_values
import quranly

load_dotenv()

# Tokenni "https://t.me/BotFather" shu yerdan oling.
BOT_TOKEN = os.getenv("BOT_TOKEN")

# dispatcher yarating
dp = Dispatcher()
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# start bot yarating
@dp.message(CommandStart())
async def start_bot(message: Message):
        text = f"Assalomu aleykum {html.bold(message.from_user.full_name)}\n\n"
        text += f"Hozir bot orqali faqat Quroni Karim oyatlari tafsiri bilan tanishib chiqishingiz mumkin !\n\n"
        text += f"Boshlash uchun pastdagi tugmani bosing yoki sura raqamini yuboring !"
       
        await message.answer(text, reply_markup=keyboard)
        
# Quran bot


@dp.message

# End Quran Bot


@dp.message(Command("info"))
async def info_bot(message: Message):
    # ? Get first_name of user
    first_name = message.from_user.first_name
    # ? Get user id
    user_id = message.from_user.id
    # ? Make general caption
    message_caption = "Ajoyib, keling siz haqingizda biroz ma'lumot beraman:\n\n"
    message_caption += f"{html.blockquote(f"Ismingiz: {first_name}")}\n"
    message_caption += f"{html.blockquote(f"Sizning ID: {html.code(user_id)}")}\n"
    if message.from_user.username:
        message_caption += f"{html.blockquote(f"Sizning username: {message.from_user.mention_html()}")}"
    # ? Send user photo and informations
    try:
        # ? GET user profile photo
        profile_pictures = await bot.get_user_profile_photos(message.from_user.id)
        await message.answer_photo(dict((profile_pictures.photos[0][0])).get("file_id"), caption=message_caption)
    except:
        await message.answer_photo("https://shorturl.at/VjGC3", caption=message_caption)

        

@dp.message()
async def echo_bot(message: Message):
    if message.text.isnumeric():
        if int(message.text) > 0:
            sura_id = int(message.text)
            sura = quranly.get_one_surah(sura=sura_id)
            audios = quranly.get_audio_of_sura(sura_id)
            suralar = quranly.get_surah_info()['names']
            sura_name = ""
            for i in range(len(suralar)):
                if i == sura_id:
                    this_sura = suralar[sura_id-1]
                    for key, item in this_sura.items():
                        sura_name += f"{html.underline(html.bold("Name of Surah"))}: {key}\n{html.underline(html.bold("Meaning"))}: {item}"
            await message.answer(sura_name)
            verse_id = 0
            for verse in sura:
                sleep(4)
                await bot.send_chat_action(chat_id=message.from_user.id, action=enums.ChatAction.UPLOAD_VOICE)
                await message.answer_audio(audio=audios[verse_id]['audio'], caption=html.blockquote(audios[verse_id]['text']))
                verse_id += 1
                sleep(4)
                await message.answer(verse)
        else:
            await message.answer("Siz yuborgan raqam yaroqsiz. 1 dan 114 gacha raqamlardan birini yuboring !...")
    else:
        if message.text == "BOSHLASH":
            res = quranly.get_surah_info()
            suralar = res['names']
            text2 = ""
            text3 = ""
            for index in range(round(len(suralar)/2)):
                sura = suralar[index]
                for key, item in sura.items():
                    text2 += f" {html.blockquote(f"{key} - {item}")}"
            for index in range(round(len(suralar)/2)+1,len(suralar)):
                sura = suralar[index]
                for key, item in sura.items():
                    text3 += f" {html.blockquote(f"{key} - {item}")}"
            await message.answer(text="Sura raqamini yuboring 1 dan 104 gacha.", reply_markup=ReplyKeyboardRemove())
            await bot.send_chat_action(chat_id=message.from_user.id, action=enums.ChatAction.TYPING)
            sleep(2)
            await message.answer(text2)
            sleep(1.5)
            await bot.send_chat_action(chat_id=message.from_user.id, action=enums.ChatAction.TYPING)
            sleep(1.5)
            await message.answer(text3)
        else:
            await message.send_copy(chat_id=message.from_user.id, reply_markup=ReplyKeyboardRemove())
            await message.answer("Bu raqam emas. Agar suraning tafsirini olmoqchi bo'lsangiz faqat butun son yuboring.(1 dan 114 gacha.)")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())