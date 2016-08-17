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
    for func in defedConsts:
        func = applyRecur(None, 'pp', (func,), isInLib = True)
        st += func + '\n'
    st += '\n(pp means PrettyPrint)'
    st = addBlockComment(st)
    st = '\n\n' + st
    return st

########## ########## ########## ########## ########## ########## 
'''
python global variables
'''

defedConsts = () # ('c1', 'c2',...)
auxFuncNum = 0
auxFuncDefs = '' # 'aux1 := 1; aux2 := 2;...'

defedFuncsQuantDeeper = set() # {2, 4,...}
    
########## ########## ########## ########## ########## ########## 
'''
unparse an LED parsetree into a string which represents a SL program

note: tree := tuple/str
'''

# unparseTop: list -> str
def unparseTop(L):
    T = listToTree(L)
    T = transformTree(T)
    
    u = UnpInfo()
    st = unparseRecur(u, T)
    
    st = importLib + st
    if auxFuncDefs != '':
        st += addBlockComment('AUXILIARY FUNCTIONS') + '\n\n' + auxFuncDefs
    st = markBeginEnd(st)
    st += printTest()
    return st
    
# transformTree: tree -> tree
def transformTree(T):
    if type(T) == str:
        return T
    if T[0] in quantOps:
        T2 = expandSymsInS(T)
        return T2
    else:
        return recurTuple(transformTree, T)

########## ########## ########## ########## ########## ########## 
'''
recursion iterators
'''

# unparseRecur: UnpInfo * tree -> str
def unparseRecur(u, T):
    if type(T) == str:
        return T
    if T[0] in lexemes:
        return unparseLexemes(u, T)
    if T[0] == 'set':
        return unparseSet(u, T)
    if T[0] == 'nrval':
        st = applyRecur(u, 'iv', T[1:], isInLib = True)
        return st
    if T[0] == 'tup':
        return unparseTuple(u, T)
    if T[0] in aggrOps:
        return unparseAggr(u, T)
    if T[0] in quantOps:
        return unparseQuant(u, T)
    if T[0] in libOps:
        return unparseLibOps(u, T)
    if T[0] == 'constDef':
        func = unparseRecur(u, T[1])
        global defedConsts
        defedConsts += func,
        st = defRecur(u, func, (), T[2], moreSpace = True)
        return st
    else:
        return recurStr(unparseRecur, u, T)

# defRecur: UnpInfo * tree * tuple(tree) * tree -> str
def defRecur(u, func, args, expr, inds = (), moreSpace = False):
    expr = unparseRecur(u, expr)
    st = applyRecur(u, func, args, inds = inds) + ' := ' + expr + ';\n'
    if moreSpace:
        st += '\n'
    return st

# applyRecur: UnpInfo * tree * tuple(tree) -> str
def applyRecur(u, func, args, isInLib = False, argsAreBracketed = False, inds = ()):
    func = unparseRecur(u, func)
    if isInLib:
        func = prependLib(func)
    st = func
    if args != ():
        st2 = unparseRecur(u, args[0])
        for arg in args[1:]:
            st2 += ', ' + unparseRecur(u, arg)
        if argsAreBracketed:
            st2 = addBrackets(st2)
        st += '(' + st2 + ')'
    st = appendInds(st, inds)
    return st

########## ########## ########## ########## ########## ########## 
'''
recursion helpers
'''

# recurStr: function * UnpInfo * tree -> str
def recurStr(F, u, T):
    st = ''
    for t in T[1:]:
        st += F(u, t)
    return st
    
# recurTuple: function * tree -> tree
def recurTuple(F, T):
    T2 = T[:1]
    for t in T[1:]:
        T2 += F(t),
    return T2
    
########## ########## ########## ########## ########## ########## 
'''
information for unparsing
'''

