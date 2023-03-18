from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

"""Лайк/дизлайк"""
kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn_like = KeyboardButton(text='❤️')
btn_dislike = KeyboardButton(text='👎')
btn_menu = KeyboardButton(text='Меню')
kb.add(btn_like, btn_dislike, btn_menu)

"""Редактирование профиля"""
kb_edit_profile = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_edit_name = KeyboardButton(text='Изменить имя')

kb_edit_profile.add(btn_edit_name)

"""Поиск"""
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_start = KeyboardButton(text='Поиск')
btn_edit_profile = KeyboardButton(text='Заполнить анкету заново')
kb_start.add(btn_start, btn_edit_profile)

"""Выбор пола"""
gender_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
male = KeyboardButton(text='Мужской')
female = KeyboardButton(text='Женский')
gender_kb.add(male, female)
