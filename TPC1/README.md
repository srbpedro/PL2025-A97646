# Somador On/Off
Autor: Pedro Silva Ferreira (A97646)

## Resumo:

Somar todas as sequências de dígitos encontradas em texto.
- *Encontrando 'off':* suspender soma até 'on' subsequente
- *Encontrando '=':* imprimir soma registada até esse ponto

## Estratégia:

1. *Filtrar excertos Off/On.*
   O padrão **sumoff** é composto pela deteção de 'off', conteúdo e finalmente 'on'.
   Para 'off' ser captado, deve haver espaço atrás dele.
   Para 'on' basta qualquer caracter que não letra (ie. espaço/pontuação).

2. *Reconhecer Números & sinais igual.*
   O padrão **pattern** deteta ora números (inteiros e fracionários) ora sinais igual.
   São usados grupos nomeados para discernir melhor o que foi capturado a seguir.

3. *Iterar por capturas.*   

## Execução:
```PS> Get-Content source.txt | python tpc1.py```
```python3 tpc1.py < source.txt```