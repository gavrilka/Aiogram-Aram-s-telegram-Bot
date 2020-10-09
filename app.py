from utils.set_bot_commands import set_default_commands
# Добавляем db_gino
from loader import db
from utils.db_api import db_gino

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    # db_gino выполняем команды при старте
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")
    print("Чистим базу")
    await db.gino.drop_all()
    print("Готово")
    print("Создаем таблицы")
    await db.gino.create_all()
    print("Готово")

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)




