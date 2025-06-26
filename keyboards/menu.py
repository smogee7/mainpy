    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard(is_admin: bool) -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton("📦Выбрать тариф"),
        KeyboardButton("🎁Пробный доступ"),
        KeyboardButton("❓Как это работает"),
        KeyboardButton("🛠Поддержка"),
    ]
    if is_admin:
        buttons.append(KeyboardButton("Админ панель"))
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard

def get_back_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton("Назад"))
    return keyboard

def get_tariffs_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton("Тариф 1"),
        KeyboardButton("Тариф 2"),
        KeyboardButton("Тариф 3"),
        KeyboardButton("Назад"),
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard
