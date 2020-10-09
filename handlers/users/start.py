from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
# Добавляем db_gino
from utils.db_api import quick_commands as commands

# Переписали команду старт под db_gino
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    await commands.add_user(id=message.from_user.id,
                            name=name)

    count = await commands.count_users()
    await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'Ты был занесен в базу',
                f'В базе <b>{count}</b> пользователей',
            ]))