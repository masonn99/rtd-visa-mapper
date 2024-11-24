
import asyncio
import re
import logging
import pycountry
from telegram_client import TelegramMessageFetcher
from extractor import VisaInfoExtractor
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MessageProcessor:
    def __init__(self):
        # Create a set of country names and common variations
        self.country_keywords = set()
        
        # Add official country names and codes
        for country in pycountry.countries:
            # Add official name with word boundaries
            self.country_keywords.add(country.name.lower())
            # Add alpha-2 code (like US)
            self.country_keywords.add(country.alpha_2.lower())
            # Add alpha-3 code (like USA)
            self.country_keywords.add(country.alpha_3.lower())
        
        # Add common variations manually
        additional_countries = {
            'uk': ['uk', 'united kingdom', 'britain', 'great britain'],
            'usa': ['usa', 'united states', 'united states of america', 'america', 'us'],
            'uae': ['uae', 'united arab emirates', 'emirates'],
            'korea': ['south korea', 'north korea', 'dprk', 'rok'],
            'russia': ['russia', 'russian federation'],
            'china': ['china', 'prc', 'mainland china'],
            'taiwan': ['taiwan', 'roc', 'chinese taipei'],
            'vietnam': ['vietnam', 'viet nam'],
            'laos': ['laos', 'lao'],
            'iran': ['iran', 'islamic republic of iran'],
            'myanmar': ['myanmar', 'burma'],
        }
        
        for variations in additional_countries.values():
            self.country_keywords.update(variations)
            
        # Remove generic words that might cause false positives
        words_to_remove = {'country', 'countries', 'nation', 'foreign'}
        self.country_keywords = self.country_keywords - words_to_remove
        
        # Create regex pattern for word boundaries
        self.country_pattern = r'\b(' + '|'.join(map(re.escape, self.country_keywords)) + r')\b'

    def contains_country_reference(self, message: str) -> bool:
        """Check if message contains any country reference using word boundaries"""
        message_lower = message.lower()
        matches = re.findall(self.country_pattern, message_lower)
        
        if matches:
            logging.debug(f"Found country references in message: {matches}")
            return True
        return False

    def filter_country_messages(self, messages: List[str]) -> List[str]:
        """Filter messages to only those containing country references"""
        filtered = []
        
        for msg in messages:
            if self.contains_country_reference(msg):
                filtered.append(msg)
                logging.info(f"Found country reference in message: {msg[:100]}...")
        
        logging.info(f"Filtered {len(filtered)} messages containing country references from {len(messages)} total messages")
        return filtered

async def main():
    try:
        # Initialize components
        telegram_client = TelegramMessageFetcher()
        # visa_extractor = VisaInfoExtractor()
        message_processor = MessageProcessor()

        # Fetch messages
        messages = await telegram_client.fetch_recent_messages()
        logging.info(f"Fetched {len(messages)} messages")

        if messages:
            # Filter messages containing country references
            filtered_messages = message_processor.filter_country_messages(messages)
            
        #     if filtered_messages:
        #         # Process filtered messages
        #         results = visa_extractor.process_batch(filtered_messages)
                
        #         print("\nExtracted Visa Information:")
        #         print("=" * 50)
                
        #         if not results:
        #             print("No visa information was extracted.")
                
        #         for entry in results:
        #             print(f"\nCountry: {entry.get('country', 'Unknown')}")
        #             print(f"Visa Requirement: {entry.get('visaRequirement', 'Unknown')}")
        #             print(f"Duration: {entry.get('duration', 'Unknown')}")
        #             if entry.get('notes'):
        #                 print(f"Notes: {entry['notes']}")
        #             print("-" * 30)
        #     else:
        #         print("No messages containing country references were found.")
        # else:
            print("Filtered messages.................................... ")
            for message in filtered_messages:
                print(message)
                print("-" * 30)

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())