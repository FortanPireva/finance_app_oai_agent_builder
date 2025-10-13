"""
Agent tools for the FinTech Support Chatbot
"""
from .knowledge_base import search_knowledge_base
from .web_search import search_web, get_market_data
from .code_interpreter import run_python_code, calculate, calculate_compound_interest, analyze_investment_returns

__all__ = [
    'search_knowledge_base',
    'search_web',
    'get_market_data',
    'run_python_code',
    'calculate',
    'calculate_compound_interest',
    'analyze_investment_returns',
]

