from aiogram import types

async def cmd_start(message: types.Message):
    await message.answer("Привет! Я помогу тебе выбрать VPN-доступ.")

def register_handlers(dp):
    dp.register_message_handler(cmd_start, commands=["start"])
