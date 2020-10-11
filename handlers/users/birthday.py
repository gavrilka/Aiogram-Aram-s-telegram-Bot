from aiogram import types
from loader import dp
from filters import IsGroup
from aiogram.dispatcher.filters import Command
from utils.db_api import quick_commands as commands
from asyncpg import UniqueViolationError
import re
import datetime


@dp.message_handler(Command("birthday", prefixes="!/"), IsGroup())
async def birthday(message: types.Message):
    if message.text == '/birthday' or message.text == '!birthday':
        await message.answer(
            f'Dear *{message.from_user.first_name}*! tell us governor name and his birthday date, for example /birthday governor 11-10-2020',
            parse_mode='Markdown')
    else:
        command_parse = re.compile(r"(!birthday|/birthday) ([a-zA-Z0-9_]+)? (\d\d)?-?(\d\d)-?(\d\d\d\d)?")
        parsed = command_parse.match(message.text)
        governor = str(parsed.group(2))
        day = int(parsed.group(3))
        month = int(parsed.group(4))
        year = int(parsed.group(5))
        d = datetime.date(year, month, day)
        text_added = f'Governors *{governor}* birthday *{d.strftime("%d %B %Y")}* is added to database'
        text_updated = f'Governors *{governor}* birthday *{d.strftime("%d %B %Y")}* is updated'
        try:
            await commands.add_birthday(governor=governor, date=d)
            await message.answer(text_added, parse_mode='Markdown')
        except UniqueViolationError:
            await message.answer(text_updated, parse_mode='Markdown')
            await commands.update_birthday(governor=governor, date=d)
        except Exception as e:
            await message.answer('I am sorry, *' + message.from_user.first_name + '*,incorrect input',
                                 parse_mode='Markdown')
            print (e)


@dp.message_handler(Command("next", prefixes="!/"), IsGroup())
async def birthday(message: types.Message):
    if message.text == '/next' or message.text == '!next':
        name = await commands.next_birthday()
        await message.answer(f'Next birthday is *{name.governor}* {name.date.strftime("%d %B")} ',
                             parse_mode='Markdown')
    else:
        await message.answer('Incorrect input',
                             parse_mode='Markdown')
