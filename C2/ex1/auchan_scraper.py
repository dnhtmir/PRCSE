from bs4 import BeautifulSoup
import json
import requests
import os
from datetime import datetime
from base_scraper import BaseWineScraper

class AuchanWineScraper(BaseWineScraper):
    def __init__(self):
        super().__init__(
            base_url="https://www.auchan.pt/pt/bebidas-e-garrafeira/garrafeira/",
            data_file=os.path.join(os.getcwd(), "generated", "auchan_wine_data.json"),
            size=24
        )

    def get_product_data(self, page=0):
        """Get products from a specific page"""
        url = f"{self.base_url}?sz={self.size}&start={page}"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        for product in soup.find_all("div", class_="product-tile"):
            product_data = self.scrape_product(product)
            if product_data:
                products.append(product_data)
            
        return products

    def scrape_product(self, product):
        """Extract product information from a product element"""
        try:
            impression_data = product.get('data-gtm')
            product_info = json.loads(impression_data)
            name = product_info.get('name', '')
            brand = product_info.get('brand', '')
            price = float(product_info.get('price', 0))
            
            quantity = self._extract_quantity(name)
            data_urls = product.get('data-urls', '')
            product_urls = json.loads(data_urls)
            link = 'https://www.auchan.pt' + product_urls.get('productUrl', '')
            ean = self._extract_ean(link)
            
            return {
                "name": name,
                "price": price,
                "brand": brand,
                "quantity": quantity,
                "ean": ean,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error scraping product: {e}")
            return None
        
    def _extract_ean(self, product_url):
        """Extract EAN from product page"""
        try:
            response = requests.get(product_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.find('span', class_='product-ean').text.strip()
        except Exception as e:
            print(f"Error extracting EAN: {e}")
            return None

    def _extract_quantity(self, name):
        """Extract quantity from product name"""
        # TODO: Implement quantity extraction logic
        # Common patterns: "750ml", "75cl", "1L", etc.
        return None

    def _get_total_products(self) -> int:
        """Get total number of pages to scrape"""
        url = f'{self.base_url}?sz={self.size}&start=0'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        input_element = soup.find('input', {'name': 'auc-js-search-results-total'})
        total_count = int(input_element.get('value'))
        return (total_count + self.size - 1) // self.size

    def _scrape_all_products(self, product_limit: int) -> list:
        """Implementation of the abstract method from BaseWineScraper"""
        all_products = []
        page = 0
        while True:
            products = self.get_product_data(page)
            if not products:
                break
            all_products.extend(products)
            page += self.size

            if page >= product_limit:
                break
                
        return all_products

