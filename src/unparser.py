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
    st = 'Copy/paste the block below into SequenceL interpreter to test:\n\n'
    for func in testConsts:
        func = applyRecur('pp', (func,), isInLib = True)
        st += func + '\n'
    st += '\n(pp means PrettyPrint)'
    st = addBlockComment(st)
    st = '\n\n' + st
    return st

########## ########## ########## ########## ########## ########## 
'''
python global variables
'''

testConsts = () # ('c1', 'c2',...)
defedFuncsQuantDeeper = set() # {2, 4,...}
auxFuncNum = 0
auxFuncs = '' # 'aux1 := 1; aux2 := 2;...'
    
########## ########## ########## ########## ########## ########## 
'''
unparse an LED parsetree into a string which represents a SL program

note: tree := tuple/str
'''

# unparseTop: list -> str
def unparseTop(L):
    T = listToTree(L)
    T = transformTree(T)
    st = unparseRecur(T)
    st = importLib + st
    st += addBlockComment('AUXILIARY FUNCTIONS') + '\n\n' + auxFuncs
    st = markBeginEnd(st)
    st += printTest()
    return st
    
# transformTree: tree -> tree
def transformTree(T):
    if type(T) == str:
        return T
    if T[0] in quantLabels:
        T2 = expandSymbolsInSet(T)
        return T2
    else:
        return recurTuple(T, transformTree)

# unparseRecur: tree -> str
def unparseRecur(T, quantIndepSymbs = ()):
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
        return unparseQuant(T, quantIndepSymbs = quantIndepSymbs)
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
recursion
'''

# recurStr: function * tuple(tree) -> str
def recurStr(func, args):
    st = ''
    for arg in args:
        st += func(arg)
    return st
    
# recurTuple: tree * function -> tree
def recurTuple(T, func):
    T2 = T[:1]
    for t in T[1:]:
        T2 += func(t),
    return T2
    
########## ########## ########## ########## ########## ########## 
'''
writing SequenceL functions
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
            st2 = addBrackets(st2)
        st += '(' + st2 + ')'
    st = appendInds(st, inds)
    return st

########## ########## ########## ########## ########## ########## 
'''
SequenceL helpers
'''
    
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
    if T != ():
        st2 = T[0]
        for t in T[1:]:
            st2 += ', ' + t
        st2 = addBrackets(st2)
        st += st2
    return st
    
# addBrackets: str -> str
def addBrackets(st):
    st = '[' + st + ']'
    return st
    
# addDoubleQuotes: str -> str
def addDoubleQuotes(st):
    st = '"' + st + '"'
    return st
    
# addBlockComment: str -> str
def addBlockComment(st):
    st = '/** ' + st + ' */'
    return st
    
# testIfFuncAux: str -> bool
def testIfFuncAux(st):
    b = st[-1] == '_'
    return b
    
########## ########## ########## ########## ########## ########## 
'''
miscellaneous
'''
    
# unionDicts: tuple(dict) -> dict
def unionDicts(ds):
    D = {}
    for d in ds:
        D.update(d)
    return D
    
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

quantLabels = {'exist', 'univ'}
libMaxSymbsInSet = 1

# unparseQuant: tree -> str
def unparseQuant(T, quantIndepSymbs = ()):
    q = QuantInfo()
    if T[0] == 'univ':
        q.isExist = False
        
    currentIndepSymbs = quantIndepSymbs
    q.indepSymbs = currentIndepSymbs
    
    symsInS = T[1]
    currentDepSymbs = getDepSymbs(symsInS[1])
    q.depSymbs = currentDepSymbs
    q.qSet = unparseRecur(symsInS[2], quantIndepSymbs = currentIndepSymbs)
    
    nextIndepSymbs = currentIndepSymbs + currentDepSymbs
    q.qPred = unparseRecur(T[2], quantIndepSymbs = nextIndepSymbs)
    
    global auxFuncs
    qFuncs = q.defFuncs()
    auxFuncs = qFuncs + auxFuncs
    
    st = q.getFuncMain()
    return st
    
# expandSymbolsInSet: tree -> tree
def expandSymbolsInSet(T):
    quantifier = T[0]
    pred = T[2]
    
    symsInS = T[1]
    syms = symsInS[1][1:][::-1]
    S = symsInS[2]
    symb = syms[0]
    symb = 'symbs', symb
    symbInS = 'symbInS', symb, S
    T2 = quantifier, symbInS, pred
    for sym in syms[1:]:
        symb = sym
        symb = 'symbs', symb
        symbInS = 'symbInS', symb, S
        T2 = quantifier, symbInS, T2
    return T2
    
