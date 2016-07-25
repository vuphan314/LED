'''
convert an LED parsetree into a SL program
'''

########## ########## ########## ########## ########## ########## 
'''
importing
'''

from tester import *

########## ########## ########## ########## ########## ########## 
'''
testing
'''

# printTest: str
def printTest():
    st = '\n\n/* Copy/paste the block below into SequenceL interpreter to test:\n\n'
    for func in testConsts:
        func = applyRecur('pp', (func,), isInLib = True)
        st += func + '\n'
    st += '\n(pp means PrettyPrint) */'
    return st

########## ########## ########## ########## ########## ########## 
'''
python global variables
'''

testConsts = () # ('c1', 'c2',...)
defedFuncsQuantDeeper = set() # {2, 4,...}

########## ########## ########## ########## ########## ########## 
'''
unparse an LED parsetree into a string which represents a SL program

note: tree := tuple/str
'''

# unparse: list -> str
def unparse(L):
    T = listToTree(L)
    st = unparseRecur(T)
    st = importLib + st
    st = markBeginEnd(st)
    st += printTest()
    return st

# unparseRecur: tree -> str
def unparseRecur(T):
    if type(T) == str:
        return T
    if T[0] in lexemes:
        return unparseLexemes(T)
    if T[0] == 'normT':
        return unparseNorm(T[1])
    if T[0] == 'set':
        return unparseSet(T)
    if T[0] == 'nrval':
        st = applyRecur('iv', T[1:], isInLib = True)
        return st
    if T[0] == 'tup':
        return unparseTuple(T)
    if T[0] == 'tupInd':
        st = applyRecur('tuIn', T[1:], isInLib = True)
        return st
    if T[0] in quantLabels:
        return unparseQuant(T)
    if T[0] in libOps:
        return unparseLibOps(T)
    if T[0] == 'cDef':
        func = unparseRecur(T[1])
        global testConsts
        testConsts += func,
        st = defFuncRecur(func, (), T[2])
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

# unparseLexemes: tree -> str
def unparseLexemes(T):
    lex = T[0]
    func = lexemes[lex]
    arg = T[1]
    if lex in lexemesDoublyQuoted:
        arg = addDoubleQuotes(arg)
    args = arg,
    st = applyRecur(func, args, isInLib = True)
    return st

########## ########## ########## ########## ########## ########## 
'''
unparse collections
'''

# unparseTuple: tree -> str
def unparseTuple(T):
    func = 'tu'
    terms = T[1]
    st = applyRecur(func, terms[1:], isInLib = True, isList = True)
    return st
    
# unparseSet: tree -> str
def unparseSet(T):
    func = 'se'
    if len(T) == 1: # empty set
        args = '',
    else:
        terms = T[1]
        args = terms[1:]
    st = applyRecur(func, args, isInLib = True, isList = True)
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

# unparseLibOps: tree -> str
def unparseLibOps(T):
    st = applyRecur(T[0], T[1:], isInLib = True)
    return st
    
# unparseNorm: tree -> str
def unparseNorm(T):
    if T[0] == 'setT':
        func = 'card'
    else: # 'arT'
        func = 'ab'
    st = applyRecur(func, T[1:], isInLib = True)
    return st
    
########## ########## ########## ########## ########## ########## 
'''
helper functions
'''

# defFuncRecur: tree * tuple(tree) * tree -> str
def defFuncRecur(func, args, expr):
    expr = unparseRecur(expr)
    st = applyRecur(func, args) + ' := ' + expr + ';\n\n'
    return st

# applyRecur: tree * tuple(tree) -> str
def applyRecur(func, args, isInLib = False, isList = False):
    func = unparseRecur(func)
    if isInLib:
        func = prependLib(func)
    st = func
    if args != ():
        st2 = unparseRecur(args[0])
        for arg in args[1:]:
            st2 += ', ' + unparseRecur(arg)
        if isList:
            st2 = '[' + st2 + ']'
        st += '(' + st2 + ')'
    return st
    
# addDoubleQuotes: str -> str
def addDoubleQuotes(st):
    st = '"' + st + '"'
    return st
    
# recurStr: function * tuple(tree) -> str
def recurStr(func, args):
    st = ''
    for arg in args:
        st += func(arg)
    return st
    
# listToTree: list -> tree
def listToTree(L):
    if type(L) == str:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += listToTree(l),
        return T
        
########## ########## ########## ########## ########## ########## 
'''
quantification
'''

quantLabels = {'univ', 'exist'}
libMaxSymbolsInSet = 1

class QuantInfo:
    isExist = True # or universal
    indepSymbols = () # ('i1', 'i2')
    depSymbols = () # ('d1', 'd2')
    qSet = '' # '{}'
    qPred = () # sub-tree, like: equal(i1, d2)
    auxNum = 1
    
    # numSymbolsInSet: int
    def numSymbolsInSet(self):
        n = len(self.depSymbols)
        return n
    
    # defFuncMain: str
    def defFuncMain(self):
        func = self.nameFuncMain()
        args = ()
        
        func2 = self.nameFuncQuant()
        args2 = self.nameFuncPred(),
        expr = applyRecur(func2, args2)
        
        st = defFuncRecur(func, args, expr)
        
        n = self.numSymbolsInSet()
        if n > libMaxSymbolsInSet and not self.isDefedFuncQuantDeeper():
            st = self.defFuncQuantDeeper() + st
        
        return st
        
    # isDefedFuncQuantDeeper: bool
    def isDefedFuncQuantDeeper(self):
        n = self.numSymbolsInSet()
        b = n in defedFuncsQuantDeeper
        return b
            
    # nameFuncQuant: str
    def nameFuncQuant(self, isDeeper = True):
        if self.isExist:
            func = 'someSet'
        else: # universal
            func = 'allSet'
        if isDeeper:
            n = self.numSymbolsInSet()
            func += '_' + str(n) + '_'
        return func
        
    # defFuncQuantDeeper: str
    def defFuncQuantDeeper(self):
        n = self.numSymbolsInSet()
        global defedFuncsQuantDeeper
        defedFuncsQuantDeeper |= {n}
        
        func = self.nameFuncQuant()
        arg = 'vs'
        args = arg + '(' + str(n) + ')',
        
        func2 = self.nameFuncQuant(isDeeper = False)
        args2 = arg,
        for i in range(n):
            args2 = applyRecur(func2, args2),
        expr = args2[0]
        
        st = defFuncRecur(func, args, expr)
        return st
    
    # nameFuncMain: str
    def nameFuncMain(self, isOfNext = False):
        st = self.appendAux('MAIN', isOfNext)
        return st
        
    # nameFuncPred: str
    def nameFuncPred(self):
        st = self.appendAux('PRED')
        return st
        
    # nameFuncSet: str
    def nameFuncSet(self):
        st = self.appendAux('SET')
        return st
        
    # appendAux: str -> str
    def appendAux(self, extraAppend, isOfNext = False):
        num = self.auxNum
        if isOfNext:
            num += 1
        st = 'AUX_' + str(num) + '_' + extraAppend + '_'
        return st
    
########## ########## ########## ########## ########## ########## 
'''
importing and using LED library
'''

libLoc = '../'
libName = 'libLED'
libAs = ''
importLib = 'import * from "' + libLoc + libName + '.sl" as ' + libAs + '*;\n\n'

# str -> str
def prependLib(st):
    st = libAs + st
    return st
