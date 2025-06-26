from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.menu import get_main_keyboard
from utils.auth import is_admin, ADMINS
from utils.messages import add_message

class SupportStates(StatesGroup):
    waiting_for_message = State()

async def support_start(message: types.Message):
    await message.answer("Пожалуйста, напишите ваше обращение. Чтобы отменить, напишите /cancel")
    await SupportStates.waiting_for_message.set()

async def support_receive(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_message = message.text

    message_id = add_message(user_id, user_name, user_message)

    await message.answer("Спасибо за ваше обращение! Мы обязательно ответим.", reply_markup=get_main_keyboard(is_admin(user_id)))

    # Уведомляем админов с ID обращения
    for admin_id in ADMINS:
        try:
            await message.bot.send_message(admin_id, f"Новое обращение #{message_id} от {user_name} (ID: {user_id}):\n{user_message}")
        except Exception as e:
            print(f"Ошибка при отправке уведомления админу {admin_id}: {e}")

    await state.finish()

async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer("Отмена обращения.", reply_markup=get_main_keyboard(is_admin(message.from_user.id)))
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(support_start, lambda message: message.text == "Поддержка", state="*")
    dp.register_message_handler(support_receive, state=SupportStates.waiting_for_message)
    dp.register_message_handler(cancel_handler, commands=["cancel"], state="*")
