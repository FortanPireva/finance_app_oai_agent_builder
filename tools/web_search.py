"""
Web Search tool for retrieving external information
"""
import requests
from typing import Optional
import config


def search_web(query: str) -> str:
    """
    Search the web for external information like market data, news, etc.
    This uses a simple search API (can be replaced with your preferred service).
    """
    try:
        # Using DuckDuckGo Instant Answer API as a simple example
        # In production, you might use Google Custom Search, Bing API, or a financial data API
        
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        
        response = requests.get(
            'https://api.duckduckgo.com/',
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Try to extract relevant information
            result_parts = []
            
            if data.get('AbstractText'):
                result_parts.append(f"Summary: {data['AbstractText']}")
            
            if data.get('Answer'):
                result_parts.append(f"Answer: {data['Answer']}")
            
            # Add related topics if available
            if data.get('RelatedTopics'):
                topics = []
                for topic in data['RelatedTopics'][:3]:
                    if isinstance(topic, dict) and topic.get('Text'):
                        topics.append(topic['Text'])
                if topics:
                    result_parts.append(f"Related: {' | '.join(topics)}")
            
            if result_parts:
                return '\n\n'.join(result_parts)
            else:
                return f"Search completed but no detailed results found for: {query}. For real-time market data, please check financial websites like Yahoo Finance or Bloomberg."
        
        return f"Unable to fetch web results at this time. Status code: {response.status_code}"
    
    except requests.Timeout:
        return "Web search timed out. Please try again or rephrase your query."
    except Exception as e:
        return f"Web search error: {str(e)}. For financial market data, please refer to official financial news sources."


def get_market_data(symbol: str) -> str:
    """
    Specialized function to get market data for stocks/crypto.
    Note: This is a placeholder. In production, integrate with a real financial API.
    """
    # In production, integrate with APIs like:
    # - Alpha Vantage
    # - Yahoo Finance API
    # - Twelve Data
    # - CoinGecko (for crypto)
    
    return f"""
    Market data retrieval for {symbol}:
    
    Note: This is a demo environment. For real-time market data, please:
    1. Visit financial websites like Yahoo Finance, Bloomberg, or MarketWatch
    2. Use your brokerage platform's market data tools
    3. Check cryptocurrency exchanges for crypto prices
    
    To enable live market data in this chatbot, configure a financial data API key in the settings.
    """

