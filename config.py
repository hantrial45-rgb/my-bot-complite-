import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
# from database import get_current_2fa
import pytz

# .env ফাইল থেকে environment variables লোড করুন
load_dotenv()

# print(get_current_2fa())
# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")  # .env ফাইল থেকে পড়বে
API_ID = int(os.getenv("API_ID")) if os.getenv("API_ID") else None
API_HASH = os.getenv("API_HASH")

# Admin and Security Configuration
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None
TWO_FA_PASSWORD = os.getenv("TWO_FA_PASSWORD")
# Directories (যদি session ফোল্ডার না থাকে তবে তৈরি করবে)
SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)
REQUIRED_CHANNEL = "@JB_TEAMRECHIVERBOTUPTED"
WITHDRAW_CHANNEL_ID =  -1002642676612  # আপনার চ্যানেলের আইডি এখানে দিন

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Join Channel Button
join_button = InlineKeyboardButton(
    text="Join Our Channel",
    url=f"https://t.me/{REQUIRED_CHANNEL.strip('@')}"  # শুধু username দিয়ে লিঙ্ক
)

# Keyboard তৈরি
keyboard = InlineKeyboardMarkup([[join_button]])

# Example usage in /start handler
# async def start(update, context):
#     await update.message.reply_text(
#         "Please join our channel first:",
#         reply_markup=keyboard
#     )
