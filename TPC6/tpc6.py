### TPC6 - YACCALCULADORA  #########################################################
####################################################################################

import ply.lex as lex
import ply.yacc as yacc

####################################################################################
####################################################################################

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

t_PLUS   = r'\+'
t_MINUS  = r'\-'
t_TIMES  = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

####################################################################################
####################################################################################

def p_exp(p):
    'exp : exp PLUS multexp'
    p[0] = p[1] + p[3]

def p_exp2(p):
    'exp : exp MINUS multexp'
    p[0] = p[1] - p[3]

def p_exp3(p):
    'exp : multexp'
    p[0] = p[1]

####################################################################################
####################################################################################

def p_mutexp(p):
    'multexp : multexp TIMES primexp'
    p[0] = p[1] * p[3]

def p_multexp2(p):
    'multexp : multexp DIVIDE primexp'
    p[0] = p[1] / p[3]

def p_multexp3(p):
    'multexp : primexp'
    p[0] = p[1]

####################################################################################
####################################################################################

def p_primexp(p):
    'primexp : NUMBER'
    p[0] = p[1]

def p_primexp2(p):
    'primexp : LPAREN exp RPAREN'
    p[0] = p[2]

####################################################################################
####################################################################################

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

####################################################################################
####################################################################################

def calc(expression):
    result = parser.parse(expression)
    print(f"{expression} = {result}")

def cleanup_directory():
    import os
    filedir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(filedir)
    if os.path.exists("parsetab.py"): os.remove("parsetab.py")        
    if os.path.exists("parser.out"):  os.remove("parser.out")

if __name__ == "__main__":

    exps = [ "2+3"
           , "67-(2+3*4)"
           , "(9-2)*(13-4)"
           ]

    for e in exps:
        calc(e)

    cleanup_directory()