from aiogram import BaseMiddleware
from aiogram.types import Message


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, message: Message, data: dict):
        print(f'Получено сообщение: {message.text}')
        return await handler(message, data)