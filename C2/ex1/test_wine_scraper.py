import unittest
from unittest.mock import patch, MagicMock
import copy
import json
import os
from datetime import datetime
from wine_price_comparator import WinePriceComparator
from continente_scraper import ContinenteWineScraper
from auchan_scraper import AuchanWineScraper

# Auxiliary function to create HTML for testing (Auchan)
def create_page_html_auchan(num_products, offset=0, price=9.99):
    products_html = []
    for i in range(num_products):
        products_html.append(f'''
            <div class="product-tile" 
                data-gtm-new='{{"item_name": "Test Wine {i+offset}", "item_brand": "Test Brand", "price": "{price}", "quantity": "1"}}' 
                data-urls='{{"productUrl": "/test-wine-{i+offset}"}}'>
                <span class="auc-measures--price-per-unit">13.32 €/Lt</span>
            </div>
        ''')
    return '<div>' + ''.join(products_html) + '</div>'

class TestWineScraper(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.getcwd(), "generated", "test")
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.sample_product = {
            "name": "Test Wine",
            "price": 9.99,
            "brand": "Test Brand",
            "quantity": "750ml",
            "price_per_litre": 13.32,
            "ean": "1234567890123"
        }
        
        self.sample_data = {
            "1234567890123": {
                "name": "Test Wine",
                "brand": "Test Brand",
                "quantity": "garrafa 75cl",
                "price_history": [
                    {"price": 9.99, "price_per_litre": 13.32, "timestamp": "2024-03-20T10:00:00"}
                ]
            }
        }

    def tearDown(self):
        for filename in ['continente_wine_data.json', 'auchan_wine_data.json']:
            filepath = os.path.join(self.test_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    @patch('requests.get')
    def test_auchan_scraper(self, mock_get):
        scraper = AuchanWineScraper(self.test_dir)

        responses = {
            f"{scraper.base_url}?sz=24&start=0": create_page_html_auchan(24, 0),
            f"{scraper.base_url}?sz=24&start=24": create_page_html_auchan(24, 24),
        }
        
        for i in range(48):
            ean = f"1234{i:04d}567890"  # Creates unique 13-digit EANs like 1234000567890, 1234000167890, etc
            responses[f"https://www.auchan.pt/test-wine-{i}"] = f'''
                <span class="product-ean">{ean}</span>
            '''

        def mock_response(*args, **kwargs):
            url = args[0]
            response = MagicMock()
            response.content = responses.get(url, '<div></div>')
            return response

        mock_get.side_effect = mock_response
        
        products = scraper._scrape_all_products(40)
        
        self.assertEqual(len(products), 40)
        
        self.assertEqual(products[0]["name"], "Test Wine 0")
        self.assertEqual(products[23]["name"], "Test Wine 23")
        self.assertEqual(products[24]["name"], "Test Wine 24")
        self.assertEqual(products[39]["name"], "Test Wine 39")

        mock_get.assert_any_call(
            f"{scraper.base_url}?sz=24&start=0",
            headers=scraper.headers
        )
        mock_get.assert_any_call(
            f"{scraper.base_url}?sz=24&start=24",
            headers=scraper.headers
        )
        for i in range(40):
            mock_get.assert_any_call(
                f"https://www.auchan.pt/test-wine-{i}",
                headers=scraper.headers
            )
            
        self.assertEqual(mock_get.call_count, 42)

    @patch('requests.get')
    def test_continente_scraper(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '''
            <div class="product-tile" data-product-tile-impression='{"name": "Test Wine", "brand": "Test Brand", "price": "9.99"}'>
                <div class="ct-pdp-link"><a href="https://www.continente.pt/test-wine"></a></div>
                <p class="pwc-tile--quantity">garrafa 75cl</p>
                <span class="ct-price-value">€13,32</span>
            </div>
        '''
        mock_get.return_value = mock_response
        
        # Mock the EAN extraction response
        ean_response = MagicMock()
        ean_response.content = '''
            <a class="js-details-header" data-url="?ean=1234567890123"></a>
        '''
        mock_get.side_effect = [mock_response, ean_response]
        
        scraper = ContinenteWineScraper(self.test_dir)
        products = scraper.get_product_data(product_offset=0, product_limit=1)
        
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Test Wine")
        self.assertEqual(products[0]["price"], 9.99)
        self.assertEqual(products[0]["quantity"], "garrafa 75cl")
        self.assertEqual(products[0]["ean"], "1234567890123")
        self.assertAlmostEqual(products[0]["price_per_litre"], 13.32, places=2)

    @patch('requests.get')
    def test_continente_scraper_fallback_parsing(self, mock_get):
        """Test Continente scraper's fallback to HTML parsing when JSON is invalid"""
        mock_response = MagicMock()
        mock_response.content = '''
            <div class="product-tile" data-product-tile-impression='{name: '>
                <h2 class="pwc-tile--description">Test Wine Fallback</h2>
                <p class="pwc-tile--brand">Test Brand Fallback</p>
                <span class="ct-price-formatted">€9,99</span>
                <div class="ct-pdp-link"><a href="https://www.continente.pt/test-wine"></a></div>
                <p class="pwc-tile--quantity">garrafa 75cl</p>
                <span class="ct-price-value">€13,32</span>
            </div>
        '''
        mock_get.return_value = mock_response
        
        ean_response = MagicMock()
        ean_response.content = '''
            <a class="js-details-header" data-url="?ean=1234567890123"></a>
        '''
        mock_get.side_effect = [mock_response, ean_response]
        
        scraper = ContinenteWineScraper(self.test_dir)
        products = scraper.get_product_data(product_offset=0, product_limit=1)
        
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Test Wine Fallback")
        self.assertEqual(products[0]["brand"], "Test Brand Fallback")
        self.assertEqual(products[0]["price"], 9.99)
        self.assertEqual(products[0]["quantity"], "garrafa 75cl")
        self.assertEqual(products[0]["ean"], "1234567890123")
        self.assertAlmostEqual(products[0]["price_per_litre"], 13.32, places=2)

    def test_price_comparator_with_price_per_litre(self):
        continente_data = copy.deepcopy(self.sample_data)
        auchan_data = copy.deepcopy(self.sample_data)
        auchan_data["1234567890123"]["price_history"][0]["price"] = 8.99
        auchan_data["1234567890123"]["price_history"][0]["price_per_litre"] = 11.99
        
        with open(os.path.join(self.test_dir, "continente_wine_data.json"), "w") as f:
            json.dump(continente_data, f)
        with open(os.path.join(self.test_dir, "auchan_wine_data.json"), "w") as f:
            json.dump(auchan_data, f)
            
        comparator = WinePriceComparator(self.test_dir)
        results = comparator.compare_prices()
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["price_difference"], 1.0)
        self.assertEqual(results[0]["continente_price"], 9.99)
        self.assertEqual(results[0]["auchan_price"], 8.99)

    def test_price_history(self):
        test_data = self.sample_data.copy()
        test_data["1234567890123"]["price_history"].append({
            "price": 10.99,
            "timestamp": "2024-03-21T10:00:00"
        })
        test_data["1234567890123"]["price_per_litre"] = 14.65
        
        with open(os.path.join(self.test_dir, "continente_wine_data.json"), "w") as f:
            json.dump(test_data, f)
            
        comparator = WinePriceComparator(self.test_dir)
        history = comparator.get_price_history("1234567890123")
        
        self.assertEqual(len(history["continente"]), 2)
        self.assertEqual(history["continente"][-1]["price"], 10.99)
        self.assertAlmostEqual(test_data["1234567890123"]["price_per_litre"], 14.65, places=2)

    @patch('requests.get')
    def test_run_method_and_file_output(self, mock_get):
        """Test the complete run method and verify output files"""
        scraper = AuchanWineScraper(self.test_dir)

        responses = {
            f"{scraper.base_url}?sz=24&start=0": create_page_html_auchan(24, 0),
            f"{scraper.base_url}?sz=24&start=24": create_page_html_auchan(24, 24),
        }

        for i in range(48):
            ean = f"1234{i:04d}567890"  # Creates unique 13-digit EANs like 1234000567890, 1234000167890, etc
            responses[f"https://www.auchan.pt/test-wine-{i}"] = f'''
                <span class="product-ean">{ean}</span>
            '''

        def mock_response(*args, **kwargs):
            url = args[0]
            response = MagicMock()
            response.content = responses.get(url, '<div></div>')
            return response

        mock_get.side_effect = mock_response
        scraper.run(40)

        self.assertTrue(os.path.exists(scraper.data_file))

        with open(scraper.data_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)

        self.assertEqual(len(saved_data), 40)
        
        first_product = saved_data[list(saved_data.keys())[0]]
        self.assertIn('name', first_product)
        self.assertIn('brand', first_product)
        self.assertIn('quantity', first_product)
        self.assertIn('price_history', first_product)
        
        price_history = first_product['price_history']
        self.assertEqual(len(price_history), 1)
        self.assertIn('price', price_history[0])
        self.assertIn('timestamp', price_history[0])
        
        modified_html = create_page_html_auchan(24, 0, 10.99)
        responses[f"{scraper.base_url}?sz=24&start=0"] = modified_html
        
        scraper.run(40)
        
        with open(scraper.data_file, 'r', encoding='utf-8') as f:
            updated_data = json.load(f)
        
        first_product_key = list(updated_data.keys())[0]
        updated_price_history = updated_data[first_product_key]['price_history']
        
        self.assertEqual(len(updated_price_history), 2)
        self.assertEqual(updated_price_history[0]['price'], 9.99)
        self.assertEqual(updated_price_history[1]['price'], 10.99)

if __name__ == '__main__':
    unittest.main()
