from aiogram.utils import executor

from create_bot import dp
from handlers import registration, line, edit_profile

registration.register_handlers_register(dp)
line.register_handlers_line(dp)
edit_profile.register_handlers_edit_profile(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
