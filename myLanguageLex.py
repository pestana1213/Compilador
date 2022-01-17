import ply.lex as lex
import sys

reserved = {
   'se' : 'IF',
   'else' : 'ELSE',
   'enquanto' : 'WHILE',
   'num' : 'DCLN',
   'string' : 'DCLS',
   'desde' : 'FOR',
   'ate' : 'UNTIL',
   'imprime' : 'PRINT',
   'le' : 'SCAN',
   'devolve' : 'RETURN',
   'lista' : 'ARRAY'
}

tokens = [
    'LPAREN',
    'RPAREN',
    'VIRG',
    'ID',
    'BOOL', 
    'NUM',
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',
    'IGUAL',
    'CONJUNCAO',
    'DISJUNCAO',
    'DOISPONTOS',
    'MAIOR',
    'MENOR',
    'ASPAS',
    'REAL',
    'PRE',
    'PRD',
    'MOD',
] + list(reserved.values())

t_MOD       = r'%'
t_PRE       = r'\['
t_PRD       = r'\]'
t_ASPAS     = r'"'
t_DOISPONTOS= r'\:'
t_IGUAL     = r'\='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_VIRG      = r','
t_CONJUNCAO = r'\&'
t_DISJUNCAO = r'\|' 
t_SOMA      = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO   = r'\/'
t_MAIOR     = r'>'
t_MENOR     = r'<'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_REAL(t): 
    r'(([1-9]+\.[0-9]+)|(0\.[0-9]+))'
    return t

def t_NUM(t): 
    r'([0-9]+)'
    return t 

def t_BOOL(t): 
    r'True|False'
    return t

t_ignore = ' \r\n\t'
def t_error(t):
    print('Illegal character: ' + t.value[0])
    t.lexer.skip
    t.lexer.skip(1)


lexer = lex.lex() # cria um AnaLex especifico a partir da especificação acima usando o gerador 'lex' do objeto 'lex'