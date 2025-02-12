import asyncio
from aiogram import Bot, Dispatcher

from handlers.common_handlers import router as common_router
from handlers.survey_handlers import router as survey_router
from handlers.log_handlers import router as log_handler
from middlewares import LoggingMiddleware
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(
    common_router,
    survey_router,
    log_handler
)
dp.message.middleware(LoggingMiddleware())

async def main():
    print('Bot started!')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped.')