# News Web Scraper 🕷️📰

A flexible, production-ready web scraper for extracting news articles from various websites. Built with Python, BeautifulSoup, and best practices for respectful web scraping.

## 🌟 Features

- ✅ **Multiple Output Formats**: JSON, CSV, TXT, or console output
- ✅ **Rate Limiting**: Respectful scraping with configurable delays
- ✅ **Error Handling**: Robust error handling and logging
- ✅ **Flexible Extraction**: Works with most news website structures
- ✅ **CLI Interface**: Easy-to-use command-line arguments
- ✅ **Type Hints**: Full type annotations for better code quality
- ✅ **Logging**: Comprehensive logging to file and console
- ✅ **Customizable**: Configurable timeout and user-agent

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/HACKTOBERFEST_25_Python.git
cd HACKTOBERFEST_25_Python/Web-Scraper
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Usage
```bash
python news_scraper.py https://example-news-site.com
```

### Scrape with Limit
```bash
python news_scraper.py https://example.com --limit 20
```

### Save to JSON
```bash
python news_scraper.py https://example.com --format json
```

### Save to CSV with Custom Filename
```bash
python news_scraper.py https://example.com --format csv --output my_articles.csv
```

### Save to All Formats
```bash
python news_scraper.py https://example.com --format all
```

### With Custom Settings
```bash
python news_scraper.py https://example.com \
  --limit 50 \
  --timeout 15 \
  --rate-limit 2.0 \
  --format json
```

## 📋 Command-Line Arguments

| Argument | Short | Type | Default | Description |
|----------|-------|------|---------|-------------|
| `url` | - | str | required | Target website URL to scrape |
| `--limit` | `-l` | int | 10 | Maximum number of articles to scrape |
| `--format` | `-f` | str | console | Output format: json, csv, txt, console, all |
| `--output` | `-o` | str | articles.[format] | Custom output filename |
| `--timeout` | - | int | 10 | Request timeout in seconds |
| `--rate-limit` | - | float | 1.0 | Delay between requests in seconds |

## 📊 Output Formats

### JSON Output
```json
[
  {
    "id": 1,
    "title": "Breaking News: Example Article",
    "url": "https://example.com/article-1",
    "description": "This is a sample article description...",
    "author": "John Doe",
    "date": "2025-10-05",
    "scraped_at": "2025-10-05T10:30:00"
  }
]
```

### CSV Output
```csv
id,title,url,description,author,date,scraped_at
1,"Breaking News: Example","https://...","Description...","John Doe","2025-10-05","2025-10-05T10:30:00"
```

### Console Output
```
================================================================================
SCRAPED ARTICLES (10 found)
================================================================================

[1] Breaking News: Example Article
    URL: https://example.com/article-1
    Author: John Doe | Date: 2025-10-05
    This is a sample article description...
```

## 🏗️ Project Structure

```
Web-Scraper/
├── news_scraper.py          # Main scraper script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── test_scraper.py         # Unit tests (pytest)
├── .env.example            # Example environment variables
└── scraper.log             # Log file (generated on run)
```

## 🧪 Testing

Run the test suite with pytest:
```bash
pip install pytest
pytest test_scraper.py -v
```

## 🎓 How It Works

1. **Fetch Page**: Sends HTTP GET request with custom user-agent
2. **Parse HTML**: Uses BeautifulSoup to parse the HTML content
3. **Extract Data**: Identifies article containers and extracts:
   - Title
   - URL
   - Description/Summary
   - Author
   - Publication date
4. **Rate Limiting**: Waits between requests to avoid overwhelming servers
5. **Output**: Saves data in requested format(s)

## ⚙️ Architecture

### `NewsScraper` Class
Main scraper class that handles:
- Page fetching with error handling
- HTML parsing with BeautifulSoup
- Article extraction with fallback strategies
- Multiple selector patterns for compatibility

### `OutputHandler` Class
Handles different output formats:
- JSON serialization
- CSV writing
- Plain text formatting
- Console printing

## 🛡️ Best Practices Implemented

- ✅ **Respectful Scraping**: Rate limiting and user-agent
- ✅ **Error Handling**: Try-except blocks with logging
- ✅ **Type Hints**: Full type annotations
- ✅ **Logging**: Comprehensive logging system
- ✅ **Documentation**: Docstrings for all functions
- ✅ **CLI Design**: Clear argparse interface
- ✅ **Flexibility**: Works with various website structures

## 🚨 Legal & Ethical Considerations

**Important**: Always follow these guidelines when web scraping:

1. ✅ Check the website's `robots.txt` file
2. ✅ Read the website's Terms of Service
3. ✅ Use rate limiting to avoid overloading servers
4. ✅ Respect copyright and intellectual property
5. ✅ Don't scrape personal or sensitive data
6. ❌ Never use scraped data for illegal purposes

**Example**: Check robots.txt
```bash
curl https://example.com/robots.txt
```

## 🔧 Customization

### Add Custom Selectors
Edit the `extract_articles` method to add site-specific selectors:
```python
article_containers = soup.find_all('div', class_='your-custom-class')
```

### Custom User-Agent
```python
scraper = NewsScraper(
    url='https://example.com',
    user_agent='Your Custom User Agent String'
)
```

## 🐛 Troubleshooting

### No articles found?
- Check if the website structure matches common patterns
- Try viewing the page source to identify article containers
- Modify selectors in `extract_articles()` method

### Request timeout?
```bash
python news_scraper.py https://example.com --timeout 30
```

### Getting blocked?
- Increase rate limit: `--rate-limit 3.0`
- Check robots.txt
- Use a custom user-agent

## 📚 Dependencies

- **requests**: HTTP library for making requests
- **beautifulsoup4**: HTML parsing and extraction
- **lxml**: Fast XML/HTML parser (optional but recommended)

## 🎯 Future Enhancements

Potential improvements for contributors:
- [ ] Add support for JavaScript-rendered pages (Selenium/Playwright)
- [ ] Implement pagination support
- [ ] Add proxy support
- [ ] Create database storage option (SQLite/MongoDB)
- [ ] Add RSS feed parsing
- [ ] Implement parallel scraping for multiple URLs
- [ ] Add sentiment analysis for articles
- [ ] Create web UI with Flask/Streamlit

## 👤 Author

- **GitHub**: [@Pasan11504](https://github.com/Pasan11504)
- **Date**: October 5, 2025
- **Event**: Hacktoberfest 2025

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## ⭐ Acknowledgments

- Built for Hacktoberfest 2025
- Inspired by best practices in web scraping
- Thanks to the Python and BeautifulSoup communities

---

**Happy Scraping! 🕷️✨**

*Remember: With great scraping power comes great responsibility!*
