from aiogram import types

markup_language = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('Русский 🇷🇺')
btn2 = types.KeyboardButton('Oʻzbek tili 🇺🇿')
markup_language.row(btn1, btn2)








