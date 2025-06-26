from aiogram import Dispatcher
from aiogram.types import Message
from aiogram import types, Dispatcher
from keyboards.menu import get_main_keyboard, get_back_keyboard
from utils.auth import is_admin
import datetime

from utils.auth import is_admin

async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Доступ запрещён.")
        return

    keyboard = get_back_keyboard()
    keyboard.add(types.KeyboardButton("Обращения"))
    await message.answer("Админ-панель", reply_markup=keyboard)

async def admin_handle_menu(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Доступ запрещён.")
        return

    if message.text == "Обращения":
        # Читаем файл с обращениями
        try:
            with open("user_messages.txt", "r", encoding="utf-8") as f:
                messages = f.readlines()
        except FileNotFoundError:
            messages = []

        if not messages:
            await message.answer("Обращений нет.")
            return

        # Покажем последние 5 обращений (например)
        last_msgs = messages[-5:]
        text = "Последние обращения:\n\n"
        for i, line in enumerate(last_msgs, 1):
            user_id_str, user_name, user_msg = line.strip().split(" | ", 2)
            text += f"{i}. {user_name} (ID: {user_id_str}):\n{user_msg}\n\n"
        await message.answer(text)
        # Позже добавим возможность отвечать по нажатию кнопки
    elif message.text == "Назад":
        keyboard = get_main_keyboard(is_admin(user_id))
        await message.answer("Главное меню", reply_markup=keyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_menu, lambda m: m.text == "Админ панель")
    dp.register_message_handler(admin_handle_menu)
