"""
Testes para modelagem de produtos
"""

import pytest
from src.product import Product, ProductStatus


def test_product_creation():
    """Testa criação básica de produto"""
    product = Product(
        code="SKU001",
        name="Notebook",
        unit_price=2500.0,
        cost_price=1750.0,
        min_stock=5,
        max_stock=30,
    )
    assert product.code == "SKU001"
    assert product.name == "Notebook"
    assert product.status == ProductStatus.ACTIVE


def test_profit_margin_calculation():
    """Testa cálculo de margem de lucro"""
    product = Product(
        code="SKU001",
        name="Test",
        unit_price=100.0,
        cost_price=70.0,
    )
    # Margem esperada: (100-70)/100 * 100 = 30%
    assert product.profit_margin() == 30.0


def test_stock_level_validations():
    """Testa validações de nível de estoque"""
    product = Product(
        code="SKU001",
        name="Test",
        unit_price=100.0,
        cost_price=70.0,
        min_stock=10,
        max_stock=50,
        current_stock=5,
    )
    assert product.is_below_minimum() == True
    assert product.is_above_maximum() == False


def test_reorder_logic():
    """Testa lógica de reordenação"""
    product = Product(
        code="SKU001",
        name="Test",
        unit_price=100.0,
        cost_price=70.0,
        min_stock=10,
        max_stock=50,
        current_stock=15,
    )
    assert product.needs_reorder() == True


def test_invalid_stock_range():
    """Testa validação de intervalo de estoque"""
    with pytest.raises(ValueError):
        Product(
            code="SKU001",
            name="Test",
            unit_price=100.0,
            cost_price=70.0,
            min_stock=50,
            max_stock=30,  # Inválido: max < min
        )


def test_invalid_price_relationship():
    """Testa validação de preços"""
    with pytest.raises(ValueError):
        Product(
            code="SKU001",
            name="Test",
            unit_price=100.0,
            cost_price=150.0,  # Inválido: custo > venda
        )
