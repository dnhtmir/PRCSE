from typing import List, Dict, Union, Optional, Any
import json
import os

class WinePriceComparator:
    def __init__(self, folder: str) -> None:
        self.continente_data = self._load_data(
            os.path.join(folder, "continente_wine_data.json")
        )
        self.auchan_data = self._load_data(
            os.path.join(folder, "auchan_wine_data.json")
        )

    def _load_data(self, filename: str) -> Dict[str, Dict[str, Any]]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def compare_prices(self) -> List[Dict[str, Union[str, float]]]:
        """Compare current prices for products between retailers"""
        results = []
        
        for ean, continente_product in self.continente_data.items():
            if ean in self.auchan_data:
                continente_price = continente_product['price_history'][-1]['price']
                auchan_price = self.auchan_data[ean]['price_history'][-1]['price']
                
                results.append({
                    "ean": ean,
                    "name": continente_product['name'],
                    "continente_price": continente_price,
                    "auchan_price": auchan_price,
                    "price_difference": continente_price - auchan_price
                })
        
        return results

    def get_price_history(self, ean: str) -> Dict[str, List[Dict[str, Union[float, str]]]]:
        """Get price history for a specific product from both retailers"""
        history = {}
        
        if ean in self.continente_data:
            history['continente'] = self.continente_data[ean]['price_history']
        
        if ean in self.auchan_data:
            history['auchan'] = self.auchan_data[ean]['price_history']
            
        return history