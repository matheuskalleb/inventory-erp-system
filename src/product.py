"""
Modelagem de Produtos
Define a estrutura e regras de negócio para produtos no inventário
"""

from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


class ProductStatus(str, Enum):
    """Estados possíveis de um produto"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    ON_ORDER = "on_order"


class Product(BaseModel):
    """
    Modelo de Produto
    
    Representa um produto no sistema com suas propriedades
    e controles de estoque
    """
    
    code: str = Field(..., min_length=1, max_length=50, description="SKU único do produto")
    name: str = Field(..., min_length=1, max_length=200, description="Nome do produto")
    description: Optional[str] = Field(None, max_length=500)
    
    # Preços e custos
    unit_price: float = Field(..., gt=0, description="Preço unitário")
    cost_price: float = Field(..., gt=0, description="Preço de custo")
    
    # Controles de estoque
    min_stock: int = Field(default=0, ge=0, description="Estoque mínimo permitido")
    max_stock: int = Field(default=100, gt=0, description="Estoque máximo permitido")
    current_stock: int = Field(default=0, ge=0, description="Quantidade atual em estoque")
    
    # Metadados
    status: ProductStatus = Field(default=ProductStatus.ACTIVE)
    category: str = Field(default="General", description="Categoria do produto")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Rastreamento
    total_sold: int = Field(default=0, ge=0, description="Total de unidades vendidas")
    total_purchased: int = Field(default=0, ge=0, description="Total de unidades compradas")
    
    class Config:
        use_enum_values = True
    
    @validator('max_stock')
    def max_stock_must_be_greater_than_min(cls, v, values):
        """Valida que estoque máximo é maior que estoque mínimo"""
        if 'min_stock' in values and v <= values['min_stock']:
            raise ValueError('max_stock deve ser maior que min_stock')
        return v
    
    @validator('cost_price')
    def cost_less_than_unit_price(cls, v, values):
        """Valida que o custo é menor que o preço de venda"""
        if 'unit_price' in values and v >= values['unit_price']:
            raise ValueError('cost_price deve ser menor que unit_price')
        return v
    
    def is_below_minimum(self) -> bool:
        """Verifica se o estoque está abaixo do mínimo"""
        return self.current_stock < self.min_stock
    
    def is_above_maximum(self) -> bool:
        """Verifica se o estoque está acima do máximo"""
        return self.current_stock > self.max_stock
    
    def needs_reorder(self) -> bool:
        """Determina se o produto precisa ser reordenado"""
        return self.current_stock <= (self.min_stock * 1.5)
    
    def profit_margin(self) -> float:
        """Calcula a margem de lucro em percentual"""
        if self.cost_price == 0:
            return 0.0
        return ((self.unit_price - self.cost_price) / self.unit_price) * 100
    
    def total_stock_value(self) -> float:
        """Calcula o valor total em estoque"""
        return self.current_stock * self.cost_price
    
    def update_timestamp(self):
        """Atualiza o timestamp de modificação"""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Converte produto para dicionário"""
        return {
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'unit_price': self.unit_price,
            'cost_price': self.cost_price,
            'current_stock': self.current_stock,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock,
            'status': self.status,
            'category': self.category,
            'profit_margin': round(self.profit_margin(), 2),
            'total_stock_value': round(self.total_stock_value(), 2),
        }
