from typing import Any, Dict, List

from src.domain.item import Item


class ItemComparison:
    @staticmethod
    def compare_items(items: List[Item]) -> Dict[str, Any]:
        if not items:
            return {"items": [], "specifications_comparison": {}}

        prices = [item.price for item in items]
        ratings = [item.rating for item in items]

        # Análise de preços
        price_analysis = {
            "lowest": min(prices),
            "highest": max(prices),
            "difference": max(prices) - min(prices),
        }

        # Análise de avaliações
        rating_analysis = {
            "lowest": min(ratings),
            "highest": max(ratings),
            "average": sum(ratings) / len(ratings),
        }

        # Compara especificações
        all_specs = set()
        for item in items:
            all_specs.update(item.specifications.keys())

        specs_comparison = {}
        for spec in all_specs:
            specs_comparison[spec] = {
                item.name: item.specifications.get(spec, "Não especificado") for item in items
            }

        return {
            "items": items,
            "price_analysis": price_analysis,
            "rating_analysis": rating_analysis,
            "specifications_comparison": specs_comparison,
        }
