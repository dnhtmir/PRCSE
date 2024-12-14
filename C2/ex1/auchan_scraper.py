# This line imports List, Dict, Any, and Optional types from the typing module
# List - Used for type hinting lists
# Dict - Used for type hinting dictionaries 
# Any - Used when the type is dynamic or unknown
# Optional - Used for values that could be None
from typing import List, Dict, Any, Optional
import requests # HTTP library for making web requests
from bs4 import BeautifulSoup # Library for parsing HTML and XML documents
import json # Built-in module for JSON data encoding and decoding
import os # Provides functions for interacting with the operating system (file paths, etc.)
from datetime import datetime # Provides classes for working with dates and times
from base_scraper import BaseWineScraper # Custom module containing the base class for wine scrapers

class AuchanWineScraper(BaseWineScraper):
    def __init__(self, folder: str) -> None:
        super().__init__(
            base_url="https://www.auchan.pt/pt/bebidas-e-garrafeira/garrafeira/",
            data_file=os.path.join(folder, "auchan_wine_data.json"),
            size=24
        )

    def _get_product_data(self, product_offset=0, product_limit: int = -1) -> List[Dict[str, Any]]:
        """Get products from a specific page"""
        url: str = f"{self.base_url}?sz={self.size}&start={product_offset}"
        response: requests.Response = requests.get(url, headers=self.headers)
        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
        
        products: List[Dict[str, Any]] = []
        for product in soup.find_all("div", class_="product-tile"):
            product_data: Optional[Dict[str, Any]] = self._scrape_product(product)
            if product_data:
                products.append(product_data)
            if len(products) >= product_limit:
                break

        return products

    def _scrape_product(self, product: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """Extract product information from a product element"""
        try:
            impression_data: Optional[str] = product.get('data-gtm-new')
            product_info: Dict[str, Any] = json.loads(impression_data)
            name: str = product_info.get('item_name', '')
            brand: str = product_info.get('item_brand', '')
            price: float = float(product_info.get('price', 0)) - float(product_info.get('discount', 0))
            quantity: str = product_info.get('quantity', '')
            price_per_litre: float = float(product.find('span', class_='auc-measures--price-per-unit')
                                        .text.strip()
                                        .replace(' €/Lt', ''))
            
            data_urls: Optional[str] = product.get('data-urls', '')
            product_urls: Dict[str, str] = json.loads(data_urls)
            link: str = 'https://www.auchan.pt' + product_urls.get('productUrl', '')
            ean: Optional[str] = self._extract_ean(link)
            
            return {
                "name": name,
                "price": price,
                "brand": brand,
                "quantity": quantity,
                "price_per_litre": price_per_litre,
                "ean": ean,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error scraping product: {e}")
            return None

    def _extract_ean(self, product_url: str) -> Optional[str]:
        """Extract EAN from product URL"""
        try:
            response = requests.get(product_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.find('span', class_='product-ean').text.strip()
        except Exception as e:
            print(f"Error extracting EAN: {e}")
            return None
    
    def _get_total_products(self) -> int:
        """Get total number of pages to scrape"""
        url = f'{self.base_url}?sz={self.size}&start=0'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        input_element = soup.find('input', {'name': 'auc-js-search-results-total'})
        return int(input_element.get('value'))
