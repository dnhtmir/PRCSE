from continente_scraper import ContinenteWineScraper
from auchan_scraper import AuchanWineScraper
from wine_price_comparator import WinePriceComparator
import sys

def main():
    product_limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    continente_scraper = ContinenteWineScraper()
    auchan_scraper = AuchanWineScraper()
    
    continente_scraper.run(product_limit)
    auchan_scraper.run(product_limit)
    
    comparator = WinePriceComparator()
    results = comparator.compare_prices()
    
    print("\nWine Price Comparison Results:")
    print("-" * 80)
    
    for result in results:
        print(f"\nProduct: {result['name']}")
        print(f"EAN: {result['ean']}")
        print(f"Continente Price: €{result['continente_price']:.2f}")
        print(f"Auchan Price: €{result['auchan_price']:.2f}")
        
        diff = result['price_difference']
        if diff != 0:
            cheaper = "Continente" if diff > 0 else "Auchan"
            print(f"Price Difference: €{abs(diff):.2f} ({cheaper} is cheaper)")
        else:
            print(f"Price Difference: €{abs(diff):.2f} (Same price)")
        print("-" * 80)

if __name__ == "__main__":
    main()