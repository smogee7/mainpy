from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard(is_admin=False):
    buttons = [
        [KeyboardButton("📦 Выбрать тариф")],
        [KeyboardButton("🎁 Пробный доступ")],
        [KeyboardButton("❓ Как это работает")],
        [KeyboardButton("🛠 Поддержка")],
    ]
    if is_admin:
        buttons.append([KeyboardButton("⚙️ Админ панель")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
