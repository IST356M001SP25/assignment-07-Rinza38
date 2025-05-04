from menuitem import MenuItem

def clean_price(price: str) -> float:
    """Clean price string and convert to float"""
    return float(price.replace('$', '').replace(',', ''))

def clean_scraped_text(scraped_text: str) -> list[str]:
    """Clean scraped text and return relevant parts"""
    lines = [line.strip() for line in scraped_text.split('\n') if line.strip()]
    unwanted = ['NEW!', 'NEW', 'S', 'V', 'GS', 'P']
    return [line for line in lines if line not in unwanted]

def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    """Extract menu item from scraped text"""
    cleaned = clean_scraped_text(scraped_text)
    name = cleaned[0] if len(cleaned) > 0 else "No name available"
    price = clean_price(cleaned[1]) if len(cleaned) > 1 else 0.0
    description = cleaned[2] if len(cleaned) > 2 else "No description available"
    
    return MenuItem(
        category=title,
        name=name,
        price=price,
        description=description
    )

if __name__ == '__main__':
    test_text = """NEW!
    Tully Tots
    $11.79
    Made from scratch with shredded potatoes, cheddar-jack cheese and Romano..."""
    
    test_item = extract_menu_item("Starters & Snacks", test_text)
    print(test_item)