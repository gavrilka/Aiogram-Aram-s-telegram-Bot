from utils.set_bot_commands import set_default_commands
# Добавляем db_gino
from loader import db, bot
from utils.db_api import db_gino
from handlers.users.send_news import scheduled
import aioschedule as schedule
import asyncio
from handlers.users.habr import habrhabr_news
import datetime


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    # db_gino выполняем команды при старте
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")
    # print("Чистим базу")
    # await db.gino.drop_all()
    print("Готово")
    print("Создаем таблицы")
    await db.gino.create_all()
    print("Готово")

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


# # schedule module example
# async def habr_news():
#     print('hello')
#     await bot.send_message(26391577, datetime.datetime.now())


async def scheduler():
    schedule.every(15).minutes.do(lambda: habrhabr_news())

    # loop = asyncio.get_event_loop()
    while True:
        await schedule.run_pending()
        await asyncio.sleep(2)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    dp.loop.create_task(scheduler())
    executor.start_polling(dp, on_startup=on_startup)
