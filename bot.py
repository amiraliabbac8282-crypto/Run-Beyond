import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "YOUR_TOKEN"

TALK_BEYOND = 372
RUNNING = 155
IMAGES = 238


async def is_admin(update, context):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )

    return member.status in ["administrator", "creator"]


async def auto_delete_warning(msg):
    await asyncio.sleep(1)

    try:
        await msg.delete()
    except:
        pass


async def guardian(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    thread_id = update.message.message_thread_id

    # Talk Beyond
    if thread_id == TALK_BEYOND:

        if not await is_admin(update, context):

            await update.message.delete()

            warn = await update.effective_chat.send_message(
                "⛔️ این تاپیک مخصوص اطلاع رسانی می‌باشد ⛔️"
            )

            asyncio.create_task(auto_delete_warning(warn))

    # Running
    elif thread_id == RUNNING:

        if not await is_admin(update, context):

            await update.message.delete()

            warn = await update.effective_chat.send_message(
                "⛔️ این تاپیک مخصوص اطلاع رسانی می‌باشد ⛔️"
            )

            asyncio.create_task(auto_delete_warning(warn))

    # Images
    elif thread_id == IMAGES:

        allowed = (
            update.message.photo or
            update.message.video
        )

        if not allowed:

            await update.message.delete()

            warn = await update.effective_chat.send_message(
                "⛔️ این تاپیک مخصوص ارسال تصاویر است ⛔️"
            )

            asyncio.create_task(auto_delete_warning(warn))


app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL, guardian)
)

app.run_polling()
