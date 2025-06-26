from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

async def handle_trial(message: Message):
    await message.answer("🎁 Пробный доступ на 1 день активирован!\n\nСкоро вы получите доступ в личные сообщения (функционал не реализован).")

async def handle_support(message: Message):
    await message.answer("🛠 Поддержка:\n\nНапишите @your_support_username")

async def handle_profile(message: Message):
    await message.answer("👤 Ваш личный кабинет (в разработке).")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_trial, Text(equals="🎁 Пробный доступ"))
    dp.register_message_handler(handle_support, Text(equals="🛠 Поддержка"))
    dp.register_message_handler(handle_profile, Text(equals="👤 Личный кабинет"))
