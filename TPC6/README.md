# Parser Recursivo de Expressões Aritméticas
Autor: Pedro Silva Ferreira (A97646)

## Resumo:

Parser capaz de calcular expressões aritméticas tendo em conta precedência.
Exemplos de expressões:
- `2+3`
- `67-(2+3*4)`
- `(9-2)*(13-4)`

## Estratégia:

1. *Definir regras de expressão.*
   - Operadores de maior precedência estão mais fundo na árvore: add/sub -> mult/div -> parênteses/literais

## Execução:
```python tpc6.py```