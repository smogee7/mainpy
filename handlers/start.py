from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

from aiogram.filters import Command
async def start_cmd(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Купить VPN", callback_data="buy_vpn")],
        [InlineKeyboardButton(text="📩 Связаться с админом", callback_data="contact_admin")]
    ])
    await msg.answer("Привет! Я бот для покупки VPN.\nВыберите действие:", reply_markup=kb)
