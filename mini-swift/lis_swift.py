################ Lispy: Scheme Interpreter in Python

## (c) Peter Norvig, 2010-14; See http://norvig.com/lispy.html

################ Types

from __future__ import division
import re
from swift_yacc import yacc

Symbol = str          # A Lisp Symbol is implemented as a Python str
List   = list         # A Lisp List is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

################ Environments

def standard_env():
    "An environment with some Scheme standard procedures."
    import math, operator as op
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.div, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   apply,
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list),
        'exec':    lambda x: eval(compile(x,'None','single')),
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        if (var in self):
            return self
        else:
            if(self.outer != None):
                self.outer.find(var)
            else:
                return 0

global_env = standard_env()

################ Interaction: A REPL

def repl(prompt='lis_swift.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None: 
            print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if  isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)

################ Procedures

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))

################ eval

toReturn = None

DEBUG = False

str_check = re.compile('[\'\"]')
var_check = re.compile('\\\\\([a-zA-Z_+=\*\-][a-zA-Z0-9_+\*\-]*\)')
var_check1 = re.compile('\\\\\([ -&,(-~]+\)')
lambda_check = re.compile('\(lambda[ -&,(-~]+\)')


def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if (isinstance(x, Symbol)):      # variable reference
        if DEBUG: print "var ref"
        if(env.find(x) != 0):
            return env.find(x)[x]
        else:
            if(str_check.match(x)):
                if(var_check1.search(x)):
                    l = var_check1.findall(x)
                    if(len(l) == 1):
                        y = (l[0])[2:(len(l[0]) - 1)]
                        y = yacc.parse(y)
                        y = str(eval(y))
                        x = x.replace(str(l[0]), y, 1)
                    else:
                        for s in (0, (len(l) - 1)):
                            y = (l[s])[2:(len(l[s]) - 1)]
                            y = yacc.parse(y)
                            y = str(eval(y))
                            x = x.replace(str(l[s]), str(eval(y)), 1)
                    return x
                elif(lambda_check.match(x)):
                    l = lambda_check.findall(x)
                    y = (l[0])[2:(len(l[0]) - 1)]
                    y = yacc.parse(y)
                    y = str(eval(y))
                    print y
                else:
                    return x
            else:
                print 'Could not resolve symbol', x
                return None
    elif not isinstance(x, List):  # constant literal
        if DEBUG: print "const lit"
        return x                
    elif x[0] == 'quote':          # (quote exp)
        if DEBUG: print "quote"
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        if DEBUG: print "if"
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # (define var exp)
        if DEBUG: print "def"
        (_, var, exp) = x
        if(eval(exp, env) != None):
            env[var] = eval(exp, env)
        else:
            print 'Not a valid constant assignment.'
    elif x[0] == 'set!':           # (set! var exp)
        if DEBUG: print "set!"
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'lambda':         # (lambda (var...) body)
        if DEBUG: print "lambda"
        (_, parms, body) = x
        return Procedure(parms, body, env)
    elif x[0] == 'exec':
        if DEBUG: print "exec"
        proc = eval(x[0], env)
        import re
        exec(proc(re.sub(r"^'|'$", '', x[1])))
        return toReturn
    else:                          # (proc arg...)
        if DEBUG: print "else"
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)
