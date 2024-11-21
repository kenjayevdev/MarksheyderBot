from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📇 Karyer hisoblash"),
        ],
       [
       	KeyboardButton(text="🤖 Bot haqida"),
       	KeyboardButton(text="👨🏻‍💻 Dasturchi"),
       ],
        [
        KeyboardButton(text="👤 Loyiha asoschisi"),
        ],
    ],
    resize_keyboard=True,
)
