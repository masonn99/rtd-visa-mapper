from transformers import pipeline
import json
from typing import List, Dict
import logging
import torch
import re

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class VisaInfoExtractor:
    def __init__(self, model_name: str = "google/flan-t5-xl"):
        try:
            logging.info("Initializing model pipeline...")
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logging.info(f"Using device: {device}")
            
            self.pipe = pipeline(
                "text2text-generation",
                model=model_name,
                device=device
            )
            logging.info("Model pipeline ready!")
        except Exception as e:
            logging.error(f"Error initializing model: {str(e)}")
            raise

    def _parse_response(self, response: str) -> Dict:
        """Parse the key-value response into a dictionary"""
        try:
            # Use regex to extract key-value pairs
            pattern = r'(\w+)\s*=\s*"([^"]*)"'
            matches = re.findall(pattern, response)
            
            if matches:
                return {key: value for key, value in matches}
            return None
            
        except Exception as e:
            logging.error(f"Error parsing response: {e}")
            return None

    def process_message(self, message: str) -> Dict:
        try:
            logging.info(f"Processing message: {message[:50]}...")
            
            prompt = f"""These are the chats from a group chat that travelers with Refugee Travel Document share their travel experience. RTD stands for REfugee Travel Document. Extract visa information from this text and output ONLY a JSON object.

Text: {message}

The JSON must contain these exact fields:
- country: the country mentioned
- visaRequirement: the visa requirement (must be one of: "Visa required", "Visa not required", "E-Visa", or "Does not recognize RTD")
- duration: how long one can stay (use "N/A" if not mentioned)
- notes: just add some notes that might be helpful (use "N/A" if there is nothing signiicant. .e.g. Visa application takes 3 months, or something like that might )

Output the JSON only, no other text."""

            # Generate response
            response = self.pipe(
                prompt,
                max_length=256,
                num_return_sequences=1,
                temperature=0,  # Deterministic output
                do_sample=False
            )[0]['generated_text'].strip()
            
            logging.info(f"Raw response: {response}")
            
            # Parse the response into a dictionary
            result = self._parse_response(response)
            if result:
                logging.info(f"Parsed result: {result}")
            return result

        except Exception as e:
            logging.error(f"Error in process_message: {str(e)}")
            return None

    def process_batch(self, messages: List[str]) -> List[Dict]:
        results = []
        unique_countries = set()
        
        logging.info(f"Processing batch of {len(messages)} messages")
        for message in messages:
            info = self.process_message(message)
            if info and info.get('country') and info['country'] not in unique_countries:
                results.append(info)
                unique_countries.add(info['country'])
                logging.info(f"Added result for {info['country']}")
        
        return results