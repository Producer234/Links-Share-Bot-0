# Simple in-memory database fallback
import base64
from datetime import datetime, timedelta
from typing import List, Optional

# In-memory storage
_users = set()
_channels = {}
_fsub_channels = set()
_admins = set()

async def add_user(user_id: int) -> bool:
    """Add a user to the database if they don't exist."""
    if not isinstance(user_id, int) or user_id <= 0:
        print(f"Invalid user_id: {user_id}")
        return False
    
    if user_id in _users:
        return False
    
    _users.add(user_id)
    return True

async def present_user(user_id: int) -> bool:
    """Check if a user exists in the database."""
    if not isinstance(user_id, int):
        return False
    return user_id in _users

async def full_userbase() -> List[int]:
    """Get all user IDs from the database."""
    return list(_users)

async def del_user(user_id: int) -> bool:
    """Delete a user from the database."""
    if user_id in _users:
        _users.remove(user_id)
        return True
    return False

async def is_admin(user_id: int) -> bool:
    """Check if a user is an admin."""
    try:
        user_id = int(user_id)
        return user_id in _admins
    except Exception as e:
        print(f"Error checking admin status for {user_id}: {e}")
        return False

async def add_admin(user_id: int) -> bool:
    """Add a user as admin."""
    try:
        user_id = int(user_id)
        _admins.add(user_id)
        return True
    except Exception as e:
        print(f"Error adding admin {user_id}: {e}")
        return False

async def remove_admin(user_id: int) -> bool:
    """Remove a user from admins."""
    try:
        if user_id in _admins:
            _admins.remove(user_id)
            return True
        return False
    except Exception as e:
        print(f"Error removing admin {user_id}: {e}")
        return False

async def list_admins() -> list:
    """List all admin user IDs."""
    return list(_admins)

async def save_channel(channel_id: int, encoded_link: str = None) -> bool:
    """Save a channel to the database with invite link expiration."""
    if not isinstance(channel_id, int):
        print(f"Invalid channel_id: {channel_id}")
        return False
    
    _channels[channel_id] = {
        "channel_id": channel_id,
        "encoded_link": encoded_link,
        "invite_link_expiry": None,
        "created_at": datetime.utcnow(),
        "status": "active"
    }
    return True

async def get_channels() -> List[int]:
    """Get all active channel IDs from the database."""
    return [cid for cid, data in _channels.items() if data.get("status") == "active"]

async def delete_channel(channel_id: int) -> bool:
    """Delete a channel from the database."""
    if channel_id in _channels:
        del _channels[channel_id]
        return True
    return False

async def save_encoded_link(channel_id: int) -> Optional[str]:
    """Save an encoded link for a channel and return it."""
    if not isinstance(channel_id, int):
        print(f"Invalid channel_id: {channel_id}")
        return None
    
    try:
        encoded_link = base64.urlsafe_b64encode(str(channel_id).encode()).decode()
        if channel_id not in _channels:
            _channels[channel_id] = {}
        _channels[channel_id].update({
            "encoded_link": encoded_link,
            "status": "active",
            "updated_at": datetime.utcnow()
        })
        return encoded_link
    except Exception as e:
        print(f"Error saving encoded link for channel {channel_id}: {e}")
        return None

async def get_channel_by_encoded_link(encoded_link: str) -> Optional[int]:
    """Get a channel ID by its encoded link."""
    if not isinstance(encoded_link, str):
        return None
    
    for cid, data in _channels.items():
        if data.get("encoded_link") == encoded_link and data.get("status") == "active":
            return cid
    return None

async def save_encoded_link2(channel_id: int, encoded_link: str) -> Optional[str]:
    """Save a secondary encoded link for a channel."""
    if not isinstance(channel_id, int) or not isinstance(encoded_link, str):
        print(f"Invalid input: channel_id={channel_id}, encoded_link={encoded_link}")
        return None
    
    if channel_id not in _channels:
        _channels[channel_id] = {}
    
    _channels[channel_id].update({
        "req_encoded_link": encoded_link,
        "status": "active",
        "updated_at": datetime.utcnow()
    })
    return encoded_link

async def get_channel_by_encoded_link2(encoded_link: str) -> Optional[int]:
    """Get a channel ID by its secondary encoded link."""
    if not isinstance(encoded_link, str):
        return None
    
    for cid, data in _channels.items():
        if data.get("req_encoded_link") == encoded_link and data.get("status") == "active":
            return cid
    return None

async def save_invite_link(channel_id: int, invite_link: str, is_request: bool) -> bool:
    """Save the current invite link for a channel and its type."""
    if not isinstance(channel_id, int) or not isinstance(invite_link, str):
        print(f"Invalid input: channel_id={channel_id}, invite_link={invite_link}")
        return False
    
    if channel_id not in _channels:
        _channels[channel_id] = {}
    
    _channels[channel_id].update({
        "current_invite_link": invite_link,
        "is_request_link": is_request,
        "invite_link_created_at": datetime.utcnow(),
        "status": "active"
    })
    return True

async def get_current_invite_link(channel_id: int) -> Optional[dict]:
    """Get the current invite link and its type for a channel."""
    if not isinstance(channel_id, int):
        return None
    
    data = _channels.get(channel_id)
    if data and "current_invite_link" in data:
        return {
            "invite_link": data["current_invite_link"],
            "is_request": data.get("is_request_link", False)
        }
    return None

async def add_fsub_channel(channel_id: int) -> bool:
    """Add a channel to the FSub list."""
    if not isinstance(channel_id, int):
        print(f"Invalid channel_id: {channel_id}")
        return False
    
    if channel_id in _fsub_channels:
        return False
    
    _fsub_channels.add(channel_id)
    return True

async def remove_fsub_channel(channel_id: int) -> bool:
    """Remove a channel from the FSub list."""
    if channel_id in _fsub_channels:
        _fsub_channels.remove(channel_id)
        return True
    return False

async def get_fsub_channels() -> List[int]:
    """Get all active FSub channel IDs."""
    return list(_fsub_channels)

async def get_original_link(channel_id: int) -> Optional[str]:
    """Get the original link stored for a channel (used by /genlink)."""
    if not isinstance(channel_id, int):
        return None
    
    data = _channels.get(channel_id)
    return data.get("original_link") if data else None

async def set_approval_off(channel_id: int, off: bool = True) -> bool:
    """Set approval_off flag for a channel."""
    if not isinstance(channel_id, int):
        print(f"Invalid channel_id: {channel_id}")
        return False
    
    if channel_id not in _channels:
        _channels[channel_id] = {}
    
    _channels[channel_id]["approval_off"] = off
    return True

async def is_approval_off(channel_id: int) -> bool:
    """Check if approval_off flag is set for a channel."""
    if not isinstance(channel_id, int):
        return False
    
    data = _channels.get(channel_id)
    return bool(data and data.get("approval_off", False))