from aiogram import types, Dispatcher
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

async def handle_menu(message: types.Message):
    text = message.text
    user_id = message.from_user.id
    admin = is_admin(user_id)

    if text == "Выбрать тариф":
        tariffs_text = (
            "Доступные тарифы:\n"
            "1️⃣ Тариф 1 – описание\n"
            "2️⃣ Тариф 2 – описание\n"
            "3️⃣ Тариф 3 – описание\n\n"
            "Выберите тариф ниже:"
        )
        keyboard = get_tariffs_keyboard()
        await message.answer(tariffs_text, reply_markup=keyboard)
    elif text == "Назад":
        keyboard = get_main_keyboard(admin)
        await message.answer("Главное меню", reply_markup=keyboard)
    elif text == "Как это работает":
        await message.answer("Подробности тут: https://t.me/LumenNetVPN/5")
    # Тут остальные кнопки (позже)
    else:
        await message.answer("Пожалуйста, выберите опцию из меню.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(handle_menu)
