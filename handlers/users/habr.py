import asyncio

from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from loader import dp, bot
from handlers.users import hparse


# @dp.message_handler(Command("habr"))
async def habrhabr_news():
    text_message = hparse.get_links(path=hparse.__file__)
    if len(text_message) == 0:
        text_message = 'There is no new interesting articles.'
        await bot.send_message(chat_id=26391577, text=text_message)
    else:
        for i in text_message:
            if i[3] != 'None':
                try:
                    title = i[1]
                    link = i[0]
                    text = i[2]
                    image = i[3]
                    if 'jpg' or 'jpeg' in image:
                        await bot.send_photo('@habranews', photo=image, caption=f'<b>{title}</b>\n'
                                                                                    f'{text}\n'
                                                                                    f'{link}')
                    if 'gif' in image:
                        await bot.send_animation('@habranews', animation=image, caption=f'<b>{title}</b>\n'
                                                                                f'{text}\n'
                                                                                f'{link}')
                except Exception as e:
                    await bot.send_message(chat_id=26391577, text=e)
            else:
                try:
                    title = i[1]
                    link = i[0]
                    text = i[2]
                    await bot.send_message('@habranews', text=f'<b>{title}</b>\n'
                                                              f'{text}\n'
                                                              f'{link}')
                except Exception as e:
                    await bot.send_message(chat_id=26391577, text=e)
            await asyncio.sleep(5)
