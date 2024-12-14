# This line imports List, Dict, Any, and Optional types from the typing module
# These are used for type hinting in Python to make the code more maintainable:
# - List: For annotating lists (e.g., List[str] is a list of strings)
# - Dict: For annotating dictionaries (e.g., Dict[str, int] is a dict with string keys and integer values) 
# - Any: Used when a value could be of any type
# - Optional: Used for values that could be None (e.g., Optional[str] means str | None)
from typing import List, Dict, Any, Optional
import requests  # HTTP library for making web requests
from bs4 import BeautifulSoup  # Library for parsing HTML and XML documents
import json  # Built-in module for JSON data encoding and decoding
from datetime import datetime  # Provides classes for working with dates and times
import os  # Provides functions for interacting with the operating system (file paths, etc.)
from urllib.parse import urlparse, parse_qs  # Parses URLs into components
from base_scraper import BaseWineScraper  # Custom module containing the base class for wine scrapers

class ContinenteWineScraper(BaseWineScraper):
    def __init__(self, folder: str) -> None:
        super().__init__(
            base_url='https://www.continente.pt/bebidas-e-garrafeira/vinhos/',
            data_file=os.path.join(folder, "continente_wine_data.json"),
            size=36
        )

    def _get_product_data(self, product_offset: int = 0, product_limit: int = -1) -> List[Dict[str, Any]]:
        """Get products from a specific page"""
        url: str = f'{self.base_url}?start={product_offset}&srule=FOOD-Bebidas&pmin=0.01'
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
            impression_data = product.get('data-product-tile-impression')
            name = ""
            brand = ""
            price = 0.0
            
            if impression_data:
                try:
                    # Try to get data from JSON first
                    product_info = json.loads(impression_data)
                    name = product_info.get('name', '')
                    brand = product_info.get('brand', '')
                    price = float(product_info.get('price', 0))
                except json.JSONDecodeError:
                    # Fallback to HTML parsing if JSON fails
                    name = product.find('h2', class_='pwc-tile--description').text.strip()
                    brand = product.find('p', class_='pwc-tile--brand').text.strip()
                    price = float(product.find('span', class_='ct-price-formatted')
                                .text.strip()
                                .replace('.', '')
                                .replace('€', '')
                                .replace(',', '.'))

            link = product.find('div', class_='ct-pdp-link').find('a').get('href')
            ean = self._extract_ean(link)
            quantity = product.find('p', class_='pwc-tile--quantity').text.strip()
            price_per_litre = float(product.find('span', class_='ct-price-value')
                                .text.strip()
                                .replace('.', '')
                                .replace('€', '')
                                .replace(',', '.'))

            if not all([name, brand, price, ean, quantity, price_per_litre]):
                return None

            return {
                'name': name,
                'brand': brand,
                'price': price,
                'ean': ean,
                'quantity': quantity,
                'price_per_litre': price_per_litre,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error scraping product: {e}")
            return None

    def _extract_ean(self, product_url: str) -> Optional[str]:
        """Extract EAN from product page"""
        try:
            response: requests.Response = requests.get(product_url, headers=self.headers)
            soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
            
            for link_element in soup.find_all('a', class_='js-details-header'):
                data_url: Optional[str] = link_element.get('data-url')
                if data_url:
                    parsed_url = urlparse(data_url)
                    query_params: Dict[str, List[str]] = parse_qs(parsed_url.query)
                    return query_params.get('ean', [None])[0]
        except Exception:
            return None

    def _get_total_products(self) -> int:
        """Get total number of pages to scrape"""
        url: str = f'{self.base_url}?start=0&srule=FOOD-Bebidas&pmin=0.01'
        response: requests.Response = requests.get(url, headers=self.headers)
        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
        grid_footer = soup.find('div', class_='col-12 grid-footer')
        return int(grid_footer.get('data-total-count'))
