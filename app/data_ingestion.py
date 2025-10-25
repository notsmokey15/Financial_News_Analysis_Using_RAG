import sys
import requests
from .config import NEWS_API_KEY
from .rag_core import add_documents_to_db

def fetch_financial_news(topic: str):
    """Fetches financial news articles from NewsAPI for a given topic."""
    print(f"Fetching news for topic: {topic}...")
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={topic}&"
        "sortBy=publishedAt&"
        "language=en&"
        f"apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        print(f"Found {len(articles)} articles.")
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def ingest_news(topic: str):
    """Main function to fetch news for a specific topic and add it to the DB."""
    articles = fetch_financial_news(topic)
    if articles:
        documents = [article['content'] for article in articles if article['content']]
        metadatas = [{'source': article['source']['name'], 'title': article['title']} for article in articles if article['content']]
        
        add_documents_to_db(documents, metadatas)
        print(f"News ingestion for '{topic}' complete.")
    else:
        print(f"No articles to ingest for '{topic}'.")

if __name__ == "__main__":
    # This part now reads the topic from your terminal command
    if len(sys.argv) > 1:
        topic_to_ingest = sys.argv[1]
        ingest_news(topic_to_ingest)
    else:
        # If no topic is provided, it will default to "NVIDIA"
        print("No topic provided. Ingesting news for the default topic: NVIDIA")
        ingest_news("NVIDIA")
