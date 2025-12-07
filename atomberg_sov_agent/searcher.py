from duckduckgo_search import DDGS
from apify_client import ApifyClient
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def search_youtube_ddg(query, max_results=20, region="in-en"):
    """
    Searches DuckDuckGo Videos for the given query.
    """
    logging.info(f"Searching for '{query}' on DuckDuckGo Videos (Region: {region})...")
    results = []
    try:
        with DDGS() as ddgs:
            search_gen = ddgs.videos(query, region=region, max_results=max_results)
            for r in search_gen:
                views = "0"
                if 'statistics' in r and 'viewCount' in r['statistics']:
                    views = str(r['statistics']['viewCount'])
                
                results.append({
                    'source': 'youtube',
                    'title': r.get('title'),
                    'href': r.get('content'),
                    'body': r.get('description'),
                    'views': views,
                    'channel': r.get('uploader')
                })
                
        logging.info(f"Successfully retrieved {len(results)} YouTube results.")
        return results
    except Exception as e:
        logging.error(f"An error occurred during YouTube search: {e}")
        return []

def search_google_apify(query, max_results=20, country_code="IN"):
    """
    Searches Google using Apify's Google Search Scraper.
    """
    api_token = os.getenv('APIFY_API_TOKEN')
    if not api_token:
        logging.error("APIFY_API_TOKEN not found in environment variables.")
        return []

    logging.info(f"Searching for '{query}' on Google (Apify)...")
    
    try:
        client = ApifyClient(api_token)
        
       
        run_input = {
            "queries": query, 
            "resultsPerPage": max_results,
            "countryCode": country_code.lower(), # Apify expects lowercase country code
            "maxPagesPerQuery": 1,
        }

      
        run = client.actor("apify/google-search-scraper").call(run_input=run_input)

        # Fetch and print Actor results from the run's dataset (if there are any)
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            organic_results = item.get('organicResults', [])
            for res in organic_results:
                results.append({
                    'source': 'google',
                    'title': res.get('title'),
                    'href': res.get('url'),
                    'body': res.get('description'),
                    'position': res.get('position')
                })
                if len(results) >= max_results:
                    break
            if len(results) >= max_results:
                break
                
        logging.info(f"Successfully retrieved {len(results)} Google results.")
        return results

    except Exception as e:
        logging.error(f"An error occurred during Google search: {e}")
        return []


if __name__ == "__main__":
    # Test the search function
    print("Testing YouTube Search...")
    res_yt = search_youtube_ddg("smart ceiling fan", 2)
    for item in res_yt:
        print(item)
        
    print("\nTesting Google Search...")
    res_g = search_google_apify("smart ceiling fan", 2)
    for item in res_g:
        print(item)