class UnpInfo:
    indepSymbs = () # ('i1',...)
    depSymbs = () # ('d1',...)  
    
    # getNumDepSymbs: int
    def getNumDepSymbs(self):
        n = len(self.depSymbs)
        return n
        
    # getDepSymbsFromAnotherInst: UnpInfo -> void
    def getDepSymbsFromAnotherInst(self, u):
        self.depSymbs = u.indepSymbs + u.depSymbs
        
    # getAnotherInst: UnpInfo
    def getAnotherInst(self, isAggr = False, isOfNext = False):
        if isAggr:
            u.makeAggr()
        symbs = self.indepSymbs
        if isOfNext:
            symbs = self.getNextIndepSymbs()
        u = UnpInfo()
        u.indepSymbs = symbs
        return u
        
    # getNextIndepSymbs: tuple(str)
    def getNextIndepSymbs(self):
        T = self.indepSymbs + self.depSymbs
        return T
        
    # appendAux: str -> str
    def appendAux(self, extraAppend, isOfNext = False):
        num = auxFuncNum
        if isOfNext:
            num += 1
        st = 'AUX_' + str(num) + '_' + extraAppend + '_'
        return st

    '''
    set fields specific to aggregation
    
    makeAggr: bool -> void
    '''
    def makeAggr(self, isTerm = False, isConj = None):
        self.isTerm = isTerm
        self.aTerm = '' # x + y
        self.isConj = isConj
        self.aPred = '' # 'x < y'
        self.aSet = '' # '{x..2*x}'
        
    # aDefCondInst: UnpInfo -> void
    def aDefCondInst(condInst):
        self.condInst = condInst
        
    # aDefSubInsts: UnpInfo * UnpInfo -> void
    def aDefSubInsts(u1, u2):        
        self.subInst1 = u1
        self.subInst2 = u2
        
    # aDefFunc: str
    def aDefFunc(self):
        global auxFuncNum
        auxFuncNum += 1
        func = self.appendAux('AGGR')
        args = self.indepSymbs
        self.aFunc = applyRecur(self, func, args)
        if self.isTerm:
            self.aDefFuncTerm()
        elif self.aPred != '':
            self.aDefFuncPred()
        elif self.aSet != '':
            self.aDefFuncSet()
        elif self.isConj:
            self.aDefFuncConj()
        else:
            self.aDefFuncDisj()
        return self.aFunc        
    # todo args = self.indepSymbs NOT ()
    # aDefFuncTerm: void
    def aDefFuncTerm(self):
        ind = 'i_'
        letCls = self.aGetTermLetClauses(ind)
        expr = writeLetClauses(letCls)
        
        inCl = self.aTerm
        expr += writeInClause(inCl)
        
        st = defRecur(self, self.aFunc, self.indepSymbs, expr, inds = (ind,))
        global auxFuncDefs
        auxFuncDefs += st
    
    # aGetTermLetClauses: str -> str
    def aGetTermLetClauses(self, ind):
        binding = 'b_'
        expr = applyRecur(self, self.condInst.aFunc, (), inds = (ind,))
        letCls = defRecur(self, binding, (), expr),
        S = self.condInst.depSymbs
        for i in range(len(S)):
            num = str(i + 1)
            expr = applyRecur(self, binding, (), inds = (num,))
            letCls += defRecur(self, S[i], (), expr)
        return letCls
        
    # aDefFuncPred: void
    def aDefFuncPred(self):        
        expr = '[[]] when ' + self.aPred + ' else []'        
        st = defRecur(self, self.aFunc, (), expr)
        global auxFuncDefs
        auxFuncDefs += st
        
    # aDefFuncSet: void
    def aDefFuncSet(self):        
        ind = 'i_'
        expr = self.aSet + addBrackets(ind)
        expr = addBrackets(expr)        
        st = defRecur(self, self.aFunc, (), expr, inds = (ind,))
        global auxFuncDefs
        auxFuncDefs += st
        
    # aDefFuncDisj: void
    def aDefFuncDisj(self):
        func = 'removeDups'
        args = self.subInst1.aFunc + ' ++ ' + self.subInst2.aFunc,
        expr = applyRecur(self, func, args)
        st = defRecur(self, self.aFunc, (), expr)
        global auxFuncDefs
        auxFuncDefs += st
        
    # aDefFuncConj: void
    def aDefFuncConj(self):
        func = 'join'
        args = self.aGetFuncConjDeep(),
        expr = applyRecur(self, func, args)
        st = defRecur(self, self.aFunc, (), expr)
        global auxFuncDefs
        auxFuncDefs += st
        self.aDefFuncConjDeep()
        
    # aDefFuncConjDeep: void
    def aDefFuncConjDeep(self):
        bindings = 'b1_', 'b2_'
        inds = 'i1_', 'i2_'
        letCls = aGetConjLetClauses(bindings, inds)
        expr = writeLetClauses(letCls)
        
        inCl = bindings[0] + ' ++ ' + bindings[1]
        expr += writeInClause(inCl)
        
        st = defRecur(self, self.aGetFuncConjDeep(), (), inds = inds, expr)
        global auxFuncDefs
        auxFuncDefs += st
        
    # aGetConjLetClauses: tuple(str) * tuple(str) -> tuple(str)
    def aGetConjLetClauses(self, bindings, inds):
        funcs = self.subInst1.aFunc, self.subInst2.aFunc
        letCls = ()
        for i in range(2):
            func = funcs[i]
            ind = inds[i]
            expr = applyRecur(self, func, (), inds = (ind,))
            binding = bindings[i]
            letCls += defRecur(self, binding, (), expr),
        
        sts = ()
        S = self.subInst2.indepSymbs
        for i in range(len(S)):
            func = bindings[0]
            num = str(i + 1)
            expr = applyRecur(self, func, (), inds = (num,))
            symb = S[i]
            sts += defRecur(self, symb, (), expr),
            
        sts = letCls[:1] + sts + letCls[1:]
        return sts            
    
    # aGetFuncConjDeep: str
    def aGetFuncConjDeep(self):
        func = self.appendAux('DEEP')
        args = self.indepSymbs
        st = applyRecur(self, func, args)
        return st
        
    '''
    set fields specific to quantification
    
    makeQuant: bool -> void
    '''
    def makeQuant(self, isUniv):
        self.isUniv = isUniv
        self.qSet = '' # '{1, 2,...}'
        self.qPred = '' # 'all y in S. y > x'
    
    # qDefFuncs: str
    def qDefFuncs(self):
        st = self.qDefFuncMain() + self.qDefFuncPred() + self.qDefFuncSet()
        return st
    
    # qDefFuncMain: str
    def qDefFuncMain(self):
        global auxFuncNum
        auxFuncNum += 1
        st = 'quantification ' + str(auxFuncNum)
        st = addBlockComment(st)
        st += '\n\n'
        
        S = self.indepSymbs
        
        funcPred = self.qGetFuncPred()
        argsQuant = applyRecur(self, funcPred, S),
        
        funcQuant = self.qGetFuncQuant()
        expr = applyRecur(self, funcQuant, argsQuant)
        
        funcMain = self.qGetFuncMain() 
        st += defRecur(self, funcMain, S, expr, moreSpace = True)
        if self.qTestIfFuncQuantDeeper() and not self.qTestIfFuncQuantDeeperDefed():
            global auxFuncDefs
            auxFuncDefs += self.qDefFuncQuantDeeper()
        
        return st
        
    # qDefFuncPred: str
    def qDefFuncPred(self):
        func = self.qGetFuncPred()
        args = self.indepSymbs
        
        letCls = self.qGetPredLetClauses()
        letCls = writeLetClauses(letCls)
        
        func2 = self.qPred
        args2 = self.getNextIndepSymbs()
        if checkIfFuncIsAux(func2):
            func2 = applyRecur(self, func2, args2)
        inCl = writeInClause(func2)
        expr = letCls + inCl
        
        inds = self.qGetPredInds()
        st = defRecur(self, func, args, expr, inds = inds, moreSpace = True)
        return st
    
    # qGetPredLetClauses: tuple(str) # ('a := S(x)[i1_];', 'b := S(x)[i2_];',...)
    def qGetPredLetClauses(self):
        T = ()
        symbs = self.depSymbs
        inds = self.qGetPredInds()
        for i in range(len(symbs)):
            symb = symbs[i]
            
            func = self.qGetFuncSet()
            args = self.indepSymbs
            func = applyRecur(self, func, args)            
            ind = inds[i],
            expr = appendInds(func, ind)
            
            T += defRecur(self, symb, (), expr),
        return T
    
    # qGetPredInds: tuple(str) # ('i1_', 'i2_',...)
    def qGetPredInds(self):
        t = ()
        for i in range(self.getNumDepSymbs()):
            ind = 'i' + str(i + 1) + '_'
            t += ind,
        return t
        
    # qDefFuncSet: str
    def qDefFuncSet(self):
        func = self.qGetFuncSet()
        args = self.indepSymbs
        expr = applyRecur(self, 'valToSet', (self.qSet,))
        st = defRecur(self, func, args, expr, moreSpace = True)
        return st
        
    # qTestIfFuncQuantDeeper: bool
    def qTestIfFuncQuantDeeper(self):
        n = self.getNumDepSymbs()
        b = n > libMaxSymbsInSet
        return b
        
    # qTestIfFuncQuantDeeperDefed: bool
    def qTestIfFuncQuantDeeperDefed(self):
        n = self.getNumDepSymbs()
        b = n in defedFuncsQuantDeeper
        return b
            
    # qGetFuncQuant: str
    def qGetFuncQuant(self, baseOverride = False):
        if self.isUniv:
            func = 'someSet'
        else: # universal
            func = 'allSet'
        if self.qTestIfFuncQuantDeeper() and not baseOverride:
            n = self.getNumDepSymbs()
            func += '_' + str(n) + '_'
        return func
        
    # qDefFuncQuantDeeper: str
    def qDefFuncQuantDeeper(self):
        n = self.getNumDepSymbs()
        global defedFuncsQuantDeeper
        defedFuncsQuantDeeper |= {n}
        
        func = self.qGetFuncQuant()
        arg = 'vs'
        args = arg + '(' + str(n) + ')',
        
        func2 = self.qGetFuncQuant(baseOverride = True)
        args2 = arg,
        for i in range(n):
            args2 = applyRecur(self, func2, args2),
        expr = args2[0]
        
        st = defRecur(self, func, args, expr, moreSpace = True)
        return st
    
    # qGetFuncMain: str
    def qGetFuncMain(self, isOfNext = False):
        st = self.appendAux('A', isOfNext = isOfNext)
        return st
        
    # qGetFuncPred: str
    def qGetFuncPred(self):
        st = self.appendAux('B')
        return st
        
    # qGetFuncSet: str
    def qGetFuncSet(self):
        st = self.appendAux('C')
        return st    
      
