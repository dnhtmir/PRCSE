import json
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import os

class BaseWineScraper:
    def __init__(self, base_url: str, data_file: str, size: int) -> None:
        self.base_url: str = base_url
        self.data_file: str = data_file
        self.size: int = size
        self.headers: Dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def load_existing_data(self) -> Dict[str, Dict[str, Any]]:
        """Load existing data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self, new_products: List[Dict[str, Any]]) -> None:
        """Save scraped data to JSON file with price history"""
        existing_data = self.load_existing_data()
        current_time = datetime.now().isoformat()

        for product in new_products:
            ean = product['ean']
            if not ean:
                continue

            if ean not in existing_data:
                existing_data[ean] = {
                    'name': product['name'],
                    'brand': product['brand'],
                    'quantity': product['quantity'],
                    'price_history': [{
                        'price': product['price'],
                        'price_per_litre': product['price_per_litre'],
                        'timestamp': current_time
                    }]
                }
            else:
                last_price = existing_data[ean]['price_history'][-1]['price']
                if last_price != product['price']:
                    existing_data[ean]['price_history'].append({
                        'price': product['price'],
                        'price_per_litre': product['price_per_litre'],
                        'timestamp': current_time
                    })
                existing_data[ean].update({
                    'name': product['name'],
                    'brand': product['brand'],
                    'quantity': product['quantity'],
                })

        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)

    def run(self, product_limit: int) -> None:
        """Base periodic scraping implementation"""
        print(f"Starting {self.__class__.__name__} scraping at {datetime.now()}")
        all_products: List[Dict[str, Any]] = []
        
        try:
            all_products = self._scrape_all_products(product_limit)
            self.save_data(all_products)
            print(f"Scraped {len(all_products)} products")
        except Exception as e:
            print(f"Error during scraping: {e}")

    def get_product_data(self, product_offset: int = 0, product_limit: int = 50) -> List[Dict[str, Any]]:
        """To be implemented by child classes"""
        raise NotImplementedError
    
    def scrape_product(self, product: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """To be implemented by child classes"""
        raise NotImplementedError

    def _extract_ean(self, product_url: str) -> Optional[str]:
        """To be implemented by child classes"""
        raise NotImplementedError

    def _get_total_products(self) -> int:
        """To be implemented by child classes"""
        raise NotImplementedError

    def _scrape_all_products(self, product_limit: int = 50) -> List[Dict[str, Any]]:
        """Implementation of the abstract method from BaseWineScraper"""
        all_products: List[Dict[str, Any]] = []
        product_offset: int = 0
        
        while len(all_products) < product_limit:
            products: List[Dict[str, Any]] = self.get_product_data(product_offset, product_limit - len(all_products))
            if not products:
                break
            all_products.extend(products)
            product_offset += self.size

        return all_products
