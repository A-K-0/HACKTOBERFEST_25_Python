"""
Unit Tests for News Web Scraper
--------------------------------
Test suite for the news_scraper module using pytest.

Author: Pasan11504
Date: 2025-10-05
"""

import pytest
from bs4 import BeautifulSoup
from news_scraper import NewsScraper, OutputHandler
import json
import csv
import os


class TestNewsScraper:
    """Test cases for NewsScraper class."""
    
    def test_scraper_initialization(self):
        """Test scraper initialization with default values."""
        scraper = NewsScraper('https://example.com')
        assert scraper.url == 'https://example.com'
        assert scraper.timeout == 10
        assert scraper.rate_limit == 1.0
        assert 'Mozilla' in scraper.user_agent
    
    def test_scraper_custom_initialization(self):
        """Test scraper with custom parameters."""
        scraper = NewsScraper(
            'https://test.com',
            user_agent='CustomAgent',
            timeout=20,
            rate_limit=2.0
        )
        assert scraper.user_agent == 'CustomAgent'
        assert scraper.timeout == 20
        assert scraper.rate_limit == 2.0
    
    def test_extract_title(self):
        """Test title extraction from article."""
        html = '<article><h2>Test Article Title</h2></article>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        scraper = NewsScraper('https://example.com')
        title = scraper._extract_title(article)
        
        assert title == 'Test Article Title'
    
    def test_extract_title_fallback(self):
        """Test title extraction fallback when no h2 present."""
        html = '<article><a>Link Title</a></article>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        scraper = NewsScraper('https://example.com')
        title = scraper._extract_title(article)
        
        assert title == 'Link Title'
    
    def test_extract_link(self):
        """Test URL extraction from article."""
        html = '<article><a href="/article-1">Title</a></article>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        scraper = NewsScraper('https://example.com')
        url = scraper._extract_link(article)
        
        assert url == 'https://example.com/article-1'
    
    def test_extract_link_absolute_url(self):
        """Test URL extraction with absolute URL."""
        html = '<article><a href="https://other.com/article">Title</a></article>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        scraper = NewsScraper('https://example.com')
        url = scraper._extract_link(article)
        
        assert url == 'https://other.com/article'
    
    def test_extract_description(self):
        """Test description extraction."""
        html = '<article><p>This is a test description for the article.</p></article>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        scraper = NewsScraper('https://example.com')
        description = scraper._extract_description(article)
        
        assert 'test description' in description
    
    def test_extract_author(self):
        """Test author extraction."""
        html = '<article><span class="author">John Doe</span></article>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        scraper = NewsScraper('https://example.com')
        author = scraper._extract_author(article)
        
        assert author == 'John Doe'
    
    def test_extract_author_fallback(self):
        """Test author extraction fallback to Unknown."""
        html = '<article><h2>Title</h2></article>'
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('article')
        
        scraper = NewsScraper('https://example.com')
        author = scraper._extract_author(article)
        
        assert author == 'Unknown'
    
    def test_extract_articles(self):
        """Test article extraction from HTML."""
        html = '''
        <article>
            <h2>Article 1</h2>
            <a href="/article-1">Read more</a>
            <p>Description 1</p>
        </article>
        <article>
            <h2>Article 2</h2>
            <a href="/article-2">Read more</a>
            <p>Description 2</p>
        </article>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        
        scraper = NewsScraper('https://example.com')
        articles = scraper.extract_articles(soup, limit=2)
        
        assert len(articles) == 2
        assert articles[0]['title'] == 'Article 1'
        assert articles[1]['title'] == 'Article 2'
        assert 'id' in articles[0]
        assert 'scraped_at' in articles[0]
    
    def test_extract_articles_with_limit(self):
        """Test article extraction respects limit."""
        html = ''.join([
            f'<article><h2>Article {i}</h2></article>' 
            for i in range(1, 11)
        ])
        soup = BeautifulSoup(html, 'html.parser')
        
        scraper = NewsScraper('https://example.com')
        articles = scraper.extract_articles(soup, limit=5)
        
        assert len(articles) == 5


class TestOutputHandler:
    """Test cases for OutputHandler class."""
    
    @pytest.fixture
    def sample_articles(self):
        """Sample articles for testing."""
        return [
            {
                'id': 1,
                'title': 'Test Article 1',
                'url': 'https://example.com/1',
                'description': 'Test description 1',
                'author': 'Author 1',
                'date': '2025-10-05',
                'scraped_at': '2025-10-05T10:00:00'
            },
            {
                'id': 2,
                'title': 'Test Article 2',
                'url': 'https://example.com/2',
                'description': 'Test description 2',
                'author': 'Author 2',
                'date': '2025-10-05',
                'scraped_at': '2025-10-05T10:00:00'
            }
        ]
    
    def test_save_json(self, sample_articles, tmp_path):
        """Test JSON output."""
        output_file = tmp_path / "test_articles.json"
        OutputHandler.save_json(sample_articles, str(output_file))
        
        assert output_file.exists()
        
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data) == 2
        assert data[0]['title'] == 'Test Article 1'
        assert data[1]['title'] == 'Test Article 2'
    
    def test_save_csv(self, sample_articles, tmp_path):
        """Test CSV output."""
        output_file = tmp_path / "test_articles.csv"
        OutputHandler.save_csv(sample_articles, str(output_file))
        
        assert output_file.exists()
        
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        assert rows[0]['title'] == 'Test Article 1'
        assert rows[1]['author'] == 'Author 2'
    
    def test_save_txt(self, sample_articles, tmp_path):
        """Test TXT output."""
        output_file = tmp_path / "test_articles.txt"
        OutputHandler.save_txt(sample_articles, str(output_file))
        
        assert output_file.exists()
        
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert 'Test Article 1' in content
        assert 'Test Article 2' in content
        assert 'Author 1' in content
        assert '=' * 80 in content
    
    def test_save_empty_csv(self, tmp_path):
        """Test CSV output with empty articles list."""
        output_file = tmp_path / "empty.csv"
        OutputHandler.save_csv([], str(output_file))
        
        # Should not create file for empty list
        # (check logs for warning instead)


class TestIntegration:
    """Integration tests."""
    
    def test_full_scraping_workflow(self):
        """Test complete scraping workflow."""
        html = '''
        <html>
            <body>
                <article>
                    <h2>Integration Test Article</h2>
                    <a href="/test-article">Read more</a>
                    <p>This is a test description for integration testing.</p>
                    <span class="author">Test Author</span>
                </article>
            </body>
        </html>
        '''
        
        soup = BeautifulSoup(html, 'html.parser')
        scraper = NewsScraper('https://example.com')
        articles = scraper.extract_articles(soup, limit=1)
        
        assert len(articles) == 1
        assert articles[0]['title'] == 'Integration Test Article'
        assert articles[0]['author'] == 'Test Author'
        assert articles[0]['url'] == 'https://example.com/test-article'
        assert 'integration testing' in articles[0]['description']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
