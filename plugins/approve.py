 
import os
import asyncio
from config import *
from pyrogram import Client, filters
from pyrogram.types import Message, User, ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, ChatAdminRequired, RPCError, UserNotParticipant
from database.database import set_approval_off, is_approval_off
from helper_func import *

# Default settings
APPROVAL_WAIT_TIME = 5  # seconds 
AUTO_APPROVE_ENABLED = True  # Toggle for enabling/disabling auto approval 

# Removed UserClient dependency - not needed for auto-approval

@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(CHAT_ID) if CHAT_ID else (filters.group | filters.channel))
async def autoapprove(client, message: ChatJoinRequest):
    global AUTO_APPROVE_ENABLED

    if not AUTO_APPROVE_ENABLED:
        return

    chat = message.chat
    user = message.from_user

    # check agr approval of hai us chnl m
    if await is_approval_off(chat.id):
        print(f"Auto-approval is OFF for channel {chat.id}")
        return

    print(f"🔄 {user.first_name} ({user.id}) requested to join {chat.title} ({chat.id})")
    print(f"📋 Auto-approval enabled: {AUTO_APPROVE_ENABLED}")
    print(f"⏱️  Waiting {APPROVAL_WAIT_TIME} seconds before approval...")
    
    await asyncio.sleep(APPROVAL_WAIT_TIME)

    # Check if user is already a participant before approving
    try:
        member = await client.get_chat_member(chat.id, user.id)
        if member.status in ["member", "administrator", "creator"]:
            print(f"User {user.id} is already a participant of {chat.id}, skipping approval.")
            return
    except UserNotParticipant:
        # User is not a member, proceed with approval
        pass
    except Exception as e:
        print(f"Error checking member status: {e}")

    try:
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        print(f"Successfully approved {user.first_name} ({user.id}) for {chat.title}")
    except Exception as e:
        print(f"Error approving join request: {e}")
        return
    
    if APPROVED == "on":
        invite_link = await client.export_chat_invite_link(chat.id)
        buttons = [
            [InlineKeyboardButton('🔥 ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ', url='https://t.me/PR_ALL_BOT')],
            [InlineKeyboardButton(f'• ᴊᴏɪɴ {chat.title} •', url=invite_link)]
        ]
        markup = InlineKeyboardMarkup(buttons)
        caption = f"<b>ʜᴇʏ {user.mention()},\n\n<blockquote> ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ _{chat.title} ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ.</blockquote> </b>"
        
        try:
            await client.send_photo(
                chat_id=user.id,
                photo=START_PIC,
                caption=caption,
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error sending approval photo: {e}")
            await client.send_message(
                chat_id=user.id,
                text=caption,
                reply_markup=markup
            )

@Client.on_message(filters.command("reqtime") & is_owner_or_admin)
async def set_reqtime(client, message: Message):
    global APPROVAL_WAIT_TIME
    
    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text("Usage: <code>/reqtime {seconds}</code>")
    
    APPROVAL_WAIT_TIME = int(message.command[1])
    await message.reply_text(f"✅ Request approval time set to <b>{APPROVAL_WAIT_TIME}</b> seconds.")

@Client.on_message(filters.command("reqmode") & is_owner_or_admin)
async def toggle_reqmode(client, message: Message):
    global AUTO_APPROVE_ENABLED
    
    if len(message.command) != 2 or message.command[1].lower() not in ["on", "off"]:
        return await message.reply_text("Usage: <code>/reqmode on</code> or <code>/reqmode off</code>")
    
    mode = message.command[1].lower()
    AUTO_APPROVE_ENABLED = (mode == "on")
    status = "enabled ✅" if AUTO_APPROVE_ENABLED else "disabled ❌"
    await message.reply_text(f"Auto-approval has been {status}.")

@Client.on_message(filters.command("approveoff") & is_owner_or_admin)
async def approve_off_command(client, message: Message):
    if len(message.command) != 2 or not message.command[1].lstrip("-").isdigit():
        return await message.reply_text("Usage: <code>/approveoff {channel_id}</code>")
    channel_id = int(message.command[1])
    success = await set_approval_off(channel_id, True)
    if success:
        await message.reply_text(f"✅ Auto-approval is now <b>OFF</b> for channel <code>{channel_id}</code>.")
    else:
        await message.reply_text(f"❌ Failed to set auto-approval OFF for channel <code>{channel_id}</code>.")

@Client.on_message(filters.command("approveon") & is_owner_or_admin)
async def approve_on_command(client, message: Message):
    if len(message.command) != 2 or not message.command[1].lstrip("-").isdigit():
        return await message.reply_text("Usage: <code>/approveon {channel_id}</code>")
    channel_id = int(message.command[1])
    success = await set_approval_off(channel_id, False)
    if success:
        await message.reply_text(f"✅ Auto-approval is now <b>ON</b> for channel <code>{channel_id}</code>.")
    else:
        await message.reply_text(f"❌ Failed to set auto-approval ON for channel <code>{channel_id}</code>.")
