'''
convert an LED parse-forest into a SL program
'''

########## ########## ########## ########## ########## ########## 

from tester import *

########## ########## ########## ########## ########## ########## 
'''
unparse an LED parse-forest (list) into a string which represents a SL program
'''

# unparse: list -> str
def unparse(L):
    T = forestToTree(L)
    st = unparseRecur(T)
    st = importLib + st
    st = markBeginEnd(st)
    return st

# unparseRecur: tuple -> str
def unparseRecur(T):
    if T[0] in lexemes:
        return unparseLexemes(T)
    if T[0] == 'id':
        return T[1]
    if T[0] == 'set':
        return unparseSet(T)
    if T[0] == 'tup':
        return unparseTuple(T)
    if T[0] == 'tupInd':
        func = 'tuIn'
        st = applyNaryRecur(func, T[1:])
        return st
    if T[0] in libOps:
        return unparseLibOps(T)
    if T[0] == 'cDef':
        st1 = unparseRecur(T[1])
        st2 = unparseRecur(T[2])
        st = st1 + ' := ' + st2 + ';\n\n'
        return st
    else:
        return recurStr(unparseRecur, T[1:])
        
########## ########## ########## ########## ########## ########## 
'''
misc functions
'''

# unionDicts: tuple(dict) -> dict
def unionDicts(ds):
    D = {}
    for d in ds:
        D.update(d)
    return D
    
########## ########## ########## ########## ########## ########## 
'''
unparse lexemes
'''

lexemesDoublyQuoted = {'numl': 'nu', 'atom': 'at'}
lexemes = unionDicts((lexemesDoublyQuoted, {'truth': 'tr'}))

# unparseLexemes: tuple -> str
def unparseLexemes(T):
    lex = T[0]
    func = lexemes[lex]
    arg = T[1]
    if lex in lexemesDoublyQuoted:
        arg = addDoubleQuotes(arg)
    st = applyUnary(func, arg)
    return st

########## ########## ########## ########## ########## ########## 
'''
unparse collections
'''

# unparseTuple: tuple -> str
def unparseTuple(T):
    func = 'tu'
    terms = T[1]
    st = applyNaryRecur(func, terms[1:], True)
    return st
    
# unparseSet: tuple -> str
def unparseSet(T):
    func = 'se'
    st = ''
    if len(T) == 1: # empty set
        arg = '[]'
        st += applyUnary(func, arg)
    else:
        terms = T[1]
        args = terms[1:]
        st += applyNaryRecur(func, args, True)
    return st

########## ########## ########## ########## ########## ########## 
'''
unparse arithmetic operations
'''

equalityOps = {'eq', 'uneq'}
relationalOps = {'less', 'greater', 'lessEq', 'greaterEq'}
arOps = {'add', 'bMns', 'uMns', 'mult', 'div', 'flr', 'clng', 'ab', 'md', 'exp'}
libOps = equalityOps | relationalOps | arOps

# unparseLibOps: tuple -> str
def unparseLibOps(T):
    func = T[0]
    st = applyNaryRecur(func, T[1:])
    return st
    
########## ########## ########## ########## ########## ########## 
'''
helper functions
'''

# applyUnary: str * str -> str
def applyUnary(func, arg):
    func = prependLib(func)
    st = func + '(' + arg + ')'
    return st

# applyNaryRecur: str * tuple -> str
def applyNaryRecur(func, args, listSL = False):
    func = prependLib(func)
    st = func + '('
    if listSL:
        st += '['
    st += unparseRecur(args[0])
    for arg in args[1:]:
        st += ', ' + unparseRecur(arg)
    if listSL:
        st += ']'
    st += ')'
    return st
    
# recurStr: function * tuple -> str
def recurStr(func, tupl):   
    st = ''
    for t in tupl:
        st += func(t)
    return st
    
# addDoubleQuotes: str -> str
def addDoubleQuotes(st):
    st = '"' + st + '"'
    return st
    
########## ########## ########## ########## ########## ########## 
'''
importing and using LED library
'''

libLoc = '../'
libName = 'ledlib'
libAs = ''
importLib = 'import * from "' + libLoc + libName + '.sl" as ' + libAs + '*;\n\n'

# str -> str
def prependLib(st):
    st = libAs + st
    return st

########## ########## ########## ########## ########## ########## 
'''
transform a parse-forest (list) to a parse-tree (tuple)
'''

# forestToTree: list -> tuple
def forestToTree(L):
    L = ['prog'] + L
    T = listToTuple(L)
    transformed = listToTuple(T)
    return transformed
    
# listToTuple: list -> tuple
def listToTuple(L):
    if type(L) != list:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += listToTuple(l),
        return T
