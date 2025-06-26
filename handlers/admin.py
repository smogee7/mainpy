from aiogram import Dispatcher
from aiogram.types import Message

from utils.auth import is_admin

async def handle_admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔️ У вас нет доступа к админ-панели.")
        return

    await message.answer("⚙️ Добро пожаловать в админ-панель!\n\n(Здесь будут доступны функции: добавить доступ, просмотреть оплаты, статистика и т.д.)")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_admin_panel, lambda msg: msg.text == "⚙️ Админ панель")
