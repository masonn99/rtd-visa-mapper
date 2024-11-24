# src/telegram_client.py
from telethon import TelegramClient
from telethon.tl.types import PeerChannel, PeerChat
import os
from dotenv import load_dotenv
import logging
from typing import List
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class TelegramMessageFetcher:
    def __init__(self):
        load_dotenv()
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not all([self.api_id, self.api_hash, self.chat_id]):
            raise ValueError("Missing Telegram credentials in .env file")
        
        self.client = TelegramClient('visa_session', self.api_id, self.api_hash)

    def _get_peer(self, chat_id: str):
        """Convert chat ID to proper peer format"""
        try:
            # Remove any leading -100 if present
            if chat_id.startswith('-100'):
                chat_id = chat_id[4:]
            elif chat_id.startswith('100'):
                chat_id = chat_id[3:]
                
            # Convert to integer
            chat_id = int(chat_id)
            
            # For supergroups and channels
            return PeerChannel(chat_id)
        except ValueError:
            logging.error(f"Invalid chat ID format: {chat_id}")
            raise

    async def fetch_recent_messages(self, days: int = 7) -> List[str]:
        """Fetch messages from the last n days"""
        messages = []
        date_from = datetime.now() - timedelta(days=days)
        
        try:
            async with self.client:
                # First try to get the chat entity
                try:
                    peer = self._get_peer(self.chat_id)
                    chat = await self.client.get_entity(peer)
                    logging.info(f"Successfully found chat: {chat.title if hasattr(chat, 'title') else chat.id}")
                except ValueError as e:
                    logging.error(f"Error getting chat: {str(e)}")
                    # Try alternative formats
                    chat_id = self.chat_id.strip()
                    if chat_id.startswith('@'):
                        chat = await self.client.get_entity(chat_id)
                    else:
                        # Try direct integer conversion
                        chat = await self.client.get_entity(int(chat_id))
                
                logging.info(f"Fetching messages from chat: {getattr(chat, 'title', chat.id)}")
                
                # Fetch messages
                async for message in self.client.iter_messages(
                    chat,
                    offset_date=date_from,
                    reverse=True
                ):
                    if message.text:
                        messages.append(message.text)
                        logging.info(f"Found message: {message.text[:50]}...")
                
                logging.info(f"Fetched {len(messages)} messages")
                return messages
                
        except Exception as e:
            logging.error(f"Error fetching messages: {str(e)}")
            return []

    async def list_all_chats(self):
        """List all accessible chats to help find the correct one"""
        try:
            async with self.client:
                logging.info("Listing all accessible chats...")
                async for dialog in self.client.iter_dialogs():
                    chat_type = "Group" if dialog.is_group else "Channel" if dialog.is_channel else "Chat"
                    print(f"\nName: {dialog.name}")
                    print(f"ID: {dialog.id}")
                    print(f"Type: {chat_type}")
                    if hasattr(dialog.entity, 'username'):
                        print(f"Username: @{dialog.entity.username}")
                    print("-" * 30)
        except Exception as e:
            logging.error(f"Error listing chats: {str(e)}")

# Add a test function
async def test_fetcher():
    fetcher = TelegramMessageFetcher()
    print("\nListing all available chats to help find the correct one...")
    await fetcher.list_all_chats()
    
    print("\nTrying to fetch messages...")
    messages = await fetcher.fetch_recent_messages(days=1)
    print(f"\nFetched {len(messages)} messages")
    for msg in messages[:5]:  # Show first 5 messages
        print(f"\n{msg}")
        print("-" * 30)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_fetcher())