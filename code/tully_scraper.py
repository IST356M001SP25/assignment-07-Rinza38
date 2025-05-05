import re  # Regular expressions (though not directly used in shown code)
from playwright.sync_api import Playwright, sync_playwright  # Browser automation
from menuitemextractor import extract_menu_item  # Custom menu item parsing module
from menuitem import MenuItem  # Custom class for menu items
import pandas as pd  # Data manipulation and CSV export


def tullyscraper(playwright: Playwright) -> None:
    """
    Scrapes menu data from Tully's Good Times website using Playwright.
    
    The function:
    1. Launches a browser and navigates to the menu page
    2. Extracts menu sections and items
    3. Processes items using custom extractor
    4. Saves results to CSV
    
    Args:
        playwright: Playwright instance for browser automation
    
    Output:
        Saves menu items to 'cache/tullys_menu.csv'
    """
    
    # Launch browser (visible window for debugging)
    browser = playwright.chromium.launch(headless=False)
    
    # Create new browser context and page
    context = browser.new_context()
    page = context.new_page()
    
    # Navigate to Tully's menu page
    page.goto("https://www.tullysgoodtimes.com/menus/")

    # List to store extracted menu items
    extracted_items = []
    
    # Find all menu section titles (h3 elements with specific class)
    for title in page.query_selector_all("h3.foodmenu__menu-section-title"):
        # Get the section name (e.g., "Appetizers", "Burgers")
        title_text = title.inner_text()
        print("MENU SECTION:", title_text) 
        
        # Navigate DOM to find the container with menu items
        # The ~ * selector finds subsequent siblings
        row = title.query_selector("~ *").query_selector("~ *")
        
        # Find all menu items within this section
        for item in row.query_selector_all("div.foodmenu__menu-item"):
            # Get full text of menu item
            item_text = item.inner_text()
            
            # Use custom extractor to parse item details
            extracted_item = extract_menu_item(title_text, item_text)
            print(f"  MENU ITEM: {extracted_item.name}")
            
            # Convert MenuItem object to dictionary and store
            extracted_items.append(extracted_item.to_dict())

    # Convert all extracted items to DataFrame and save as CSV
    df = pd.DataFrame(extracted_items)
    df.to_csv("cache/tullys_menu.csv", index=False)    
    
    # Clean up - close browser context and instance
    context.close()
    browser.close()

# Main execution block
with sync_playwright() as playwright:
    tullyscraper(playwright)