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
auxFuncNum = 1
    
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
        st = defFuncRecur(func, (), T[2], moreSpace = True)
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
    st = applyRecur(func, terms[1:], isInLib = True, argsAreBracketed = True)
    return st
    
# unparseSet: tree -> str
def unparseSet(T):
    func = 'se'
    if len(T) == 1: # empty set
        args = '',
    else:
        terms = T[1]
        args = terms[1:]
    st = applyRecur(func, args, isInLib = True, argsAreBracketed = True)
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
def defFuncRecur(func, args, expr, inds = (), moreSpace = False):
    expr = unparseRecur(expr)
    st = applyRecur(func, args, inds = inds) + ' := ' + expr + ';\n'
    if moreSpace:
        st += '\n'
    return st

# applyRecur: tree * tuple(tree) -> str
def applyRecur(func, args, isInLib = False, argsAreBracketed = False, inds = ()):
    func = unparseRecur(func)
    if isInLib:
        func = prependLib(func)
    st = func
    if args != ():
        st2 = unparseRecur(args[0])
        for arg in args[1:]:
            st2 += ', ' + unparseRecur(arg)
        if argsAreBracketed:
            st2 = addBrackets(st)
        st += '(' + st2 + ')'
    st = appendInds(st, inds)
    return st

# writeLetClauses: tuple(str) -> str
def writeLetClauses(T):
    st = '\n\tlet\n'
    for t in T:
        st += '\t\t' + t
    return st
    
# writeInClause: str -> str
def writeInClause(st):
    st = '\tin\n\t\t' + st;
    return st
    
# appendInds: str * tuple(str) -> str
def appendInds(st, T):
    for t in T:
        st += addBrackets(t)
    return st
    
# addBrackets: str -> str
def addBrackets(st):
    st = '[' + st + ']'
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
libMaxSymbsInSet = 1

class QuantInfo:
    isExist = True # or universal
    indepSymbs = () # ('x', 'y',...)
    depSymbs = () # ('a', 'b',...)
    qSet = '' # '{1, 2,...}'
    qPred = () # sub-tree, like: equal(x, b)
    
    # getNumSymbsInSet: int
    def getNumSymbsInSet(self):
        n = len(self.depSymbs)
        return n
        
    # defFuncs: str
    def defFuncs(self):
        st = self.defFuncMain() + self.defFuncPred() + self.defFuncSet()
        return st
    
    # defFuncMain: str
    def defFuncMain(self):
        S = self.indepSymbs
        
        funcPred = self.getNameFuncPred()
        argsQuant = applyRecur(funcPred, S),
        
        funcQuant = self.getNameFuncQuant()
        expr = applyRecur(funcQuant, argsQuant)
        
        funcMain = self.getNameFuncMain()        
        st = defFuncRecur(funcMain, S, expr, moreSpace = True)
    
        n = self.getNumSymbsInSet()
        if n > libMaxSymbsInSet and not self.testIfDefedFuncQuantDeeper():
            st = self.defFuncQuantDeeper() + st
        
        return st
        
    # defFuncPred: str
    def defFuncPred(self):
        func = self.getNameFuncPred()
        args = self.indepSymbs
        
        letCls = self.getPredLetClauses()
        letCls = writeLetClauses(letCls)        
        inCl = self.qPred
        inCl = writeInClause(inCl)
        expr = letCls + inCl
        
        st = defFuncRecur(func, args, expr, inds = self.getPredInds(), moreSpace = True)
        return st
    
    # getPredLetClauses: tuple(str) # ('a := S[i1];', 'b := S[i2];',...)
    def getPredLetClauses(self):
        T = ()
        symbs = self.depSymbs
        inds = self.getPredInds()
        for i in range(len(symbs)):
            symb = symbs[i]
            ind = inds[i],
            expr = appendInds(self.getNameFuncSet(), ind)
            T += defFuncRecur(symb, (), expr),
        return T
    
    # getPredInds: tuple(str) # ('i1', 'i2',...)
    def getPredInds(self):
        t = ()
        for i in range(self.getNumSymbsInSet()):
            ind = 'i' + str(i + 1)
            t += ind,
        return t
        
    # defFuncSet: str
    def defFuncSet(self):
        func = self.getNameFuncSet()
        args = self.indepSymbs
        expr = self.qSet
        st = defFuncRecur(func, args, expr, moreSpace = True)
        global auxFuncNum
        auxFuncNum += 1
        return st
        
    # testIfDefedFuncQuantDeeper: bool
    def testIfDefedFuncQuantDeeper(self):
        n = self.getNumSymbsInSet()
        b = n in defedFuncsQuantDeeper
        return b
            
    # getNameFuncQuant: str
    def getNameFuncQuant(self, isDeeper = True):
        if self.isExist:
            func = 'someSet'
        else: # universal
            func = 'allSet'
        if isDeeper:
            n = self.getNumSymbsInSet()
            func += '_' + str(n) + '_'
        return func
        
    # defFuncQuantDeeper: str
    def defFuncQuantDeeper(self):
        n = self.getNumSymbsInSet()
        global defedFuncsQuantDeeper
        defedFuncsQuantDeeper |= {n}
        
        func = self.getNameFuncQuant()
        arg = 'vs'
        args = arg + '(' + str(n) + ')',
        
        func2 = self.getNameFuncQuant(isDeeper = False)
        args2 = arg,
        for i in range(n):
            args2 = applyRecur(func2, args2),
        expr = args2[0]
        
        st = defFuncRecur(func, args, expr, moreSpace = True)
        return st
    
    # getNameFuncMain: str
    def getNameFuncMain(self, isOfNext = False):
        st = self.appendAux('MAIN', isOfNext)
        return st
        
    # getNameFuncPred: str
    def getNameFuncPred(self):
        st = self.appendAux('PRED')
        return st
        
    # getNameFuncSet: str
    def getNameFuncSet(self):
        st = self.appendAux('SET')
        return st
        
    # appendAux: str -> str
    def appendAux(self, extraAppend, isOfNext = False):
        num = auxFuncNum
        if isOfNext:
            num += 1
        st = 'AUX_' + str(num) + '_' + extraAppend + '_'
        return st
    
########## ########## ########## ########## ########## ########## 
''' 
testing
'''

q = QuantInfo()
q.isExist = False
q.indepSymbs = ('z', 'x')
q.depSymbs = ('y', 'y2')
q.qSet = 'se([])'
q.qPred = 'z = y2'

# test(q.defFuncs())

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
