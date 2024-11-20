from extractor import VisaInfoExtractor  # Update this import

def main():
    try:
        # Initialize extractor
        extractor = VisaInfoExtractor()
        
        # Test messages
        messages = [
            "Just entered Germany with RTD, no visa needed for 90 days!",
            "UK requires visa application through VFS, got 90 days",
            "Japan embassy requires in-person visa application for RTD holders"
        ]
        
        # Process messages
        print("Processing messages...")
        results = extractor.process_batch(messages)
        
        # Print results
        print("\nExtracted Visa Information:")
        print("=" * 50)
        for entry in results:
            print(f"\nCountry: {entry.get('country', 'Unknown')}")
            print(f"Visa Requirement: {entry.get('visaRequirement', 'Unknown')}")
            print(f"Duration: {entry.get('duration', 'Unknown')}")
            print(f"Notes: {entry.get('notes', '')}")
            print("-" * 30)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()