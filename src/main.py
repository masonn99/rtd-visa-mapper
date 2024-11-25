
import asyncio
import logging
from telegram_client import TelegramMessageFetcher
from message_processor import MessageProcessor
from extractor import VisaInfoExtractor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main():
    try:
        # Initialize components
        telegram_client = TelegramMessageFetcher()
        message_processor = MessageProcessor()
        visa_extractor = VisaInfoExtractor()

        # Step 1: Fetch messages from Telegram
        messages = await telegram_client.fetch_recent_messages()
        logging.info(f"Fetched {len(messages)} messages")

        if not messages:
            print("No messages were fetched")
            return

        # Step 2: Filter messages with country references
        filtered_results = message_processor.filter_country_messages(messages)
        
        print("\nMessages with country references:")
        print("=" * 50)
        for i, (msg, countries) in enumerate(filtered_results, 1):
            print(f"\nMessage {i}:")
            print("-" * 30)
            print(msg)
            print(f"Countries mentioned: {', '.join(countries)}")
            print("-" * 30)
        
        print(f"\nTotal messages with country references: {len(filtered_results)}")

        # Step 3: Process filtered messages with visa extractor
        if filtered_results:
            # Extract just the messages from the filtered results
            messages_to_process = [msg for msg, _ in filtered_results]
            
            # Process with visa extractor
            visa_results = visa_extractor.process_batch(messages_to_process)
            
            print("\nExtracted Visa Information:")
            print("=" * 50)
            
            if not visa_results:
                print("No visa information was extracted.")
            
            for entry in visa_results:
                print(f"\nCountry: {entry.get('country', 'Unknown')}")
                print(f"Visa Requirement: {entry.get('visaRequirement', 'Unknown')}")
                print(f"Duration: {entry.get('duration', 'Unknown')}")
                if entry.get('notes'):
                    print(f"Notes: {entry['notes']}")
                print("-" * 30)

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())