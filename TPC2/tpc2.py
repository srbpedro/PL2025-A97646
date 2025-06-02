### TPC2 - ANÁLISE DATASET DE OBRAS MUSICAIS #######################################
# processar o dataset de modo a criar os seguintes resultados...
# 1. lista ordenada alfabeticamente dos compositores musicais
# 2. quantas obras há por período
# 3. dicionário que mapeia um período a uma lista alfabética dos títulos das obras 
# executar: python3 tpc2.py < obras.csv
####################################################################################

import re, sys

csv = sys.stdin.buffer.read().decode('utf-8')


### PASSO 1: RECONHECER CAMPOS E LINHAS ############################################
# nome;desc;anoCriacao;periodo;compositor;duracao;_id
# só nos interessa nome, periodo e compositor
# campos não utilizados podem conter tudo menos o separador ;
####################################################################################

linha = r"""
    (?P<nome>[^;]+);
    \"?([\s\S]*?)\"?;        
    \d{4};
    (?P<periodo>[^;]+);
    (?P<compositor>[^;]+);
    [^;]+;
    [^;]+
"""

pattern = re.compile(
    rf'^(?P<linha>{linha})$',
    flags=re.MULTILINE | re.VERBOSE)


### PASSO 2: REGISTAR DADOS SOLICITADOS ############################################
####################################################################################

matches      = list(re.finditer(pattern, csv))
periodos     = {} # p -> [nome_obra]
compositores = set()

for match in matches:
    n, p, c = match.group("nome", "periodo", "compositor")
    compositores.add(c)
    periodos[p] = sorted(periodos[p]+[n]) if p in periodos else [n]


### PASSO 3: IMPRIMIR ##############################################################
####################################################################################

print("// PERÍODOS //")
for p in periodos:
    print(f"{p} (x{len(periodos[p])}) -> {' | '.join(sorted(periodos[p]))}\n")

print("// COMPOSITORES //")
print(' | '.join(sorted(list(compositores))))