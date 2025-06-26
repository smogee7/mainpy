from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards.menu import get_main_keyboard, get_back_keyboard, get_tariffs_keyboard
from utils.auth import is_admin

async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # Записываем в базу (файл)
    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(f"{user_id} | {user_name}\n")

    keyboard = get_main_keyboard(is_admin(user_id))
    await message.answer("Добро пожаловать!", reply_markup=keyboard)

async def handle_tariff(message: types.Message):
    tariffs_text = (
        "📦 Доступные тарифы:\n"
        "1️⃣ Тариф 1 – описание\n"
        "2️⃣ Тариф 2 – описание\n"
        "3️⃣ Тариф 3 – описание\n\n"
        "Выберите тариф ниже:"
    )
    keyboard = get_tariffs_keyboard()
    await message.answer(tariffs_text, reply_markup=keyboard)

async def handle_how_it_works(message: types.Message):
    await message.answer("❓ Подробности тут: https://t.me/LumenNetVPN/5")

async def handle_back(message: types.Message):
    user_id = message.from_user.id
    keyboard = get_main_keyboard(is_admin(user_id))
    await message.answer("🔙 Главное меню", reply_markup=keyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(handle_tariff, Text(equals="📦 Выбрать тариф"))
    dp.register_message_handler(handle_how_it_works, Text(equals="❓ Как это работает"))
    dp.register_message_handler(handle_back, Text(equals="🔙 Назад"))
