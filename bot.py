# bot.py

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType
from aiogram.utils import executor

API_TOKEN = 'توکن_ربات_خود_را_اینجا_قرار_دهید'
ADMIN_ID = 123456789  # آیدی عددی مدیر

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# لیست کاربران ساکت‌شده
muted_users = set()

# ------------------- مدیریت گروه -------------------

@dp.message_handler(content_types=types.ContentTypes.TEXT, chat_type=ChatType.SUPERGROUP)
async def group_handler(message: types.Message):
    # قفل لینک
    if "http://" in message.text or "https://" in message.text or "t.me/" in message.text:
        await message.delete()
        await message.reply("🚫 ارسال لینک ممنوع است.")

    # خوش‌آمدگویی
    if message.new_chat_members:
        for member in message.new_chat_members:
            await message.reply(f"🎉 خوش آمدی {member.full_name}!")

    # بررسی سکوت
    if message.from_user.id in muted_users:
        await message.delete()

# دستور بن کردن کاربر
@dp.message_handler(commands=['ban'], chat_type=ChatType.SUPERGROUP)
async def ban_user(message: types.Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        await message.chat.kick(user_id)
        await message.reply("✅ کاربر بن شد.")
    else:
        await message.reply("لطفاً این دستور را در پاسخ به پیام کاربر ارسال کنید.")

# دستور سکوت کردن کاربر
@dp.message_handler(commands=['mute'], chat_type=ChatType.SUPERGROUP)
async def mute_user(message: types.Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        muted_users.add(user_id)
        await message.reply("🔇 کاربر ساکت شد.")
    else:
        await message.reply("لطفاً این دستور را در پاسخ به پیام کاربر ارسال کنید.")

# دستور لغو سکوت کاربر
@dp.message_handler(commands=['unmute'], chat_type=ChatType.SUPERGROUP)
async def unmute_user(message: types.Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        muted_users.discard(user_id)
        await message.reply("🔊 سکوت کاربر لغو شد.")
    else:
        await message.reply("لطفاً این دستور را در پاسخ به پیام کاربر ارسال کنید.")

# دستور اخطار دادن به کاربر
@dp.message_handler(commands=['warn'], chat_type=ChatType.SUPERGROUP)
async def warn_user(message: types.Message):
    if message.reply_to_message:
        await message.reply(f"⚠️ {message.reply_to_message.from_user.full_name}، لطفاً قوانین گروه را رعایت کنید.")
    else:
        await message.reply("لطفاً این دستور را در پاسخ به پیام کاربر ارسال کنید.")

# ------------------- ارسال پیام به مدیر -------------------

@dp.message_handler(content_types=types.ContentTypes.ANY, chat_type=ChatType.PRIVATE)
async def private_handler(message: types.Message):
    # فوروارد به مدیر
    await bot.send_message(ADMIN_ID, f"📩 پیام جدید از {message.from_user.full_name} (@{message.from_user.username or 'ندارد'}):")
    await message.forward(ADMIN_ID)

    # پاسخ به فرستنده
    await message.reply("✅ پیام شما به مدیر ارسال شد. لطفاً منتظر پاسخ بمانید.")

# ------------------- اجرای ربات -------------------

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
