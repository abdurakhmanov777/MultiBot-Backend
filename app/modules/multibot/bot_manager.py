import asyncio
from aiogram import Bot
from loguru import logger
from app.modules.multibot.polling_manager import PollingManager
from app.routers import create_router


async def _start_bot_polling(api_token: str, polling_manager: PollingManager):
    try:
        async with Bot(api_token) as bot:
            await bot.delete_webhook(drop_pending_updates=False)
            dp = create_router()
            polling_manager.start_bot_polling(
                dp=dp,
                bot=bot,
                polling_timeout=10,
                handle_as_tasks=True
            )
    except Exception as e:
        logger.error(f"Ошибка при запуске бота с токеном {api_token}: {e}")


async def start_multiple_bots(api_tokens: list[str], polling_manager: PollingManager):
    """Параллельный запуск нескольких ботов"""
    await asyncio.gather(*[
        _start_bot_polling(token, polling_manager)
        for token in api_tokens
    ])


async def start_bot(api_token: str, polling_manager: PollingManager):
    """Запуск одного бота"""
    await _start_bot_polling(api_token, polling_manager)


async def stop_bot(api_token: str, polling_manager: PollingManager):
    """Остановка бота по токену"""
    try:
        async with Bot(api_token) as bot:
            bot_id = (await bot.get_me()).id
        polling_manager.stop_bot_polling(bot_id)
    except Exception as e:
        logger.error(f"Ошибка остановки бота: {e}")
