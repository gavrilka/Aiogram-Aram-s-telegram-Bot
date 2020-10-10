from asyncpg import UniqueViolationError
from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User

# async def get_user(self, user_id):
#     user = await User.query.where(User.user_id == user_id).gino.first()
#     return user
#
#
# async def add_new_user(self, referral=None):
#     user = types.User.get_current()
#     old_user = await self.get_user(user.id)
#     if old_user:
#         return old_user
#     new_user = User()
#     new_user.user_id = user.id
#     new_user.username = user.username
#     new_user.full_name = user.full_name
#
#     # if referral:
#     #     new_user.referral = int(referral)
#     await new_user.create()
#     return new_user
#
#
# async def set_language(self, language):
#     user_id = types.User.get_current().id
#     user = await self.get_user(user_id)
#     await user.update(language=language).apply()
#
#
# async def count_users(self) -> int:
#     total = await db.func.count(User.id).gino.scalar()
#     return total


# async def check_referrals(self):
#     bot = Bot.get_current()
#     user_id = types.User.get_current().id
#
#     user = await User.query.where(User.user_id == user_id).gino.first()
#     referrals = await User.query.where(User.referral == user.id).gino.all()
#
#     return ", ".join([
#         f"{num + 1}. " + (await bot.get_chat(referral.user_id)).get_mention(as_html=True)
#         for num, referral in enumerate(referrals)
#     ])


# async def show_items(self):
#     items = await Item.query.gino.all()
#
#     return items


async def add_user(id: int, name: str, username: str, language_code: str, email: str = None):
    try:

        user = User(id=id, name=name, email=email, username=username, language_code=language_code)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def update_user_email(id, email):
    user = await User.get(id)
    await user.update(email=email).apply()