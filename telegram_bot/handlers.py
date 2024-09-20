from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


url_note = '/api/v1/notes/'
url_auth = '/api/v1/auth/'


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer("Привет! Вот что я могу: "
                     "4. Создать заметку "
                     "3. Показать все твои заметки "
                     "2. Найти заметки по тегам "
                     "1. Зарегистрировать в приложении 'Note service' ")


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
