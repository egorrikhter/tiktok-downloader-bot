import asyncio
import logging
from os import getenv

import aiohttp
from dotenv.main import load_dotenv

load_dotenv()
MY_API_KEY = getenv("MY_API_KEY")
API_URL = "https://api.tikwmapi.com"
headers = {"x-tikwmapi-key": str(MY_API_KEY)}


async def download_video(url: str) -> dict[str, str]:
    params = {"url": url, "hd": 1}
    async with (
        aiohttp.ClientSession() as session,
        session.get(API_URL, params=params, headers=headers) as resp,
    ):
        if resp.status != 200:
            error = {"code": resp.status, "error": await resp.text()}
            print(error)
            return error
        else:
            data = await resp.json()
            print(data)
            return data


if __name__ == "__main__":
    asyncio.run(download_video("https://vm.tiktok.com/ZN8YJG2hN/"))


# все сработало, думаю что нельзя делать как я сделал в 11 строчке, подумать об этом потом
# а вообще надо теперь делать парсинг, получать из ответа только title, url
