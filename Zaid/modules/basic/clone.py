import os

from pyrogram import *
from pyrogram.types import *

from Zaid.helper.basic import get_text, get_user
from Zaid.modules.help import *

from Zaid.database.clonedb import save_clone, get_clone, delete_clone


@Client.on_message(filters.command("clone", ".") & filters.me)
async def clone(client: Client, message: Message):
    text = get_text(message)
    op = await message.edit_text("`Cloning`")

    try:
        me = await client.get_me()
        my_id = me.id

        # 👉 SAVE ORIGINAL DATA FIRST
        my_chat = await client.get_chat("me")

        photos = [p async for p in client.get_chat_photos("me")]
        my_photo = photos[0].file_id if photos else None

        await save_clone(my_id, {
            "first_name": me.first_name,
            "last_name": me.last_name,
            "bio": my_chat.bio or "",
            "photo": my_photo
        })

        # 👉 TARGET USER
        userk = get_user(message, text)[0]
        user_ = await client.get_users(userk)

        if not user_:
            await op.edit("`Whom i should clone:(`")
            return

        get_bio = await client.get_chat(user_.id)

        f_name = user_.first_name or ""
        l_name = user_.last_name or ""
        c_bio = get_bio.bio or ""

        # 👉 PROFILE PHOTO
        if user_.photo:
            pic = user_.photo.big_file_id
            poto = await client.download_media(pic)
            await client.set_profile_photo(photo=poto)

            try:
                os.remove(poto)
            except:
                pass

        # 👉 UPDATE PROFILE
        await client.update_profile(
            first_name=f_name,
            last_name=l_name,
            bio=c_bio
        )

        # KEEP ORIGINAL MESSAGE ✅
        await message.edit(f"**From now I'm** __{f_name}__")

    except Exception as e:
        await message.edit(f"`Error: {str(e)}`")


@Client.on_message(filters.command("revert", ".") & filters.me)
async def revert(client: Client, message: Message):
    await message.edit("`Reverting`")

    try:
        me = await client.get_me()
        my_id = me.id

        data = await get_clone(my_id)

        if not data:
            await message.edit("`No clone data found!`")
            return

        # 👉 RESTORE PROFILE
        await client.update_profile(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            bio=data.get("bio")
        )

        # 👉 DELETE CURRENT PHOTO
        photos = [p async for p in client.get_chat_photos("me")]
        if photos:
            await client.delete_profile_photos(photos[0].file_id)

        # 👉 RESTORE OLD PHOTO
        if data.get("photo"):
            poto = await client.download_media(data["photo"])
            await client.set_profile_photo(photo=poto)

            try:
                os.remove(poto)
            except:
                pass

        # 👉 CLEAN DB
        await delete_clone(my_id)

        await message.edit("`I am back!`")

    except Exception as e:
        await message.edit(f"`Error: {str(e)}`")


add_command_help(
    "clone",
    [
        ["clone", "To Clone someone Profile."],
        ["revert", "To Get Your Account Back."],
    ],
)
