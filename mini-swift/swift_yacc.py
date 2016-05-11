import ply.yacc as yacc
import re

# Get the token map from the lexer.  This is required.
from swift_lex import tokens

DEBUG = False

# Namespace & built-in functions

name = {}

global ast
ast = []

def cons(l):
    return [l[0]] + l[1]

name['cons'] = cons

def concat(l):
    return l[0] + l[1]

name['concat'] = concat

def listar(l):
    return l

name['list'] = listar

def car(l):
    return l[0][0]

name['car'] = car

def cdr(l):
    return l[0][1:]

name['cdr'] = cdr

def eq(l):
    return l[0] == l[1]

name['eq'] = eq
name['='] = eq

def _and(l):
    return not False in l

name['and'] = _and

def _or(l):
    return True in l

name['or'] = _or

def cond(l):
    if l[0]:
        return l[1]

name['cond'] = cond

def add(l):
    return sum(l)

name['+'] = add

def minus(l):
    '''Unary minus'''
    return -l[0]

name['-'] = minus

def _print(l):
    print lisp_str(l[0])

name['print'] = _print

#  Evaluation functions

def lisp_eval(simb, items):
    if simb in name:
        return call(name[simb], eval_lists(items))
    else:
       return [simb] + items

def call(f, l):
    try:
        return f(eval_lists(l))  
    except TypeError:
        return f

def eval_lists(l):
    r = []
    for i in l:
        if is_list(i):
            if i:
                r.append(lisp_eval(i[0], i[1:]))
            else:
                r.append(i)
        else:
            r.append(i)
    return r

# Utilities functions

def is_list(l):
    return type(l) == type([])

def lisp_str(l):
    if type(l) == type([]):
        if not l:
            return "()"
        r = "("
        for i in l[:-1]:
            r += lisp_str(i) + " "
        r += lisp_str(l[-1]) + ")"
        return r
    elif l is True:
        return "true"
    elif l is False:
        return "false"
    elif l is None:
        return 'nil'
    else:
        return str(l)

# BNF
#def p_

def p_exp_binop(p):
    'exp : binop'
    if DEBUG: print "p_exp_binop"
    p[0] = p[1]

def p_binop(p):
    'binop : exp BIN exp'
    if DEBUG: print "Calling", p[2], "with", p[1], "and", p[3]
    ast = [p[2], p[1], p[3]]
    p[0] = ast

def p_exp_atom(p):
    'exp : atom'
    if DEBUG: print "p_exp_atom"
    p[0] = p[1]


def p_exp_qlist(p):
    'exp : quoted_list'
    if DEBUG: print "p_exp_qlist"
    p[0] = p[1]

def p_exp_call(p):
    'exp : call'
    if DEBUG: print "p_exp_call"
    p[0] = p[1]

def p_quoted_list(p):
    'quoted_list : QUOTE list'
    if DEBUG: print "p_quoted_list"
    #p[0] = p[2]
    p[0] = ["quote"] + [p[2]]

def p_list(p):
    'list : LPAREN items RPAREN'
    if DEBUG: print "p_list"
    p[0] = p[2]

def p_items(p):
    'items : item items'
    if DEBUG: print "p_items"
    p[0] = [p[1]] + p[2]

def p_items_empty(p):
    'items : empty'
    if DEBUG: print "p_items_empty"
    p[0] = []

def p_empty(p):
    'empty :'
    if DEBUG: print "p_empty"
    pass

def p_item_atom(p):
    'item : atom'
    if DEBUG: print "p_item_atom"
    p[0] = p[1]

def p_item_list(p):
    'item : list'
    if DEBUG: print "p_item_list"
    p[0] = p[1]

def p_item_list(p):
    'item : quoted_list'
    if DEBUG: print "p_item_list"
    p[0] = p[1]
        
def p_item_call(p):
    'item : call'
    if DEBUG: print "p_item_call"
    p[0] = p[1]

def p_item_empty(p):
    'item : empty'
    if DEBUG: print "p_item_empty"
    p[0] = p[1]

def p_call(p):
    'call : LPAREN SIMB items RPAREN'
    global ast
    if DEBUG: print "Calling", p[2], "with", p[3]
    #if isinstance(p[3], list) and isinstance(p[3][0], list) and p[3][0][0] == "'":
        #p[3] = [["quote"] + [p[3][0][1:]]]
    ast = [p[2]] + [i for i in p[3]]
    p[0] = ast
    #p[0] = lisp_eval(p[2], p[3])

def p_let(p):
    'exp : LET atom EQ exp'
    if DEBUG: print "p_let"
    varname1 = re.compile('[a-zA-Z][a-zA-Z0-9_]*')
    varname2 = re.compile('[a-zA-Z]')
    if(varname1.match(p[2]) or varname2.match(p[2])):
        ast = ['define', p[2], p[4]]
        p[0] = ast
    else:
        p[0] = "Constant names must begin with a letter and contain" \
               " only letters, digits, and underscores."

def p_atom_simbol(p):
    'atom : SIMB'
    if DEBUG: print "p_atom_simbol"
    p[0] = p[1]

def p_atom_bool(p):
    'atom : bool'
    if DEBUG: print "p_atom_bool"
    p[0] = p[1]

def p_atom_num(p):
    'atom : NUM'
    if DEBUG: print "p_atom_num"
    p[0] = p[1]

def p_atom_word(p):
    'atom : QUOTE SIMB'
    if DEBUG: print "p_atom_word"
    p[0] = p[1]

def p_atom_word(p):
    'atom : TEXT'
    if DEBUG: print "p_atom_word"
    #var_check = re.compile('\\([a-zA-Z_+=\*\-][a-zA-Z0-9_+\*\-]*\)')
    #p[0] = p[1]
    #if(var_check.match(p[1]) != None):
    #    l = var_check.find_all(p[1])
    #    for s in l:
    #        s = s[2:(len(l) - 1)]
    #        p[]

    p[0] = p[1]

def p_atom_empty(p): 
    'atom :'
    if DEBUG: print "p_atom_empty"
    pass


def p_true(p):
    'bool : TRUE'
    if DEBUG: print "p_true"
    p[0] = True

def p_false(p):
    'bool : FALSE'
    if DEBUG: print "p_false"
    p[0] = False

def p_nil(p):
    'atom : NIL'
    if DEBUG: print "p_nil"
    p[0] = None

# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()


