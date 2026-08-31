import asyncio
import os
import sys
import uuid


async def download_video(url: str) -> str:
    file_id = str(uuid.uuid4())
    if not await asyncio.to_thread(os.path.exists, "downloads"):
        await asyncio.to_thread(os.makedirs, "downloads")
    template = f"downloads/{file_id}.%(ext)s"
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "yt_dlp",
        "--proxy", "",
        "-o", template,
        "-f", "b",  # или "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        "--merge-output-format", "mp4",
        "--impersonate", "chrome",
        "--cookies", "cookies.txt",
        url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise ValueError(stderr.decode())
    else:
        found_file = next(
            (
                f
                for f in await asyncio.to_thread(os.listdir, "downloads")
                if f.startswith(file_id)
            ),
            None,
        )
        rel_path = (
            os.path.relpath(os.path.join("downloads", found_file))
            if found_file
            else None
        )
        if rel_path is None:
            raise FileNotFoundError("Файл не найден")
        return rel_path
