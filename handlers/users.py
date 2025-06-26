from aiogram import Dispatcher
from aiogram.types import Message

async def handle_tariff(message: Message):
    await message.answer("🔐 Доступные тарифы:\n\n1 мес – 300₽\n3 мес – 800₽\n6 мес – 1500₽\n\nДля покупки выберите тариф и оплатите.")

async def handle_trial(message: Message):
    await message.answer("🎁 Пробный доступ на 1 день активирован!\n\nСкоро вы получите доступ в личные сообщения (функционал не реализован).")

async def handle_how_it_works(message: Message):
    await message.answer("❓ Как это работает:\n\nВы покупаете доступ к VPN через Outline.\nПосле оплаты вы получаете ссылку для подключения.")

async def handle_support(message: Message):
    await message.answer("🛠 Поддержка:\n\nНапишите @your_support_username")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_tariff, lambda msg: msg.text == "📦 Выбрать тариф")
    dp.register_message_handler(handle_trial, lambda msg: msg.text == "🎁 Пробный доступ")
    dp.register_message_handler(handle_how_it_works, lambda msg: msg.text == "❓ Как это работает")
    dp.register_message_handler(handle_support, lambda msg: msg.text == "🛠 Поддержка")
