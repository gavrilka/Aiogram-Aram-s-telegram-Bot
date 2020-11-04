from loader import dp, bot
import aiohttp
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
#Импорты парсинга
from utils.stopgame import StopGame
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
import logging

# задаем уровень логов
logging.basicConfig(level=logging.INFO)
# инициализируем парсер



# проверяем наличие новых игр и делаем рассылки
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        # проверяем наличие новых игр


@dp.message_handler(Command("news"))
async def send_new_news(message: types.Message):
    await message.answer("Error")
    sg = StopGame('lastkey.txt')
    print(sg.new_games())
    new_games = sg.new_games()
    if (new_games):
        # если игры есть, переворачиваем список и итерируем
        new_games.reverse()
        for ng in new_games:
            # парсим инфу о новой игре
            nfo = sg.game_info(ng)

            # # получаем список подписчиков бота
            # subscriptions = db.get_subscriptions()

            # отправляем всем новость
            with open(sg.download_image(nfo['image']), 'rb') as photo:
                # отправить конкретному пользователю
                await message.answer_photo(
                    photo,
                    caption=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" +
                            nfo['link'],
                    disable_notification=True
                )

                # # часть кода отправит всем подписчкам из базы
                # for s in subscriptions:
                #     await bot.send_photo(
                #         s[1],
                #         photo,
                #         caption=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" +
                #                 nfo['link'],
                #         disable_notification=True
                #     )

            # обновляем ключ
            sg.update_lastkey(nfo['id'])