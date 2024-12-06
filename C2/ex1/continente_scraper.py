# [7.5 values] Web scraping is sometimes used for malicious purposes. For example, large retailers
# can use web scraping to exploit websites of their own competitors, building a huge database of
# products, prices and discounts for further analysis. In the context of PRCSE UC, pretend that you
# were hired to perform such a task.
# a. Start by choosing a Portuguese retailer website (e.g., continente) and a set of product
# categories (e.g., cookies, cheese).
# b. Perform a web scraping script that can extract all relevant information (description,
# brand, price, price by gram or liter, quantity) about all available products within the
# chosen retailer’s website for the selected categories.
# c. Implement the logic that allows the script to be executed periodically (e.g., every 24
# hours), persisting the obtained data in a database (e.g. SQLite) or a .json file. Don’t
# persist duplicate products and watch for price updates.
# d. Compare products among different retailers.

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import os
from urllib.parse import urlparse, parse_qs
from base_scraper import BaseWineScraper

class ContinenteWineScraper(BaseWineScraper):
    def __init__(self):
        super().__init__(
            base_url='https://www.continente.pt/bebidas-e-garrafeira/vinhos/',
            data_file=os.path.join(os.getcwd(), "generated", "continente_wine_data.json"),
            size=36
        )

    def get_product_data(self, page: int = 0) -> list:
        """Get products from a specific page"""
        url = f'{self.base_url}?start={page}&srule=FOOD-Bebidas&pmin=0.01'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        for product in soup.find_all('div', class_='product-tile'):
            product_data = self.scrape_product(product)
            if product_data:
                products.append(product_data)
            
        return products

    def scrape_product(self, product) -> dict:
        """Extract product information from a product element"""
        try:
            impression_data = product.get('data-product-tile-impression')
            
            if impression_data:
                try:
                    # Try to get data from JSON first
                    product_info = json.loads(impression_data)
                    name = product_info.get('name', '')
                    brand = product_info.get('brand', '')
                    price = float(product_info.get('price', 0))
                except:
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
            quantity = self._extract_quantity(name)

            return {
                'name': name,
                'brand': brand,
                'price': price,
                'ean': ean,
                'quantity': quantity,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error scraping product: {e}")
            return None

    def _extract_ean(self, product_url: str) -> str:
        """Extract EAN from product page"""
        try:
            response = requests.get(product_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link_element in soup.find_all('a', class_='js-details-header'):
                data_url = link_element.get('data-url')
                if data_url:
                    parsed_url = urlparse(data_url)
                    query_params = parse_qs(parsed_url.query)
                    return query_params.get('ean', [None])[0]
        except Exception:
            return None

    def _extract_quantity(self, name: str) -> str:
        """Extract quantity from product name"""
        # TODO: Implement quantity extraction logic
        # Common patterns: "750ml", "75cl", "1L", etc.
        return None

    def _get_total_products(self) -> int:
        """Get total number of pages to scrape"""
        url = f'{self.base_url}?start=0&srule=FOOD-Bebidas&pmin=0.01'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        grid_footer = soup.find('div', class_='col-12 grid-footer')
        total_count = int(grid_footer.get('data-total-count'))
        return (total_count + self.size - 1) // self.size 

    def _scrape_all_products(self, product_limit: int) -> list:
        """Implementation of the abstract method from BaseWineScraper"""
        all_products = []
        total_pages = min(self._get_total_products(), (product_limit + self.size - 1) // self.size)
        for page in range(0, product_limit, self.size):
            products = self.get_product_data(page)
            if not products:
                break
            all_products.extend(products)
        return all_products
