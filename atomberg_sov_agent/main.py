import sys
import os

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from searcher import search_youtube_ddg, search_google_apify
from analyzer import SoVAnalyzer

def main():
    print("--- Atomberg Share of Voice (SoV) Agent ---")
    
    # Configuration
    QUERY = "smart ceiling fan india"
    N_RESULTS = 20 
    BRANDS = ["atomberg", "orient", "havells", "crompton", "ottomate", "polycab", "panasonic", "lg", "samsung"]
    
    all_results = []

    # 1. YouTube Search
    print(f"1. Searching for '{QUERY}' on YouTube (Top {N_RESULTS} results)...")
    yt_results = search_youtube_ddg(QUERY, N_RESULTS, region="in-en")
    if yt_results:
        print(f"   Found {len(yt_results)} YouTube results.")
        all_results.extend(yt_results)
    else:
        print("   No YouTube results found.")

    # 2. Google Search
    print(f"2. Searching for '{QUERY}' on Google (Top {N_RESULTS} results)...")
    google_results = search_google_apify(QUERY, N_RESULTS, country_code="IN")
    if google_results:
        print(f"   Found {len(google_results)} Google results.")
        all_results.extend(google_results)
    else:
        print("   No Google results found.")
    
    if not all_results:
        print("No results found from any source. Exiting.")
        return

    print("\n3. Analyzing Share of Voice...")
    analyzer = SoVAnalyzer(all_results, BRANDS)
    stats = analyzer.analyze()
    sov_data = analyzer.calculate_sov()
    
    print("\n--- Share of Voice Results (Combined) ---")
    print(f"{'Brand':<15} | {'Mentions':<10} | {'Views SoV':<10} | {'Composite SoV':<15}")
    print("-" * 60)
    
    # Sort by Composite SoV
    sorted_sov = sorted(sov_data.items(), key=lambda x: x[1]['composite_sov'], reverse=True)
    
    for brand, data in sorted_sov:
        mentions = stats[brand]['mentions']
        print(f"{brand.title():<15} | {mentions:<10} | {data['engagement_sov']:.2f}%      | {data['composite_sov']:.2f}%")
        
    print("\n--- Insights ---")
    insights = analyzer.get_insights()
    for insight in insights:
        print(f"- {insight}")
        
    print("\n--- Recommendations for Content & Marketing Team ---")
    print("1. **Cross-Platform Strategy**: Ensure consistency between YouTube video content and Google search articles.")
    print("2. **SEO & Video Synergy**: Embed top-performing YouTube videos in high-ranking blog posts to boost engagement.")
    print("3. **Influencer Collaboration**: Identify channels with high view counts (Engagement SoV) but low Atomberg mentions and partner with them.")
    print("4. **Competitive Benchmarking**: Analyze the top-performing videos of competitors to understand what content format (review, unboxing, comparison) works best.")
    print("5. **Sentiment Analysis**: Monitor comments on top videos to address user concerns and highlight positive feedback.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
