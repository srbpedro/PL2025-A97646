# Máquina de Estados - Venda Automática
Autor: Pedro Silva Ferreira (A97646)

## Resumo:

Máquina de venda automática com stock definido em ficheiro json.
Possíveis interações:
- `>> LISTAR`
- `>> MOEDA 1e, 20c, 5c, 5c .`
- `>> SELECIONAR A23`
- `>> SAIR`

## Estratégia:

1. *Definir estados e tokens.*
   - Estado inicial de onde se sai do programa, se lista os itens disponíveis ou se passa para um dos estados seguintes
   - Estado de inserção de moedas em que só moedas são aceites como tokens. Regressa a estado inicial quando lê '\.'.
   - Estado de seleção de produto em que só códigos são aceites como tokens. Regressa a estado inicial quando lê código.

2. *Definir classe para máquina e itens.*
   - carregamento do ficheiro de stock
   - registo de saldo atual, de itens disponíveis, de inserção de moedas.
   - método para cada um dos comandos.

## Execução:
```python tpc5.py```