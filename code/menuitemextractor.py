# Import handling - different paths when run directly vs imported as module
if __name__ == "__main__":
    import sys
    sys.path.append('code')  # Add 'code' directory to Python path
    from menuitem import MenuItem  # Import MenuItem class from local module
else:
    from code.menuitem import MenuItem  # Alternative import path when used as module

def clean_price(price: str) -> float:
    """
    Cleans and converts a price string to a float.
    
    Args:
        price: String containing price (e.g., "$12.99")
        
    Returns:
        float: Numeric price value
        
    Example:
        "$12.99" → 12.99
        "1,000.50" → 1000.5
    """
    # Remove dollar sign if present
    price = price.replace("$", "")
    # Remove thousands separators
    price = price.replace(",", "")
    # Convert to float and return
    return float(price)

def clean_scraped_text(scraped_text: str) -> list[str]:
    """
    Cleans raw scraped menu item text by:
    - Splitting into lines
    - Removing unwanted markers (GS, V, S, P)
    - Removing "NEW" indicators
    - Removing empty lines
    
    Args:
        scraped_text: Raw multi-line text from web scraping
        
    Returns:
        list: Cleaned list of relevant text lines
        
    Example Input:
        '''NEW!\n\nItem Name\n$10.99\nGS\nDescription...'''
    Example Output:
        ['Item Name', '$10.99', 'Description...']
    """
    # Split text by newlines
    items = scraped_text.split("\n")
    cleaned = []
    
    # Filter out unwanted lines
    for item in items:
        # Skip dietary/portion indicators
        if item in ['GS', "V", "S", "P"]:
            continue
        # Skip "NEW" announcements
        if item.startswith("NEW"):
            continue
        # Skip empty/whitespace lines
        if len(item.strip()) == 0:
            continue

        cleaned.append(item)

    return cleaned

def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    """
    Extracts and structures menu item data from raw scraped text.
    
    Args:
        title: Menu category/section name (e.g., "Appetizers")
        scraped_text: Raw text block for a single menu item
        
    Returns:
        MenuItem: Structured menu item object with:
            - category
            - name
            - price
            - description
            
    Processing Logic:
        1. Cleans raw text
        2. Creates MenuItem with default values
        3. Sets name from first cleaned line
        4. Sets price from second cleaned line
        5. Sets description from third line (if exists)
    """
    # Clean and split the raw text
    cleaned_items = clean_scraped_text(scraped_text)
    
    # Create base MenuItem with default values
    item = MenuItem(
        category=title,
        name="",
        price=0.0,
        description=""
    )
    
    # First line is always the item name
    item.name = cleaned_items[0]
    
    # Second line is always the price
    item.price = clean_price(cleaned_items[1])
    
    # Description is optional (third line if exists)
    if len(cleaned_items) > 2:
        item.description = cleaned_items[2]
    else:
        item.description = "No description available."
        
    return item

# Test code - runs when script is executed directly
if __name__ == '__main__':
    # Test cases with various menu item formats
    test_items = [
        # Case 1: Item with "NEW" marker and description
        '''
NEW!

Tully Tots

$11.79

Made from scratch with shredded potatoes...
        ''',
        
        # Case 2: Item with portion marker (GS) and long description
        '''Super Nachos
$15.49
GS
Tortilla chips topped with...
        ''',
        
        # Case 3: Vegetarian item (V marker) with add-ons
        '''Veggie Quesadilla
$11.99
V
A flour tortilla packed with...
Add chicken $2.99 | Add guacamole $2.39
''',
        
        # Case 4: Simple item with no description
        '''Kid's Burger & Fries
$6.99
'''
    ]
    
    title = "TEST"
    # Process each test case
    for scraped_text in test_items:
        item = extract_menu_item(title, scraped_text)
        print(item)  # Print the structured MenuItem object