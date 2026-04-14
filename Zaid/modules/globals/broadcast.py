import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

SCHEDULED = {}
TASKS = {}


@Client.on_message(filters.command("schedule", ".") & filters.me)
async def schedule_broadcast(client: Client, message: Message):

    if len(message.command) < 3:
        return await message.edit(
            "⏳ ᴜsᴀɢᴇ:\n\n"
            "`.schedule <minutes> <gc/dm/hybrid> ᴍsɢ`\n"
            "💡 ᴍᴇᴅɪᴀ ᴋᴇ ʟɪᴇ ʀᴇᴘʟʏ"
        )

    try:
        delay = int(message.command[1])
    except:
        return await message.edit("❌ ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ")

    mode = message.command[2].lower()

    text = None
    if len(message.command) > 3:
        text = message.text.split(None, 3)[3]

    reply = message.reply_to_message
    user_id = message.from_user.id

    task_id = len(SCHEDULED) + 1

    SCHEDULED[task_id] = {
        "user": user_id,
        "mode": mode,
        "text": text,
        "reply": reply,
        "delay": delay
    }

    async def runner():

        await asyncio.sleep(delay * 60)

        try:
            msg = await client.send_message(
                message.chat.id,
                f"⚡ sᴄʜᴇᴅᴜʟᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛɪɴɢ..."
            )

            sent = 0
            failed = 0
            total = 0

            async def push(chat_id):
                nonlocal sent, failed
                try:
                    if reply:
                        await reply.copy(chat_id)
                    else:
                        await client.send_message(chat_id, text)
                    sent += 1
                except:
                    failed += 1

            async for dialog in client.get_dialogs():

                chat = dialog.chat
                total += 1

                if mode == "gc":
                    if chat.type not in ["group", "supergroup"]:
                        continue

                elif mode == "dm":
                    if chat.type != "private":
                        continue
                    if chat.id == client.me.id:
                        continue

                elif mode == "hybrid":
                    if chat.type == "private" and chat.id == client.me.id:
                        continue

                await push(chat.id)
                await asyncio.sleep(0.2)

            await msg.edit(
                f"📡 sᴄʜᴇᴅᴜʟᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏɴᴇ\n\n"
                f"📊 ᴛᴏᴛᴀʟ : `{total}`\n"
                f"✅ sᴇɴᴛ : `{sent}`\n"
                f"❌ ғᴀɪʟᴇᴅ : `{failed}`"
            )

        except Exception as e:
            print("scheduler error:", e)

        SCHEDULED.pop(task_id, None)
        TASKS.pop(task_id, None)

    TASKS[task_id] = asyncio.create_task(runner())

    await message.edit(
        f"⏳ sᴄʜᴇᴅᴜʟᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛ\n\n"
        f"🆔 ɪᴅ : `{task_id}`\n"
        f"⏱ ɪɴ : `{delay}` ᴍɪɴ\n"
        f"⚡ ᴍᴏᴅᴇ : `{mode}`"
    )


# 🔥 LIST SCHEDULES
@Client.on_message(filters.command("schedules", ".") & filters.me)
async def list_schedules(client, message: Message):

    if not SCHEDULED:
        return await message.edit("📭 ɴᴏ sᴄʜᴇᴅᴜʟᴇs")

    txt = "⏳ sᴄʜᴇᴅᴜʟᴇs:\n\n"

    for i, d in SCHEDULED.items():
        txt += (
            f"🆔 `{i}` | ⏱ `{d['delay']}ᴍ` | ⚡ `{d['mode']}`\n"
        )

    await message.edit(txt)


# 🔥 CANCEL SCHEDULE
@Client.on_message(filters.command("cancelschedule", ".") & filters.me)
async def cancel_schedule(client, message: Message):

    if len(message.command) < 2:
        return await message.edit("❌ ɢɪᴠᴇ ɪᴅ")

    try:
        task_id = int(message.command[1])
    except:
        return await message.edit("❌ ɪɴᴠᴀʟɪᴅ ɪᴅ")

    if task_id not in TASKS:
        return await message.edit("❌ ɴᴏ sᴄʜᴇᴅᴜʟᴇ")

    TASKS[task_id].cancel()
    TASKS.pop(task_id, None)
    SCHEDULED.pop(task_id, None)

    await message.edit(f"🛑 sᴄʜᴇᴅᴜʟᴇ `{task_id}` ᴄᴀɴᴄᴇʟʟᴇᴅ")
