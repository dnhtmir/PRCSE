from typing import List, Dict, Union
from continente_scraper import ContinenteWineScraper
from auchan_scraper import AuchanWineScraper
from wine_price_comparator import WinePriceComparator
import sys
import os

def main() -> None:
    if len(sys.argv) not in [1, 2]:
        print(f"Usage: python {sys.argv[0]} [product_limit]")
        print("product_limit: Optional integer for number of products to scrape (default: 50)")
        sys.exit(1)
        
    product_limit: int = int(sys.argv[1]) if len(sys.argv) == 2 else 50
    output_dir = os.path.join(os.getcwd(), 'generated')
    
    scrapers = [
        ContinenteWineScraper(output_dir),
        AuchanWineScraper(output_dir)
    ]
    
    for scraper in scrapers:
        scraper.run(product_limit)
    
    comparator = WinePriceComparator(*scrapers)
    results = comparator.compare_prices()
    comparator.print_comparison(results)

if __name__ == "__main__":
    main()