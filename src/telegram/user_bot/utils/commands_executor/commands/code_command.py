import sys
import time
import asyncio
import aiohttp
from io import StringIO
from contextlib import redirect_stdout

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from .base_command import BaseCommand, Commands


class CodeCommand(BaseCommand):
    """
    Code executor
    """

    def __init__(self, client: Client):
        self._client = client
        self._trigger = Commands.code

    async def filter(self, message: Message) -> bool:
        return self._trigger in message.text

    async def execute(self, message: Message) -> None:
        args = message.text.split("\n", 1)
        if len(args) > 1:
            code = args[1]
        else:
            await message.reply_text("❌ No code provided")
            return

        await message.edit_text("⏳Выполняю...")

        try:
            start_time = time.perf_counter()
            result = await async_exec(code, self._client, message, timeout=300)
            stop_time = time.perf_counter()

            result = result.strip()

            result = result.replace(self._client.me.phone_number, "*****")

            if len(result) > 3072:
                result = await paste_neko(result)

            if result.strip() != '':
                result = result if result.startswith('nekobin.com/') else f"<pre>{result}</pre>"
            else:
                result = "<emoji id=5465665476971471368>❌</emoji> Вывода нет"

            await message.edit_text(
                text=f"""
<emoji id=5418368536898713475>🐍</emoji> Python + {sys.version.split()[0]}

<pre language='python'><code>{code}</code></pre>

<emoji id=5472164874886846699>✨</emoji> Вывод:
{result}

<emoji id=5298728804074666786>⏱</emoji> Выполнено за {round(stop_time - start_time, 5)}s.
                """,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
            return
        except TimeoutError:
            await message.edit_text(
                "<emoji id=5418368536898713475>🐍</emoji> Python " + sys.version.split()[0]
                + "\n\n"
                + "<pre language='python'><code>" + code + "</code></pre>"
                + "\n\n"
                + "<emoji id=5465665476971471368>❌</emoji> Время на исполнение кода исчерапно! TimeoutError",
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
            return
        except Exception as e:
            err = StringIO()
            await message.edit_text(
                "<emoji id=5418368536898713475>🐍</emoji> Python " + sys.version.split()[0]
                + "\n\n"
                + "<pre language='python'><code>" + code + "</code></pre>"
                + "\n\n"
                + f"<emoji id=5465665476971471368>❌</emoji> {b(e.__class__.__name__)}: {b(e)}\n"
                + f"Traceback: {await paste_neko(err.getvalue())}",
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )


async def paste_neko(code: str):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(
                "https://nekobin.com/api/documents",
                json={"content": code},
            ) as paste:
                paste.raise_for_status()
                result = await paste.json()
    except Exception as e:
        return f"Pasting failed: {e}"
    else:
        return f"nekobin.com/{result['result']['key']}.py"


async def async_exec(code, *args, timeout=None):
    exec(
        f"async def __todo(client, message, *args):\n"
        + " app = client; "
        + " msg = m = message; "
        + " r = msg.reply_to_message; "
        + " f = msg.from_user; "
        + " p = print; "
        + " q = msg.quote_text; "
        + " import asyncio; "
        + " ru = getattr(r, 'from_user', None)\n"
        + "".join(f"\n {_l}" for _l in code.split("\n"))
    )

    f = StringIO()
    with redirect_stdout(f):
        await asyncio.wait_for(locals()["__todo"](*args), timeout=timeout)

    return f.getvalue()
