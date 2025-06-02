# Conversor de Markdown Para HTML
Autor: Pedro Silva Ferreira (A97646)

## Resumo:

Conversor compatível com:
1. Headers
2. Listas
3. Variações de texto (itálico, negrito, etc)
4. Imagens e Hiperligações

## Estratégia:

1. *Definir padrão regex.*
   ```python
   pattern = r"""
   ( 
      (?P<header>
         (?: ^[ ]*\#{3}[ ]+(?P<header3>.*)$ )
      |  (?: ^[ ]*\#{2}[ ]+(?P<header2>.*)$ )
      |  (?: ^[ ]*\#{1}[ ]+(?P<header1>.*)$ )
      ) 
   |  (?P<enumlist> 
         ^\d+\.[ ]+.*$ (?:\n\d+\.[ ]+.*$)*
      )
   |  (?P<fontformat>
         ((?:\*\*\*)(?!\s) (?P<bolditalic>(?:\\\*|[^\n\r])+?)(?!\s) (?:\*\*\*))
      |  ((?:\*\*)(?!\s)   (?P<bold>      (?:\\\*|[^\n\r])+?)(?!\s) (?:\*\*))
      |  ((?:\*)(?!\s)     (?P<italic>    (?:\\\*|[^\n\r])+?)(?!\s) (?:\*))
      )
   |  (?P<img>
         \!\[ (?P<imgdesc> [^\n]+?) \] \( (?P<imgpath> [\w]+?:\/{2}?[\w\d]+?\.[\w\d]+?\.[\w\d]+?.*?) \)
      )
   |  (?P<href>
         \[ (?P<hrefdesc> [^\n]+?) \] \( (?P<hrefpath> [\w]+?:\/{2}?[\w\d]+?\.[\w\d]+?\.[\w\d]+?.*?) \)
      )
   )
   """
   ```

2. *Definir funções de tradução para HTML.*
   Funções que tomem cada um dos matches e os traduza corretamente consoante o seu tipo.

3. *Gerar ficheiro HTML resultante.*

## Execução:
```PS> Get-Content source.md | python tpc3.py```
```python3 tpc3.py < source.md```