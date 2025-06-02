### TPC4 - LEXER SPARQL ############################################################
# python3 tpc4.py < source.rq
####################################################################################

import sys
import ply.lex as lex

src = sys.stdin.read()

####################################################################################
####################################################################################

literals = [
    '{',
    '}',
    '.',
]

tokens = (
    # palavras reservadas
    'SELECT',
    'WHERE',
    'LIMIT',
    'A',

    # misc
    'NUMBER',
    'VARIABLE',
    'PROPERTY',
    'STRINGLIT',
    'COMMENT'
)

### PASSO 2: REGRAS ################################################################
####################################################################################

def t_A(t):
    r'(?i:a)'
    return t

def t_SELECT(t):
    r'(?i:select)'
    return t

def t_WHERE(t):
    r'(?i:where)'
    return t

def t_LIMIT(t):
    r'(?i:limit)'
    return t

def t_NUMBER(t):
    r'[\d]+'
    t.value = int(t.value)
    return t

def t_VARIABLE(t):
    r'\?\w[\w\_\d]*'
    return t

def t_PROPERTY(t):
    r'\w+\:\w+'
    return t

def t_STRINGLIT(t):
    r'"[^"]*?"(?:\@\w+)?'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

t_ignore = ' \t\n'

def t_error(t):
    print(rf"Illegal -> '{t.value[0]}'")
    t.lexer.skip(1)

### PASSO 3: LEITURA ###############################################################
# faz-se com que se imprima a fonte com os tokens substituídos pelos tipos
####################################################################################

lexer = lex.lex()
lexer.input(src)

output = ""
current_pos = 0

for tok in lexer:
    # texto intermediário desde tok prévio ++ tipo atual
    output += src[current_pos:tok.lexpos] + f"<{tok.type}>"
    current_pos = tok.lexpos + len(str(tok.value))

# texto após último tok
output += src[current_pos:]
                 
print(''.join(output))