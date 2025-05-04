from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
import pandas as pd
from pathlib import Path

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/")

    menu_items = []
    menu_sections = page.locator('h2.menu-title').all()
    
    for section in menu_sections:
        title = section.inner_text()
        parent_div = section.locator('xpath=../..')
        items = parent_div.locator('div.menu-item').all()
        
        for item in items:
            item_text = item.inner_text()
            menu_item = extract_menu_item(title, item_text)
            menu_items.append(menu_item.to_dict())
    
    df = pd.DataFrame(menu_items)
    csv_path = Path('cache/tullys_menu.csv')
    csv_path.parent.mkdir(exist_ok=True)
    df.to_csv(csv_path, index=False)
    
    context.close()
    browser.close()

with sync_playwright() as playwright:
    tullyscraper(playwright)