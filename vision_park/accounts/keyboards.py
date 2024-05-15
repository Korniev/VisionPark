from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='💲Price'), KeyboardButton(text='🌐Website')],
    [KeyboardButton(text='ℹ️Available parking'), KeyboardButton(text='🙌Support')]
],
    resize_keyboard=True,
    input_field_placeholder='waiting for a menu item...')

link_website = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Open website', url='http://127.0.0.1:8000/auth/profile/')]])