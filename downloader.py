import asyncio
from os import getenv

import aiohttp
from aiohttp import ClientTimeout
from dotenv import load_dotenv

load_dotenv()
MY_API_KEY = getenv("MY_API_KEY")
API_URL = "https://api.tikwmapi.com"

if not MY_API_KEY:
    raise ValueError("Critical error: environment variable MY_API_KEY is not set")
headers = {"x-tikwmapi-key": MY_API_KEY}


async def download_video(url: str) -> str:
    params = {"url": url, "hd": 1}
    try:
        async with (
            aiohttp.ClientSession(timeout=ClientTimeout(10)) as session,
            session.get(API_URL, params=params, headers=headers) as resp,
        ):
            if resp.status != 200:
                error = {"code": resp.status, "error": await resp.text()}
                raise ValueError(f"Critical error: {error}")

            else:
                data = await resp.json()
                if data["code"] != 0:
                    raise ValueError(f"Error code {data['code']}, {data['msg']}")

                video_link = data["data"].get("hdplay") or data["data"].get("play")
                if not video_link:
                    raise ValueError("Direct link to the video not found")
                return video_link

    except asyncio.TimeoutError:
        raise ValueError(
            "Request timed out: external API did not respond in 10 seconds"
        )

    except aiohttp.ClientError as err:
        raise ValueError(f"Error: {err}")
