"""
Exemplo Básico de Simulação
Demonstra o uso completo do Sistema de ERP de Inventário
"""

import sys
sys.path.insert(0, '..')

from src.erp_simulator import ErpSimulator
import json


def print_section(title: str):
    """Imprime um separador de seção"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def main():
    """Executa a simulação completa"""
    
    # Inicializar o sistema
    print_section("INICIALIZANDO SISTEMA DE ERP")
    erp = ErpSimulator()
    print("✓ Sistema inicializado com sucesso")
    
    # ===== CRIAR PRODUTOS =====
    print_section("CRIANDO PRODUTOS")
    
    products = [
        {
            "code": "SKU001",
            "name": "Notebook Dell Inspiron 15",
            "unit_price": 2500.00,
            "cost_price": 1750.00,
            "min_stock": 5,
            "max_stock": 30,
            "category": "Eletrônicos",
        },
        {
            "code": "SKU002",
            "name": "Mouse Logitech MX Master",
            "unit_price": 250.00,
            "cost_price": 150.00,
            "min_stock": 20,
            "max_stock": 100,
            "category": "Periféricos",
        },
        {
            "code": "SKU003",
            "name": "Teclado Mecânico RGB",
            "unit_price": 450.00,
            "cost_price": 280.00,
            "min_stock": 15,
            "max_stock": 80,
            "category": "Periféricos",
        },
    ]
    
    for prod in products:
        success, msg = erp.create_product(**prod)
        print(f"{'✓' if success else '✗'} {msg}")
    
    # ===== TRANSAÇÕES DE ENTRADA =====
    print_section("REGISTRANDO ENTRADAS DE ESTOQUE")
    
    entries = [
        ("SKU001", 15, "purchase_order", "NF-2025-001"),
        ("SKU002", 50, "purchase_order", "NF-2025-002"),
        ("SKU003", 40, "purchase_order", "NF-2025-003"),
    ]
    
    for code, qty, txn_type, ref in entries:
        success, msg = erp.input_transaction(code, qty, txn_type, reference=ref)
        print(f"{'✓' if success else '✗'} {msg}")
    
    # ===== RELATÓRIO DE ESTOQUE APÓS ENTRADA =====
    print_section("ESTOQUE APÓS RECEBIMENTO")
    print(erp.generate_inventory_report())
    
    # ===== TRANSAÇÕES DE SAÍDA =====
    print_section("REGISTRANDO SAÍDAS DE ESTOQUE")
    
    sales = [
        ("SKU001", 3, "sales_order", "PV-2025-001"),
        ("SKU002", 15, "sales_order", "PV-2025-002"),
        ("SKU001", 2, "sales_order", "PV-2025-003"),
        ("SKU003", 8, "sales_order", "PV-2025-004"),
    ]
    
    for code, qty, txn_type, ref in sales:
        success, msg = erp.output_transaction(code, qty, txn_type, reference=ref)
        print(f"{'✓' if success else '✗'} {msg}")
    
    # ===== RELATÓRIO DE MOVIMENTAÇÃO =====
    print_section("HISTÓRICO DE MOVIMENTAÇÃO")
    print(erp.generate_movement_report())
    
    # ===== SIMULAÇÃO DE OPERAÇÃO PROBLEMÁTICA =====
    print_section("TESTE: TRANSAÇÃO COM ERRO")
    print("Tentando vender 100 unidades de SKU001 (disponível: 10)...")
    success, msg = erp.output_transaction("SKU001", 100, "sales_order")
    print(f"{'✓' if success else '✗'} {msg}")
    
    # ===== AJUSTES =====
    print_section("AJUSTES DE ESTOQUE")
    success, msg = erp.adjust_stock("SKU002", -5, "Quebra/Dano")
    print(f"{'✓' if success else '✗'} {msg}")
    
    # ===== RELATÓRIO FINAL DE ESTOQUE =====
    print_section("ESTOQUE FINAL")
    print(erp.generate_inventory_report())
    
    # ===== ANÁLISE DE VALUATION =====
    print_section("AVALIAÇÃO DE INVENTÁRIO")
    valuation = erp.generate_valuation_report()
    print(f"Valor Total do Estoque: R$ {valuation['total_value']:,.2f}")
    print(f"Total de Itens: {valuation['total_items']}")
    print(f"Valor Médio por Item: R$ {valuation['average_value_per_item']:,.2f}")
    
    print("\nTop 5 Produtos por Valor:")
    for idx, prod in enumerate(valuation['top_5_by_value'], 1):
        print(f"  {idx}. {prod['name']:30} R$ {prod['value']:>12,.2f}")
    
    # ===== ANÁLISE DE VENDAS =====
    print_section("ANÁLISE DE VENDAS")
    sales_analysis = erp.generate_sales_analysis()
    print(f"Total Vendido: {sales_analysis['total_units_sold']} unidades")
    print(f"Valor Total Vendido: R$ {sales_analysis['total_value']:,.2f}")
    print(f"Número de Transações: {sales_analysis['transaction_count']}")
    
    # ===== ALERTAS DO SISTEMA =====
    print_section("ALERTAS DO SISTEMA")
    alerts = erp.get_system_alerts()
    
    if alerts['low_stock_products']:
        print("\n⚠️  ESTOQUE BAIXO:")
        for prod in alerts['low_stock_products']:
            print(f"  - {prod['name']} ({prod['code']}): {prod['current']}/{prod['minimum']}")
    else:
        print("✓ Nenhum produto com estoque baixo")
    
    if alerts['reorder_needed']:
        print("\n📋 REORDENAÇÃO NECESSÁRIA:")
        for prod in alerts['reorder_needed']:
            print(f"  - {prod['name']} ({prod['code']}): {prod['current']}/{prod['minimum']}")
    else:
        print("✓ Nenhuma reordenação necessária")
    
    # ===== RESUMO FINAL =====
    print_section("RESUMO GERAL DO SISTEMA")
    summary = erp.get_inventory_summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    
    print_section("SIMULAÇÃO CONCLUÍDA")
    print("✓ Sistema funcionando corretamente")


if __name__ == "__main__":
    main()
