from textblob import TextBlob
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SoVAnalyzer:
    def __init__(self, results, brands):
        """
        Initializes the analyzer with search results and a list of brands.
        
        Args:
            results (list): List of search result dictionaries.
            brands (list): List of brand names to track.
        """
        self.results = results
        self.brands = [b.lower() for b in brands]
        self.stats = defaultdict(lambda: {'mentions': 0, 'sentiment_score': 0.0, 'weighted_score': 0.0, 'total_views': 0})

    def parse_views(self, view_text):
        """
        Parses view count string (e.g., '1.2M views', '50K views') into an integer.
        """
        if not view_text:
            return 0
        
        text = view_text.lower().replace('views', '').replace('view', '').strip()
        if not text:
            return 0
            
        multiplier = 1
        if 'k' in text:
            multiplier = 1000
            text = text.replace('k', '')
        elif 'm' in text:
            multiplier = 1000000
            text = text.replace('m', '')
        elif 'b' in text:
            multiplier = 1000000000
            text = text.replace('b', '')
            
        try:
            return int(float(text) * multiplier)
        except ValueError:
            return 0

    def analyze(self):
        """
        Performs the analysis on the search results.
        """
        logging.info("Starting analysis of search results...")
        
        for rank, item in enumerate(self.results):
            # Combine title and body for analysis
            text = f"{item.get('title', '')} {item.get('body', '')} {item.get('channel', '')}".lower()
            
            source = item.get('source', 'unknown')
            views = 0
            if source == 'youtube':
                views = self.parse_views(item.get('views', '0'))
            
            # Sentiment analysis of the snippet
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity # -1 to 1
            
            # Rank weight: Top results matter more. 
            rank_weight = 1 / (rank + 1)
            
            for brand in self.brands:
                if brand in text:
                    self.stats[brand]['mentions'] += 1
                    self.stats[brand]['sentiment_score'] += sentiment
                    
                    if source == 'youtube':
                        self.stats[brand]['total_views'] += views
                    
                    # Weighted score: 
                    # For YouTube: (1 + Sentiment) * Rank_Weight
                    # For Google: (1 + Sentiment) * Rank_Weight * 1.5 (Give slightly more weight to SEO dominance?)
                    self.stats[brand]['weighted_score'] += (1 + sentiment) * rank_weight
        
        logging.info("Analysis complete.")
        return self.stats

    def calculate_sov(self):
        """
        Calculates the Share of Voice percentage for each brand.
        Returns a dictionary with 'mention_sov' and 'engagement_sov'.
        """
        total_mentions = sum(s['mentions'] for s in self.stats.values())
        total_views = sum(s['total_views'] for s in self.stats.values())
        
        sov_data = {}
        
        for brand, data in self.stats.items():
            m_sov = (data['mentions'] / total_mentions * 100) if total_mentions > 0 else 0
            v_sov = (data['total_views'] / total_views * 100) if total_views > 0 else 0
            
            # Composite SoV: 50% Mentions, 50% Engagement
            c_sov = (m_sov * 0.5) + (v_sov * 0.5)
            
            sov_data[brand] = {
                'mention_sov': m_sov,
                'engagement_sov': v_sov,
                'composite_sov': c_sov
            }
            
        return sov_data

    def get_insights(self):
        """
        Generates insights based on the analysis.
        """
        insights = []
        
        sov = self.calculate_sov()
        # Sort by Composite SoV
        sorted_brands = sorted(sov.items(), key=lambda x: x[1]['composite_sov'], reverse=True)
        
        if not sorted_brands:
            return ["No brands detected in the top results."]

        top_brand = sorted_brands[0][0]
        top_score = sorted_brands[0][1]['composite_sov']
        insights.append(f"The dominant brand is '{top_brand.title()}' with a Composite SoV of {top_score:.2f}%.")
        
        # Check Atomberg specifically
        if 'atomberg' in sov:
            atom_data = sov['atomberg']
            insights.append(f"Atomberg: Mentions SoV: {atom_data['mention_sov']:.2f}%, Engagement (Views) SoV: {atom_data['engagement_sov']:.2f}%.")
            
            if atom_data['engagement_sov'] > atom_data['mention_sov']:
                insights.append("Atomberg's content is highly engaging (high views per mention).")
            elif atom_data['mention_sov'] > atom_data['engagement_sov']:
                insights.append("Atomberg has good visibility but lower engagement compared to competitors.")
        
        return insights
