from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from config import ADMIN_ID

router = Router()
chat_sessions = {}  # user_id <-> сообщение админа

@router.callback_query(F.data == "contact_admin")
async def contact_admin(callback: CallbackQuery):
    await callback.message.answer("Напишите сообщение для администратора. Он ответит вам здесь.")
    chat_sessions[callback.from_user.id] = "pending"
    await callback.answer()

@router.message(F.text)
async def handle_user_message(msg: Message):
    if chat_sessions.get(msg.from_user.id) == "pending":
        forwarded = await msg.bot.send_message(
            ADMIN_ID,
            f"📨 Сообщение от @{msg.from_user.username or msg.from_user.id}:\n{msg.text}"
        )
        chat_sessions[msg.from_user.id] = forwarded.message_id

@router.message(F.reply_to_message)
async def handle_admin_reply(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    if not msg.reply_to_message:
        return
    for user_id, mid in chat_sessions.items():
        if mid == msg.reply_to_message.message_id:
            await msg.bot.send_message(user_id, f"💬 Ответ от админа:\n{msg.text}")