def t():
    u = UnpInfo()
    u.makeAggr(True)
    u.indepSymbs = 'x', 'y'
    # u.aPred = 'x < y'
    # u.aSet = 'x...y'
    u.subInst1.aFunc = 'f(x)'
    u.subInst2.aFunc = 'g(x, y)'
    st = u.aDefFunc()
    test(st)
    test(auxFuncDefs)
    
########## ########## ########## ########## ########## ########## 
'''
unparse collections
'''

# unparseTuple: UnpInfo * tree -> str
def unparseTuple(u, T):
    func = 'tu'
    terms = T[1]
    st = applyRecur(u, func, terms[1:], isInLib = True, argsAreBracketed = True)
    return st
    
# unparseSet: UnpInfo * tree -> str
def unparseSet(u, T):
    func = 'se'
    if len(T) == 1: # empty set
        args = '',
    else:
        terms = T[1]
        args = terms[1:]
    st = applyRecur(u, func, args, isInLib = True, argsAreBracketed = True)
    return st

########## ########## ########## ########## ########## ########## 
'''
unparse library operations
'''

equalityOps = {'eq', 'uneq'}
relationalOps = {'less', 'greater', 'lessEq', 'greaterEq'}
arOps = {'add', 'bMns', 'uMns', 'mult', 'div', 'flr', 'clng', 'md', 'exp'}
setOps = {'setMem', 'sbset', 'unn', 'nrsec', 'diff', 'cross', 'powSet'}
pipeOp = {'pip'}
boolOps = {'equiv', 'impl', 'disj', 'conj', 'neg'}
tupleOps = {'tuConc', 'tuIn', 'tuSl'}
libOps = equalityOps | relationalOps | arOps | setOps | pipeOp | boolOps | tupleOps

