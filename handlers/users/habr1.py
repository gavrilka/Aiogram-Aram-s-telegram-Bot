from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from aiogram.types import Message

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import pprint
import time

url = "https://habr.com/ru/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

async def get_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            return await resp.text()

async def get_stock_data(i):
    response = await get_html(url + i['href'])
    soup = BeautifulSoup(response, 'html.parser')
    stock_data = {}

    try:
        stock_data["Old price"] = soup.find('span', class_='line-through red').find('span', class_='text-muted greyColor').text.strip().replace('\u2009','')
    except:
        stock_data["Old price"] = "Отсутствует"
    try:
        stock_data["Price"] = soup.find('div', id='calc-price', class_='price').text.strip().replace('\u2009','')
    except:
        stock_data["Price"] = "Ошибка"
    try:
        stock_data["Title"] = soup.find('div', class_='title').find('h1', itemprop='name').text.strip().replace('\u2009','')
    except:
        stock_data["Title"] = "Ошибка"
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(stock_data)


@dp.message_handler(Command("habr1"))
async def chech_habr(message: types.Message):
    response = await get_html(url)
    soup = BeautifulSoup(response, 'html.parser')
    last_post = soup.find('li', class_='content-list__item content-list__item_post shortcuts_item focus')
    print(last_post)
    # await message.answer(response)
