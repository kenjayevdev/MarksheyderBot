from aiogram import types
from loader import dp, bot
from aiogram.dispatcher.filters import Command

@dp.message_handler(text="👨🏻‍💻 Dasturchi")
async def bot_dev(message: types.Message):
    text = "<b>👨‍💻 Dasturchi haqida</b>\n\n🤖 Ushbu bot Jasur Kenjayev tomonidan ishlab chiqilgan bo'lib, ma'lumotlarni qayta ishlash, muhandislik hisob-kitoblarini avtomatlashtirish va foydalanuvchilarga qulay xizmat ko'rsatishni maqsad qilgan.\n\n<b>📌 Dasturchining maqsadi:</b>\n\n- Muhandislik sohasida tezkor va aniq hisob-kitoblarni amalga oshiruvchi zamonaviy dasturlarni yasash.\n- Foydalanuvchilar uchun texnik masalalarni soddalashtirish va vaqtni tejash.\n\n<b>💡 Ilhom manbasi:</b>\n\nDasturchi texnologiyalarni inson hayotini qulaylashtirish uchun foydalanishni sevadi va har doim yangi, foydali yechimlarni ishlab chiqishga intiladi. Ushbu bot ham ana shunday intilishlarning samarasi.\n\n✉️ Aloqa:\n\nAgar sizda botga oid takliflar yoki savollar bo'lsa, dasturchiga murojaat qiling:\n\n- Telegram: @Kenjayevdev\n- Email: Kenjayevdev@gmail.com\n- Web site: https://techscript.uz\n\n✅ @MarksheyderBot"
    photo_id = "AgACAgIAAxkBAAIC_Gc7MW5nHcJbk8NkmWNf9XCG648mAALf9zEbwIjISYja59njme6fAQADAgADeQADNgQ"
    await message.answer_photo(photo_id,caption=text)

@dp.message_handler(text="👤 Loyiha asoschisi")
async def bot_creator(message: types.Message):
    text = "<b>🏢 Termiz davlat muhandislik va agrotexnologiyalar universiteti\n\n⚙️ Mexanika va konchilik ishi fakulteti\n\n⛏️ Neft-gaz va konchilik ishi kafedrasi Assistenti Chorshanbiyev Shohruh Bahrom o'g'li\n\n✅ @MarksheyderBot</b>"
    await message.answer(text)