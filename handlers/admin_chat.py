from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID

router = Router()

class AnswerState(StatesGroup):
    waiting_for_answer = State()

# Кнопка "Связь с администратором"
@router.callback_query(F.data == "contact_admin")
async def contact_admin(callback: CallbackQuery):
    await callback.message.answer("✍️ Напишите сообщение администратору. Он ответит вам здесь.")
    await callback.answer()

# Пользователь пишет сообщение — оно уходит админу с кнопкой "Ответить"
@router.message(F.chat.type == "private")
async def handle_user_message(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")]
    ])

    await message.bot.send_message(
        chat_id=643408817,
        text=f"📨 Сообщение от @{message.from_user.username or message.from_user.id}:\n\n{message.text}",
        reply_markup=keyboard
    )

    await message.answer("✅ Сообщение отправлено администратору.")

# Админ нажал кнопку "Ответить"
@router.callback_query(F.data.startswith("reply_"))
async def start_reply(callback: CallbackQuery, state: FSMContext):
    try:
        user_id = int(callback.data.split("_")[1])
    except (IndexError, ValueError):
        await callback.message.answer("❌ Ошибка в ID пользователя.")
        return

    await state.set_state(AnswerState.waiting_for_answer)
    await state.update_data(target_user_id=user_id)

    await callback.message.answer(f"✉️ Введите сообщение, которое будет отправлено пользователю ID: {user_id}")
    await callback.answer()

# Админ ввёл ответ — отправляем пользователю
@router.message(AnswerState.waiting_for_answer)
async def send_reply_to
