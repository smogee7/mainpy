from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN_ID
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class AnswerState(StatesGroup):
    waiting_for_answer = State()

# Обработка команды "Связь с админом"
@router.callback_query(F.data == "contact_admin")
async def contact_admin(callback: CallbackQuery):
    await callback.message.answer("✍️ Напишите сообщение для администратора. Он ответит вам здесь.")
    await callback.answer()

# Принимаем сообщение пользователя и пересылаем админу с кнопкой "Ответить"
@router.message(F.chat.type == "private")
async def handle_user_message(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")]
    ])
    await message.bot.send_message(
        chat_id=643408817,
        text=f"📨 Сообщение от @{message.from_user.username or message.from_user.id}:\n{message.text}",
        reply_markup=keyboard
    )
    await message.answer("✅ Сообщение отправлено администратору.")

# Обработка кнопки "Ответить"
@router.callback_query(F.data.startswith("reply_"))
async def start_reply(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[1])
    await state.set_state(AnswerState.waiting_for_answer)
    await state.update_data(target_user_id=user_id)
    await callback.message.answer("✉️ Введите сообщение, которое будет отправлено пользователю.")
    await callback.answer()

# Отправка ответа пользователю
@router.message(AnswerState.waiting_for_answer)
async def send_reply_to_user(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("target_user_id")
    try:
        await message.bot.send_message(chat_id=user_id, text=f"💬 Ответ от администратора:\n\n{message.text}")
        await message.answer("✅ Ответ отправлен.")
    except Exception:
        await message.answer("❌ Не удалось отправить сообщение пользователю.")
    await state.clear()
