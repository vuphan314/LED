'''
convert an LED parse tree into a SL program
'''

########## ########## ########## ########## ########## ########## 

from tester import *

########## ########## ########## ########## ########## ########## 
'''
unparse an LED parse tree into a string which represents a SL program
'''

# unparse: list -> str
def unparse(L):
    T = listToTuple(L)
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
    if T[0] == 'normT':
        return unparseNorm(T[1])
    if T[0] == 'set':
        return unparseSet(T)
    if T[0] == 'nrval':
        func = 'iv'
        st = applyNaryRecur(func, T[1:])
        return st
    if T[0] == 'tup':
        return unparseTuple(T)
    if T[0] == 'tupInd':
        func = 'tuIn'
        st = applyNaryRecur(func, T[1:])
        return st
    if T[0] in parseQuantifiers:
        return unparseQuantification(T)
    if T[0] in libOps:
        return unparseLibOps(T)
    if T[0] == 'cDef':
        func = unparseRecur(T[1])
        args = ()
        expr = unparseRecur(T[2])
        st = defineFunction(func, args, expr)
        return st
    else:
        return recurStr(unparseRecur, T[1:])
        
########## ########## ########## ########## ########## ########## 
'''
quantification
'''

parseQuantifiers = {'univ', 'exist'}
libMaxSymbolsInSet = 2

class QuantInfo:
    isExistential = True # or universal
    independentSymbols = () # ('i1', 'i2')
    dependentSymbols = () # ('d1', 'd2')
    quantSet = '' # '{}'
    quanPred = () # sub-tree, like: equal(i1, d2)
    auxNum = 1
    
    # writeMain: str
    def writeMain(self):
        xx
    
    # funcMain: (bool ->) str
    def funcMain(self, next = False):
        st = self.appendAux('A', next)
        return st
        
    # funcPred: str
    def funcPred(self):
        st = self.appendAux('B')
        return st
        
    # funcSet: str
    def funcSet(self):
        st = self.appendAux('C')
        return st
        
    # appendAux: str (* bool) -> str
    def appendAux(self, extraAppend, next = False):
        num = self.auxNum
        if next:
            num += 1
        st = 'AUX_' + str(num) + '_' + extraAppend + '_'
        return st
    
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
    args = arg,
    st = applyNary(func, args, True)
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
        args = arg,
        st += applyNary(func, args, True)
    else:
        terms = T[1]
        args = terms[1:]
        st += applyNaryRecur(func, args, True)
    return st

########## ########## ########## ########## ########## ########## 
'''
unparse library operations
'''

equalityOps = {'eq', 'uneq'}
relationalOps = {'less', 'greater', 'lessEq', 'greaterEq'}
arOps = {'add', 'bMns', 'uMns', 'mult', 'div', 'flr', 'clng', 'md', 'exp'}
setOps = {'setMem', 'sbset', 'unn', 'nrsec', 'diff', 'cross', 'powSet'}
boolOps = {'equiv', 'impl', 'disj', 'conj', 'neg'}
libOps = equalityOps | relationalOps | arOps | setOps | boolOps

# unparseLibOps: tuple -> str
def unparseLibOps(T):
    func = T[0]
    st = applyNaryRecur(func, T[1:])
    return st
    
def unparseNorm(T):
    if T[0] == 'setT':
        func = 'card'
    else: # 'arT'
        func = 'ab'
    st = applyNaryRecur(func, T[1:])
    return st
    
########## ########## ########## ########## ########## ########## 
'''
helper functions
'''

# defineFunction: str * list(str) * str -> str;
def defineFunction(func, args, expr):
    st = applyNary(func, args, False) + ' := ' + expr + ';\n\n'
    return st

# applyNary: str * list(str) * bool -> str
def applyNary(func, args, addLib):
    if addLib:
        func = prependLib(func)
    st = func
    if args != ():
        st += '(' + args[0]
        for arg in args[1:]
            st += ', ' + arg
        st += ')'
    return st

# applyNaryRecur: str * tuple(tuple) (* bool) -> str
def applyNaryRecur(func, args, listSL = False):
    st = prependLib(func)
    if args != ():
        st += '('
        if listSL:
            st += '['
        st += unparseRecur(args[0])
        for arg in args[1:]:
            st += ', ' + unparseRecur(arg)
        if listSL:
            st += ']'
        st += ')'
    return st
    
# addDoubleQuotes: str -> str
def addDoubleQuotes(st):
    st = '"' + st + '"'
    return st
    
# recurStr: function * tuple -> str
def recurStr(func, tupl):   
    st = ''
    for t in tupl:
        st += func(t)
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

# listToTuple: list -> tuple
def listToTuple(L):
    if type(L) != list:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += listToTuple(l),
        return T
