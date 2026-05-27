"""
Geração de Relatórios
Cria relatórios consolidados de estoque e movimentação
"""

from typing import List, Dict
from datetime import datetime
import pandas as pd
from .product import Product
from .transaction import Transaction


class ReportGenerator:
    """Gera relatórios diversos do sistema de inventário"""
    
    @staticmethod
    def generate_stock_report(products: Dict[str, Product]) -> pd.DataFrame:
        """
        Gera relatório de estoque consolidado
        
        Retorna: DataFrame com informações de estoque
        """
        data = []
        for product in products.values():
            data.append({
                'Código': product.code,
                'Produto': product.name,
                'Categoria': product.category,
                'Estoque Atual': product.current_stock,
                'Mínimo': product.min_stock,
                'Máximo': product.max_stock,
                'Preço Unit.': round(product.unit_price, 2),
                'Valor Total': round(product.total_stock_value(), 2),
                'Margem (%)': round(product.profit_margin(), 2),
                'Status': product.status,
            })
        
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values('Código')
        return df
    
    @staticmethod
    def generate_movement_report(transactions: List[Transaction]) -> pd.DataFrame:
        """
        Gera relatório de movimentação de estoque
        
        Retorna: DataFrame com histórico de transações
        """
        data = []
        for txn in transactions:
            data.append({
                'Data': txn.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'ID': txn.id[:8],  # Primeiros 8 caracteres do UUID
                'Código Produto': txn.product_code,
                'Tipo': txn.transaction_type,
                'Quantidade': txn.quantity if txn.is_inbound() else -txn.quantity,
                'Preço Unit.': round(txn.unit_price, 2),
                'Valor Total': round(txn.total_value, 2),
                'Usuário': txn.user,
                'Status': txn.status,
            })
        
        df = pd.DataFrame(data)
        if not df.empty:
            df = df.sort_values('Data', ascending=False)
        return df
    
    @staticmethod
    def generate_valuation_report(products: Dict[str, Product]) -> dict:
        """Gera relatório de avaliação de inventário"""
        total_value = sum(p.total_stock_value() for p in products.values())
        total_items = sum(p.current_stock for p in products.values())
        
        by_category = {}
        for product in products.values():
            cat = product.category
            if cat not in by_category:
                by_category[cat] = {'items': 0, 'value': 0.0}
            by_category[cat]['items'] += product.current_stock
            by_category[cat]['value'] += product.total_stock_value()
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'total_items': total_items,
            'total_value': round(total_value, 2),
            'average_value_per_item': round(total_value / total_items if total_items > 0 else 0, 2),
            'by_category': by_category,
            'top_5_by_value': sorted(
                [{'code': p.code, 'name': p.name, 'value': round(p.total_stock_value(), 2)}
                 for p in products.values()],
                key=lambda x: x['value'],
                reverse=True
            )[:5]
        }
    
    @staticmethod
    def generate_sales_analysis(transactions: List[Transaction]) -> dict:
        """
        Analisa vendas e saídas
        
        Retorna análise de movimentação de saída
        """
        outbound_txns = [t for t in transactions if t.is_outbound()]
        
        total_units = sum(t.quantity for t in outbound_txns)
        total_value = sum(t.total_value for t in outbound_txns)
        
        by_product = {}
        for txn in outbound_txns:
            if txn.product_code not in by_product:
                by_product[txn.product_code] = {'units': 0, 'value': 0.0}
            by_product[txn.product_code]['units'] += txn.quantity
            by_product[txn.product_code]['value'] += txn.total_value
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'total_units_sold': total_units,
            'total_value': round(total_value, 2),
            'transaction_count': len(outbound_txns),
            'by_product': by_product,
        }
    
    @staticmethod
    def generate_purchase_analysis(transactions: List[Transaction]) -> dict:
        """
        Analisa compras e entradas
        
        Retorna análise de movimentação de entrada
        """
        inbound_txns = [t for t in transactions if t.is_inbound()]
        
        total_units = sum(t.quantity for t in inbound_txns)
        total_value = sum(t.total_value for t in inbound_txns)
        
        by_product = {}
        for txn in inbound_txns:
            if txn.product_code not in by_product:
                by_product[txn.product_code] = {'units': 0, 'value': 0.0}
            by_product[txn.product_code]['units'] += txn.quantity
            by_product[txn.product_code]['value'] += txn.total_value
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'total_units_received': total_units,
            'total_value': round(total_value, 2),
            'transaction_count': len(inbound_txns),
            'by_product': by_product,
        }
