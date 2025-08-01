from aiogram import Router, types, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID
from utils.logger import log_purchase
from datetime import datetime
from aiogram.filters import Command


router = Router()
user_states = {}  # Словарь: user_id -> ожидается ли чек оплаты

@router.callback_query(F.data == "buy_vpn")
async def process_buy(callback: CallbackQuery):
    user_states[callback.from_user.id] = "waiting_for_payment"
    await callback.message.answer(
        "💳 Оплатите 300 руб по номеру XXXX XXXX XXXX\n"
        "После оплаты отправьте сюда скриншот подтверждения."
    )
    await callback.answer()

@router.message(F.photo)
async def process_payment_screenshot(msg: Message):
    if user_states.get(msg.from_user.id) == "waiting_for_payment":
        await msg.bot.send_message(
            ADMIN_ID,
            f"💰 Новый платёж от @{msg.from_user.username or msg.from_user.id}.\n"
            f"Скриншот оплаты ниже:"
        )
        await msg.bot.send_photo(ADMIN_ID, msg.photo[-1].file_id)
        await msg.answer("Спасибо! Ожидайте подтверждение от администратора.")
        user_states[msg.from_user.id] = "waiting_key"

@router.message(Command("start"))
async def send_key(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    parts = msg.text.strip().split(maxsplit=2)
    if len(parts) < 3:
        await msg.reply("❌ Используй команду так: /выдать @username VPN_KEY")
        return
    username, key = parts[1], parts[2]
    try:
        user = await msg.bot.get_chat(username)
        await msg.bot.send_message(user.id, f"🔑 Ваш VPN-ключ:\n`{key}`", parse_mode="Markdown")
        log_purchase(username)
        await msg.reply("✅ Ключ выдан и пользователь записан в лог.")
    except Exception as e:
        await msg.reply(f"❌ Не удалось отправить ключ: {e}")
