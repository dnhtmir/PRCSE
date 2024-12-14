import unittest  # Built-in module providing a testing framework
from unittest.mock import patch, MagicMock  # Built-in module providing mocking functionality for tests
import copy  # Built-in module for shallow and deep copying operations
import json  # Built-in module for JSON data encoding and decoding
import os  # Provides functions for interacting with the operating system (file paths, etc.)
from wine_price_comparator import WinePriceComparator  # Custom module containing price comparison functionality
from continente_scraper import ContinenteWineScraper  # Custom module containing Continente scraper implementation
from auchan_scraper import AuchanWineScraper  # Custom module containing Auchan scraper implementation

class TestScraperBase(unittest.TestCase):
    """Base test class with common setup and teardown"""
    
    def setUp(self):
        """Initialize test environment and sample data"""
        self.test_dir = os.path.join(os.getcwd(), "generated", "test")
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Sample product data for testing
        self._sample_product = {
            "name": "Test Wine",
            "price": 9.99,
            "brand": "Test Brand",
            "quantity": "garrafa 75cl",
            "price_per_litre": 13.32,
            "ean": "1234567890123"
        }
        
        self._sample_data = {
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
        """Clean up test files and directories"""
        for filename in ['continente_wine_data.json', 'auchan_wine_data.json']:
            filepath = os.path.join(self.test_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

class TestAuchanScraper(TestScraperBase):
    """Test suite for Auchan wine scraper functionality"""

    @staticmethod
    def _create_page_html(num_products, offset=0, price=9.99):
        """Helper function to create mock HTML for Auchan product pages
        
        Args:
            num_products (int): Number of product entries to generate
            offset (int): Starting offset for product numbering
            price (float): Price to set for the products
        """
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

    @patch('requests.get')
    def test_product_extraction(self, mock_get):
        """Test complete product extraction process including pagination"""
        scraper = AuchanWineScraper(self.test_dir)

        # Setup mock responses
        responses = {
            f"{scraper.base_url}?sz=24&start=0": self._create_page_html(24, 0),
            f"{scraper.base_url}?sz=24&start=24": self._create_page_html(24, 24),
        }
        
        # Create mock EAN pages
        for i in range(48):
            ean = f"1234{i:04d}567890"
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
        
        # Verify product extraction
        self.assertEqual(len(products), 40)
        self.assertEqual(products[0]["name"], "Test Wine 0")
        self.assertEqual(products[39]["name"], "Test Wine 39")

        # Verify correct API calls
        mock_get.assert_any_call(
            f"{scraper.base_url}?sz=24&start=0",
            headers=scraper.headers
        )
        mock_get.assert_any_call(
            f"{scraper.base_url}?sz=24&start=24",
            headers=scraper.headers
        )

    @patch('requests.get')
    def test_run_method(self, mock_get):
        """Test the complete run method and verify output files"""
        scraper = AuchanWineScraper(self.test_dir)

        responses = {
            f"{scraper.base_url}?sz=24&start=0": self._create_page_html(24, 0),
            f"{scraper.base_url}?sz=24&start=24": self._create_page_html(24, 24),
        }

        for i in range(48):
            ean = f"1234{i:04d}567890"
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

        # Verify file creation and content
        self.assertTrue(os.path.exists(scraper.data_file))
        with open(scraper.data_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        self.assertEqual(len(saved_data), 40)

        # Test price history update
        modified_html = self._create_page_html(24, 0, 10.99)
        responses[f"{scraper.base_url}?sz=24&start=0"] = modified_html
        
        scraper.run(40)
        
        with open(scraper.data_file, 'r', encoding='utf-8') as f:
            updated_data = json.load(f)
        
        first_product_key = list(updated_data.keys())[0]
        price_history = updated_data[first_product_key]['price_history']
        self.assertEqual(len(price_history), 2)
        self.assertEqual(price_history[0]['price'], 9.99)
        self.assertEqual(price_history[1]['price'], 10.99)

class TestContinenteScraper(TestScraperBase):
    """Test suite for Continente wine scraper functionality"""

    @patch('requests.get')
    def test_product_extraction(self, mock_get):
        """Test basic product extraction and parsing"""
        mock_response = MagicMock()
        mock_response.content = '''
            <div class="product-tile" data-product-tile-impression='{"name": "Test Wine", "brand": "Test Brand", "price": "9.99"}'>
                <div class="ct-pdp-link"><a href="https://www.continente.pt/test-wine"></a></div>
                <p class="pwc-tile--quantity">garrafa 75cl</p>
                <span class="ct-price-value">€13,32</span>
            </div>
        '''
        
        ean_response = MagicMock()
        ean_response.content = '''
            <a class="js-details-header" data-url="?ean=1234567890123"></a>
        '''
        mock_get.side_effect = [mock_response, ean_response]
        
        scraper = ContinenteWineScraper(self.test_dir)
        products = scraper._get_product_data(product_offset=0, product_limit=1)
        
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Test Wine")
        self.assertEqual(products[0]["ean"], "1234567890123")
        self.assertAlmostEqual(products[0]["price_per_litre"], 13.32, places=2)

    @patch('requests.get')
    def test_fallback_parsing(self, mock_get):
        """Test HTML parsing fallback when JSON data is invalid"""
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
        
        ean_response = MagicMock()
        ean_response.content = '''
            <a class="js-details-header" data-url="?ean=1234567890123"></a>
        '''
        mock_get.side_effect = [mock_response, ean_response]
        
        scraper = ContinenteWineScraper(self.test_dir)
        products = scraper._get_product_data(product_offset=0, product_limit=1)
        
        self.assertEqual(products[0]["name"], "Test Wine Fallback")
        self.assertEqual(products[0]["brand"], "Test Brand Fallback")

class TestPriceComparator(TestScraperBase):
    """Test suite for wine price comparison functionality"""

    def test_price_comparison(self):
        """Test price comparison between different retailers"""
        # Setup test data with different prices
        continente_data = copy.deepcopy(self._sample_data)
        auchan_data = copy.deepcopy(self._sample_data)
        auchan_data["1234567890123"]["price_history"][0]["price"] = 8.99
        
        # Save test data
        with open(os.path.join(self.test_dir, "continente_wine_data.json"), "w") as f:
            json.dump(continente_data, f)
        with open(os.path.join(self.test_dir, "auchan_wine_data.json"), "w") as f:
            json.dump(auchan_data, f)

        scrapers = [
            ContinenteWineScraper(self.test_dir),
            AuchanWineScraper(self.test_dir)
        ]
            
        comparator = WinePriceComparator(*scrapers)
        results = comparator.compare_prices()
        
        # Verify comparison results
        self.assertEqual(results[0]["price_differences"]["Continente"], 1.0)
        self.assertEqual(results[0]["cheapest_retailer"], "Auchan")
        self.assertEqual(results[0]["retailers"], 2)

    def test_price_history(self):
        """Test price history tracking and updates"""
        continente_data = copy.deepcopy(self._sample_data)
        auchan_data = copy.deepcopy(self._sample_data)
        
        # Add price history entries
        continente_data["1234567890123"]["price_history"].append({
            "price": 10.99,
            "price_per_litre": 14.65,
            "timestamp": "2024-03-21T10:00:00"
        })
        
        auchan_data["1234567890123"]["price_history"].append({
            "price": 9.99,
            "price_per_litre": 13.32,
            "timestamp": "2024-03-21T10:00:00"
        })
        
        with open(os.path.join(self.test_dir, "continente_wine_data.json"), "w") as f:
            json.dump(continente_data, f)
        with open(os.path.join(self.test_dir, "auchan_wine_data.json"), "w") as f:
            json.dump(auchan_data, f)
            
        scrapers = [
            ContinenteWineScraper(self.test_dir),
            AuchanWineScraper(self.test_dir)
        ]
        
        comparator = WinePriceComparator(*scrapers)
        history = comparator.get_price_history("1234567890123")
        
        # Verify price history
        self.assertEqual(len(history["Continente"]), 2)
        self.assertEqual(len(history["Auchan"]), 2)
        self.assertEqual(history["Continente"][-1]["price"], 10.99)
        self.assertEqual(history["Auchan"][-1]["price"], 9.99)

if __name__ == '__main__':
    unittest.main()
