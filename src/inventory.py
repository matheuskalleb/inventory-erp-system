"""
Gerenciador de Inventário
Controla todas as operações de estoque e produtos
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from .product import Product, ProductStatus
from .transaction import Transaction, TransactionType, TransactionStatus
from .rules_engine import RulesEngine, BusinessRuleViolation


class Inventory:
    """
    Gerenciador de Inventário
    
    Controla produtos, estoque e transações no sistema
    """
    
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.transactions: List[Transaction] = []
        self.rules_engine = RulesEngine()
    
    def add_product(self, product: Product) -> Tuple[bool, str]:
        """
        Adiciona um novo produto ao inventário
        
        Retorna: (sucesso, mensagem)
        """
        if product.code in self.products:
            return False, f"Produto com código '{product.code}' já existe"
        
        valid, errors = self.rules_engine.validate_product_creation(
            product.code, product.name, product.min_stock, product.max_stock
        )
        
        if not valid:
            return False, "; ".join(errors)
        
        self.products[product.code] = product
        return True, f"Produto '{product.code}' adicionado com sucesso"
    
    def get_product(self, code: str) -> Optional[Product]:
        """Obtém um produto pelo código"""
        return self.products.get(code)
    
    def remove_product(self, code: str) -> Tuple[bool, str]:
        """Remove um produto do inventário"""
        if code not in self.products:
            return False, f"Produto '{code}' não encontrado"
        
        del self.products[code]
        return True, f"Produto '{code}' removido"
    
    def process_transaction(self, transaction: Transaction) -> Tuple[bool, str]:
        """
        Processa uma transação de entrada ou saída
        
        Retorna: (sucesso, mensagem)
        """
        product = self.get_product(transaction.product_code)
        if not product:
            return False, f"Produto '{transaction.product_code}' não encontrado"
        
        # Validar contra regras de negócio
        valid, errors = self.rules_engine.validate_transaction(transaction, product)
        if not valid:
            return False, "; ".join(errors)
        
        # Processar a transação
        adjustment = transaction.get_quantity_adjustment()
        product.current_stock += adjustment
        
        # Atualizar histórico
        if transaction.is_inbound():
            product.total_purchased += transaction.quantity
        else:
            product.total_sold += transaction.quantity
        
        product.update_timestamp()
        transaction.complete()
        
        self.transactions.append(transaction)
        
        return True, f"Transação '{transaction.id}' processada com sucesso"
    
    def get_transaction_history(self, product_code: Optional[str] = None) -> List[Transaction]:
        """Obtém histórico de transações"""
        if product_code:
            return [t for t in self.transactions if t.product_code == product_code]
        return self.transactions.copy()
    
    def get_stock_level(self, code: str) -> Optional[int]:
        """Obtém nível de estoque de um produto"""
        product = self.get_product(code)
        return product.current_stock if product else None
    
    def get_low_stock_products(self) -> List[Product]:
        """Lista produtos com estoque baixo"""
        return [p for p in self.products.values() if p.is_below_minimum()]
    
    def get_high_stock_products(self) -> List[Product]:
        """Lista produtos com estoque alto"""
        return [p for p in self.products.values() if p.is_above_maximum()]
    
    def get_reorder_list(self) -> List[Product]:
        """Lista produtos que precisam de reordenação"""
        return [p for p in self.products.values() if p.needs_reorder()]
    
    def get_stock_value(self) -> float:
        """Calcula o valor total do estoque"""
        return sum(p.total_stock_value() for p in self.products.values())
    
    def get_alerts(self) -> dict:
        """Gera todos os alertas do sistema"""
        alerts = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_products': len(self.products),
            'low_stock_products': [],
            'high_stock_products': [],
            'reorder_needed': [],
            'total_stock_value': round(self.get_stock_value(), 2),
        }
        
        for product in self.products.values():
            product_alerts = self.rules_engine.validate_stock_levels(product)
            
            if product_alerts['is_below_minimum']:
                alerts['low_stock_products'].append({
                    'code': product.code,
                    'name': product.name,
                    'current': product.current_stock,
                    'minimum': product.min_stock,
                })
            
            if product_alerts['is_above_maximum']:
                alerts['high_stock_products'].append({
                    'code': product.code,
                    'name': product.name,
                    'current': product.current_stock,
                    'maximum': product.max_stock,
                })
            
            if product_alerts['needs_reorder']:
                alerts['reorder_needed'].append({
                    'code': product.code,
                    'name': product.name,
                    'current': product.current_stock,
                    'minimum': product.min_stock,
                })
        
        return alerts
    
    def get_inventory_summary(self) -> dict:
        """Retorna um resumo do inventário"""
        all_products = list(self.products.values())
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'total_products': len(all_products),
            'total_items': sum(p.current_stock for p in all_products),
            'total_value': round(self.get_stock_value(), 2),
            'average_stock_value': round(
                self.get_stock_value() / len(all_products) if all_products else 0, 2
            ),
            'products_overview': [p.to_dict() for p in all_products],
        }
