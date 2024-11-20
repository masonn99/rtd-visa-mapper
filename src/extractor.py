from transformers import pipeline
import json
from typing import List, Dict

class VisaInfoExtractor:
    def __init__(self, model_name: str = "meta-llama/Llama-2-7b-chat-hf"):
        """
        Initialize the extractor with Meta's Llama model.
        Make sure to run 'huggingface-cli login' first.
        """
        print("Initializing model pipeline...")
        self.pipe = pipeline(
            "text-generation",
            model=model_name,
            max_length=512,
            temperature=0.1,
            device_map="auto"
        )
        print("Model pipeline ready!")

    def process_message(self, message: str) -> Dict:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts visa requirement information from text."},
            {"role": "user", "content": f"""
            Extract visa requirement information for refugee travel document holders from this message
            and format it exactly like this JSON structure:
            {{
                "country": "",
                "visaRequirement": "Visa required/Visa not required/E-Visa/Does not recognize US issued Refugee Travel Document",
                "duration": "90 days or N/A",
                "notes": ""
            }}
            
            Message: {message}
            """}
        ]
        
        response = self.pipe(messages)[0]['generated_text']
        try:
            json_str = response[response.find('{'):response.rfind('}')+1]
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None

    def process_batch(self, messages: List[str]) -> List[Dict]:
        results = []
        unique_countries = set()
        
        for message in messages:
            info = self.process_message(message)
            if info and info['country'] not in unique_countries:
                results.append(info)
                unique_countries.add(info['country'])
                
        return results