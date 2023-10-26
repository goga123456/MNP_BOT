import logging
import os
import requests
from aiogram import Bot, Dispatcher
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_webhook
from config import TOKEN_API
from markups.reply_mrkps import *
from markups.reply_mrkps import markup_language
from messages import *
from states import ProfileStatesGroup

#storage = MemoryStorage()
#bot = Bot(TOKEN_API)
#dp = Dispatcher(bot, storage=storage)

storage = MemoryStorage()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

dp = Dispatcher(bot,
                storage=storage)



@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text="Xizmat ko'rsatish tilini tanlang\n\nВыберите язык обслуживания",
                           reply_markup=markup_language)
    if state is None:
        return
    await state.finish()


@dp.message_handler(content_types=['text'])
async def lang_choose(message: types.Message, state: FSMContext) -> None:
    try:
        async with state.proxy() as data:
            data['lang'] = message.text
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['mnp_what'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['address'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['prices'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['docs'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['how'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1).row(btn2).row(btn3).row(btn4).row(btn5).row(btn6).row(btn7)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['choose'][data['lang']],
                                   reply_markup=markup_buttons)
        await ProfileStatesGroup.razdel.set()
    except KeyError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите вариант кнопкой!")

button_text = 'Хотите связаться с оператором?'
button_options = ['Связаться']
message_btn = {
    'text': button_text,
    'buttons': button_options
}

@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.razdel)
async def number_send(message: types.Message, state: FSMContext) -> None:
    try:
        async with state.proxy() as data:
            if message.text == lang_dict['mnp_what'][data['lang']]:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['about_mnp'][data['lang']])
            if message.text == lang_dict['address'][data['lang']]:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['ssilka'][data['lang']])
            if message.text == lang_dict['prices'][data['lang']]:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['price_about'][data['lang']])
            if message.text == lang_dict['docs'][data['lang']]:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['docs_about'][data['lang']])
            if message.text == lang_dict['how'][data['lang']]:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['use_about'][data['lang']])
            if message.text == lang_dict['connect'][data['lang']]:
                #await bot.send_message(chat_id=message.from_user.id,
                #                       text=lang_dict['connect_about'][data['lang']])
                response = requests.post(f'https://api.livetex.ru/bot/v1/{TOKEN_API}/message_btn', json=message_btn)

                # Проверьте статус ответа
                if response.status_code == 200:
                    print('Сообщение с кнопками успешно отправлено')
                else:
                    print('Ошибка при отправке сообщения с кнопками')
            if message.text == lang_dict['back'][data['lang']]:
                await state.finish()
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Xizmat ko'rsatish tilini tanlang\n\nВыберите язык обслуживания",
                                       reply_markup=markup_language)
    except KeyError:
        await bot.send_message(chat_id=message.from_user.id,
                           text="Выберите вариант кнопкой!")



#if __name__ == '__main__':
#    executor.start_polling(dp, skip_updates=True)
async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
async def on_shutdown(dispatcher):
    await bot.delete_webhook()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