# unparseLibOps: UnpInfo * tree -> str
def unparseLibOps(u, T):
    st = applyRecur(u, T[0], T[1:], isInLib = True)
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
    
# addParentheses: str -> str
def addParentheses(st):
    st = '(' + st + ')'
    return st
    
# addBlockComment: str -> str
def addBlockComment(st):
    st = '/** ' + st + ' */'
    return st
    
# checkIfFuncIsAux: str -> bool
def checkIfFuncIsAux(st):
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
aggregation
'''

aggrOps = {'setCompr', 'aggrUnn', 'aggrNrsec', 'sum', 'prod'}

unparseAggr: UnpInfo * tree -> str
def unparseAggr(u, T):
    if T[0] in aggrOps:
        u.makeAggr(isTerm = True)
        
        u2 = u.getAnotherInst(isAggr = True)
        unparseAggr(u2, T[2])
        
        u.getDepSymbsFromAnotherInst(u2)
        st = u.aDefFunc()
        return st
    if isGround(u, T):
        u.makeAggr()
        u.aPred = unparseRecur(u, T)
        st = u.aDefFunc()
        return st
    if T[0] == 'setMem':
        u.makeAggr()
        u.depSymbs = unparseRecur(u, T[1]),
        u.aSet = unparseRecur(u, T[2])
        st = u.aDefFunc()
        return st
    if T[0] in {'conj', 'disj'}:
        u.makeAggr(isConj = T[0] == 'conj')
        
        u1 = u.getAnotherInst(isAggr = True)
        unparseAggr(u1, T[1])
        
        u2 = u1.getAnotherInst(isAggr = True, isOfNext = u.isConj)
        unparseAggr(u2, T[2])
        
        u.getDepSymbsFromAnotherInst(u2)
        u.aDefSubInsts(u1, u2)
        
        st = u.aDefFunc()
        return st
    else:
        return recurStr(unparseAggr, u, T)

# isGround: UnpInfo * tree -> bool
def isGround(u, T):
    return not depSymbFound(u, T)

# depSymbFound: UnpInfo * tree -> bool
def depSymbFound(u, T):
    if type(T) == str:
        return False
    if T[0] == 'userSVC':
        if isDepSymb(u, T[1][1]):
            return True
        return False
    else:
        for t in T[1:]:
            if depSymbFound(u, t):
                return True
        return False
        
# isDepSymb: UnpInfo * str -> bool
def isDepSymb(u, id):
    return id not in u.indepSymbs + defedConsts

########## ########## ########## ########## ########## ########## 
'''
quantification
'''

quantOps = {'exist', 'univ'}
libMaxSymbsInSet = 1

# unparseQuant: UnpInfo * tree -> str
def unparseQuant(u, T):
    u.makeQuant(isUniv = T[0] == 'univ')
        
    symsInS = T[1]
    u.depSymbs = getDepSymbsFromSyms(symsInS[1])
    
    u2 = u.getAnotherInst()
    u.qSet = unparseRecur(u2, symsInS[2])
    
    u3 = u.getAnotherInst(isOfNext = True)
    u.qPred = unparseRecur(u3, T[2])
    
    global auxFuncDefs
    qFuncs = u.qDefFuncs()
    auxFuncDefs += qFuncs
    
    func = u.qGetFuncMain()
    args = u.indepSymbs
    st = applyRecur(u, func, args)
    
    return st
    
# expandSymsInS: tree -> tree
def expandSymsInS(T):
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
    T2 = recurTuple(transformTree, T2)
    return T2
    
# getDepSymbsFromSyms: tree -> tuple(str)
def getDepSymbsFromSyms(T):
    syms = T[1:]
    symbs = ()
    for sym in syms:
        symb = sym[1][1]
        symbs += symb,
    return symbs

########## ########## ########## ########## ########## ########## 
'''
unparse lexemes
'''

lexemesDoublyQuoted = {'numl': 'nu', 'atom': 'at'}
lexemes = unionDicts((lexemesDoublyQuoted, {'truth': 'tr'}))

# unparseLexemes: UnpInfo * tree -> str
def unparseLexemes(u, T):
    lex = T[0]
    func = lexemes[lex]
    arg = T[1]
    if lex in lexemesDoublyQuoted:
        arg = addDoubleQuotes(arg)
    args = arg,
    st = applyRecur(u, func, args, isInLib = True)
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
