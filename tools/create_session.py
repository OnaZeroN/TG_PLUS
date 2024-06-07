import os
import asyncio

from pyrogram import Client
from dotenv import load_dotenv


load_dotenv()


async def main():
    client = Client(
        name=os.getenv("COMMON_APP_NAME"),
        api_id=os.getenv("COMMON_API_ID"),
        api_hash=os.getenv("COMMON_API_HASH"),
        app_version=os.getenv("COMMON_APP_VERSION"),
        device_model=os.getenv("COMMON_DEVICE_MODEL"),
        lang_pack=os.getenv("COMMON_LANG_PACK"),
        workdir=os.getenv("COMMON_WORK_DIR"),
    )
    await client.start()
    print(await client.get_me())
    await client.stop()

asyncio.run(main())
