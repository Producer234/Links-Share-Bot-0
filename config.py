 
import os
from os import environ
import logging
import re
from logging.handlers import RotatingFileHandler

# Recommended
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

# Main
OWNER_ID = int(os.environ.get("OWNER_ID", "7753899951"))
PORT = int(os.environ.get("PORT", "5000"))

# Database
DB_URI = os.environ.get("DB_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "linksharebot")

# Pattern for matching numeric channel IDs
id_pattern = re.compile(r'^-?\d+$')

#Auto approve - Set your channel IDs in CHAT_ID environment variable
CHAT_ID = [int(app_chat_id) if id_pattern.search(app_chat_id) else app_chat_id for app_chat_id in environ.get('CHAT_ID', '').split() if app_chat_id] or [] 
TEXT = environ.get("APPROVED_WELCOME_TEXT", "<b>{mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.</b>")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()

# Default
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "40"))
#--- ---- ---- --- --- --- - -- -  - - - - - - - - - - - --  - -

# Start pic
START_PIC_FILE_ID = "https://res.cloudinary.com/dqs0i4x9y/image/upload/v1756735243/ucigusyujb5bwxsjy1rm.jpg"
START_IMG = "https://res.cloudinary.com/dqs0i4x9y/image/upload/v1756735243/ucigusyujb5bwxsjy1rm.jpg"
START_PIC = START_IMG  # For compatibility with plugins
# Messages
START_MSG = os.environ.get("START_MESSAGE", "<b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ʟɪɴᴋs sʜᴀʀɪɴɢ ʙᴏᴛ. ᴡɪᴛʜ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴄᴀɴ sʜᴀʀᴇ ʟɪɴᴋs ᴀɴᴅ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs sᴀғᴇ ғʀᴏᴍ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs.\n\n<blockquote>‣ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://t.me/owner_of_pr'>PR Owner</a></blockquote></b>")
HELP = os.environ.get("HELP_MESSAGE", "<b><blockquote expandable>» Creator: <a href=https://t.me/owner_of_pr>PR Owner</a>\n» Our Channel: <a href=https://t.me/PR_ALL_BOT>PR All Bot</a>\n» Support Group: <a href=https://t.me/PR_ALL_BOT_SUPPORT>PR Support</a></b>")
ABOUT = os.environ.get("ABOUT_MESSAGE", "<b><blockquote expandable>This bot is developed by PR Owner (@owner_of_pr) to securely share Telegram channel links with temporary invite links, protecting your channels from copyright issues.</b>")

ABOUT_TXT = """<b>›› ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/PR_ALL_BOT'>PR All Bot</a>
<blockquote expandable>›› sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ: <a href='https://t.me/PR_ALL_BOT_SUPPORT'>PR Support</a>
›› ᴏᴡɴᴇʀ: <a href='https://t.me/owner_of_pr'>PR Owner</a>
›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a>
›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>
›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a>
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @owner_of_pr</b></blockquote>"""

CHANNELS_TXT = """<b>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/PR_ALL_BOT'>PR All Bot</a>
<blockquote expandable>›› ᴘʀ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/MAIN_CHANNEL_PR'>PR Main Channel</a>
›› ʜᴀʀᴇᴍ ʀᴇᴀʟᴍ: <a href='https://t.me/Harem_realm'>Harem Realm</a>
›› sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ: <a href='https://t.me/PR_ALL_BOT_SUPPORT'>PR Support</a>
›› ᴏᴡɴᴇʀ: <a href='https://t.me/owner_of_pr'>PR Owner</a>
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @owner_of_pr</b></blockquote>"""

#--- ---- ---- --- --- --- - -- -  - - - - - - - - - - - --  - -
# Default
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "⚠️ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ. 🤖"

# Logging
LOG_FILE_NAME = "links-sharingbot.txt"
DATABASE_CHANNEL = int(os.environ.get("DATABASE_CHANNEL", "-1002751155801")) # Channel where user links are stored

# Database Mode - Simple database for now (channel_logs has bot permission issues)
DATABASE_MODE = "simple"  # "mongodb", "channel_logs", or "simple"
#--- ---- ---- --- --- --- - -- -  - - - - - - - - - - - --  - -

try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "7753899951").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Admin == OWNER_ID
ADMINS.append(OWNER_ID)


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
