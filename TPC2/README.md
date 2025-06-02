# Análise de Dataset de Obras Musicais
Autor: Pedro Silva Ferreira (A97646)

## Resumo:

Processamento de um dataset de obras musicais para extrair:

1. Lista alfabética de compositores
2. Distribuição quantitativa de obras por período histórico
3. Dicionário organizando obras alfabeticamente por período

## Estratégia:

1. *Reconhecer campos e linhas relevantes*
   Campos não utilizados podem conter tudo menos o separador ';'.
   ```python
   linha = r'''
      (?P<nome>[^;]+);       # Título da obra
      \"?([\s\S]*?)\"?;      # Descrição (ignorada)
      \d{4};                 # Ano (ignorado)
      (?P<periodo>[^;]+);    # Período histórico
      (?P<compositor>[^;]+); # Compositor
      [^;]+;[^;]+            # Campos restantes (ignorados)
   '''
   ```

2. *Registar dados segundo disposição solicitada.*
   ```python
   matches      = list(re.finditer(pattern, csv))
   periodos     = {} # p -> [nome_obra]
   compositores = set()

   for match in matches:
      n, p, c = match.group("nome", "periodo", "compositor")
      compositores.add(c)
      periodos[p] = sorted(periodos[p]+[n]) if p in periodos else [n]
   ```

## Execução:
```PS> Get-Content obras.csv | python tpc2.py```
```python3 tpc2.py < obras.csv```