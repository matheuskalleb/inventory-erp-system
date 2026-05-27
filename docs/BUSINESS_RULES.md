# Regras de Negócio

## 1. Gestão de Produtos

### 1.1 Criação e Status
- **Código único**: Cada produto deve ter um SKU único
- **Preço de custo < Preço de venda**: Margem de lucro sempre positiva
- **Estados válidos**: ACTIVE, INACTIVE, DISCONTINUED, ON_ORDER
- Apenas produtos ACTIVE podem ter transações

### 1.2 Limites de Estoque
- **min_stock < max_stock**: Limites devem ser válidos
- **Limite máximo com tolerância**: Até 110% do máximo permitido
- **Alerta de reorder**: Quando estoque ≤ 150% do mínimo

## 2. Transações de Estoque

### 2.1 Tipos de Entrada
- `PURCHASE_ORDER`: Recebimento de compra
- `SALES_RETURN`: Devolução de venda
- `INVENTORY_ADJUSTMENT`: Ajuste positivo
- `DONATION`: Doação recebida

### 2.2 Tipos de Saída
- `SALES_ORDER`: Venda
- `PURCHASE_RETURN`: Devolução de compra
- `WRITE_OFF`: Perda/Sucata
- `TRANSFER`: Transferência entre estoques

### 2.3 Validações de Transação

#### Regra 1: Quantidade Positiva
```python
quantity > 0
```

#### Regra 2: Produto Deve Estar Ativo
```python
product.status == ACTIVE
```

#### Regra 3: Saída Requer Disponibilidade
```python
if transaction.is_outbound():
    available_stock >= requested_quantity
```

#### Regra 4: Entrada Não Deve Exceder Máximo (com tolerância)
```python
if transaction.is_inbound():
    new_stock <= (max_stock * 1.1)
```

#### Regra 5: Preço Unitário Válido
```python
unit_price > 0
```

#### Regra 6: Devolução de Compra Válida
```python
if transaction.is_purchase_return():
    quantity <= product.total_purchased
```

## 3. Rastreamento de Histórico

### 3.1 Registros Obrigatórios
- Data/hora de transação
- Tipo de transação
- Quantidade e preço
- Usuário responsável
- Referência externa (quando aplicável)
- Status final

### 3.2 Auditoria
- Todas as transações são imutáveis após conclusão
- Histórico completo mantido indefinidamente
- Reversão cria novo registro de transação

## 4. Alertas do Sistema

### 4.1 Alerta Crítico: Estoque Baixo
**Condição**: `current_stock < min_stock`

**Ação**: 
- Marcado como crítico
- Impede vendas (se configurado)
- Dispara notificação

### 4.2 Aviso: Estoque Alto
**Condição**: `current_stock > max_stock`

**Ação**:
- Marcado como aviso
- Sugestão de redução
- Análise de padrão de compra

### 4.3 Sugestão: Reordenação
**Condição**: `min_stock < current_stock <= (min_stock * 1.5)`

**Ação**:
- Aparece na lista de reorden
- Sugestão de quantidade ideal

## 5. Métricas e Cálculos

### 5.1 Margem de Lucro
```
Margem (%) = ((unit_price - cost_price) / unit_price) * 100
```

### 5.2 Valor em Estoque
```
Total_Value = current_stock * cost_price
```

### 5.3 Rotatividade
```
Rotation = total_sold / average_stock_per_period
```

## 6. Estados de Transação

### 6.1 Ciclo de Vida
```
PENDING → COMPLETED → [REVERSED]
       → CANCELLED
```

### 6.2 Transições Válidas
- `PENDING` → `COMPLETED`: Após validação
- `COMPLETED` → `REVERSED`: Apenas se necessário corrigir
- Qualquer → `CANCELLED`: Se erro antes de completion

## 7. Consistência de Dados

### 7.1 Invariantes
- `current_stock >= 0`
- `min_stock < max_stock`
- `cost_price < unit_price`
- `total_sold >= 0`
- `total_purchased >= 0`

### 7.2 Recuperação de Erros
1. Validação antes de aplicar transação
2. Transação atômica (aplicar ou não aplicar)
3. Log de erro para auditoria
4. Rollback automático

## 8. Regras de Integração (Futuro)

### 8.1 Integração com Fornecedores
- Sincronizar preços automaticamente
- Validar quantidades contra MOQ (Minimum Order Quantity)

### 8.2 Integração com Sistema de Vendas
- Sincronizar estoque em tempo real
- Bloquear vendas se estoque negativo

### 8.3 Integração com Financeiro
- Auditoria de custos
- Rastreamento de margens

## 9. Exemplos de Violações

### ✗ Venda com Estoque Insuficiente
```python
# Erro: produto tem 5, solicitado 10
output_transaction("SKU001", 10)
# Result: "Estoque insuficiente. Disponível: 5"
```

### ✗ Devolução de Compra Inválida
```python
# Erro: nunca comprou essa quantidade
reverse_purchase("SKU001", 100)
# Result: "Devolução inválida. Total comprado: 50"
```

### ✗ Transação com Produto Inativo
```python
# Erro: produto foi descontinuado
product.status = DISCONTINUED
input_transaction("SKU001", 10)
# Result: "Produto não está ativo"
```

## 10. Configuração de Políticas (Futuro)

Será possível configurar:
- Limites de estoque por categoria
- Regras de preço mínimo/máximo
- Períodos de retenção de histórico
- Permissões por tipo de transação
- Notificações automáticas
