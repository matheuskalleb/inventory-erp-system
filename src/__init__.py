"""
Inventory ERP System
Sistema de gestão de estoque com simulação de processos ERP
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .product import Product
from .inventory import Inventory
from .transaction import Transaction, TransactionType
from .erp_simulator import ErpSimulator

__all__ = [
    "Product",
    "Inventory",
    "Transaction",
    "TransactionType",
    "ErpSimulator",
]
