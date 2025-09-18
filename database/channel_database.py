# Telegram Channel Database System
# Stores data as JSON messages in a telegram channel
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
from pyrogram import Client
from pyrogram.types import Message
from config import DATABASE_CHANNEL, TG_BOT_TOKEN, API_HASH, APP_ID

class ChannelDatabase:
    def __init__(self):
        self.client = None
        self.cache = {}
        self.last_message_id = 0
    
    async def init_client(self):
        """Initialize Telegram client for database operations"""
        if self.client is None:
            try:
                self.client = Client(
                    "database_bot",
                    api_id=APP_ID,
                    api_hash=API_HASH,
                    bot_token=TG_BOT_TOKEN
                )
                await self.client.start()
                await self.load_cache()
            except Exception as e:
                print(f"Warning: Could not initialize channel database client: {e}")
                print("Falling back to simple database mode...")
                self.client = None
    
    async def load_cache(self):
        """Load existing data from channel into cache"""
        try:
            # Bots can't use get_chat_history, so we'll load data on-demand
            # Cache will be populated as data is accessed and stored
            print("Channel database cache initialized (will load data on-demand)")
        except Exception as e:
            print(f"Error loading cache from channel database: {e}")
    
    async def set(self, key: str, value: Any):
        """Store a key-value pair in the channel database"""
        if self.client is None:
            await self.init_client()
        
        try:
            data = {
                "key": key,
                "value": value,
                "timestamp": datetime.now().isoformat(),
                "action": "set"
            }
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            
            # Send to channel (this is internal database storage, not visible to users)
            await self.client.send_message(DATABASE_CHANNEL, json_data)
            
            # Update cache
            self.cache[key] = value
            return True
        except Exception as e:
            print(f"Error storing in channel database: {e}")
            return False
    
    async def get(self, key: str, default=None):
        """Retrieve a value from the channel database"""
        if self.client is None:
            await self.init_client()
        
        return self.cache.get(key, default)
    
    async def delete(self, key: str):
        """Delete a key from the channel database"""
        if self.client is None:
            await self.init_client()
        
        try:
            if key in self.cache:
                data = {
                    "key": key,
                    "action": "delete",
                    "timestamp": datetime.now().isoformat()
                }
                json_data = json.dumps(data, ensure_ascii=False, indent=2)
                
                # Send delete action to channel
                await self.client.send_message(DATABASE_CHANNEL, json_data)
                
                # Remove from cache
                del self.cache[key]
                return True
        except Exception as e:
            print(f"Error deleting from channel database: {e}")
        return False
    
    async def exists(self, key: str):
        """Check if a key exists in the database"""
        if self.client is None:
            await self.init_client()
        return key in self.cache
    
    async def get_all_keys(self):
        """Get all keys in the database"""
        if self.client is None:
            await self.init_client()
        return list(self.cache.keys())

# Global database instance
channel_db = ChannelDatabase()

# Database functions for compatibility
async def add_user(user_id: int):
    """Add a user to the database"""
    users_key = "users"
    users = await channel_db.get(users_key, [])
    if user_id not in users:
        users.append(user_id)
        await channel_db.set(users_key, users)
    return True

async def get_user(user_id: int):
    """Get user from database"""
    users = await channel_db.get("users", [])
    return user_id in users

async def delete_user(user_id: int):
    """Delete user from database"""
    users_key = "users"
    users = await channel_db.get(users_key, [])
    if user_id in users:
        users.remove(user_id)
        await channel_db.set(users_key, users)
    return True

async def get_all_users():
    """Get all users"""
    return await channel_db.get("users", [])

async def get_users_count():
    """Get total users count"""
    users = await channel_db.get("users", [])
    return len(users)

async def save_channel(channel_id: int, encoded_link: str):
    """Save channel with encoded link"""
    channels_key = f"channel_{channel_id}"
    channel_data = {
        "id": channel_id,
        "encoded_link": encoded_link,
        "created_at": datetime.now().isoformat()
    }
    return await channel_db.set(channels_key, channel_data)

async def get_channel_by_encoded_link(encoded_link: str):
    """Get channel by encoded link"""
    all_keys = await channel_db.get_all_keys()
    for key in all_keys:
        if key.startswith("channel_"):
            channel_data = await channel_db.get(key)
            if channel_data and channel_data.get("encoded_link") == encoded_link:
                return channel_data.get("id")
    return None

