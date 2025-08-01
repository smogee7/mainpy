from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID

router = Router()

class AnswerState(StatesGroup):
    waiting_for_answer = State()

# Пользователь нажал "Связь с админом"
@router.callback_query(F.data == "contact_admin")
async def contact_admin(callback: CallbackQuery):
    if callback.from_user.id == ADMIN_ID:
        await callback.message.answer("Вы — администратор.")
        return

    await callback.message.answer("✍️ Напишите сообщение администратору. Он ответит вам здесь.")
    await callback.answer()

# Пользователь пишет сообщение — оно уходит админу с кнопкой "Ответить"
@router.message(F.chat.type == "private", ~F.from_user.id == ADMIN_ID)
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

# Админ нажимает кнопку "Ответить"
@router.callback_query(F.data.startswith("reply_"))
async def start_reply(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Эта кнопка только для администратора.", show_alert=True)
        return

    try:
        user_id = int(callback.data.split("_")[1])
    except (IndexError, ValueError):
        await callback.message.answer("❌ Не удалось извлечь ID пользователя.")
        return

    await state.set_state(AnswerState.waiting_for_answer)
    await state.update_data(target_user_id=user_id)
    await callback.message.answer(f"✉️ Введите сообщение, которое будет отправлено пользователю ID {user_id}")
    await callback.answer()

# Админ пишет ответ — он уходит пользователю
@router.message(AnswerState.waiting_for_answer, F.from_user.id == ADMIN_ID)
async def send_reply_to_user(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("target_user_id")

    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=f"💬 Ответ от администратора:\n\n{message.text}"
        )
        await message.answer("✅ Ответ отправлен пользователю.")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить сообщение:\n{e}")

    await state.clear()
