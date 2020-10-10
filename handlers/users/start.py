from aiogram import types, bot
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
# Добавляем db_gino
from utils.db_api import quick_commands as commands

#новый user
import utils.db_api.db_gino

# Переписали команду старт под db_gino
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    username = message.from_user.username
    language_code = message.from_user.language_code
    await commands.add_user(id=message.from_user.id,
                            name=name, username=username,language_code=language_code)

    count = await commands.count_users()
    await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'Твой язык по умолчанию: {language_code}',
                f'Твой юзернейм: {username}',
                f'Ты был занесен в базу',
                f'В базе <b>{count}</b> пользователей',
            ]))

# # Для команды /start есть специальный фильтр, который можно тут использовать
# @dp.message_handler(CommandStart())
# async def register_user(message: types.Message):
#     chat_id = message.from_user.id
#     # referral = message.get_args()
#     user = await commands.add_new_user()
#     id = user.id
#     count_users = await commands.count_users()
#
#     # # Отдадим пользователю клавиатуру с выбором языков
#     # languages_markup = InlineKeyboardMarkup(
#     #     inline_keyboard=
#     #     [
#     #         [
#     #             InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
#     #         [
#     #             InlineKeyboardButton(text="English", callback_data="lang_en"),
#     #             InlineKeyboardButton(text="Україньска", callback_data="lang_uk"),
#     #         ]
#     #     ]
#     # )
#
#     bot_username = (await bot.me).username
#     bot_link = f"https://t.me/{bot_username}?start={id}"
#
#     # Для многоязычности, все тексты, передаваемые пользователю должны передаваться в функцию "_"
#     # Вместо "текст" передаем _("текст")
#
#     text = ("Приветствую вас!!\n"
#              "Сейчас в базе {count_users} человек!\n"
#              "\n"
#              "Ваша реферальная ссылка: {bot_link}\n"
#              "Проверить рефералов можно по команде: /referrals\n"
#              "Просмотреть товары: /items").format(
#         count_users=count_users,
#         bot_link=bot_link
#     )
#     # if message.from_user.id == admin_id:
#     #     text += _("\n"
#     #               "Добавить новый товар: /add_item")
#     # await bot.send_message(chat_id, text, reply_markup=languages_markup)
#     await bot.send_message(chat_id, text)
#
#     # @dp.message_handler(commands=["referrals"])
#     # async def check_referrals(message: types.Message):
#     #     referrals = await commands.check_referrals()
#     #     text = ("Ваши рефералы:\n{referrals}").format(referrals=referrals)
#     #     await message.answer(text)