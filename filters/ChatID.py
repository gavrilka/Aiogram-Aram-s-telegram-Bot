from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data import config


class ChatIDFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.id == config.ILITA_CHAT_ID
