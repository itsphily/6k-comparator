import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sec_api import QueryApi

# Load environment variables
load_dotenv()

def fetch_recent_6k(ticker, num_filings=12):
    """
    Fetch the most recent 6-K filings URLs for any company
    """
    # Initialize the API with key from environment variables
    api_key = os.getenv('SEC_API_KEY')
    query_api = QueryApi(api_key=api_key)

    # Set up search parameters for the company's latest 6-K filings
    search_params = {
        "query": f'formType:"6-K" AND ticker:"{ticker}"',
        "from": "0",
        "size": str(num_filings),  # Get the specified number of filings
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    try:
        # Make the API request
        response = query_api.get_filings(search_params)
        
        if response and "filings" in response and response["filings"]:
            filings = response["filings"]
            
            # Write results to text file
            with open('recent_6k_filings.txt', 'w', encoding='utf-8') as f:
                f.write(f"Recent {ticker} 6-K Filings\n")
                f.write("=" * 80 + "\n\n")
                
                for i, filing in enumerate(filings, 1):
                    f.write(f"Filing #{i}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Filed At: {filing.get('filedAt', 'N/A')}\n")
                    f.write(f"Period of Report: {filing.get('periodOfReport', 'N/A')}\n")
                    f.write(f"URL: {filing.get('linkToFilingDetails')}\n\n")
            
            # Print to console as well
            print(f"\nFound {len(filings)} 6-K filings for {ticker}")
            print("Results have been saved to 'recent_6k_filings.txt'")
            
            return True
        else:
            print(f"No 6-K filings found for ticker {ticker}")
            return False

    except Exception as e:
        print(f"Error fetching filings: {str(e)}")
        return False

if __name__ == "__main__":
    ticker = input("Enter the stock ticker: ").upper()
    fetch_recent_6k(ticker)