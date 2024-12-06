import json
import os

class WinePriceComparator:
    def __init__(self):
        self.continente_data = self._load_data(os.path.join(os.getcwd(), "generated", "continente_wine_data.json"))
        self.auchan_data = self._load_data(os.path.join(os.getcwd(), "generated", "auchan_wine_data.json"))

    def _load_data(self, filename: str) -> list[dict]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def compare_prices(self) -> list[dict[str, str | float]]:
        """Compare prices for products between retailers"""
        results: list[dict[str, str | float]] = []
        
        auchan_by_ean: dict[str, dict] = {p["ean"]: p for p in self.auchan_data if p.get("ean")}
        
        for continente_product in self.continente_data:
            ean: str | None = continente_product.get("ean")
            if not ean:
                continue
                
            auchan_product = auchan_by_ean.get(ean)
            if auchan_product:
                results.append({
                    "ean": ean,
                    "name": continente_product["name"],
                    "continente_price": continente_product["price"],
                    "auchan_price": auchan_product["price"],
                    "price_difference": continente_product["price"] - auchan_product["price"]
                })
                
        return results