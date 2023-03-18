from aiogram import types, Dispatcher

from handlers.registration import ProfileStateGroup


async def edit_profile_full(message: types.Message):
    """Редактирование анкеты"""
    await message.answer(text='Давай заполним анкету заново. Как тебя зовут?')
    await ProfileStateGroup.name.set()


def register_handlers_edit_profile(dp: Dispatcher):
    dp.register_message_handler(edit_profile_full, text='Заполнить анкету заново')
