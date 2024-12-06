import json
from datetime import datetime
import time
import os

class BaseWineScraper:
    def __init__(self, base_url: str, data_file: str, size: int):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.data_file = data_file
        self.size = size

    def load_existing_data(self) -> list:
        """Load existing data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self, products: list) -> None:
        """Save or update product data"""
        existing_data = self.load_existing_data()
        
        for product in products:
            product_exists = False
            for existing in existing_data:
                if existing['name'] == product['name'] and existing['brand'] == product['brand']:
                    if existing['price'] != product['price']:
                        existing['price'] = product['price']
                        existing['timestamp'] = product['timestamp']
                    product_exists = True
                    break
            
            if not product_exists:
                existing_data.append(product)

        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

    def run(self, product_limit: int) -> None:
        """Base periodic scraping implementation"""
        print(f"Starting {self.__class__.__name__} scraping at {datetime.now()}")
        all_products = []
        
        try:
            all_products = self._scrape_all_products(product_limit)
            
            self.save_data(all_products)
            print(f"Scraped {len(all_products)} products")
        except Exception as e:
            print(f"Error during scraping: {e}")

    def _extract_ean(self, product_url: str) -> str:
        """To be implemented by child classes"""
        raise NotImplementedError

    def _extract_quantity(self, name: str) -> str:
        """To be implemented by child classes"""
        raise NotImplementedError

    def _get_total_products(self) -> int:
        """To be implemented by child classes"""
        raise NotImplementedError
    
    def _scrape_all_products(self, product_limit: int) -> list:
        """To be implemented by child classes"""
        raise NotImplementedError