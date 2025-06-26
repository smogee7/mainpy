from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

from config import BOT_TOKEN
from keyboards.menu import get_main_keyboard
from utils.auth import is_admin

from handlers import start, user, admin  # Объединённый импорт

# Сначала создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    keyboard = get_main_keyboard(is_admin(message.from_user.id))
    await message.answer("Добро пожаловать!", reply_markup=keyboard)

# Регистрируем обработчики
start.register_handlers(dp)
user.register_handlers(dp)
admin.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
