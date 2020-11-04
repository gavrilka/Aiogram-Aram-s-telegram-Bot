from aiogram import Dispatcher

from .private_chat import IsPrivate
from .group_chat import IsGroup
from .ChatID import ChatIDFilter

def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(ChatIDFilter)