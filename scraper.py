"""
Web Scraper for OpenTable Restaurant Reviews
Scrapes reviews including reviewer name, rating, date, and review text from OpenTable restaurant pages
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def scrape_restaurant_reviews(url, output_file='restaurant_reviews_content.csv', max_pages=None):
    """
    Scrape reviews from an OpenTable restaurant page
    
    Args:
        url (str): OpenTable restaurant URL
        output_file (str): Output CSV filename
        max_pages (int): Maximum number of pages to scrape (None for all pages)
    
    Returns:
        str: Path to the output CSV file
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)
    
    data = []
    page_number = 1
    
    while True:
        print(f"Scraping page {page_number}...")
        
        # Find all review items on the current page
        reviews = driver.find_elements(By.CSS_SELECTOR, "ol[aria-label='Reviews List'] > li")
        
        for review in reviews:
            try:
                reviewer_name = review.find_element(By.CLASS_NAME, '_1p30XHjz2rI-').text
                rating = review.find_element(By.CLASS_NAME, 'yEKDnyk-7-g-').get_attribute('aria-label')
                review_date = review.find_element(By.CLASS_NAME, 'iLkEeQbexGs-').text
                review_text = review.find_element(By.CLASS_NAME, 'l9bbXUdC9v0-').text
                
                data.append({
                    'Reviewer Name': reviewer_name,
                    'Rating': rating,
                    'Date': review_date,
                    'Review Text': review_text
                })
            except Exception as e:
                print(f"Error extracting review: {e}")
                continue
        
        # Check if we've reached the max pages limit
        if max_pages and page_number >= max_pages:
            print(f"Reached maximum pages limit: {max_pages}")
            break
        
        # Try to find and click the next page button
        next_buttons = driver.find_elements(By.CSS_SELECTOR, f'a[aria-label="Go to page number {page_number + 1}"]')
        
        if next_buttons:
            next_button = next_buttons[0]
            if next_button.is_displayed() and next_button.is_enabled():
                next_button.click()
                time.sleep(3)
                page_number += 1
            else:
                print("Next button not clickable")
                break
        else:
            print("No more pages found")
            break
    
    driver.quit()
    
    # Save scraped data to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Scraping complete. {len(data)} reviews saved to '{output_file}'")
    return output_file


def scrape_competitor_reviews(url, output_file='competitor_reviews.csv'):
    """
    Scrape only ratings and dates from a competitor restaurant (lighter version)
    
    Args:
        url (str): OpenTable competitor restaurant URL
        output_file (str): Output CSV filename
    
    Returns:
        str: Path to the output CSV file
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)
    
    data = []
    page_number = 1
    
    while True:
        try:
            print(f"Scraping competitor page {page_number}...")
            
            reviews = driver.find_elements(By.CSS_SELECTOR, "ol[aria-label='Reviews List'] > li")
            
            for review in reviews:
                try:
                    rating = review.find_element(By.CLASS_NAME, 'yEKDnyk-7-g-').get_attribute('aria-label')
                    review_date = review.find_element(By.CLASS_NAME, 'iLkEeQbexGs-').text
                    
                    data.append({
                        'Rating': rating,
                        'Date': review_date,
                    })
                except Exception as e:
                    continue
            
            # Try to find next page
            next_buttons = driver.find_elements(By.CSS_SELECTOR, f'a[aria-label="Go to page number {page_number + 1}"]')
            
            if next_buttons:
                next_button = next_buttons[0]
                if next_button.is_displayed() and next_button.is_enabled():
                    next_button.click()
                    time.sleep(3)
                    page_number += 1
                else:
                    break
            else:
                break
                
        except Exception as e:
            print(f"Error during scraping: {e}")
            break
    
    driver.quit()
    
    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Competitor scraping complete. {len(data)} reviews saved to '{output_file}'")
    return output_file


if __name__ == "__main__":
    # Example usage
    url = "https://www.opentable.com/r/swizzle-louisville"
    scrape_restaurant_reviews(url, max_pages=5)  # Scrape first 5 pages as example
