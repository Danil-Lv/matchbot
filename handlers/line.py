from sqlalchemy import select, func, between
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.markdown import hlink
from aiogram import types, Dispatcher

from create_bot import bot, dp
from keyboards import kb_start, kb
from sqlalchemy_folder.db import get_user
from sqlalchemy_folder.test_bd import s
from sqlalchemy_folder.db import Profile


class LikeStateGroup(StatesGroup):
    like = State()


# @dp.message_handler(text='Поиск')
async def start_show(message: types.Message):
    """Начало поиска"""
    await LikeStateGroup.like.set()
    state = dp.current_state()
    user = get_user(message.from_user.id)['Profile']

    async with state.proxy() as data:
        data['city'] = user.city
        data['age'] = user.age

    await show_profiles(message, state)


def get_random_profile(city, age):
    """Получение случайного профиля"""
    query = select(Profile).where(Profile.city == city).where(between(Profile.age, age - 3, age + 3)).order_by(
        func.random()).limit(1)
    return s.execute(query).first()._asdict()


# @dp.message_handler(text=['👎'])
async def show_profiles(message: types.Message, state: FSMContext):
    """Вывод сулчайного профиля"""
    async with state.proxy() as data:
        profile = get_random_profile(data['city'], data['age'])['Profile']
        data['user_id'] = profile.id

    # data = await sq3.get_random()
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=profile.photo,
        caption=f"""{profile.name} {profile.age}, {profile.city}\n{profile.description}""",
        reply_markup=kb

    )


# @dp.message_handler(text='❤️')
async def like_foo(message: types.Message, state: FSMContext):
    """Лайк"""
    async with state.proxy() as data:
        await bot.send_message(chat_id=data['user_id'],
                               text=f'Тобой заинтересовались - {hlink(str(message.from_user.full_name), message.from_user.url)}',
                               parse_mode='HTML')
        await show_profiles(message, state)


# @dp.message_handler(text='Меню')
async def menu(message: types.Message, state: FSMContext):
    """Вывод меню"""
    await state.finish()
    await message.answer('Выбери, что нужно сделать', reply_markup=kb_start)


def register_handlers_line(dp: Dispatcher):
    dp.register_message_handler(start_show, text='Поиск')
    dp.register_message_handler(show_profiles, text='👎', state=LikeStateGroup.like)
    dp.register_message_handler(like_foo, text='❤️', state=LikeStateGroup.like)
    dp.register_message_handler(menu, text='Меню', state=LikeStateGroup.like)
