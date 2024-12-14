from typing import List, Dict, Union
from continente_scraper import ContinenteWineScraper
from auchan_scraper import AuchanWineScraper
from wine_price_comparator import WinePriceComparator
from base_scraper import BaseWineScraper
import sys
import os

def main() -> None:
    if len(sys.argv) not in [2, 3]:
        print(f"Usage: python {sys.argv[0]} output_path [product_limit]")
        print("output_path: Directory path for storing scraped data")
        print("product_limit: Optional integer for number of products to scrape (default: gets every product available in the website)")
        sys.exit(1)
        
    output_path = sys.argv[1]
    product_limit: int = int(sys.argv[2]) if len(sys.argv) == 3 else -1
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Initialize scrapers with provided output path
    scrapers: List[BaseWineScraper] = [
        ContinenteWineScraper(output_path),
        AuchanWineScraper(output_path)
        # Add more scrapers here as needed
    ]
    
    # Run all scrapers
    for scraper in scrapers:
        scraper.run(product_limit)
    
    # Compare prices across all scrapers
    comparator = WinePriceComparator(*scrapers)
    results = comparator.compare_prices()
    comparator.print_comparison(results)

if __name__ == "__main__":
    main()