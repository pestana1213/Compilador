import ply.yacc as yacc
import sys
from myLanguageLex import tokens 
 
global store 
global nroIf
global nroWhile
global nroFor
variaveis = {}
array = {}

nroWhile = 0
nroIf = 0
nroFor = 0 
store = 0

def p_final(p): 
    'final : reconhece'
    p[0] = r'START' + '\n' + p[1] +  r'STOP '+ '\n'
    print(p[0])

def p_reconhece(p): 
    '''reconhece : tipos
                 | declara
                 | ciclos
                 | print
                 | scan
                 | devolve
                 | atribuicao
    '''
    p[0] = p[1] 

def p_reconheceComposto(p): 
    '''reconhece : tipos reconhece
                 | declara reconhece
                 | ciclos reconhece 
                 | print reconhece
                 | scan reconhece
                 | atribuicao reconhece
    '''
    p[0] =p[1] + p[2] 

def p_multiplicacao(p):
    'expression : expression MULTIPLICACAO term'
    p[0] = p[1] + ' \n' + p[3] + '\n' + r'MUL' + '\n'

def p_multiplicacaoId(p): 
    'expression : expression MULTIPLICACAO ID'
    if p[3] in variaveis: 
        p[0] = p[1] + '\n' + r'PUSHG ' + str(variaveis[p[3]]) + '\n' +  r'MUL' + '\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_divisao(p):
    'expression : expression DIVISAO term'
    p[0] = p[1] + ' \n' + p[3] + '\n' + r'DIV' + '\n'

def p_divisaoId(p): 
    'expression : expression DIVISAO ID'
    if p[3] in variaveis: 
        p[0] = p[1] + '\n' + r'PUSHG ' + str(variaveis[p[3]]) + '\n' + r'DIV' + '\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_somaId(p): 
    'expression : expression SOMA ID'
    if p[3] in variaveis: 
        p[0] = p[1] + '\n' + r'PUSHG ' + str(variaveis[p[3]])  + '\n' + r'ADD' + '\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'
 
def p_soma(p):
    'expression : expression SOMA term'
    p[0] = p[1] + ' \n' + p[3] + '\n' + r'ADD' + '\n'

def p_subtracao(p):
    'expression : expression SUBTRACAO term'
    p[0] = p[1] + ' \n' + p[3] + '\n' + r'SUB' + '\n'

def p_subtracaoId(p): 
    'expression : expression SUBTRACAO ID'
    if p[3] in variaveis: 
        p[0] = p[1] + '\n' + r'PUSHG ' + str(variaveis[p[3]])  + '\n' + r'SUB' + '\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_modulo(p): 
    'expression : NUM MOD NUM'
    p[0] = r'PUSHI ' + str(int(p[1])) + '\n' + r'PUSHI ' + str(int(p[3])) + '\nMOD\n'

def p_moduloId(p): 
    'expression : ID MOD NUM'
    if p[1] in variaveis: 
        p[0] = r'PUSHG ' + str(variaveis[p[1]]) + '\n' + r'PUSHI ' + str(int(p[3])) + '\nMOD\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_moduloNUMId(p): 
    'expression : NUM MOD ID'
    if p[3] in variaveis:
        p[0] = r'PUSHI ' + str(int(p[1])) + '\n' + r'PUSHG ' + str(variaveis[p[3]]) +'\nMOD\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_moduloIdID(p): 
    'expression : ID MOD ID'
    if p[1] in variaveis and p[3] in variaveis:
        p[0] = r'PUSHG ' + str(variaveis[p[1]]) +  r'PUSHG ' + str(variaveis[p[3]]) + 'MOD\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_fator(p):
    'factor : NUM'
    p[0] = r'PUSHI ' + str(int(p[1])) + '\n'

def p_fatorReal(p):
    'factor : REAL'
    p[0] = r'PUSHI ' + str(int(p[1])) + '\n'

def p_termo(p):
    'term : factor'
    p[0] = p[1]

def p_expressao(p):
    'expression : term'
    p[0] = p[1]
    
