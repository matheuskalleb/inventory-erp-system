"""
Transações de Estoque
Define tipos de transações e seu fluxo de entrada/saída
"""

from typing import Optional
from datetime import datetime
from enum import Enum
import uuid
from pydantic import BaseModel, Field, validator


class TransactionType(str, Enum):
    """Tipos de transação suportados"""
    # Entrada
    PURCHASE_ORDER = "purchase_order"
    SALES_RETURN = "sales_return"
    INVENTORY_ADJUSTMENT = "inventory_adjustment"
    DONATION = "donation"
    
    # Saída
    SALES_ORDER = "sales_order"
    PURCHASE_RETURN = "purchase_return"
    WRITE_OFF = "write_off"
    TRANSFER = "transfer"


class TransactionStatus(str, Enum):
    """Estados de uma transação"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REVERSED = "reversed"


class Transaction(BaseModel):
    """
    Modelo de Transação
    
    Representa uma transação de entrada ou saída de estoque
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="ID único")
    product_code: str = Field(..., description="Código do produto")
    transaction_type: TransactionType = Field(..., description="Tipo de transação")
    quantity: int = Field(..., gt=0, description="Quantidade movimentada")
    
    # Informações financeiras
    unit_price: float = Field(..., gt=0, description="Preço unitário na transação")
    total_value: float = Field(default=0.0, description="Valor total da transação")
    
    # Metadados
    user: str = Field(default="system", description="Usuário que realizou a transação")
    reference: Optional[str] = Field(None, description="Referência externa (NF, PO, etc)")
    notes: Optional[str] = Field(None, max_length=500, description="Observações")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Status
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)
    
    class Config:
        use_enum_values = True
    
    @validator('total_value', always=True)
    def calculate_total_value(cls, v, values):
        """Calcula o valor total automaticamente"""
        if 'quantity' in values and 'unit_price' in values:
            return values['quantity'] * values['unit_price']
        return v
    
    def is_inbound(self) -> bool:
        """Retorna True se é uma transação de entrada"""
        inbound_types = {
            TransactionType.PURCHASE_ORDER,
            TransactionType.SALES_RETURN,
            TransactionType.INVENTORY_ADJUSTMENT,
            TransactionType.DONATION,
        }
        return TransactionType(self.transaction_type) in inbound_types
    
    def is_outbound(self) -> bool:
        """Retorna True se é uma transação de saída"""
        return not self.is_inbound()
    
    def get_quantity_adjustment(self) -> int:
        """
        Retorna o ajuste de quantidade considerando a direção
        Positivo para entrada, negativo para saída
        """
        adjustment = self.quantity
        if self.is_outbound():
            adjustment = -adjustment
        return adjustment
    
    def complete(self):
        """Marca a transação como completa"""
        self.status = TransactionStatus.COMPLETED
        self.completed_at = datetime.utcnow()
    
    def cancel(self):
        """Cancela a transação"""
        self.status = TransactionStatus.CANCELLED
    
    def reverse(self):
        """Reverte uma transação completa"""
        if self.status == TransactionStatus.COMPLETED:
            self.status = TransactionStatus.REVERSED
        else:
            raise ValueError("Apenas transações completadas podem ser revertidas")
    
    def to_dict(self) -> dict:
        """Converte transação para dicionário"""
        return {
            'id': self.id,
            'product_code': self.product_code,
            'type': self.transaction_type,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_value': round(self.total_value, 2),
            'user': self.user,
            'reference': self.reference,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'is_inbound': self.is_inbound(),
        }
