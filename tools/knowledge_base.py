"""
Knowledge Base tool using FAISS for vector similarity search
"""
import json
import numpy as np
import faiss
from typing import List, Dict
from pathlib import Path
from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)


class KnowledgeBase:
    """Manages the FAISS vector store and document retrieval"""
    
    def __init__(self):
        self.index = None
        self.documents = []
        self.dimension = 1536  # text-embedding-ada-002 dimension
        self._initialized = False
    
    def _ensure_initialized(self):
        """Lazy initialization of the knowledge base"""
        if not self._initialized:
            self._load_or_create_index()
            self._initialized = True
    
    def _load_or_create_index(self):
        """Load existing FAISS index or create a new one"""
        if config.FAISS_INDEX_PATH.exists() and config.DOCUMENTS_PATH.exists():
            # Load existing index
            self.index = faiss.read_index(str(config.FAISS_INDEX_PATH))
            with open(config.DOCUMENTS_PATH, 'r') as f:
                self.documents = json.load(f)
            print(f"Loaded knowledge base with {len(self.documents)} documents")
        else:
            # Create new index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.documents = []
            self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample financial support documents"""
        sample_docs = [
            {
                "title": "Account Withdrawal Procedure",
                "content": "To withdraw funds from your investment account: 1) Log in to your account, 2) Navigate to 'Withdraw Funds', 3) Select the account and amount, 4) Choose your bank account, 5) Confirm the transaction. Withdrawals are processed within 2-3 business days. Minimum withdrawal is $100."
            },
            {
                "title": "Savings Account Interest Rates",
                "content": "Our high-yield savings account currently offers 4.5% APY (Annual Percentage Yield) on all balances. Interest is compounded daily and paid monthly. There are no minimum balance requirements and no monthly maintenance fees."
            },
            {
                "title": "Investment Account Types",
                "content": "We offer three main investment account types: 1) Individual Brokerage Account - for general investing with flexible withdrawals, 2) Traditional IRA - tax-deferred retirement account, 3) Roth IRA - after-tax retirement account with tax-free growth. Each has different contribution limits and tax implications."
            },
            {
                "title": "Account Security and Two-Factor Authentication",
                "content": "Protect your account with two-factor authentication (2FA). Enable it in Settings > Security. We support SMS codes, authenticator apps (Google Authenticator, Authy), and biometric authentication. 2FA adds an extra layer of security beyond your password."
            },
            {
                "title": "Trading Fees and Commission Structure",
                "content": "Stock and ETF trades are commission-free. Options trades are $0.65 per contract. Mutual fund trades may have fees depending on the fund. Cryptocurrency trading has a spread of 0.5-2% depending on market conditions. There are no account maintenance or inactivity fees."
            },
            {
                "title": "Account Funding Methods",
                "content": "Fund your account via: 1) ACH bank transfer (free, 3-5 business days), 2) Wire transfer ($25 fee, same day), 3) Check deposit (mobile check deposit available, 5-7 days), 4) Account transfer from another brokerage (ACATS transfer, 5-10 days). Minimum initial deposit is $500."
            },
            {
                "title": "Tax Documents and Reporting",
                "content": "Tax documents (1099 forms) are available by February 15th each year. Access them in Account > Tax Documents. We report all taxable events to the IRS including dividends, interest, and capital gains. You can download CSV files of all transactions for your records."
            },
            {
                "title": "Customer Support Hours and Contact",
                "content": "Customer support is available Monday-Friday 8am-8pm ET, Saturday 9am-5pm ET. Contact us via: phone (1-800-555-0123), email (support@fintechco.com), live chat (on website), or this AI assistant 24/7. For urgent account security issues, call our 24/7 security line at 1-800-555-9999."
            },
            {
                "title": "Dividend Reinvestment Program (DRIP)",
                "content": "Automatically reinvest dividends to purchase additional shares at no cost. Enable DRIP in your account settings for individual securities or all holdings. Fractional shares are supported. You can disable DRIP anytime to receive cash dividends instead."
            },
            {
                "title": "Account Closure Process",
                "content": "To close your account: 1) Sell or transfer all positions, 2) Withdraw remaining cash balance, 3) Submit closure request via Secure Message Center or call support, 4) Confirm closure. No fees for account closure. Keep records for tax purposes. Reopening requires a new application."
            }
        ]
        
        # Add documents and generate embeddings
        for doc in sample_docs:
            self.add_document(doc["title"], doc["content"])
        
        # Save the index
        self.save()
        print(f"Initialized knowledge base with {len(sample_docs)} sample documents")
    
    def add_document(self, title: str, content: str):
        """Add a document to the knowledge base"""
        # Create embedding
        text = f"{title}\n{content}"
        response = client.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=text
        )
        embedding = response.data[0].embedding
        
        # Add to FAISS index
        embedding_array = np.array([embedding], dtype='float32')
        self.index.add(embedding_array)
        
        # Store document
        self.documents.append({
            "title": title,
            "content": content,
            "full_text": text
        })
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for relevant documents"""
        self._ensure_initialized()
        
        if self.index.ntotal == 0:
            return []
        
        # Create query embedding
        response = client.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=query
        )
        query_embedding = np.array([response.data[0].embedding], dtype='float32')
        
        # Search FAISS index
        k = min(k, self.index.ntotal)  # Don't search for more docs than we have
        distances, indices = self.index.search(query_embedding, k)
        
        # Return matched documents
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc['distance'] = float(distance)
                results.append(doc)
        
        return results
    
    def save(self):
        """Save the FAISS index and documents to disk"""
        faiss.write_index(self.index, str(config.FAISS_INDEX_PATH))
        with open(config.DOCUMENTS_PATH, 'w') as f:
            json.dump(self.documents, f, indent=2)


# Global knowledge base instance
kb = KnowledgeBase()


def search_knowledge_base(query: str) -> str:
    """
    Search the internal knowledge base for relevant information.
    This is the main tool function used by the agent.
    """
    try:
        results = kb.search(query, k=3)
    except Exception as e:
        return f"Error accessing knowledge base: {str(e)}. Please ensure OPENAI_API_KEY is configured."
    
    if not results:
        return "No relevant information found in the knowledge base."
    
    # Format results
    formatted_results = []
    for i, doc in enumerate(results, 1):
        formatted_results.append(f"Result {i} - {doc['title']}:\n{doc['content']}")
    
    return "\n\n".join(formatted_results)

