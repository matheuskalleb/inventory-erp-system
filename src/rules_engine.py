"""
Motor de Regras de Negócio
Implementa validações e regras de negócio para o sistema
"""

from typing import List, Tuple
from .product import Product
from .transaction import Transaction, TransactionType


class BusinessRuleViolation(Exception):
    """Exceção para violações de regras de negócio"""
    pass


class RulesEngine:
    """
    Motor de execução de regras de negócio
    
    Valida transações e operações contra regras configuradas
    """
    
    def __init__(self):
        self.violations: List[str] = []
    
    def validate_transaction(self, transaction: Transaction, product: Product) -> Tuple[bool, List[str]]:
        """
        Valida uma transação contra as regras de negócio
        
        Retorna: (válido, lista_de_erros)
        """
        self.violations = []
        
        # Regra 1: Produto deve estar ativo
        if product.status != "active":
            self.violations.append(f"Produto '{product.code}' não está ativo")
        
        # Regra 2: Quantidade deve ser positiva
        if transaction.quantity <= 0:
            self.violations.append("Quantidade deve ser maior que zero")
        
        # Regra 3: Para saída, verificar disponibilidade
        if transaction.is_outbound():
            available = product.current_stock
            if transaction.quantity > available:
                self.violations.append(
                    f"Estoque insuficiente. Disponível: {available}, Solicitado: {transaction.quantity}"
                )
        
        # Regra 4: Após entrada, não deve exceder máximo (com tolerância de 10%)
        if transaction.is_inbound():
            new_stock = product.current_stock + transaction.quantity
            max_allowed = product.max_stock * 1.1
            if new_stock > max_allowed:
                self.violations.append(
                    f"Entrada excederia estoque máximo. Máximo permitido: {int(max_allowed)}, "
                    f"Resultado: {int(new_stock)}"
                )
        
        # Regra 5: Preço deve ser coerente
        if transaction.unit_price <= 0:
            self.violations.append("Preço unitário deve ser positivo")
        
        # Regra 6: Devolução de compra não pode ser maior que histórico de compras
        if transaction.transaction_type == TransactionType.PURCHASE_RETURN:
            if transaction.quantity > product.total_purchased:
                self.violations.append(
                    f"Devolução de compra inválida. Total comprado: {product.total_purchased}, "
                    f"Solicitado: {transaction.quantity}"
                )
        
        return len(self.violations) == 0, self.violations
    
    def validate_stock_levels(self, product: Product) -> dict:
        """
        Valida níveis de estoque e gera alertas
        
        Retorna um dicionário com status de alertas
        """
        alerts = {
            'is_below_minimum': product.is_below_minimum(),
            'is_above_maximum': product.is_above_maximum(),
            'needs_reorder': product.needs_reorder(),
            'messages': []
        }
        
        if alerts['is_below_minimum']:
            alerts['messages'].append(
                f"ALERTA CRÍTICO: Produto '{product.code}' abaixo do mínimo "
                f"({product.current_stock}/{product.min_stock})"
            )
        
        if alerts['is_above_maximum']:
            alerts['messages'].append(
                f"AVISO: Produto '{product.code}' acima do máximo "
                f"({product.current_stock}/{product.max_stock})"
            )
        
        if alerts['needs_reorder'] and not alerts['is_below_minimum']:
            alerts['messages'].append(
                f"INFO: Produto '{product.code}' próximo ao mínimo. Considere reordenar."
            )
        
        return alerts
    
    def can_perform_transaction(self, transaction: Transaction, product: Product) -> bool:
        """Verificação rápida se transação pode ser realizada"""
        valid, _ = self.validate_transaction(transaction, product)
        return valid
    
    def get_last_violations(self) -> List[str]:
        """Retorna as últimas violações de regras registradas"""
        return self.violations.copy()
    
    def validate_product_creation(self, code: str, name: str, min_stock: int, max_stock: int) -> Tuple[bool, List[str]]:
        """Valida criação de novo produto"""
        errors = []
        
        if not code or len(code) > 50:
            errors.append("Código do produto inválido")
        
        if not name or len(name) > 200:
            errors.append("Nome do produto inválido")
        
        if min_stock < 0:
            errors.append("Estoque mínimo não pode ser negativo")
        
        if max_stock <= min_stock:
            errors.append("Estoque máximo deve ser maior que o mínimo")
        
        return len(errors) == 0, errors