def p_expressaoId(p): 
    'expression : ID'
    if (p[1] in variaveis):
        p[0] = r'PUSHG ' + str(variaveis[p[1]]) + '\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_elementosC(p):
    '''els : comparacoes
             | term 
    '''
    p[0] = p[1]

def p_elementosUnicos(p): 
    '''els : ID
           | BOOL
    '''
    if p[1] == 'True': 
        p[0] = r'PUSHI 1' + '\n'
    elif p[1]=='False': 
        p[0] = r'PUSHI 0' + '\n'
    elif isinstance(p[1],str):  
        if (p[1] in variaveis):
            p[0] = r'PUSHG ' + str(variaveis[p[1]]) + '\n'
        else: 
            p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_atribuicaoArray(p):
    'atribuicao : ID PRE NUM PRD IGUAL expression'
    if p[1] in variaveis: 
        p[0] = r'PUSHGP' + '\nPUSHI 0\n' + 'PADD\n' +'PUSHI ' + str(variaveis[p[1]]+int(p[3])) + '\n' + p[6] + '\nSTOREN\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel nao definida :("' + '\n' + r'ERR' + '\n' 

def p_atribuicaoArrayID(p):
    'atribuicao : ID PRE ID PRD IGUAL expression'
    if p[1] in variaveis and p[3] in variaveis: 
        p[0] = r'PUSHGP' + '\nPUSHI ' + str(store-array[p[1]]) + '\nPADD\n' + 'PUSHG ' + str(variaveis[p[3]]) + '\n' + p[6] + '\nSTOREN\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel nao definida :("' + '\n' + r'ERR' + '\n' 

def p_atribuicaoIdArray(p):
    'atribuicao : ID IGUAL ID PRE ID PRD'
    if p[1] in variaveis and p[3] in variaveis and p[5] in variaveis: 
        p[0] = r'PUSHGP' + '\nPUSHI ' + str(store-array[p[3]]) + '\nPADD\n' + 'PUSHG ' + str(variaveis[p[5]]) + '\nLOADN\n' + 'STOREG ' + str(variaveis[p[1]]) + '\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel nao definida :("' + '\n' + r'ERR' + '\n' 

def p_atribuicaoNumArray(p):
    'atribuicao : ID IGUAL ID PRE NUM PRD'
    if p[1] in variaveis and p[3] in variaveis and p[5] in variaveis: 
        p[0] = r'PUSHGP' + '\nPUSHI ' + str(store-array[p[3]]) + '\nPADD\n' + 'PUSHG ' + str(p[5]) + '\nLOADN\n' + 'STOREG ' + str(variaveis[p[1]]) + '\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel nao definida :("' + '\n' + r'ERR' + '\n' 


def p_declararArray(p): 
    'declara : ARRAY PRE NUM PRD ID'
    global store
    if p[5] not in variaveis: 
        p[0] = r'PUSHN ' + str(p[3]) + '\n'
        variaveis[p[5]] = store
        store += int(p[3])
        array[p[5]] = int(p[3])
    else: 
        p[0] = r'PUSHS "Erro: Variavel ja declarada :(" ' + '\n' + r'ERR' + '\n'

def p_declararNum(p): 
    'declara : DCLN ID IGUAL expression'
    global store
    if p[2] not in variaveis: 
        p[0] = p[4] + '\n'
        variaveis[p[2]] = store
        store += 1
    else: 
        p[0] = p[4] + '\n' + r'STOREG ' + str(variaveis[p[2]]) + '\n'

def p_declararNumSolo(p): 
    'declara : DCLN ID'
    global store
    if p[2] not in variaveis: 
        p[0] = r'PUSHI 0' + '\n'
        variaveis[p[2]] = store
        store += 1
    else: 
        p[0] = r'PUSHI 0' + '\n'

def p_declararString(p): 
    'declara : DCLS ID'
    p[0] = r'PUSHS ' + "" + '\n'
    global store
    if p[2] not in variaveis: 
        p[0] = r'PUSHS ' + "" + '\n'
        variaveis[p[2]] = store
        store += 1
    else: 
        p[0] = r'PUSHS ' + ""+ '\n'

