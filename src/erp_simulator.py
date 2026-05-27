"""
Simulador de ERP
Orquestrador principal que integra todos os módulos do sistema
"""

from typing import Optional, List, Dict, Tuple
from .product import Product, ProductStatus
from .inventory import Inventory
from .transaction import Transaction, TransactionType
from .reports import ReportGenerator


class ErpSimulator:
    """
    Simulador de Sistema ERP
    
    Orquestra todas as funcionalidades do sistema de inventário
    com uma interface unificada
    """
    
    def __init__(self):
        self.inventory = Inventory()
        self.report_gen = ReportGenerator()
    
    # ===== OPERAÇÕES COM PRODUTOS =====
    
    def create_product(
        self,
        code: str,
        name: str,
        unit_price: float,
        cost_price: float = None,
        min_stock: int = 0,
        max_stock: int = 100,
        category: str = "General",
        description: str = None
    ) -> Tuple[bool, str]:
        """Cria um novo produto no sistema"""
        
        if cost_price is None:
            cost_price = unit_price * 0.7  # Padrão: 30% de margem
        
        try:
            product = Product(
                code=code,
                name=name,
                description=description,
                unit_price=unit_price,
                cost_price=cost_price,
                min_stock=min_stock,
                max_stock=max_stock,
                category=category,
            )
            return self.inventory.add_product(product)
        except Exception as e:
            return False, f"Erro ao criar produto: {str(e)}"
    
    def get_product_info(self, code: str) -> Optional[Dict]:
        """Obtém informações completas de um produto"""
        product = self.inventory.get_product(code)
        if product:
            return product.to_dict()
        return None
    
    def update_product_price(self, code: str, new_price: float) -> Tuple[bool, str]:
        """Atualiza o preço de um produto"""
        product = self.inventory.get_product(code)
        if not product:
            return False, f"Produto '{code}' não encontrado"
        
        try:
            product.unit_price = new_price
            product.update_timestamp()
            return True, f"Preço atualizado para R$ {new_price:.2f}"
        except Exception as e:
            return False, f"Erro ao atualizar preço: {str(e)}"
    
    def deactivate_product(self, code: str) -> Tuple[bool, str]:
        """Desativa um produto"""
        product = self.inventory.get_product(code)
        if not product:
            return False, f"Produto '{code}' não encontrado"
        
        product.status = ProductStatus.INACTIVE
        product.update_timestamp()
        return True, f"Produto '{code}' desativado"
    
    # ===== TRANSAÇÕES DE ESTOQUE =====
    
    def input_transaction(
        self,
        product_code: str,
        quantity: int,
        transaction_type: str = "purchase_order",
        unit_price: float = None,
        user: str = "system",
        reference: str = None,
    ) -> Tuple[bool, str]:
        """Registra uma transação de entrada de estoque"""
        
        product = self.inventory.get_product(product_code)
        if not product:
            return False, f"Produto '{product_code}' não encontrado"
        
        price = unit_price if unit_price else product.unit_price
        
        try:
            transaction = Transaction(
                product_code=product_code,
                transaction_type=TransactionType(transaction_type),
                quantity=quantity,
                unit_price=price,
                user=user,
                reference=reference,
            )
            return self.inventory.process_transaction(transaction)
        except Exception as e:
            return False, f"Erro ao processar entrada: {str(e)}"
    
    def output_transaction(
        self,
        product_code: str,
        quantity: int,
        transaction_type: str = "sales_order",
        unit_price: float = None,
        user: str = "system",
        reference: str = None,
    ) -> Tuple[bool, str]:
        """Registra uma transação de saída de estoque"""
        
        product = self.inventory.get_product(product_code)
        if not product:
            return False, f"Produto '{product_code}' não encontrado"
        
        price = unit_price if unit_price else product.unit_price
        
        try:
            transaction = Transaction(
                product_code=product_code,
                transaction_type=TransactionType(transaction_type),
                quantity=quantity,
                unit_price=price,
                user=user,
                reference=reference,
            )
            return self.inventory.process_transaction(transaction)
        except Exception as e:
            return False, f"Erro ao processar saída: {str(e)}"
    
    def adjust_stock(
        self,
        product_code: str,
        quantity_adjustment: int,
        reason: str = "inventory_adjustment"
    ) -> Tuple[bool, str]:
        """Realiza ajuste direto de estoque (quebra, perda, etc)"""
        
        if quantity_adjustment > 0:
            return self.input_transaction(
                product_code=product_code,
                quantity=quantity_adjustment,
                transaction_type="inventory_adjustment",
                reference=reason,
            )
        else:
            return self.output_transaction(
                product_code=product_code,
                quantity=abs(quantity_adjustment),
                transaction_type="write_off",
                reference=reason,
            )
    
    # ===== CONSULTAS E RELATÓRIOS =====
    
    def get_stock_level(self, code: str) -> Optional[int]:
        """Obtém o nível de estoque de um produto"""
        return self.inventory.get_stock_level(code)
    
    def get_low_stock_alerts(self) -> List[Dict]:
        """Lista produtos com estoque baixo"""
        products = self.inventory.get_low_stock_products()
        return [p.to_dict() for p in products]
    
    def get_reorder_list(self) -> List[Dict]:
        """Lista produtos que precisam ser reordenados"""
        products = self.inventory.get_reorder_list()
        return [p.to_dict() for p in products]
    
    def generate_inventory_report(self) -> str:
        """Gera relatório de estoque em formato texto"""
        df = self.report_gen.generate_stock_report(self.inventory.products)
        return f"\n=== RELATÓRIO DE ESTOQUE ===\n{df.to_string(index=False)}\n"
    
    def generate_movement_report(self) -> str:
        """Gera relatório de movimentação em formato texto"""
        df = self.report_gen.generate_movement_report(self.inventory.transactions)
        if df.empty:
            return "\n=== RELATÓRIO DE MOVIMENTAÇÃO ===\nSem transações registradas\n"
        return f"\n=== RELATÓRIO DE MOVIMENTAÇÃO ===\n{df.to_string(index=False)}\n"
    
    def generate_valuation_report(self) -> Dict:
        """Gera relatório de avaliação de inventário"""
        return self.report_gen.generate_valuation_report(self.inventory.products)
    
    def generate_sales_analysis(self) -> Dict:
        """Analisa vendas e saídas"""
        return self.report_gen.generate_sales_analysis(self.inventory.transactions)
    
    def get_system_alerts(self) -> Dict:
        """Obtém todos os alertas do sistema"""
        return self.inventory.get_alerts()
    
    def get_inventory_summary(self) -> Dict:
        """Obtém resumo geral do inventário"""
        return self.inventory.get_inventory_summary()
    
    # ===== UTILIDADES =====
    
    def reset_simulation(self):
        """Limpa todos os dados (útil para testes)"""
        self.inventory = Inventory()
    
    def get_all_products(self) -> List[Dict]:
        """Lista todos os produtos"""
        return [p.to_dict() for p in self.inventory.products.values()]
    
    def get_transaction_history(self, product_code: Optional[str] = None) -> List[Dict]:
        """Obtém histórico de transações"""
        transactions = self.inventory.get_transaction_history(product_code)
        return [t.to_dict() for t in transactions]
