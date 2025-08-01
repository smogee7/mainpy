import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, buy, admin_chat

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(start.router)
dp.include_router(buy.router)
dp.include_router(admin_chat.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())