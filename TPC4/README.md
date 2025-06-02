# Lexer de SPARQL
Autor: Pedro Silva Ferreira (A97646)

## Resumo:

Analisador léxico para linguagem SPARQL que suporta:
1. palavras reservadas SELECT, WHERE, LIMIT, A
2. números, variáveis, propriedades, strings

## Estratégia:

1. *Definir tokens e regras.*
   - variáveis começam com '?'.
   - propriedades são duas palavras separadas por ':'.
   - comentários começam por '#'.

2. *Imprimir fonte com os tipos de token a substituir os tipos.*

## Execução:
```PS> Get-Content source.rq | python tpc4.py```
```python3 tpc4.py < source.rq```