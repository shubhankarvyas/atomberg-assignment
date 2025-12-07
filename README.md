# Atomberg Share of Voice (SoV) Agent

This repository contains an AI agent designed to quantify the Share of Voice (SoV) for Atomberg in the "smart fan" category.

## Page 1: Tech Stack and Tools

### Tech Stack
*   **Language**: Python 3.13
*   **Search Engines**:
    *   **DuckDuckGo (via `duckduckgo-search`)**: Used for fetching YouTube video results without API costs.
    *   **Google Search (via Apify `google-search-scraper`)**: Used for fetching organic text search results.
*   **Analysis Libraries**:
    *   **TextBlob**: For sentiment analysis of titles and descriptions.
    *   **Pandas/Collections**: For data aggregation (implied in logic).
*   **Environment Management**: `python-dotenv` for secure API key management.

### Tools Used
*   **VS Code**: IDE for development.
*   **GitHub Copilot**: AI Pair Programmer for code generation and debugging.
*   **Apify**: Cloud scraping platform for Google Search results.

### Supplementary Content
*   **GitHub Repository**: [https://github.com/shubhankarvyas/atomberg-assignment](https://github.com/shubhankarvyas/atomberg-assignment)
*   **Demo**: To run the demo locally, follow the setup instructions below.

### Setup & Usage
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    python -m textblob.download_corpora
    ```
2.  **Configure Environment**:
    Create a `.env` file:
    ```env
    APIFY_API_TOKEN=your_apify_api_token_here
    ```
3.  **Run the Agent**:
    ```bash
    python atomberg_sov_agent/main.py
    ```

---

## Page 2: Findings and Recommendations

### Findings (Sample Run)
*   **Dominant Brand**: Atomberg consistently appears as a top contender with a **Composite SoV of ~30-33%**.
*   **Visibility vs. Engagement**:
    *   **Mentions**: Atomberg leads in mentions (~42-47%), indicating strong SEO and content quantity.
    *   **Engagement**: Competitors like **LG** often have higher engagement (Views SoV ~53%) despite fewer videos, driven by specific high-performing viral or ad-boosted content.
*   **Sentiment**: Sentiment across top results is generally neutral to positive for Atomberg.

### Recommendations for Atomberg’s Team

1.  **Cross-Platform Consistency**:
    *   Ensure that the strong presence on YouTube is matched by high-quality articles ranking on Google. The agent found discrepancies between video and text dominance.

2.  **Boost Engagement Quality**:
    *   While Atomberg has *many* videos, they average fewer views than LG's top hits. Focus on **"Hero Content"**—high-production value videos designed to go viral or be used in ads—rather than just volume.

3.  **Influencer Partnerships**:
    *   Identify the specific channels driving LG's high view counts (e.g., "LG India", major tech reviewers) and target similar high-tier influencers for Atomberg reviews.

4.  **Leverage "Smart" Keywords**:
    *   Competitors are ranking for specific long-tail keywords like "smart ceiling fan price" or "best smart fan 2025". Create targeted content (blogs/videos) for these specific queries to capture intent.

5.  **Sentiment Monitoring**:
    *   Continue monitoring comments on the high-ranking videos. Addressing user questions in the comments of *competitor* reviews (where appropriate/allowed) or your own can boost community sentiment.

## Project Structure
- `atomberg_sov_agent/`
  - `main.py`: Orchestrator.
  - `searcher.py`: Search logic (DuckDuckGo + Apify).
  - `analyzer.py`: SoV and Sentiment calculation.
- `requirements.txt`: Dependencies.
