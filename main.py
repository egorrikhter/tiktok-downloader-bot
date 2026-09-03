import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from database import close_db, init_db
from downloader import download_video

logger = logging.getLogger(__name__)

load_dotenv()
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Send video link!")


@dp.message()
async def echo_handler(message: Message) -> None:
    if not message.text:
        await message.answer("You didn't send link.")
        return

    if "tiktok.com" not in message.text:
        await message.answer("Invalid link format.")
        return
    try:
        video_link = await download_video(message.text)

    except ValueError as error:
        logger.error(f"Download failed: {error}")
        await message.answer("The download server is temporarily unresponsive.")
        return

    try:
        await message.answer_video(video=video_link)

    except TelegramBadRequest as err:
        logger.error(f"Bad request error, {err}")
        if (
            "file is too big" in str(err).lower()
            or "req_file_too_big" in str(err).lower()
        ):
            await message.answer(
                f"The video is too large to send directly via Telegram. You can download the video directly via the link: {video_link}"
            )
        else:
            await message.answer("Failed to send video. Please try again later.")
        return


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
