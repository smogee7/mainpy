from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.menu import get_main_keyboard, get_back_keyboard
from utils.auth import is_admin
from utils.messages import load_messages, update_message_answer

class AnswerStates(StatesGroup):
    waiting_for_answer = State()

async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Доступ запрещён.")
        return

    keyboard = get_back_keyboard()
    keyboard.add(types.KeyboardButton("Обращения"))
    await message.answer("Админ-панель", reply_markup=keyboard)

async def admin_handle_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Доступ запрещён.")
        return

    if message.text == "Обращения":
        messages = load_messages()
        if not messages:
            await message.answer("Обращений нет.")
            return

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for m in messages[-10:]:  # последние 10 обращений
            status = "✅" if m["answered"] else "❌"
            button_text = f"#{m['id']} {m['user_name']} {status}"
            keyboard.add(types.InlineKeyboardButton(button_text, callback_data=f"answer_{m['id']}"))

        await message.answer("Выберите обращение для ответа:", reply_markup=keyboard)
    elif message.text == "Назад":
        keyboard = get_main_keyboard(is_admin(user_id))
        await message.answer("Главное меню", reply_markup=keyboard)

async def callback_answer_request(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not is_admin(user_id):
        await call.answer("Доступ запрещён.", show_alert=True)
        return

    message_id = int(call.data.split("_")[1])
    await state.update_data(message_id=message_id)

    await call.message.answer(f"Введите ответ на обращение #{message_id} (или /cancel для отмены):")
    await AnswerStates.waiting_for_answer.set()
    await call.answer()

async def process_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")

    answer_text = message.text
    update_message_answer(message_id, answer_text)

    messages = load_messages()
    original_msg = next((m for m in messages if m["id"] == message_id), None)

    if original_msg:
        user_id = original_msg["user_id"]
        try:
            await message.bot.send_message(user_id, f"Администратор ответил на ваше обращение:\n\n{answer_text}")
            await message.answer("Ответ отправлен пользователю.")
        except Exception as e:
            await message.answer(f"Ошибка при отправке ответа пользователю: {e}")
    else:
        await message.answer("Не найдено исходное обращение.")

    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_menu, lambda m: m.text == "Админ панель")
    dp.register_message_handler(admin_handle_menu)
    dp.register_callback_query_handler(callback_answer_request, lambda c: c.data and c.data.startswith("answer_"))
    dp.register_message_handler(process_answer, state=AnswerStates.waiting_for_answer)
