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

# TODO: classe é aplicável apenas ao continente. Deve ser adaptada para outros sites,
# talvez recebendo um input que permita definir urls e os locais onde a informação pode ser adquirida
class WineScraperContinente:
    def __init__(self):
        self.base_url = 'https://www.continente.pt/bebidas-e-garrafeira/vinhos/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.data_file = 'wine_data.json' # TODO: mover para C2/ex1/wine_data.json

    def get_product_data(self, page=0):
        url = f'{self.base_url}?start={page}&srule=FOOD-Bebidas&pmin=0.01'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        for product in soup.find_all('div', class_='product-tile'):
            try:
                name = product.find('h2', class_='pwc-tile--description').text.strip()
                print(name)
                brand = product.find('p', class_='pwc-tile--brand').text.strip()
                print(brand)
                price = float(product.find('span', class_='ct-price-formatted').text.strip().replace('.', '').replace('€', '').replace(',', '.'))
                print(price)
                price_per_liter = float(product.find('span', class_='ct-price-value').text.strip().replace('.', '').replace('€', '').replace(',', '.'))
                print(price_per_liter)
                # TODO: avaliar a possível inclusão do id do produto e da utilização do mesmo para efeitos de update de preço
                
                products.append({
                    'name': name,
                    'brand': brand,
                    'price': price,
                    'price per liter': price_per_liter,
                    'timestamp': datetime.now().isoformat()
                })
            except AttributeError:
                continue
            
        return products

    def load_existing_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self, products):
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

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

    def run_periodic_scraping(self, interval_hours=24):
        while True:
            print(f"Starting scraping at {datetime.now()}")

            url = f'{self.base_url}?start=0&srule=FOOD-Bebidas&pmin=0.01'
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            grid_footer = soup.find('div', class_='col-12 grid-footer')
            total_count = int(grid_footer.get('data-total-count'))

            all_products = []
            # TODO: o total_count é 8000+, logo para efeitos de teste limita-se a 200 para não ficar eternamente à espera
            # for page in range(0, total_count, 36):
            for page in range(0, 200, 36):
                products = self.get_product_data(page)
                if not products:
                    break
                all_products.extend(products)
            
            self.save_data(all_products)
            print(f"Scraped {len(all_products)} products. Waiting {interval_hours} hours...")
            # TODO: validar se a script fica em produção 24 sob 24 horas e faz o sleep por si própria ou se colocamos no crontab
            time.sleep(interval_hours * 3600)

if __name__ == "__main__":
    scraper = WineScraperContinente()
    scraper.run_periodic_scraping()
