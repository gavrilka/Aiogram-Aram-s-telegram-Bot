from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from filters import ChatIDFilter
import aiohttp


async def get_random_gif(tag):
    async with aiohttp.ClientSession() as session:
        api_key = '106Mfux6s8O57lP5krOwnbxOuJ6c52ms'
        tag = tag
        url = f'https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}&rating=g'
        async with session.get(url) as resp:
            async with session.get(url) as resp:
                data = await resp.json()
                gif_link = data['data']['images']['original']['mp4']
                return gif_link

@dp.message_handler(Command("gif"), chat_id=-1001434503735)
async def send_chat_id(message: types.Message):
    try:
        text = message.text
        texts = text.split(' ', 1)
        tag = str.upper(texts[1])
        # tag1 = 'https://media3.giphy.com/media/4KFwbI7GuE3QHPMCgd/giphy-hd.mp4?cid=f8cb1ff2e496ccb4752c980814112c0a3b48d93e75035fc7&rid=giphy-hd.mp4'
        await message.answer_video(await get_random_gif(tag))
        # await message.answer(await get_random_gif(tag))
        # await message.answer_video(await get_random_gif(tag))
    except Exception as e:
        await message.answer(e)
    # await message.answer(message.chat.id)
