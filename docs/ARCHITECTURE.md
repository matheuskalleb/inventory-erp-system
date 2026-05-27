# Arquitetura do Sistema

## Visão Geral

O **Inventory ERP System** é um simulador de sistema de gestão de estoque baseado em conceitos de ERP (Enterprise Resource Planning). A arquitetura foi projetada com ênfase em clareza funcional, separação de responsabilidades e extensibilidade.

## Camadas da Arquitetura

### 1. Camada de Modelagem de Dados (`product.py`, `transaction.py`)

Define as estruturas fundamentais do sistema:

- **Product**: Representa um SKU no inventário com propriedades como código, nome, preços, níveis de estoque
- **Transaction**: Registra movimentações de estoque (entrada/saída)
- **ProductStatus**: Estados possíveis de um produto (ativo, inativo, descontinuado)
- **TransactionType**: Tipos de operações (compra, venda, devolução, ajuste, etc)

**Responsabilidades**:
- Validação de integridade de dados (Pydantic)
- Cálculos relativos a cada entidade (margens, valores, etc)
- Estados e transições válidas

### 2. Camada de Regras de Negócio (`rules_engine.py`)

Motor de validação de regras e políticas empresariais:

- Valida transações contra políticas definidas
- Verifica níveis críticos de estoque
- Garante integridade de dados
- Impõe restrições de negócio

**Exemplos de Regras Implementadas**:
- Produto deve estar ativo para transações
- Quantidade não pode ser negativa
- Estoque não pode ser negativo em saída
- Estoque não deve exceder máximo (com tolerância)
- Margens de lucro válidas

### 3. Camada de Gerenciamento de Inventário (`inventory.py`)

Gerencia o estado completo do inventário:

- Adiciona/remove produtos
- Processa transações
- Mantém histórico de movimentações
- Calcula alertas e métricas
- Gera sumários e consultas

**Responsabilidades Principais**:
- Aplicar transações aos produtos
- Manter integridade de dados
- Rastrear histórico completo
- Identificar situações críticas

### 4. Camada de Relatórios (`reports.py`)

Gera análises e relatórios consolidados:

- **Stock Report**: Visão atual de todos os produtos
- **Movement Report**: Histórico de transações
- **Valuation Report**: Avaliação financeira do estoque
- **Sales Analysis**: Análise de vendas
- **Purchase Analysis**: Análise de compras

**Tecnologia**: Utiliza Pandas para manipulação e formatação de dados.

### 5. Camada de Orquestração (`erp_simulator.py`)

Interface única unificada para o sistema:

- Coordena operações entre módulos
- Fornece API amigável ao usuário
- Garante fluxo correto de dados
- Trata erros e exceções

**Padrão**: Facade Pattern - simplifica complexidade interna

## Fluxo de uma Transação

```
Usuário → ErpSimulator
  ↓
Validações (Rules Engine)
  ↓
Aplicar à Product
  ↓
Registrar Transaction
  ↓
Atualizar Inventory
  ↓
Retornar Resultado
```

## Estrutura de Dados

### Produto
```
Product
├── code (SKU)
├── name
├── prices (unit_price, cost_price)
├── stock (current, min, max)
├── status
├── category
└── metrics (total_sold, total_purchased)
```

### Transação
```
Transaction
├── id (UUID)
├── product_code
├── type (entrada/saída)
├── quantity
├── prices
├── user & reference
└── status (pending/completed/cancelled)
```

## Padrões de Design Utilizados

### 1. **Facade Pattern** (`ErpSimulator`)
Fornece interface simplificada para sistema complexo.

### 2. **Strategy Pattern** (`RulesEngine`)
Diferentes estratégias de validação podem ser configuradas.

### 3. **Repository Pattern** (`Inventory`)
Centraliza acesso aos dados de produtos e transações.

### 4. **Builder Pattern** (Pydantic Models)
Facilita criação e validação de objetos complexos.

## Extensibilidade

O sistema foi projetado para extensão:

### Para Adicionar Nova Regra de Negócio
1. Implementar em `RulesEngine.validate_transaction()`
2. Adicionar testes em `tests/`

### Para Adicionar Novo Tipo de Relatório
1. Criar método em `ReportGenerator`
2. Expor através de `ErpSimulator`

### Para Persistência de Dados
1. Implementar camada de DAO/ORM
2. Integrar em `Inventory`

### Para API REST
1. Usar FastAPI/Flask com `ErpSimulator`
2. Mapear endpoints para métodos

## Tecnologias

- **Python 3.8+**: Linguagem principal
- **Pydantic**: Validação e serialização
- **Pandas**: Análise e relatórios
- **Pytest**: Testing
- **SQLAlchemy**: ORM (preparado para futura integração)

## Considerações de Performance

- Produtos mantidos em `Dict` (O(1) lookup)
- Transações em `List` (histórico completo)
- Índices para busca por categoria (futura otimização)

## Segurança

- Validação de entrada em todas as camadas
- Tipos fortemente tipados
- Auditoria via histórico de transações
- Preparado para RBAC (Role Based Access Control)