def p_declararStringSolo(p): 
    'declara : DCLS ID IGUAL ASPAS ID ASPAS'
    global store
    if p[2] not in variaveis: 
        p[0] = r'PUSHS ' +  r'"' + p[5] + r'"' + '\n'
        variaveis[p[2]] = store
        store += 1
    else: 
        p[0] = r'PUSHS ' + r'"' + p[4] + r'"' + '\n'

def p_conjuncao(p): 
    '''conjuncao : els CONJUNCAO els
                 | els CONJUNCAO aux
    '''
    p[0] = p[1] + p[3]

def p_disjuncao(p): 
    '''disjuncao : els DISJUNCAO els
                 | els DISJUNCAO aux
    '''
    p[0] = p[1] + p[3]

def p_auxiliar(p):
    '''aux : conjuncao
           | disjuncao
    '''
    p[0] = p[1]

def p_comparacoes(p):
    '''comparacoes : expression IGUAL IGUAL expression
                    | aux IGUAL IGUAL aux
                    | aux MAIOR aux
                    | aux MENOR aux
                    | expression MAIOR expression
                    | expression MENOR expression
                    | term MAIOR term
                    | term MENOR term
                    | term IGUAL IGUAL term 
    '''
    if p[2] == '=':
        p[0] = p[1] + ' \n' + p[4]  + r'EQUAL' + '\n'
    elif p[2] == '<':
        p[0] = p[1] + ' \n' + p[3]  + r'INF' + '\n'
    elif p[2] == '>':
        p[0] = p[1] + ' \n' + p[3]  + r'SUP' + '\n'        
 

def p_comparacoesComIgualdade(p):
    '''comparacoes :  aux MAIOR IGUAL aux
                    | aux MENOR IGUAL aux
                    | expression MAIOR IGUAL expression
                    | expression MENOR IGUAL expression
                    | term MAIOR IGUAL term
                    | term MENOR IGUAL term
    '''
    if p[2] == '<':
        p[0] = p[1] + ' \n' + p[4]  + r'INFEQ' + '\n'
    elif p[2] == '>':
        p[0] = p[1] + ' \n' + p[4]  + r'SUPEQ' + '\n'        
 

def p_tiposExpressao(p): 
    '''tipos : aux
             | expression
             | comparacoes
             | print
             | devolve
             | scan
             | declara
    '''
    p[0] = p[1]

def p_statements(p): 
    'statements : stat'
    p[0] = p[1]

def p_statementsComposto(p):
    'statements : stat statements'
    p[0] = p[1] + p[2]       

def p_stat(p): 
    '''stat : atribuicao 
            | tipos
            | ciclos
    '''
    p[0] = p[1]

def p_statVazia(p): 
    'stat : '
    p[0] = '\n'

def p_atribuicao(p):
    'atribuicao : ID IGUAL expression'
    if p[1] in variaveis: 
        p[0] = p[3] + r'STOREG ' + str(variaveis[p[1]]) + '\n'
    else: 
        p[0] = r'PUSHS "Erro: Variavel nao definida :("' + '\n' + r'ERR' + '\n' 

def p_cicloIf(p): 
    'if : IF tipos DOISPONTOS LPAREN statements RPAREN ELSE LPAREN statements RPAREN'
    global nroIf
    aux = nroIf + 1 
    p[0] = p[2] + r'JZ L' + str(nroIf) + '\n' + p[5] + '\nJUMP L' + str(aux) + '\nL' + str(nroIf) + ':\n' + p[9] + '\nL' + str(aux) + ':\n'

def p_cicloIfSolo(p):
    'if : IF tipos DOISPONTOS LPAREN statements RPAREN'
    global nroIf
    p[0] = p[2] + r'JZ L' + str(nroIf) + '\n' + p[5] + '\nJUMP L' + str(nroIf) + '\nL' + str(nroIf) + ':\n'
    nroIf += 1 

def p_sinal(p): 
    '''sinal : SOMA
               | SUBTRACAO
               | MULTIPLICACAO
               | DIVISAO
    '''
    if p[1] == '+' : 
        p[0] = '\nADD\n'
    elif p[1] == '-' : 
        p[0] = '\nSUB\n'
    elif p[1] == '*' : 
        p[0] = '\nMUL\n'
    elif p[1] == '/' : 
        p[0] = '\nDIV\n'

