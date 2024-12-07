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
    continente_scraper: ContinenteWineScraper = ContinenteWineScraper(os.path.join(os.getcwd(), 'generated'))
    auchan_scraper: AuchanWineScraper = AuchanWineScraper(os.path.join(os.getcwd(), 'generated'))
    
    continente_scraper.run(product_limit)
    auchan_scraper.run(product_limit)
    
    comparator: WinePriceComparator = WinePriceComparator(os.path.join(os.getcwd(), 'generated'))
    results: List[Dict[str, Union[str, float]]] = comparator.compare_prices()
    
    print("\nWine Price Comparison Results:")
    print("-" * 80)
    
    for result in results:
        print(f"\nProduct: {result['name']}")
        print(f"EAN: {result['ean']}")
        print(f"Continente Price: €{result['continente_price']:.2f}")
        print(f"Auchan Price: €{result['auchan_price']:.2f}")
        
        diff: float = result['price_difference']
        if diff != 0:
            cheaper: str = "Continente" if diff > 0 else "Auchan"
            print(f"Price Difference: €{abs(diff):.2f} ({cheaper} is cheaper)")
        else:
            print(f"Price Difference: €{abs(diff):.2f} (Same price)")
        print("-" * 80)

if __name__ == "__main__":
    main()