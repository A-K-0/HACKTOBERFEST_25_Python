import logging
import random
import time
from datetime import datetime
from urllib.parse import urlencode
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("indiamart_scraper.log"),
        logging.StreamHandler()
    ]
)

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

def setup_driver():
    """Sets up the Selenium WebDriver with visible browser for debugging."""
    user_agent = random.choice(USER_AGENTS)
    logging.info(f"Using user agent: {user_agent}")
    
    chrome_options = Options()
    # Set headless to False to see the browser in action
    # chrome_options.add_argument("--headless=new")  # Commented out
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Additional anti-bot measures
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    try:
        # Use webdriver_manager to handle driver installation
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP commands to prevent detection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        
        return driver
    except Exception as e:
        logging.error(f"Failed to set up driver: {str(e)}")
        raise

def human_like_delay():
    """Simulates human-like delay between actions"""
    time.sleep(random.uniform(2, 5))

def scroll_down_page(driver, scroll_pause=0.5):
    """Scroll down the page gradually to load all content"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down in smaller increments
        for i in range(3):
            scroll_amount = random.uniform(0.2, 0.5) * last_height / 3
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(scroll_pause)
        
        # Wait for page to load
        time.sleep(random.uniform(1, 2))
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same, we've reached the bottom
            break
        last_height = new_height

def extract_product_data_from_sample(product):
    """Extract data using the exact selectors from the HTML sample"""
    product_data = {}
    
    try:
        # Product Name - from the producttitle or prd-name class
        try:
            name_element = product.find_element(By.CSS_SELECTOR, 'div.producttitle a') or product.find_element(By.CSS_SELECTOR, '.prd-name a')
            product_data['name'] = name_element.text.strip()
            product_data['product_url'] = name_element.get_attribute('href')
        except:
            logging.warning("Could not extract product name")
            product_data['name'] = None
            product_data['product_url'] = None
        
        # Price - try multiple selectors (prioritize .prc.cur, then p.price)
        price_selectors = [
            '.prc.cur',  # Primary selector from your Tavily output and web results
            'p.price',   # Fallback
            'span.price' # Another potential fallback
        ]
        price_found = False
        for selector in price_selectors:
            try:
                price_element = product.find_element(By.CSS_SELECTOR, selector)
                price_text = price_element.text.strip()
                # Clean up price (remove currency symbols, "/Piece", etc.)
                price_text = price_text.replace('₹', '').replace('/Piece', '').strip()
                if price_text and not price_text.lower() == 'price on request':
                    product_data['price'] = price_text
                    price_found = True
                    break
            except:
                continue
        
        if not price_found:
            logging.warning("Could not extract price")
            product_data['price'] = None

        # Company Name - from companyname or comp-name class
        try:
            company_element = product.find_element(By.CSS_SELECTOR, 'div.companyname a') or product.find_element(By.CSS_SELECTOR, '.comp-name a')
            product_data['supplier'] = company_element.text.strip()
            product_data['supplier_url'] = company_element.get_attribute('href')
        except:
            logging.warning("Could not extract supplier information")
            product_data['supplier'] = None
            product_data['supplier_url'] = None
        
        # Location - from newLocationUi or loc class
        try:
            location_element = product.find_element(By.CSS_SELECTOR, 'div.newLocationUi .to-txt-gn span.elps1 span') or product.find_element(By.CSS_SELECTOR, '.loc')
            product_data['location'] = location_element.text.strip()
        except:
            logging.warning("Could not extract location")
            product_data['location'] = None
        
        # Rating - from starRating, rtg-val, or ratingValue class
        rating_selectors = [
            'span.bo.color',
            '.rtg-val',
            '.ratingValue'
        ]
        rating_found = False
        for selector in rating_selectors:
            try:
                rating_element = product.find_element(By.CSS_SELECTOR, selector)
                rating_text = rating_element.text.strip()
                if '/' in rating_text:
                    product_data['rating'] = rating_text.split('/')[0].strip()
                else:
                    product_data['rating'] = rating_text
                rating_found = True
                break
            except:
                continue
        
        if not rating_found:
            logging.warning("Could not extract rating")
            product_data['rating'] = None
        
        # Min Order Quantity
        try:
            moq_element = product.find_element(By.CSS_SELECTOR, '.moq')
            moq_text = moq_element.text.strip()
            if 'Min. Order:' in moq_text:
                product_data['min_order'] = moq_text.replace('Min. Order:', '').strip()
            else:
                product_data['min_order'] = moq_text
        except:
            product_data['min_order'] = None
        
        # Product ID
        try:
            product_data['product_id'] = product.get_attribute('data-dispid')
        except:
            product_data['product_id'] = None
        
        # Product Image URL
        try:
            img_element = product.find_element(By.CSS_SELECTOR, 'img.productimg')
            product_data['image_url'] = img_element.get_attribute('src')
        except:
            product_data['image_url'] = None
            
        return product_data
        
    except Exception as e:
        logging.error(f"Error in extract_product_data_from_sample: {str(e)}")
        return product_data

def scrape_indiamart(search_query, max_pages=10, max_retries=3):
    base_url = "https://dir.indiamart.com/search.mp"
    params = {"ss": search_query.replace(" ", "+")}
    
    all_products = []
    page = 1
    driver = None
    
    try:
        driver = setup_driver()
        
        while page <= max_pages:
            retries = 0
            while retries < max_retries:
                try:
                    logging.info(f"Scraping page {page}...")
                    
                    # Navigate to the page
                    full_url = f"{base_url}?{urlencode(params)}"
                    logging.info(f"Accessing URL: {full_url}")
                    driver.get(full_url)
                    
                    # Human-like delay
                    human_like_delay()
                    
                    # Scroll down to load all content
                    scroll_down_page(driver)
                    
                    # Using the exact selector from the HTML sample
                    product_selector = 'div.card.brs5'
                    
                    try:
                        # First try with the provided selector
                        logging.info(f"Looking for products with selector: {product_selector}")
                        products = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, product_selector))
                        )
                    except:
                        # If that fails, try alternative selectors
                        logging.warning("Primary selector failed, trying alternatives...")
                        alternative_selectors = [
                            'div.prd-card-simple',
                            'div.product-card',
                            'div.prd-block',
                            'div.prd-list',
                            'div[id^="LST"]'  # IDs that start with LST
                        ]
                        
                        products = None
                        for selector in alternative_selectors:
                            try:
                                logging.info(f"Trying alternative selector: {selector}")
                                products = WebDriverWait(driver, 5).until(
                                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                                )
                                if products:
                                    logging.info(f"Found products using selector: {selector}")
                                    break
                            except:
                                continue
                    
                    if not products:
                        logging.error("No product elements found with any selector")
                        # Take screenshot for debugging
                        driver.save_screenshot(f"page_{page}_no_products.png")
                        # Since browser is visible, pause to let user see the page
                        input("No products found. Press Enter to continue...")
                        break
                    
                    logging.info(f"Found {len(products)} products on page {page}")
                    
                    # Extract data for each product
                    for product in products:
                        try:
                            product_data = extract_product_data_from_sample(product)
                            if product_data:
                                all_products.append(product_data)
                                logging.info(f"Extracted product: {product_data.get('name', 'Unknown')} with price: {product_data.get('price', 'No price')}")
                        except StaleElementReferenceException:
                            logging.warning("Stale element encountered, skipping product")
                            continue
                        except Exception as e:
                            logging.error(f"Error extracting product data: {str(e)}")
                            continue
                    
                    # Check for next page
                    try:
                        next_selectors = [
                            'a[rel="next"]',
                            'a.next-page',
                            'li.next a',
                            'a.pg-next'
                        ]
                        
                        next_button = None
                        for selector in next_selectors:
                            logging.info(f"Looking for next button with selector: {selector}")
                            elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements:
                                next_button = elements[0]
                                logging.info(f"Found next button with selector: {selector}")
                                break
                        
                        if not next_button or page >= max_pages:
                            logging.info("No next page found or reached max pages.")
                            if not next_button:
                                driver.quit()
                                logging.info("Browser closed. Scraping complete.")
                                return all_products  # <- Exit completely after closing browser
                            break
                        
                        # Click next button
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                        human_like_delay()
                        logging.info("Clicking next page button...")
                        driver.execute_script("arguments[0].click();", next_button)  # Use JavaScript click for reliability
                        human_like_delay()
                        page += 1
                        
                    except Exception as e:
                        logging.error(f"Error navigating to next page: {str(e)}")
                        if page == 1:
                            # Take screenshot for debugging
                            driver.save_screenshot(f"page_{page}_navigation_error.png")
                            # For visible mode, pause to let user see the page
                            input("Error navigating. Press Enter to continue...")
                        break
                    
                    # Success, break retry loop
                    break
                    
                except TimeoutException:
                    retries += 1
                    logging.warning(f"Timeout on page {page}, retry {retries}/{max_retries}")
                    if retries >= max_retries:
                        logging.error(f"Max retries reached for page {page}")
                        # Take screenshot for debugging
                        driver.save_screenshot(f"page_{page}_timeout.png")
                        # For visible mode, pause to let user see the page
                        input("Timeout error. Press Enter to continue...")
                        break
                except Exception as e:
                    logging.error(f"Unexpected error on page {page}: {str(e)}")
                    # Take screenshot to help debug what went wrong
                    driver.save_screenshot(f"error_page_{page}.png")
                    # For visible mode, pause to let user see the page
                    input(f"Error occurred: {str(e)}. Press Enter to retry...")
                    retries += 1
                    if retries >= max_retries:
                        break
    
    except Exception as e:
        logging.error(f"Fatal error in scraper: {str(e)}")
    finally:
        if driver:
            # In visible mode, give user a chance to review final state
            input("Scraping complete. Press Enter to close the browser...")
            driver.quit()
            logging.info("WebDriver closed.")

    return all_products

def save_to_csv_and_text(data, search_term):
    """Save data to both CSV and a text file with query name and timestamp"""
    if not data:
        logging.warning("No data to save")
        return False
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save to CSV (existing functionality)
    csv_filename = f"indiamart_{search_term.replace(' ', '_')}_{timestamp}.csv"
    df = pd.DataFrame(data)
    df.to_csv(csv_filename, index=False)
    logging.info(f"Saved {len(data)} records to {csv_filename}")
    
    # Save to text file
    text_filename = f"indiamart_{search_term.replace(' ', '_')}_{timestamp}.txt"
    with open(text_filename, 'w', encoding='utf-8') as text_file:
        text_file.write(f"Search Query: {search_term}\n")
        text_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        text_file.write(f"Total Products Scraped: {len(data)}\n\n")
        text_file.write("Scraped Products:\n")
        text_file.write("-" * 50 + "\n")
        for i, product in enumerate(data, 1):
            text_file.write(f"Product {i}:\n")
            for key, value in product.items():
                if value:  # Only write non-None values
                    text_file.write(f"  {key.capitalize()}: {value}\n")
            text_file.write("-" * 50 + "\n")
    
    logging.info(f"Saved data to text file: {text_filename}")
    return csv_filename, text_filename

if __name__ == "__main__":
    try:
        search_term = input("Enter product to search on IndiaMart: ")
        max_pages = int(input("Enter maximum number of pages to scrape (default 2): ") or 2)
        
        logging.info(f"Starting scrape for '{search_term}' with max {max_pages} pages")
        products = scrape_indiamart(search_term, max_pages=max_pages)
        
        if products:
            csv_file, text_file = save_to_csv_and_text(products, search_term)
            print(f"\nSuccess! Scraped {len(products)} products.")
            print(f"Data saved to CSV: {csv_file}")
            print(f"Data saved to text file: {text_file}")
            
            # Print first 3 products as sample
            print("\nSample of scraped data:")
            for i, product in enumerate(products[:3]):
                print(f"\nProduct {i+1}:")
                for key, value in product.items():
                    if value:  # Only print non-None values
                        print(f"  {key.capitalize()}: {value}")
        else:
            print("No products found or scraping failed. Check the log file for details.")
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        logging.error(f"Main execution error: {str(e)}")
        print(f"An error occurred: {str(e)}")