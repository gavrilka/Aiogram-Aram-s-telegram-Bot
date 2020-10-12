from asyncpg import UniqueViolationError
from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User, Birthday

async def next_birthday():
    query_old = db.text("select governor, date, DATE_PART('doy', date) - DATE_PART('doy', NOW()) as days FROM birthdays WHERE DATE_PART('doy', date) - DATE_PART('doy', NOW()) > 0 ORDER BY 3 LIMIT 1")
    query = db.text("select governor, date, (case when to_char(date, 'MM-DD') >= to_char(now(), 'MM-DD') then "
                    "to_date(to_char(current_date, 'YYYY') || '-' || to_char(date, 'MM-DD'), 'YYYY-MM-DD') else "
                    "to_date(to_char(current_date, 'YYYY') || '-' || to_char(date, 'MM-DD'), 'YYYY-MM-DD') + interval "
                    "'1 year' end) from birthdays order by 3")
    row = await db.first(query)
    return row

async def add_birthday(governor:str, date:str):
    governor = Birthday(governor=governor, date=date)
    await governor.create()

async def update_birthday(governor:str, date:str):
    governor = await Birthday.get(governor)
    await governor.update(date=date).apply()

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