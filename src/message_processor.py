# src/message_processor.py
import logging
import pycountry
import re
from typing import List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MessageProcessor:
    def __init__(self):
        self.country_keywords = set()
        
        # Add official country names
        for country in pycountry.countries:
            self.country_keywords.add(country.name.lower())
        
        # Add common variations manually
        additional_countries = {
            'uk': ['uk', 'united kingdom', 'britain', 'great britain'],
            'usa': ['usa', 'united states', 'united states of america', 'america'],
            'uae': ['uae', 'united arab emirates', 'emirates', 'dubai'],
            'korea': ['south korea', 'north korea'],
            'russia': ['russia', 'russian federation'],
            'china': ['china', 'mainland china'],
            'taiwan': ['taiwan'],
            'vietnam': ['vietnam'],
            'laos': ['laos'],
            'iran': ['iran'],
            'myanmar': ['myanmar', 'burma'],
        }
        
        for variations in additional_countries.values():
            self.country_keywords.update(variations)

        # Create regex pattern for countries with word boundaries
        self.country_pattern = r'\b(?:' + '|'.join(re.escape(k) for k in self.country_keywords) + r')\b'

    def find_countries(self, message: str) -> list:
        """Find all country references in a message"""
        message_lower = message.lower()
        matches = re.findall(self.country_pattern, message_lower)
        if matches:
            logging.info(f"Found countries in message: {matches}")
        return matches

    def filter_country_messages(self, messages: List[str]) -> List[Tuple[str, list]]:
        """
        Filter messages containing country references
        Returns: List of tuples (message, country_matches)
        """
        filtered = []
        
        for msg in messages:
            countries = self.find_countries(msg)
            if countries:
                filtered.append((msg, countries))
        
        logging.info(f"Filtered {len(filtered)} messages with country references from {len(messages)} total")
        return filtered