# Overview

This is a Telegram Links Sharing Bot built with Python and Pyrogram that helps manage and share private Telegram channel links securely. The bot creates temporary invite links that automatically revoke after 5 minutes to prevent copyright issues, supports bulk link management, and includes auto-approval features for join requests.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Bot Framework
- **Pyrogram Client**: Main bot framework using pyrofork==2.3.59 for Telegram API interactions
- **Async Architecture**: Built with asyncio for handling concurrent operations like link generation and auto-approval
- **Plugin System**: Modular plugin architecture with separate files for different functionalities (admin, approval, channels, etc.)

## Database Layer
- **Fallback System**: Currently uses simple in-memory storage (`simple_database.py`) as a fallback
- **MongoDB Ready**: Configured for MongoDB integration with connection strings and database name setup
- **Data Models**: Stores users, channels, admins, FSub channels, and encoded links

## Web Server Integration
- **aiohttp Server**: Runs a web server on port 5000 for health checks and potential webhook endpoints
- **Route Handling**: Basic routing system for web responses

## Security & Access Control
- **Multi-tier Admin System**: Owner-only commands and admin-level permissions
- **User Authentication**: Filter system to verify admin status before executing privileged commands
- **Temporary Links**: Auto-revocation of invite links after 5 minutes for security

## Link Management System
- **Base64 Encoding**: Encodes channel IDs and links for secure sharing
- **Dual Link Types**: Support for both normal invite links and join request links
- **Bulk Operations**: Can manage multiple channels and generate links in batch

## Auto-Approval System
- **Join Request Handling**: Automatically processes and approves join requests with configurable delays
- **Channel-specific Settings**: Can enable/disable auto-approval per channel
- **Spam Protection**: Rate limiting and temporary bans for users who spam commands

## Message Broadcasting
- **Mass Communication**: Built-in broadcast system for sending messages to all users
- **Cancellation Support**: Ability to cancel ongoing broadcast operations

# External Dependencies

## Required APIs
- **Telegram Bot API**: Requires BOT_TOKEN from @Botfather
- **Telegram App API**: Needs APP_ID and API_HASH from my.telegram.org

## Database Services
- **MongoDB**: Configured for persistent storage (currently using fallback)
- **Connection String**: Expects DATABASE_URL environment variable

## Python Libraries
- **pyrogram/pyrofork**: Telegram MTProto API wrapper
- **TgCrypto**: Cryptographic functions for Telegram
- **aiohttp**: Async HTTP client/server
- **motor**: Async MongoDB driver
- **pymongo**: MongoDB Python driver

## Deployment Platforms
- **Heroku**: Configured with app.json for one-click deployment
- **Koyeb**: Alternative deployment option
- **Docker**: Can be containerized for various cloud platforms

## Environment Variables
- **TG_BOT_TOKEN**: Bot authentication token
- **OWNER_ID**: Primary administrator user ID
- **ADMINS**: Space-separated list of admin user IDs
- **APP_ID/API_HASH**: Telegram application credentials
- **DATABASE_URL/DATABASE_NAME**: MongoDB connection details