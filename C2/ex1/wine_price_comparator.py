# This line imports types from the typing module for type hinting:
# - List: For annotating lists (e.g., List[str] is a list of strings)
# - Dict: For annotating dictionaries (e.g., Dict[str, int] is a dict with string keys and integer values)
# - Union: For types that could be one of several types (e.g., Union[str, int] means str or int)
# - Any: Used when a value could be of any type
from typing import List, Dict, Union, Any
from base_scraper import BaseWineScraper  # Custom module containing the base class for wine scrapers
import json  # Built-in module for JSON data encoding and decoding

class WinePriceComparator:
    def __init__(self, *scrapers: BaseWineScraper) -> None:
        """Initialize comparator with any number of scrapers"""
        if len(scrapers) < 2:
            raise ValueError("At least two scrapers are required for comparison")
            
        self.retailer_data: Dict[str, Dict[str, Dict[str, Any]]] = {}
        
        for scraper in scrapers:
            retailer_name = scraper.__class__.__name__.replace('WineScraper', '')
            try:
                with open(scraper.data_file, 'r', encoding='utf-8') as f:
                    self.retailer_data[retailer_name] = json.load(f)
            except FileNotFoundError:
                print(f"Warning: No data file found for {retailer_name}")
                self.retailer_data[retailer_name] = {}

    def compare_prices(self) -> List[Dict[str, Union[str, float]]]:
        """Compare prices for products across all retailers"""
        results = []
        all_eans = set()
        
        for retailer_products in self.retailer_data.values():
            all_eans.update(retailer_products.keys())
            
        for ean in all_eans:
            retailers_with_product = {
                retailer: data[ean]
                for retailer, data in self.retailer_data.items()
                if ean in data
            }
            
            if len(retailers_with_product) < 2:
                continue
                
            current_prices = {
                retailer: data['price_history'][-1]['price']
                for retailer, data in retailers_with_product.items()
            }
            
            price_per_litre = {
                retailer: data['price_history'][-1].get('price_per_litre')
                for retailer, data in retailers_with_product.items()
            }
            
            cheapest_retailer = min(current_prices.items(), key=lambda x: x[1])[0]
            
            comparison = {
                "ean": ean,
                "name": next(iter(retailers_with_product.values()))['name'],
                "retailers": len(retailers_with_product),
                "prices": current_prices,
                "price_per_litre": price_per_litre,
                "cheapest_retailer": cheapest_retailer,
                "price_differences": {
                    retailer: price - min(current_prices.values())
                    for retailer, price in current_prices.items()
                }
            }
            
            results.append(comparison)
            
        return results

    def get_price_history(self, ean: str) -> Dict[str, List[Dict[str, Union[float, str]]]]:
        """Get price history for a product across all retailers"""
        history = {}
        
        for retailer, data in self.retailer_data.items():
            if ean in data:
                history[retailer] = data[ean]['price_history']
                
        return history

    def print_comparison(self, results: List[Dict[str, Any]]) -> None:
        """Print formatted comparison results"""
        print("\nWine Price Comparison Results:")
        print("-" * 80)
        
        for result in results:
            print(f"\nProduct: {result['name']}")
            print(f"EAN: {result['ean']}")
            print(f"Available in {result['retailers']} retailers")
            
            for retailer, price in result['prices'].items():
                print(f"{retailer} Price: €{price:.2f}")
                if result['price_per_litre'][retailer]:
                    print(f"{retailer} Price per Litre: €{result['price_per_litre'][retailer]:.2f}")
            
            
            for retailer, diff in result['price_differences'].items():
                if diff > 0:
                    print(f"\nCheapest at: {result['cheapest_retailer']}")
                    print(f"{retailer} is €{diff:.2f} more expensive than the cheapest option")
            
            print("-" * 80)