### TPC5 - MÁQUINA DE VENDA ########################################################
# python3 tpc5.py
# exemplos de interaçao com a máquina:
# >> LISTAR
# >> MOEDA 1e, 20c, 5c, 5c .
# >> SELECIONAR A23
# >> SAIR
####################################################################################

import sys, json
import ply.lex as lex

with open('stock.json', 'r', encoding='utf-8') as file:
    stockdb = json.load(file)

def maqprint(*args, **kwargs):
    args = ("maq:",) + args
    print(*args, **kwargs)

####################################################################################
####################################################################################

class Item:
    def __init__(self, cod, nome, quant, preco):
        self.cod = cod
        self.nome = nome
        self.quant = quant
        self.preco = preco

class Maquina:

    # enche ao longo de 'MOEDA 1e, 20c, 5c, 5c .'
    # esvazia ao ler o ponto
    # convertendo o montante em saldo
    moedas_a_inserir = []

    saldo_cents = 0
    stock = {}

    @staticmethod
    def carregar_stock():
        stock_dict = {}
        for elem in stockdb:
            stock_dict[elem["cod"]] = Item(
                elem["cod"],
                elem["nome"],
                elem["quant"],
                elem["preco"]
            )
        return stock_dict

    @staticmethod
    def strnumerario(valor_cents):
        if valor_cents<=0:
            return "0c"

        euros = valor_cents // 100
        cents = valor_cents % 100

        return "".join([
            f"{euros}e" if euros>0 else "",
            f"{cents}c" if cents>0 else ""
        ])

    @staticmethod
    def strmoedas(valor_cents):
        if valor_cents <= 0: return "0c"
        possiveis = [200, 100, 50, 20, 10, 5, 2, 1]
        usadas = []

        sobra = valor_cents
        for moeda in possiveis:
            if sobra >= moeda:
                qtd = sobra // moeda
                usadas.append(f"{qtd}x {Maquina.strnumerario(moeda)}")
                sobra -= qtd * moeda

        return f"{', '.join(usadas[:-1])} e {usadas[-1]}"        

    @staticmethod
    def valor_moeda(strmoeda):
        valor_cents = float(strmoeda[:-1])
        if strmoeda[-1] == 'e':
            valor_cents *= 100
        return int(valor_cents)

    @classmethod
    def saldo(cls):
        return f"Saldo = {cls.strnumerario(cls.saldo_cents)}"

    @classmethod
    def pedido(cls, cod):
        return f"Pedido = {cls.strnumerario(int(round(cls.stock[cod].preco*100)))}"

    @classmethod
    def adicionar_saldo(cls, valor_cents):
        cls.saldo_cents += valor_cents
    
    # chamado no comando 'MOEDA ...'
    @classmethod
    def inserir_moedas(cls):
        while cls.moedas_a_inserir:
            valor_moeda = cls.moedas_a_inserir.pop()
            cls.adicionar_saldo(valor_moeda)
        maqprint(cls.saldo())    

    # chamado no comando 'SELECIONAR ...'
    @classmethod
    def selecionar_item(cls, cod):

        if cod not in cls.stock:
            maqprint("Item inexistente.")
            maqprint(cls.saldo())
            return
        
        if cls.stock[cod].quant <= 0:
            maqprint("Stock insuficiente para satisfazer o seu pedido.")
            maqprint(cls.saldo())
            return
        
        sobra_cents = (cls.saldo_cents - int(cls.stock[cod].preco*100))

        if sobra_cents < 0:
            maqprint("Saldo insuficiente para satisfazer o seu pedido.")
            maqprint(cls.saldo() + f"; {cls.pedido(cod)}")
            return

        cls.saldo_cents = sobra_cents
        cls.stock[cod].quant -= 1

        maqprint(f"Pode retirar o produto dispensado \"{cls.stock[cod].nome}\".")
        maqprint(cls.saldo())

    # chamado no comando 'LISTAR'
    @classmethod
    def listar_itens(cls):

        header = [
            "cod | nome            | qtd | preço",
            "-----------------------------------"
            ]

        linhas = [
            f"{i.cod} | {i.nome.ljust(15) if len(i.nome) < 15 else i.nome[:15-3] + '...'} | x{i.quant}  | {i.preco}"
            for i in cls.stock.values()
        ]

        maqprint('\n'+'\n'.join(header+linhas))

    # chamado no comando 'SAIR'
    @classmethod
    def sair(cls):
        if cls.saldo_cents > 0:
            maqprint(f"Pode retirar o troco: {cls.strmoedas(cls.saldo_cents)}.")
        else:
            maqprint(f"Não há troco a devolver.")
        maqprint("Até à próxima.")    

####################################################################################
####################################################################################

states = (
    ('CMDMOEDA', 'exclusive'),
    ('CMDSELECIONAR', 'exclusive')
)

literals = [
    ',',
]

tokens = (
    'NEWLINE',
    'DOT',

    # estado inicial
    'CMDLISTAR',
    'CMDMOEDA',
    'CMDSELECIONAR',
    'CMDSAIR',

    # estado cmdmoeda
    'MOEDAINSERIDA',

    # estado cmdselecionar
    'CODINSERIDO'
)

####################################################################################
####################################################################################

def t_CMDLISTAR(t):
    r'^LISTAR$'
    Maquina.listar_itens()
    return t

def t_CMDMOEDA(t):
    r'^MOEDA'
    t.lexer.begin('CMDMOEDA')
    return t

def t_CMDSELECIONAR(t):
    r'^SELECIONAR'
    t.lexer.begin('CMDSELECIONAR')
    return t

def t_CMDSAIR(t):
    r'^SAIR$'
    Maquina.sair()
    return t

####################################################################################
####################################################################################

def t_CMDSELECIONAR_CODINSERIDO(t):
    r'[\w\d]+$'
    Maquina.selecionar_item(t.value)
    t.lexer.begin('INITIAL')
    return t

####################################################################################
####################################################################################

def t_CMDMOEDA_MOEDAINSERIDA(t):
    r'(2e)|(1e)|(50c)|(20c)|(10c)|(5c)|(2c)|(1c)'
    t.value = Maquina.valor_moeda(t.value)
    Maquina.moedas_a_inserir.append(t.value)
    return t

def t_CMDMOEDA_DOT(t):
    r'\.$'
    Maquina.inserir_moedas()
    t.lexer.begin('INITIAL')
    return t

t_ANY_ignore = ' \t,\n'

def t_ANY_error(t):
    print(rf"Illegal -> '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
####################################################################################
####################################################################################

Maquina.stock = Maquina.carregar_stock()
maqprint("2024-03-08, Stock carregado, Estado atualizado.")
maqprint("Bom dia. Estou disponível para atender o seu pedido.")

while True:
    user_input = lexer.input(input(">> "))

    for tok in lexer:
        print(f"{tok}")
        print(lexer.lexstate)