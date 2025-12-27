from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class PricingInput:
    base_price: float
    quantity: int
    complexity_multiplier: float
    material_multiplier: float = 1.0
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None


@dataclass
class PricingBreakdown:
    base_price: float
    complexity_multiplier: float
    material_multiplier: float
    quantity_multiplier: float
    dimension_multiplier: float
    subtotal_before_quantity: float
    total_price: float
    breakdown: Dict[str, float]


class PricingEngine:
    QUANTITY_DISCOUNT_TIERS = [
        (1, 1.0),
        (10, 0.95),
        (25, 0.90),
        (50, 0.85),
        (100, 0.80),
    ]
    
    DIMENSION_BASE_VOLUME = 1000.0
    DIMENSION_SCALE_FACTOR = 0.15
    
    @staticmethod
    def calculate_quantity_multiplier(quantity: int) -> float:
        multiplier = 1.0
        for threshold, discount in reversed(PricingEngine.QUANTITY_DISCOUNT_TIERS):
            if quantity >= threshold:
                multiplier = discount
                break
        return multiplier
    
    @staticmethod
    def calculate_dimension_multiplier(
        length: Optional[float],
        width: Optional[float],
        height: Optional[float]
    ) -> float:
        if not all([length, width, height]) or any(d <= 0 for d in [length, width, height]):
            return 1.0
        
        volume = length * width * height
        
        if volume <= PricingEngine.DIMENSION_BASE_VOLUME:
            return 1.0
        
        ratio = volume / PricingEngine.DIMENSION_BASE_VOLUME
        multiplier = 1.0 + (ratio - 1.0) * PricingEngine.DIMENSION_SCALE_FACTOR
        
        return round(multiplier, 3)
    
    @staticmethod
    def calculate_price(pricing_input: PricingInput) -> PricingBreakdown:
        quantity_multiplier = PricingEngine.calculate_quantity_multiplier(
            pricing_input.quantity
        )
        
        dimension_multiplier = PricingEngine.calculate_dimension_multiplier(
            pricing_input.length,
            pricing_input.width,
            pricing_input.height
        )
        
        unit_price = (
            pricing_input.base_price
            * pricing_input.complexity_multiplier
            * pricing_input.material_multiplier
            * dimension_multiplier
        )
        
        subtotal_before_quantity = unit_price
        total_price = unit_price * pricing_input.quantity * quantity_multiplier
        
        breakdown = {
            "base_price": pricing_input.base_price,
            "after_complexity": pricing_input.base_price * pricing_input.complexity_multiplier,
            "after_material": pricing_input.base_price * pricing_input.complexity_multiplier * pricing_input.material_multiplier,
            "unit_price": unit_price,
            "before_quantity_discount": unit_price * pricing_input.quantity,
            "total": total_price
        }
        
        return PricingBreakdown(
            base_price=pricing_input.base_price,
            complexity_multiplier=pricing_input.complexity_multiplier,
            material_multiplier=pricing_input.material_multiplier,
            quantity_multiplier=quantity_multiplier,
            dimension_multiplier=dimension_multiplier,
            subtotal_before_quantity=subtotal_before_quantity,
            total_price=round(total_price, 2),
            breakdown=breakdown
        )
