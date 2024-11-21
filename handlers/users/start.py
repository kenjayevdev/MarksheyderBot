import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.keybordmenu import menu
from aiogram.types import ParseMode, Message
from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    try:
        db.add_user(id=message.from_user.id,
                    name=name)
    except sqlite3.IntegrityError as err:
    	pass
    
    await message.answer(f"*👋 Assalomu alaykum hurmatli* {message.from_user.full_name}\n\n🤖 *Bu bot karyer ma'lumotlarini hisoblash va tahlil qilish uchun dasturlandi. Quyida uning asosiy imkoniyatlari va foydalari keltirilgan:*\n\n*📌 Botning asosiy maqsadi:*\n- Karyerning o'lchovlari va parametrlari asosida hajm, qazib olinadigan material miqdori, yillik qazib olish hajmi kabi muhim ko'rsatkichlarni hisoblash.\n- Foydalanuvchilarga hisoblash natijalari bilan birga karyer hajmi grafigini taqdim etish.\n\n*⬇️ Marhamat kerakli menyuni tanlang ⬇️*",parse_mode=ParseMode.MARKDOWN,reply_markup=menu)
    count = db.count_users()[0]
    msg = f"*{message.from_user.full_name} 📇Bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor✅*"
    await bot.send_message(chat_id=ADMINS[0], text=msg,parse_mode=ParseMode.MARKDOWN)
    #await bot.send_message(chat_id=ADMINS[1], text=msg,parse_mode=ParseMode.MARKDOWN)