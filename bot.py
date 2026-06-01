import os
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

# توکن از Railway Variables
TOKEN = os.getenv("BOT_TOKEN")

# شناسه تاپیک‌ها
# بعداً باید با ID واقعی جایگزین شوند
TALK_BEYOND = 372
RUNNING = 155
IMAGES = 238


async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )

    return member.status in ["administrator", "creator"]


async def delete_after_1s(message):
    await asyncio.sleep(1)

    try:
        await message.delete()
    except:
        pass


async def guardian(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    thread_id = update.message.message_thread_id

    # تاپیک Talk Beyond
    if thread_id == TALK_BEYOND:

        if not await is_admin(update, context):

            try:
                await update.message.delete()
            except:
                pass

            warn = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⛔️ این تاپیک مخصوص اطلاع رسانی می‌باشد ⛔️",
                message_thread_id=TALK_BEYOND
            )

            asyncio.create_task(delete_after_1s(warn))

    # تاپیک Running
    elif thread_id == RUNNING:

        if not await is_admin(update, context):

            try:
                await update.message.delete()
            except:
                pass

            warn = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⛔️ این تاپیک مخصوص اطلاع رسانی می‌باشد ⛔️",
                message_thread_id=RUNNING
            )

            asyncio.create_task(delete_after_1s(warn))

    # تاپیک Images
    elif thread_id == IMAGES:

        allowed = False

        # عکس
        if update.message.photo:
            allowed = True

        # ویدیو
        elif update.message.video:
            allowed = True

        # فایل تصویری
        elif update.message.document:

            mime = update.message.document.mime_type

            if mime:
                if mime.startswith("image/"):
                    allowed = True

                elif mime.startswith("video/"):
                    allowed = True

        if not allowed:

            try:
                await update.message.delete()
            except:
                pass

            warn = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⛔️ این تاپیک مخصوص ارسال تصاویر است ⛔️",
                message_thread_id=IMAGES
            )

            asyncio.create_task(delete_after_1s(warn))


async def get_topic_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    برای پیدا کردن Topic ID ها
    بعد از پیدا شدن ID ها این هندلر را حذف کن
    """

    if update.message:
        print(
            f"Topic ID: {update.message.message_thread_id}"
        )


def main():

    if not TOKEN:
        raise ValueError(
            "BOT_TOKEN Variable Not Found"
        )

    app = Application.builder().token(TOKEN).build()

    # برای پیدا کردن Topic ID
    app.add_handler(
        MessageHandler(
            filters.ALL,
            get_topic_id
        )
    )

    # سیستم محافظت
    app.add_handler(
        MessageHandler(
            filters.ALL,
            guardian
        )
    )

    print("RunBeyondGuardianBot Started")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
