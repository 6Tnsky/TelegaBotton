from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Задание 1: Простое меню с кнопками
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    # Создаем клавиатуру с кнопками "Привет" и "Пока"
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Привет"), KeyboardButton("Пока"))
    await message.answer("Выберите опцию:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Привет")
async def greet_user(message: types.Message):
    # Ответ на кнопку "Привет"
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message_handler(lambda message: message.text == "Пока")
async def goodbye_user(message: types.Message):
    # Ответ на кнопку "Пока"
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Задание 2: Кнопки с URL-ссылками
@dp.message_handler(commands=["links"])
async def links_command(message: types.Message):
    # Создаем инлайн-кнопки с URL-ссылками
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(
        InlineKeyboardButton("Новости", url="https://news.ycombinator.com/"),
        InlineKeyboardButton("Музыка", url="https://open.spotify.com/"),
        InlineKeyboardButton("Видео", url="https://www.youtube.com/")
    )
    await message.answer("Выберите ссылку:", reply_markup=inline_keyboard)

# Задание 3: Динамическое изменение клавиатуры
@dp.message_handler(commands=["dynamic"])
async def dynamic_command(message: types.Message):
    # Создаем инлайн-кнопку "Показать больше"
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton("Показать больше", callback_data="show_more"))
    await message.answer("Нажмите на кнопку:", reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda c: c.data == "show_more")
async def show_more_callback(callback_query: types.CallbackQuery):
    # Заменяем кнопку на две новых кнопки "Опция 1" и "Опция 2"
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(
        InlineKeyboardButton("Опция 1", callback_data="option_1"),
        InlineKeyboardButton("Опция 2", callback_data="option_2")
    )
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=inline_keyboard
    )

@dp.callback_query_handler(lambda c: c.data in ["option_1", "option_2"])
async def option_callback(callback_query: types.CallbackQuery):
    # Обрабатываем выбор пользователя
    option_text = "Опция 1" if callback_query.data == "option_1" else "Опция 2"
    await bot.send_message(callback_query.message.chat.id, f"Вы выбрали: {option_text}")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)