# getDepSymbs: tree -> tuple(str)
def getDepSymbs(T):
    syms = T[1:]
    symbs = ()
    for sym in syms:
        symb = sym[1][1]
        symbs += symb,
    return symbs

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
        global auxFuncNum
        auxFuncNum += 1
        st = 'quantification ' + str(auxFuncNum)
        st = addBlockComment(st)
        st += '\n\n'
        
        S = self.indepSymbs
        
        funcPred = self.getFuncPred()
        argsQuant = applyRecur(funcPred, S),
        
        funcQuant = self.getFuncQuant()
        expr = applyRecur(funcQuant, argsQuant)
        
        funcMain = self.getFuncMain() 
        st += defFuncRecur(funcMain, S, expr, moreSpace = True)
        if self.testIfFuncQuantDeeper() and not self.testIfDefedFuncQuantDeeper():
            global auxFuncs
            auxFuncs += self.defFuncQuantDeeper()
        
        return st
        
    # defFuncPred: str
    def defFuncPred(self):
        func = self.getFuncPred()
        args = self.indepSymbs
        
        letCls = self.getPredLetClauses()
        letCls = writeLetClauses(letCls)
        
        func2 = self.qPred
        args2 = self.getIndepSymbsNext()
        if testIfFuncAux(func2):
            func2 = applyRecur(func2, args2)
        inCl = writeInClause(func2)
        expr = letCls + inCl
        
        st = defFuncRecur(func, args, expr, inds = self.getPredInds(), moreSpace = True)
        return st
    
    # getPredLetClauses: tuple(str) # ('a := S(x)[i1];', 'b := S(x)[i2];',...)
    def getPredLetClauses(self):
        T = ()
        symbs = self.depSymbs
        inds = self.getPredInds()
        for i in range(len(symbs)):
            symb = symbs[i]
            
            func = self.getFuncSet()
            args = self.indepSymbs
            func = applyRecur(func, args)            
            ind = inds[i],
            expr = appendInds(func, ind)
            
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
        func = self.getFuncSet()
        args = self.indepSymbs
        expr = applyRecur('valToSet', (self.qSet,))
        st = defFuncRecur(func, args, expr, moreSpace = True)
        return st
        
    # testIfFuncQuantDeeper: bool
    def testIfFuncQuantDeeper(self):
        n = self.getNumSymbsInSet()
        b = n > libMaxSymbsInSet
        return b
        
    # testIfDefedFuncQuantDeeper: bool
    def testIfDefedFuncQuantDeeper(self):
        n = self.getNumSymbsInSet()
        b = n in defedFuncsQuantDeeper
        return b
            
    # getFuncQuant: str
    def getFuncQuant(self, baseOverride = False):
        if self.isExist:
            func = 'someSet'
        else: # universal
            func = 'allSet'
        if self.testIfFuncQuantDeeper() and not baseOverride:
            n = self.getNumSymbsInSet()
            func += '_' + str(n) + '_'
        return func
        
    # defFuncQuantDeeper: str
    def defFuncQuantDeeper(self):
        n = self.getNumSymbsInSet()
        global defedFuncsQuantDeeper
        defedFuncsQuantDeeper |= {n}
        
        func = self.getFuncQuant()
        arg = 'vs'
        args = arg + '(' + str(n) + ')',
        
        func2 = self.getFuncQuant(baseOverride = True)
        args2 = arg,
        for i in range(n):
            args2 = applyRecur(func2, args2),
        expr = args2[0]
        
        st = defFuncRecur(func, args, expr, moreSpace = True)
        return st
    
    # getFuncMain: str
    def getFuncMain(self, isOfNext = False):
        st = self.appendAux('A', isOfNext = isOfNext)
        return st
        
    # getFuncPred: str
    def getFuncPred(self):
        st = self.appendAux('B')
        return st
        
    # getFuncSet: str
    def getFuncSet(self):
        st = self.appendAux('C')
        return st
        
    # appendAux: str -> str
    def appendAux(self, extraAppend, isOfNext = False):
        num = auxFuncNum
        if isOfNext:
            num += 1
        st = 'AUX_' + str(num) + '_' + extraAppend + '_'
        return st
        
    # getIndepSymbsNext: tuple(str)
    def getIndepSymbsNext(self):
        T = self.indepSymbs + self.depSymbs
        return T

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
