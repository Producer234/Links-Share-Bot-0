 

# Database mode configuration
from config import DATABASE_MODE, DATABASE_CHANNEL

try:
    if DATABASE_MODE == "channel_logs":
        # Use telegram channel database
        from .channel_database import *
        print(f"Using telegram channel database. Data stored in channel: {DATABASE_CHANNEL}")
    else:
        # Use simple database
        from .simple_database import *
        print("Using simple in-memory database. Data will not persist between restarts.")
        print("Note: Set DATABASE_MODE to 'channel_logs' to use telegram channel storage")
except Exception as e:
    print(f"Error loading database, falling back to simple database: {e}")
    from .simple_database import *
    print("Using simple in-memory database. Data will not persist between restarts.")