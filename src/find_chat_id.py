# find the chat_id of a telegram group
import asyncio
from telegram_client import TelegramMessageFetcher

async def find_chat():
    fetcher = TelegramMessageFetcher()
    print("\nListing all your Telegram chats to help find the RTD group...")
    await fetcher.list_all_chats()

if __name__ == "__main__":
    asyncio.run(find_chat())