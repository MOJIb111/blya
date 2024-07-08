import datetime
import json
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from aiogram.utils.markdown import hbold,hlink
from aiogram.dispatcher.filters import Text
from main import check_news_upd

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ['Все новости', 'Последние 5', 'Свежак']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = (f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n"
                f"{hlink(v['article_title'],v['article_url'])}")

        await message.answer(news)


@dp.message_handler(Text(equals="Последние 5"))
async def get_last_five(message: types.Message):
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = (f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n"
                f"{hlink(v['article_title'], v['article_url'])}")

        await message.answer(news)


@dp.message_handler(Text(equals="Свежак"))
async def get_fresh(message: types.Message):
    fresh_news = check_news_upd()
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = (f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n"
                    f"{hlink(v['article_title'], v['article_url'])}")

            await message.answer(news)
    else:
        await message.answer("Пока нет свежих новостей")


if __name__ == "__main__":
    executor.start_polling(dp)