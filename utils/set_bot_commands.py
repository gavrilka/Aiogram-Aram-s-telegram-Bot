from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("email", "Записать email пользователя "),
        types.BotCommand("weather", "Узнать погоду"),
        types.BotCommand("fixer", "Узнать курс обмена валюты"),
    ])
