from extractor import VisaInfoExtractor
import logging
def main():
    try:
        # Initialize extractor
        extractor = VisaInfoExtractor()
        
        # Test messages
        messages = [
            "Just entered Germany with RTD, no visa needed for 90 days!",
            "UK requires visa application through VFS, got 180 days",
            "Japan embassy requires in-person visa application for RTD holders",
            "I went in the Chinese embassy and they were confused about the document at first, and they said it is impossible. but then after several inquiries, they finally gave me the visa"
  
        ]
        
        # Process messages
        logging.info("Starting message processing...")
        results = extractor.process_batch(messages)
        print("here is the result....")
        print(results)
        print(type(results))

        
        # Print results
        print("\nExtracted Visa Information:")
        print("=" * 50)
        
        if not results:
            print("No results were extracted. Please check the logs for details.")
        
        for entry in results:
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
    main()