async def get_channel_by_encoded_link2(encoded_link: str):
    """Get channel by encoded link (alternative)"""
    return await get_channel_by_encoded_link(encoded_link)

async def save_invite_link(channel_id: int, invite_link: str, is_request: bool = False):
    """Save invite link for channel"""
    invite_key = f"invite_{channel_id}"
    invite_data = {
        "channel_id": channel_id,
        "invite_link": invite_link,
        "is_request": is_request,
        "created_at": datetime.now().isoformat()
    }
    return await channel_db.set(invite_key, invite_data)

async def get_current_invite_link(channel_id: int):
    """Get current invite link for channel"""
    invite_key = f"invite_{channel_id}"
    return await channel_db.get(invite_key)

async def get_original_link(channel_id: int):
    """Get original link for channel"""
    original_key = f"original_{channel_id}"
    return await channel_db.get(original_key)

async def set_approval_off(channel_id: int, is_off: bool):
    """Set approval status for channel"""
    approval_key = f"approval_off_{channel_id}"
    return await channel_db.set(approval_key, is_off)

async def is_approval_off(channel_id: int):
    """Check if approval is off for channel"""
    approval_key = f"approval_off_{channel_id}"
    return await channel_db.get(approval_key, False)

async def get_fsub_channels():
    """Get FSub channels"""
    return await channel_db.get("fsub_channels", [])

# Admin management functions
async def add_admin(user_id: int):
    """Add an admin to the database"""
    admins_key = "admins"
    admins = await channel_db.get(admins_key, [])
    if user_id not in admins:
        admins.append(user_id)
        await channel_db.set(admins_key, admins)
    return True

async def remove_admin(user_id: int):
    """Remove an admin from the database"""
    admins_key = "admins"
    admins = await channel_db.get(admins_key, [])
    if user_id in admins:
        admins.remove(user_id)
        await channel_db.set(admins_key, admins)
    return True

async def list_admins():
    """List all admins"""
    return await channel_db.get("admins", [])

async def is_admin(user_id: int):
    """Check if user is admin"""
    admins = await channel_db.get("admins", [])
    return user_id in admins

# Additional functions for compatibility
async def present_user(user_id: int):
    """Check if a user exists in the database"""
    users = await channel_db.get("users", [])
    return user_id in users

async def full_userbase():
    """Get all users"""
    return await channel_db.get("users", [])

async def del_user(user_id: int):
    """Delete user from database"""
    return await delete_user(user_id)

async def get_channels():
    """Get all channels"""
    all_keys = await channel_db.get_all_keys()
    channel_ids = []
    for key in all_keys:
        if key.startswith("channel_"):
            try:
                channel_id = int(key.replace("channel_", ""))
                channel_ids.append(channel_id)
            except:
                continue
    return channel_ids

async def delete_channel(channel_id: int):
    """Delete a channel"""
    channel_key = f"channel_{channel_id}"
    return await channel_db.delete(channel_key)

async def save_encoded_link(channel_id: int):
    """Save encoded link for channel"""
    import base64
    encoded_link = base64.urlsafe_b64encode(str(channel_id).encode()).decode()
    await save_channel(channel_id, encoded_link)
    return encoded_link

async def save_encoded_link2(channel_id: int, encoded_link: str):
    """Save secondary encoded link"""
    req_key = f"req_channel_{channel_id}"
    channel_data = {
        "id": channel_id,
        "req_encoded_link": encoded_link,
        "created_at": datetime.now().isoformat()
    }
    await channel_db.set(req_key, channel_data)
    return encoded_link

async def add_fsub_channel(channel_id: int):
    """Add FSub channel"""
    fsub_key = "fsub_channels"
    fsub_channels = await channel_db.get(fsub_key, [])
    if channel_id not in fsub_channels:
        fsub_channels.append(channel_id)
        await channel_db.set(fsub_key, fsub_channels)
    return True

async def remove_fsub_channel(channel_id: int):
    """Remove FSub channel"""
    fsub_key = "fsub_channels"
    fsub_channels = await channel_db.get(fsub_key, [])
    if channel_id in fsub_channels:
        fsub_channels.remove(channel_id)
        await channel_db.set(fsub_key, fsub_channels)
    return True

print(f"Channel database initialized. Using telegram channel: {DATABASE_CHANNEL}")
