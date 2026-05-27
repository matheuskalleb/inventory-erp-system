<div align="center">

# 📦 Inventory ERP System

[![GitHub](https://img.shields.io/badge/GitHub-Matheuskalleb-black?logo=github&style=flat-square)](https://github.com/Matheuskalleb)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=flat-square)](#)

**Sistema profissional de gestão de estoque com simulação de processos ERP**

Desenvolvimento técnico focado em modelagem de regras de negócio, fluxos empresariais e análise de inventário.

[🚀 Quick Start](#quick-start) • [📚 Documentação](#documentação) • [🎯 Características](#características) • [💻 Exemplos](#exemplos)

</div>

---

## 🎯 Sobre o Projeto

Um simulador de **ERP (Enterprise Resource Planning)** desenvolvido em Python que implementa conceitos reais de gestão de inventário. O projeto demonstra como modelar regras de negócio, estruturar fluxos de entrada/saída de estoque e gerar relatórios consolidados.

**Ideal para:**
- 📚 Aprender conceitos de ERP e gestão de estoque
- 💼 Entender modelagem de regras de negócio
- 🔍 Estudo de arquitetura de software
- 🎓 Projeto de portfólio técnico

---

## ✨ Características

### ✅ Modelagem de Regras de Negócio
- Validações automáticas de transações
- Controle de limites mínimo e máximo
- Cálculos de margem de lucro
- Rastreamento de histórico completo

### ✅ Gestão de Estoque
- Entrada e saída de produtos em tempo real
- Múltiplos tipos de transações (compra, venda, devolução, ajuste)
- Alertas automáticos de estoque crítico
- Histórico imutável de movimentações

### ✅ Relatórios e Análises
- Relatório consolidado de estoque
- Histórico de movimentação
- Análise de vendas e compras
- Avaliação financeira de inventário

### ✅ Arquitetura Profissional
- Separação clara de responsabilidades
- Padrões de design (Facade, Strategy, Repository)
- Validação com Pydantic
- Testes unitários com Pytest

---

## 🚀 Quick Start

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Matheuskalleb/inventory-erp-system.git
cd inventory-erp-system

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Exemplo Básico

```python
from src.erp_simulator import ErpSimulator

# Inicializar o sistema
erp = ErpSimulator()

# Criar um produto
erp.create_product(
    code="SKU001",
    name="Notebook Dell",
    unit_price=2500.00,
    min_stock=5,
    max_stock=30
)

# Registrar entrada de estoque
erp.input_transaction(
    product_code="SKU001",
    quantity=15,
    transaction_type="purchase_order",
    reference="NF-2025-001"
)

# Registrar saída
erp.output_transaction(
    product_code="SKU001",
    quantity=3,
    transaction_type="sales_order",
    reference="PV-2025-001"
)

# Gerar relatório
print(erp.generate_inventory_report())

# Obter alertas
alerts = erp.get_system_alerts()
print(alerts)
```

### Executar Simulação Completa

```bash
python examples/basic_simulation.py
```

Saída esperada:
```
============================================================
  INICIALIZANDO SISTEMA DE ERP
============================================================
✓ Sistema inicializado com sucesso

============================================================
  CRIANDO PRODUTOS
============================================================
✓ Produto SKU001 adicionado com sucesso
✓ Produto SKU002 adicionado com sucesso
...
```

---

## 📁 Estrutura do Projeto

```
inventory-erp-system/
│
├── src/                              # Código principal
│   ├── __init__.py
│   ├── product.py                   # Modelagem de produtos
│   ├── transaction.py               # Transações de estoque
│   ├── rules_engine.py              # Motor de regras de negócio
│   ├── inventory.py                 # Gerenciador de estoque
│   ├── reports.py                   # Geração de relatórios
│   └── erp_simulator.py              # Orquestrador principal
│
├── tests/                            # Suite de testes
│   ├── __init__.py
│   ├── test_product.py
│   └── test_inventory.py
│
├── examples/                         # Exemplos de uso
│   └── basic_simulation.py           # Simulação completa
│
├── docs/                             # Documentação
│   ├── ARCHITECTURE.md              # Design do sistema
│   └── BUSINESS_RULES.md            # Regras implementadas
│
├── .github/workflows/                # CI/CD
│   └── tests.yml                    # GitHub Actions
│
├── README.md                         # Este arquivo
├── requirements.txt                  # Dependências Python
├── setup.py                         # Configuração do pacote
├── LICENSE                          # MIT License
└── .gitignore                       # Arquivos ignorados pelo Git
```

---

## 📚 Documentação

### 📖 Arquitetura do Sistema
Entenda o design, padrões utilizados e fluxos de dados:
→ [Ler ARCHITECTURE.md](docs/ARCHITECTURE.md)

**Tópicos:**
- Visão geral da arquitetura
- Camadas do sistema
- Padrões de design (Facade, Strategy, Repository)
- Fluxo de uma transação
- Estrutura de dados

### 📋 Regras de Negócio
Conheça todas as validações e políticas implementadas:
→ [Ler BUSINESS_RULES.md](docs/BUSINESS_RULES.md)

**Tópicos:**
- Gestão de produtos
- Tipos de transações
- Validações obrigatórias
- Alertas do sistema
- Métricas e cálculos
- Consistência de dados

---

## 🧪 Testes

### Rodar Todos os Testes
```bash
pytest tests/ -v
```

### Rodar com Cobertura
```bash
pytest tests/ --cov=src/ --cov-report=html
```

### Testes Específicos
```bash
pytest tests/test_product.py -v
pytest tests/test_inventory.py -v
```

---

## 💻 Exemplos de Uso

### 1. Criar Múltiplos Produtos
```python
erp = ErpSimulator()

products = [
    ("SKU001", "Notebook", 2500.00, 1750.00),
    ("SKU002", "Mouse", 250.00, 150.00),
    ("SKU003", "Teclado", 450.00, 280.00),
]

for code, name, price, cost in products:
    erp.create_product(code, name, price, cost)
```

### 2. Simular Operações
```python
# Entrada de estoque
erp.input_transaction("SKU001", 20, "purchase_order")

# Saídas múltiplas
erp.output_transaction("SKU001", 5, "sales_order")
erp.output_transaction("SKU001", 3, "sales_order")

# Devolução
erp.output_transaction("SKU001", 2, "sales_return")
```

### 3. Gerar Relatórios
```python
# Estoque atual
print(erp.generate_inventory_report())

# Movimentações
print(erp.generate_movement_report())

# Análise financeira
valuation = erp.generate_valuation_report()
print(f"Valor total: R$ {valuation['total_value']:,.2f}")

# Análise de vendas
sales = erp.generate_sales_analysis()
print(f"Total vendido: {sales['total_units_sold']} unidades")
```

### 4. Obter Alertas
```python
# Todos os alertas
alerts = erp.get_system_alerts()

# Produtos com estoque baixo
low_stock = erp.get_low_stock_alerts()

# Produtos para reordenar
reorder = erp.get_reorder_list()
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| **Python** | 3.8+ | Linguagem principal |
| **Pydantic** | 2.5+ | Validação de dados |
| **Pandas** | 2.1+ | Análise e relatórios |
| **Pytest** | 7.4+ | Testes unitários |
| **SQLAlchemy** | 2.0+ | ORM (preparado) |

---

## 🔮 Roadmap (Próximas Features)

- [ ] **Persistência de Dados**
  - Integração com SQLAlchemy
  - Suporte a SQLite/PostgreSQL

- [ ] **API REST**
  - FastAPI ou Flask
  - Endpoints CRUD completos
  - Autenticação JWT

- [ ] **Dashboard Web**
  - React/Vue.js
  - Gráficos em tempo real
  - Visualizações interativas

- [ ] **Recursos Avançados**
  - Previsão de demanda (ML)
  - Integração com fornecedores
  - Sistema de autorização (RBAC)

- [ ] **Melhorias**
  - Mais tipos de relatórios
  - Exportação (PDF, Excel)
  - Notificações por email

---

## 🤝 Contribuindo

Este é um projeto de aprendizado. Sinta-se livre para:
- 🐛 Reportar bugs (abra uma issue)
- 💡 Sugerir melhorias
- 🔨 Fazer fork e contribuir com PRs

---

## 📝 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Matheus Kalleb**
- GitHub: [@Matheuskalleb](https://github.com/Matheuskalleb)
- Projeto focado em demonstrar conhecimento de engenharia de software e processos empresariais

---

## 📊 Status do Projeto

| Aspecto | Status |
|--------|--------|
| Modelagem de Dados | ✅ Completo |
| Regras de Negócio | ✅ Completo |
| Gerenciamento de Estoque | ✅ Completo |
| Relatórios | ✅ Completo |
| Testes | 🟡 Básicos |
| Documentação | ✅ Completa |
| API REST | ⏳ Planejado |
| Dashboard | ⏳ Planejado |

---

<div align="center">

**⭐ Se este projeto ajudou você, considere deixar uma estrela!**

[⬆ Voltar ao topo](#-inventory-erp-system)

</div>