def p_cicloFor(p): 
    'for : FOR ID UNTIL comparacoes VIRG sinal NUM DOISPONTOS LPAREN statements RPAREN'
    global nroFor 
    if p[2] in variaveis: 
        p[0] = r'CICLO' + str(nroFor) + ':\n' + p[4] + r'JZ FIM' + str(nroFor) + '\n' + p[10] + r'PUSHG ' + str(variaveis[p[2]]) + '\n' + r'PUSHI ' + p[7] + p[6] + '\nSTOREG ' + str(variaveis[p[2]]) + '\n' + r'JUMP CICLO' + str(nroFor) + '\nFIM' + str(nroFor) + ':\n'
        nroFor+=1

def p_cicloWhile(p):
    'while : WHILE tipos DOISPONTOS LPAREN statements RPAREN'
    global nroWhile
    aux = nroWhile +1 
    p[0] = r'L' + str(nroWhile) + ':\n' + p[2] + '\n' + r'JZ L' + str(aux) + '\n' + p[5] + '\n' + r'JUMP L' + str(nroWhile) + '\n' + r'L' + str(aux) + ':\n'
    nroWhile += 1 

def p_cicloSIf(p): 
    'ciclos : if'
    p[0] = p[1]
    global nroIf
    nroIf+=1 

def p_cicloSFor(p): 
    'ciclos : for'
    p[0] = p[1]
    global nroFor
    nroFor+=1 

def p_cicloSWhile(p): 
    'ciclos : while'
    p[0] = p[1]
    global nroWhile
    nroWhile+=1 
    
def p_printId(p): 
    'print : PRINT LPAREN ID RPAREN'
    if p[3] in variaveis: 
        p[0] = r'PUSHG ' + str(variaveis[p[3]]) + '\nSTRI\n' + r'WRITES' + '\n'
    else:
        p[0] = r'PUSHS ' + r'"Erro: Variavel desconhecida :(" '  + '\n' + r'ERR' + '\n'

def p_print(p): 
    '''print : PRINT LPAREN ASPAS ID ASPAS RPAREN
    '''
    p[0] = r'PUSHS ' + r'"' + p[4] + r'"' + '\n' + r'WRITES' + '\n'
    
def p_printN(p): 
    '''print : PRINT LPAREN ASPAS term ASPAS RPAREN
    '''
    p[0] = r'PUSHG ' + r'"' + p[4] + r'"' + '\n' + r'WRITEI' + '\n'

def p_printComposto(p): 
    '''print : PRINT LPAREN ASPAS ID ASPAS VIRG expression RPAREN
    '''
    p[0] = r'PUSHS ' + r'"' + p[4] + r'"' + '\n' +  r'WRITES' + '\n' + r'PUSHG ' + p[7] + r'WRITEI' + '\n'

def p_printExpressao(p):
    'print : PRINT LPAREN expression RPAREN'
    p[0] = p[3] + r'WRITEI' + '\n'

def p_printVirgula(p): 
    'print : PRINT LPAREN VIRG RPAREN'
    p[0] = 'PUSHS ","\n' + r'WRITES' + '\n'

def p_scan(p): 
    '''scan : SCAN LPAREN ID RPAREN 
    '''
    global store
    if p[3] in variaveis: 
        p[0] = r'READ' + '\n' + r'ATOI' + '\n' + r'STOREG '  + str(variaveis[p[3]]) + '\n' 
    else: 
        p[0] = r'PUSHS "Erro: Variavel desconhecida :(" ' + '\n' + r'ERR' + '\n'

def p_return(p): 
    'devolve : RETURN LPAREN expression RPAREN'
    p[0] = p[3] + '\n' + r'PUSHS "O return é: "' + '\nWRITES\n' + 'WRITEI\n'

def p_error(p):
    parser.success = False
    print('Syntax error!')

###inicio do parsing
parser = yacc.yacc()
parser.success = True

fonte = ""
for line in sys.stdin:
    fonte += line
parser.parse(fonte)
