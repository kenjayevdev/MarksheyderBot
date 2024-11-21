import asyncio
from aiogram.dispatcher import FSMContext
from keyboards.default.keybordmenu import menu
from states.stett import PersonalData
from aiogram import types
from keyboards.default.adminKeyboard import panel, bekor 
from data.config import ADMINS
from loader import dp, db, bot
import datetime
import pytz

@dp.message_handler(text= "Orqaga🔜",state=PersonalData.adss,user_id=ADMINS)
async def enter_exiit(message:
	types.Message, state: FSMContext):
	await state.finish()
	await message.answer("<b>📨 Xabar Yuborish Bekor Qilindi 🚫</b>",reply_markup=panel)
	
@dp.message_handler(text = "/panel", user_id=ADMINS)
async def admin_panel(message:
	types.Message):
		await message.answer(f"<b>🤖Assalomu Alaykum Xurmatli {message.from_user.full_name}\n\n👤Admin Panelga Xush Kelibsiz\n🎗Kerakli Tugmani Tanlang✅</b>",reply_markup=panel)
		
@dp.message_handler(text="👤 ALL USERS", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    await message.answer(users)

@dp.message_handler(text="📨 SEND MSG", user_id=ADMINS)
async def enter_texto(message: types.Message):
    await message.answer("<b>🤖 Ushbu bo'lim orqali botdagi Barcha Foydalanuvchilarga 📬 Xabar Yuborishingiz Mumkun✅</b>",reply_markup=bekor)
    await PersonalData.adss.set()


@dp.message_handler(user_id = ADMINS,state=PersonalData.adss,content_types=types.ContentType.ANY)
async def send_message_users(message:
	types.Message,state: FSMContext):
	await state.finish()
	await message.answer("<i>🗞 Xabar Yuborilmoqda....</i>")
	n = 0
	for i in db.get_users_id():
		user_id = i[0]
		try:
			await message.send_copy(chat_id = user_id)
			n+=1
		except:
			pass
		await asyncio.sleep(0.3)
	await message.answer(f"<b>📲 Xabar {n} ta foydalanuvchiga muafaqiyatli yuborildi ✅</b>",reply_markup=panel)

@dp.message_handler(text='🤖BOT STATISTIKASI📊',user_id=ADMINS)
async def send_usd(message:
	types.Message):
		utc_now = pytz.utc.localize(datetime.datetime.utcnow())
		pst_now = utc_now.astimezone(pytz.timezone("Asia/Tashkent"))
		dt_string = pst_now.strftime("<i>%d.%m.%Y-YIL</i>\n<b>⏰ Soat 👉</b> <i>%H:%M:%S</i>")
		count = db.count_users()[0]
		msg = f"<b>🤖 BOT STATISTIKASI 📊\n\n📆 Bugun 👉</b> {dt_string}\n👥 <b>Barcha Obunachilar =</b> <i>{count} ta</i>\n\n<b>✅ @Termiz_ITcenterBot</b>"
		photo_id = "AgACAgIAAxkBAAIC_mc7MZjaTAVDK0vCJSRfrZQ27nzaAAIb5zEbYp7ZSWG7-5n1jC3gAQADAgADeQADNgQ"
		await message.answer_photo(photo_id,caption=msg)
		  
@dp.message_handler(text="🔚MENU🔜",user_id=ADMINS)
async def boshmenu(message:
	types.Message):
		await message.answer(f"<b>🤖Xurmatli {message.from_user.full_name} Bosh Menudasiz✅</b>",reply_markup=menu)