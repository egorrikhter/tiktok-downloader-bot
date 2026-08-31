import asyncio
import html
import logging
import sys
from os import getenv, remove
from os.path import exists

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

from database import close_db, init_db
from downloader import download_video

load_dotenv()
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Присылайте ссылку на видео!")


@dp.message()
async def echo_handler(message: Message) -> None:
    if not message.text:
        await message.answer("Вы прислали не текст")
        return

    if "tiktok.com" not in message.text:
        await message.answer("Неверный формат ссылки")
        return
    file_path = None
    try:
        file_path = await download_video(message.text)
        await message.answer_video(FSInputFile(file_path), supports_streaming=True)
    except ValueError as error:
        logging.error(f"При скачивании файла возникла ошибка: {error}")
        await message.answer(f"При скачивании файла возникла ошибка: {html.escape(str(error))}")
    except FileNotFoundError as error:
        logging.error(error)
        await message.answer(f"{error}")
    finally:
        if file_path and await asyncio.to_thread(exists, file_path):
            await asyncio.to_thread(remove, file_path)


async def main() -> None:
    TOKEN = getenv("BOT_TOKEN")

    if not TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(init_db)
    dp.shutdown.register(close_db)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
