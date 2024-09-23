from aiogram import types, F, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


url_note = '/api/v1/notes/'
url_auth = 'http:/127.0.0.1/api/v1/auth/'


class FormData(StatesGroup):
    login = State()
    password = State()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        f'Привет, {message.from_user.username}!\nВот что я могу:\n'
        '1. Создать заметку\n'
        '2. Показать все твои заметки\n'
        '3. Найти заметки по тегам '
    )


@router.message(Command('signup'))
async def message_handler(message: Message, state: FSMContext):
    await state.set_state(FormData.login)
    await message.answer(
        'Для создания заметки необходимо зарегистрироваться!\nВведите логин'
    )


@router.message(FormData.login)
async def process_login(message: Message, state: FSMContext) -> None:
    await state.update_data(login=message.text)
    await state.set_state(FormData.password)
    await message.answer(
        'Введите пароль'
    )


@router.message(FormData.password)
async def process_password(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    login = data.get('login')
    password = message.text
    await message.answer(f'Логин: {login}\nПароль: {password}')
