"""
News Web Scraper
-----------------
A flexible web scraper for extracting news articles from various news websites.
Supports multiple output formats (JSON, CSV, TXT) and includes rate limiting.

Author: Pasan11504
Date: 2025-10-05
Hacktoberfest 2025 Contribution
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import argparse
import logging
import time
from typing import List, Dict, Optional
from datetime import datetime
import sys
from urllib.parse import urljoin, urlparse


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class NewsScraper:
    """
    A web scraper for extracting news articles from websites.
    
    Attributes:
        url (str): The target URL to scrape
        user_agent (str): User-agent string for requests
        timeout (int): Request timeout in seconds
        rate_limit (float): Delay between requests in seconds
    """
    
    def __init__(self, url: str, user_agent: Optional[str] = None, 
                 timeout: int = 10, rate_limit: float = 1.0):
        """
        Initialize the news scraper.
        
        Args:
            url: Target website URL
            user_agent: Custom user-agent string (optional)
            timeout: Request timeout in seconds
            rate_limit: Delay between requests in seconds
        """
        self.url = url
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.user_agent = user_agent or (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        self.headers = {'User-Agent': self.user_agent}
        
    def fetch_page(self) -> Optional[BeautifulSoup]:
        """
        Fetch and parse the target webpage.
        
        Returns:
            BeautifulSoup object if successful, None otherwise
        """
        try:
            logger.info(f"Fetching page: {self.url}")
            response = requests.get(
                self.url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Respect rate limiting
            time.sleep(self.rate_limit)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            logger.info("Page fetched successfully")
            return soup
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    def extract_articles(self, soup: BeautifulSoup, limit: int = 10) -> List[Dict[str, str]]:
        """
        Extract article information from the parsed HTML.
        
        Args:
            soup: BeautifulSoup object containing parsed HTML
            limit: Maximum number of articles to extract
            
        Returns:
            List of dictionaries containing article information
        """
        articles = []
        
        try:
            # Generic selectors - works with many news sites
            # Try multiple common article container patterns
            article_containers = (
                soup.find_all('article', limit=limit) or
                soup.find_all('div', class_=['article', 'post', 'story'], limit=limit) or
                soup.find_all('div', {'data-testid': 'article'}, limit=limit)
            )
            
            if not article_containers:
                logger.warning("No article containers found. Trying headline extraction...")
                # Fallback: try to find headlines directly
                headlines = soup.find_all(['h1', 'h2', 'h3'], limit=limit)
                for idx, headline in enumerate(headlines, 1):
                    articles.append({
                        'id': idx,
                        'title': headline.get_text(strip=True),
                        'url': self._extract_link(headline),
                        'description': 'N/A',
                        'author': 'Unknown',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'scraped_at': datetime.now().isoformat()
                    })
                return articles
            
            logger.info(f"Found {len(article_containers)} article containers")
            
            for idx, article in enumerate(article_containers, 1):
                article_data = {
                    'id': idx,
                    'title': self._extract_title(article),
                    'url': self._extract_link(article),
                    'description': self._extract_description(article),
                    'author': self._extract_author(article),
                    'date': self._extract_date(article),
                    'scraped_at': datetime.now().isoformat()
                }
                articles.append(article_data)
                
            logger.info(f"Extracted {len(articles)} articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error extracting articles: {e}")
            return articles
    
    def _extract_title(self, article) -> str:
        """Extract article title."""
        title_tag = (
            article.find(['h1', 'h2', 'h3']) or
            article.find(class_=['title', 'headline']) or
            article.find('a')
        )
        return title_tag.get_text(strip=True) if title_tag else 'No title'
    
    def _extract_link(self, article) -> str:
        """Extract article URL."""
        link_tag = article.find('a', href=True)
        if link_tag:
            href = link_tag['href']
            # Convert relative URLs to absolute
            return urljoin(self.url, href)
        return 'No URL'
    
    def _extract_description(self, article) -> str:
        """Extract article description/summary."""
        desc_tag = (
            article.find('p') or
            article.find(class_=['description', 'summary', 'excerpt'])
        )
        return desc_tag.get_text(strip=True)[:200] if desc_tag else 'No description'
    
    def _extract_author(self, article) -> str:
        """Extract article author."""
        author_tag = (
            article.find(class_=['author', 'byline']) or
            article.find('span', {'rel': 'author'})
        )
        return author_tag.get_text(strip=True) if author_tag else 'Unknown'
    
    def _extract_date(self, article) -> str:
        """Extract article publication date."""
        date_tag = (
            article.find('time') or
            article.find(class_=['date', 'published', 'timestamp'])
        )
        if date_tag:
            # Try to get datetime attribute first
            date_str = date_tag.get('datetime', date_tag.get_text(strip=True))
            return date_str
        return datetime.now().strftime('%Y-%m-%d')


class OutputHandler:
    """Handle different output formats for scraped data."""
    
    @staticmethod
    def save_json(articles: List[Dict], filename: str = 'articles.json'):
        """Save articles to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(articles)} articles to {filename}")
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
    
    @staticmethod
    def save_csv(articles: List[Dict], filename: str = 'articles.csv'):
        """Save articles to CSV file."""
        try:
            if not articles:
                logger.warning("No articles to save")
                return
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=articles[0].keys())
                writer.writeheader()
                writer.writerows(articles)
            logger.info(f"Saved {len(articles)} articles to {filename}")
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
    
    @staticmethod
    def save_txt(articles: List[Dict], filename: str = 'articles.txt'):
        """Save articles to plain text file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for article in articles:
                    f.write(f"{'='*80}\n")
                    f.write(f"Title: {article['title']}\n")
                    f.write(f"URL: {article['url']}\n")
                    f.write(f"Author: {article['author']}\n")
                    f.write(f"Date: {article['date']}\n")
                    f.write(f"Description: {article['description']}\n")
                    f.write(f"{'='*80}\n\n")
            logger.info(f"Saved {len(articles)} articles to {filename}")
        except Exception as e:
            logger.error(f"Error saving TXT: {e}")
    
    @staticmethod
    def print_console(articles: List[Dict]):
        """Print articles to console."""
        print(f"\n{'='*80}")
        print(f"SCRAPED ARTICLES ({len(articles)} found)")
        print(f"{'='*80}\n")
        
        for article in articles:
            print(f"[{article['id']}] {article['title']}")
            print(f"    URL: {article['url']}")
            print(f"    Author: {article['author']} | Date: {article['date']}")
            print(f"    {article['description'][:100]}...")
            print()


def main():
    """Main function to run the news scraper."""
    parser = argparse.ArgumentParser(
        description='Web Scraper for News Articles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python news_scraper.py https://example-news.com
  python news_scraper.py https://example.com --limit 20 --format json
  python news_scraper.py https://news.site --format csv --output my_articles.csv
  python news_scraper.py https://blog.com --format all
        """
    )
    
    parser.add_argument('url', help='Target website URL to scrape')
    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=10,
        help='Maximum number of articles to scrape (default: 10)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'csv', 'txt', 'console', 'all'],
        default='console',
        help='Output format (default: console)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output filename (default: articles.[format])'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    parser.add_argument(
        '--rate-limit',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = NewsScraper(
        url=args.url,
        timeout=args.timeout,
        rate_limit=args.rate_limit
    )
    
    # Fetch and parse page
    soup = scraper.fetch_page()
    if not soup:
        logger.error("Failed to fetch page. Exiting.")
        sys.exit(1)
    
    # Extract articles
    articles = scraper.extract_articles(soup, limit=args.limit)
    
    if not articles:
        logger.warning("No articles found!")
        sys.exit(0)
    
    # Output results
    output_handler = OutputHandler()
    
    if args.format == 'json' or args.format == 'all':
        filename = args.output or 'articles.json'
        output_handler.save_json(articles, filename)
    
    if args.format == 'csv' or args.format == 'all':
        filename = args.output or 'articles.csv'
        output_handler.save_csv(articles, filename)
    
    if args.format == 'txt' or args.format == 'all':
        filename = args.output or 'articles.txt'
        output_handler.save_txt(articles, filename)
    
    if args.format == 'console' or args.format == 'all':
        output_handler.print_console(articles)
    
    logger.info("Scraping completed successfully!")


if __name__ == '__main__':
    main()
