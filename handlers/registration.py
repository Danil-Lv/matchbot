from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from create_bot import bot
from keyboards import kb_start, gender_kb
from sqlalchemy_folder.db import create_user, get_user

storage = MemoryStorage()


class ProfileStateGroup(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    description = State()
    photo = State()


# @dp.message_handler(commands=['start'])
async def start_foo(message: types.Message):
    data = get_user(message.from_user.id)
    if not data:
        await message.answer('Давай создадим тебе профиль. Как тебя зовут?')
        await ProfileStateGroup.name.set()
    else:
        await message.answer('Так выглядит твоя анкета:')
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=data["Profile"].photo,
            caption=f'{data["Profile"].name} {data["Profile"].age}, {data["Profile"].city}\n{data["Profile"].description}',
            reply_markup=kb_start

        )


# @dp.message_handler(state=ProfileStateGroup.name)
async def get_name(message: types.Message, state):
    """Имя"""
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Сколько тебе лет?')

    await ProfileStateGroup.next()


# @dp.message_handler(lambda message: not message.text.isdigit(), state=ProfileStateGroup.age)
async def process_age_invalid(message: types.Message):
    """Валидация возраста"""
    return await message.reply("Возраст должен быть числом.")


# @dp.message_handler(state=ProfileStateGroup.age)
async def get_age(message: types.Message, state):
    """Возраст"""
    async with state.proxy() as data:
        data['age'] = message.text

    await message.answer('Из какого ты города?')
    await ProfileStateGroup.next()


# @dp.message_handler(state=ProfileStateGroup.city)
async def get_city(message: types.Message, state):
    """Город"""
    async with state.proxy() as data:
        data['city'] = message.text

    await message.answer('Какой у тебя пол?', reply_markup=gender_kb)
    await ProfileStateGroup.next()


async def get_gender(message: types.Message, state):
    """Пол"""
    async with state.proxy() as data:
        data['gender'] = message.text

    await message.answer('Напиши о себе')
    await ProfileStateGroup.next()


# @dp.message_handler(state=ProfileStateGroup.description)
async def get_description(message: types.Message, state):
    """Описание"""
    async with state.proxy() as data:
        data['description'] = message.text

    await message.answer('Теперь пришли свою фотографию')
    await ProfileStateGroup.next()


# @dp.message_handler(content_types=['photo'], state=ProfileStateGroup.photo)
async def get_photo(message: types.Message, state):
    """Фото"""
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        create_user(message.from_user.id, data)
        await message.answer('Так выглядит твоя анкета:')
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=data['photo'],
            caption=f"""{data["name"]} {data["age"]}, {data["city"]}\n{data["description"]}""",
            reply_markup=kb_start

        )

    await state.finish()


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_foo, commands=['start'])
    dp.register_message_handler(get_name, state=ProfileStateGroup.name)
    dp.register_message_handler(process_age_invalid, lambda message: not message.text.isdigit(),
                                state=ProfileStateGroup.age)
    dp.register_message_handler(get_age, state=ProfileStateGroup.age)
    dp.register_message_handler(get_city, state=ProfileStateGroup.city)
    dp.register_message_handler(get_gender, state=ProfileStateGroup.gender)

    dp.register_message_handler(get_description, state=ProfileStateGroup.description)
    dp.register_message_handler(get_photo, content_types=['photo'], state=ProfileStateGroup.photo)
