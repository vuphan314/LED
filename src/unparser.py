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
SL testing
'''

# printTest: str
def printTest():
    st = 'Copy/paste the block below into SequenceL interpreter to test:\n\n'
    for const in defedConsts:
        func = applyRecur(None, 'pp', (const,))
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
    if T[0] == 'tup':
        return unparseTuple(u, T)
    if T[0] == 'set':
        return unparseSet(u, T)
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
        st += addParentheses(st2)
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

    # getNumIndepSymbs: int
    def getNumIndepSymbs(self):
        n = len(self.indepSymbs)
        return n

    # getNumDepSymbs: int
    def getNumDepSymbs(self):
        n = len(self.depSymbs)
        return n

    # getSymbs: tuple(str)
    def getSymbs(self):
        T = self.indepSymbs + self.depSymbs
        return T

    # assignDepSymbsFromSubInst: UnpInfo -> void
    def assignDepSymbsFromSubInst(self, u):
        for s in u.getSymbs():
            if s not in self.indepSymbs:
                self.depSymbs += s,

    # getOtherInst: UnpInfo
    def getOtherInst(self, isNext = False):
        if isNext:
            symbs = self.getNextIndepSymbs()
        else:
            symbs = self.indepSymbs
        u = UnpInfo()
        u.indepSymbs = symbs
        return u

    # getNextIndepSymbs: tuple(str)
    def getNextIndepSymbs(self):
        T = self.getSymbs()
        return T

    # appendToAux: str -> str
    def appendToAux(self, extraAppend, isNext = False):
        num = auxFuncNum
        if isNext:
            num += 1
        st = 'AUX_' + str(num) + '_' + extraAppend + '_'
        return st

    '''
    fields specific to aggregation
    '''
    # must assign immediately when instantiating
    aCateg = None # str
    # must assign later by calling function aDefFunc
    aFunc = None # 'AUX_3_(x, y)'

    aVal = ''
    '''
    pred:   'x < y'
    eq:     'x + 1'
    set:    'x...2*x'
    '''

    # conj/disj
    subInst1 = None # UnpInfo
    subInst2 = None # UnpInfo

    # term
    aTerm = None # 'x + y'
    condInst = None # UnpInfo

    # aCheckCateg: void
    def aCheckCateg(self):
        if self.aCateg not in aggregateCategories:
            err('invalid aggregate category')

    # aDefFunc: str
    def aDefFunc(self):
        global auxFuncNum
        auxFuncNum += 1

        func = self.appendToAux('AGGR')
        args = self.indepSymbs
        self.aFunc = applyRecur(self, func, args)

        self.aCheckCateg()
        if self.aCateg == 'isPred':
            self.aDefFuncPred()
        if self.aCateg == 'isEq':
            self.aDefFuncEq()
        elif self.aCateg == 'isSet':
            self.aDefFuncSet()
        elif self.aCateg == 'isConj':
            self.aDefFuncConj()
        elif self.aCateg == 'isDisj':
            self.aDefFuncDisj()
        else:
            self.aDefFuncTerm()
        return self.aFunc

    # aDefFuncPred: void
    def aDefFuncPred(self):
        whenCond = applyRecur(self, 'valToTrth', (self.aVal,))
        expr = '[[]] when ' + whenCond + ' else []'
        st = defRecur(self, self.aFunc, (), expr, moreSpace = True)
        global auxFuncDefs
        auxFuncDefs += st

    # aDefFuncEq: void
    def aDefFuncEq(self):
        expr = addBrackets(self.aVal)
        expr = addBrackets(expr)
        st = defRecur(self, self.aFunc, (), expr, moreSpace = True)
        global auxFuncDefs
        auxFuncDefs += st        

    # aDefFuncSet: void
    def aDefFuncSet(self):
        ind = 'i_'
        inds = ind,

        func = 'valToSet'
        args = self.aVal,
        expr = applyRecur(self, func, args, inds = inds)
        expr = addBrackets(expr)

        st = defRecur(self, self.aFunc, (), expr, inds = inds, moreSpace = True)
        global auxFuncDefs
        auxFuncDefs += st

    # aDefFuncDisj: void
    def aDefFuncDisj(self):
        func = 'disjSols'
        args = self.subInst1.aFunc, self.subInst2.aFunc
        expr = applyRecur(self, func, args)
        st = defRecur(self, self.aFunc, (), expr, moreSpace = True)
        global auxFuncDefs
        auxFuncDefs += st

    # aDefFuncConj: void
    def aDefFuncConj(self):
        func = 'join'
        args = self.aGetFuncConjDeep(),
        expr = applyRecur(self, func, args)
        st = defRecur(self, self.aFunc, (), expr, moreSpace = True)
        self.aDefFuncConjDeep()
        global auxFuncDefs
        auxFuncDefs += st

    # aDefFuncConjDeep: void
    def aDefFuncConjDeep(self):
        bindings = 'b1_', 'b2_'
        inds = 'i1_', 'i2_'

        letCls = self.aGetConjLetClauses(bindings, inds)
        expr = writeLetClauses(letCls)

        inCl = applyRecur(self, 'unnBinds', bindings)
        expr += writeInClause(inCl)

        func = self.aGetFuncConjDeep()
        st = defRecur(self, func, (), expr, inds = inds, moreSpace = True)
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
        for i in range(self.subInst2.getNumIndepSymbs()):
            func = bindings[0]
            num = str(i + 1)
            expr = applyRecur(self, func, (), inds = (num,))
            symb = self.subInst2.indepSymbs[i]
            sts += defRecur(self, symb, (), expr),

        sts = letCls[:1] + sts + letCls[1:]
        return sts

    # aGetFuncConjDeep: str
    def aGetFuncConjDeep(self):
        func = self.appendToAux('DEEP')
        args = self.indepSymbs
        st = applyRecur(self, func, args)
        return st

    # aDefFuncTerm: void
    def aDefFuncTerm(self):
        ind = 'i_'

        letCls = self.aGetTermLetClauses(ind)
        expr = writeLetClauses(letCls)

        inCl = self.aTerm
        expr += writeInClause(inCl)

        st = defRecur(self, self.aFunc, (), expr, inds = (ind,), moreSpace = True)
        global auxFuncDefs
        auxFuncDefs += st

    # aGetTermLetClauses: str -> str
    def aGetTermLetClauses(self, ind):
        binding = 'b_'
        expr = applyRecur(self, self.condInst.aFunc, (), inds = (ind,))
        letCls = defRecur(self, binding, (), expr),
        for i in range(self.condInst.getNumDepSymbs()):
            num = str(i + 1)
            expr = applyRecur(self, binding, (), inds = (num,))
            letCls += defRecur(self, self.condInst.depSymbs[i], (), expr),
        return letCls

    '''
    fields specific to quantification
    '''
    isUniv = None # bool
    qSet = '' # '{1, 2,...}'
    qPred = '' # 'all y in S. y > x'

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
        return st

    # qDefFuncPred: str
    def qDefFuncPred(self):
        ind = 'i_'

        letCls = self.qGetPredLetClause(ind),
        letCls = writeLetClauses(letCls)

        func = self.qPred
        if funcIsAux(func):
            args = self.getNextIndepSymbs()
            func = applyRecur(self, func, args)
        inCl = writeInClause(func)
        expr = letCls + inCl

        func2 = self.qGetFuncPred()
        args2 = self.indepSymbs
        st = defRecur(self, func2, args2, expr, inds = (ind,), moreSpace = True)
        return st

    # qGetPredLetClause: str -> str # 'y := S(x)[i_];'
    def qGetPredLetClause(self, ind):
        expr = applyRecur(self, self.qGetFuncSet(), self.indepSymbs, inds = (ind,))
        st = defRecur(self, self.depSymbs[0], (), expr)
        return st

    # qDefFuncSet: str
    def qDefFuncSet(self):
        func = self.qGetFuncSet()
        args = self.indepSymbs
        expr = applyRecur(self, 'valToSet', (self.qSet,))
        st = defRecur(self, func, args, expr, moreSpace = True)
        return st

    # qGetFuncQuant: str
    def qGetFuncQuant(self):
        if self.isUniv:
            func = 'allSet'
        else: # universal
            func = 'someSet'
        return func

    # qGetFuncMain: str
    def qGetFuncMain(self):
        st = self.appendToAux('A')
        return st

    # qGetFuncPred: str
    def qGetFuncPred(self):
        st = self.appendToAux('B')
        return st

    # qGetFuncSet: str
    def qGetFuncSet(self):
        st = self.appendToAux('C')
        return st

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
setOps = {'setMem', 'sbset', 'unn', 'nrsec', 'diff', 'cross', 'powSet', 'iv'}
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

# funcIsAux: str -> bool
def funcIsAux(st):
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
transform complicated parsetree to simple parsetree
'''

aggrOps = {'setCompr', 'aggrUnn', 'aggrNrsec', 'aggrSum', 'aggrProd'}
quantOps = {'exist', 'univ'}

# transformTree: tree -> tree
def transformTree(T):
    if type(T) == str:
        return T
    if T[0] in quantOps:
        T2 = symsInSetToSymbInSet(T)
        return T2
    else:
        return recurTuple(transformTree, T)

# symsInSetToSymbInSet: tree -> tree
def symsInSetToSymbInSet(T):
    quantifier = T[0]
    pred = T[2]

    symsInSet = T[1]
    syms = symsInSet[1][1:][::-1]
    theSet = symsInSet[2]
    symb = syms[0]
    symb = 'symb', symb
    symbInS = 'symbInS', symb, theSet
    T2 = quantifier, symbInS, pred
    for sym in syms[1:]:
        symb = sym
        symb = 'symb', symb
        symbInS = 'symbInSet', symb, theSet
        T2 = quantifier, symbInS, T2
    T2 = recurTuple(transformTree, T2)
    return T2

########## ########## ########## ########## ########## ##########
'''
aggregation
'''

aggregateCategories = {'isPred', 'isEq', 'isSet', 'isConj', 'isDisj', 'isTerm'}

# unparseAggr: UnpInfo * tree -> str
def unparseAggr(u, T):
    if T[0] in aggrOps:
        u.aCateg = 'isTerm'
        if T[0] == 'setCompr':
            term = T[1]
            condition = T[2]
        else:
            term = T[2]
            condition = T[1]

        u.aTerm = unparseRecur(u, term)

        u2 = u.getOtherInst()
        unparseAggr(u2, condition)
        u.condInst = u2
        u.assignDepSymbsFromSubInst(u2)

        args = u.aDefFunc(),
        st = applyRecur(u, T[0], args)
        return st
    if isGround(u, T):
        u.aCateg = 'isPred'
        u.aVal = unparseRecur(u, T)
        st = u.aDefFunc()
        return st
    if T[0] in {'eq', 'setMem'}:
        if T[0] == 'eq':
            u.aCateg = 'isEq'
        else:
            u.aCateg = 'isSet'
        u.depSymbs = unparseRecur(u, T[1]),
        u.aVal = unparseRecur(u, T[2])
        st = u.aDefFunc()
        return st
    if T[0] == 'conj':
        u.aCateg = 'isConj'

        u1 = u.getOtherInst()
        unparseAggr(u1, T[1])
        u.subInst1 = u1

        u2 = u1.getOtherInst(isNext = True)
        unparseAggr(u2, T[2])
        u.subInst2 = u2
        u.assignDepSymbsFromSubInst(u2)

        st = u.aDefFunc()
        return st
    if T[0] == 'disj':
        u.aCateg = 'isDisj'

        u1 = u.getOtherInst()
        unparseAggr(u1, T[1])
        u.subInst1 = u1
        u.assignDepSymbsFromSubInst(u1)

        u2 = u.getOtherInst()
        unparseAggr(u2, T[2])
        u.subInst2 = u2

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

# unparseQuant: UnpInfo * tree -> str
def unparseQuant(u, T):
    u.isUniv = T[0] == 'univ'

    symsInSet = T[1]
    u.depSymbs = getDepSymbsFromSyms(symsInSet[1])

    u2 = u.getOtherInst()
    u.qSet = unparseRecur(u2, symsInSet[2])

    u3 = u.getOtherInst(isNext = True)
    u.qPred = unparseRecur(u3, T[2])

    global auxFuncDefs
    qFuncs = u.qDefFuncs()
    auxFuncDefs += qFuncs

    func = u.qGetFuncMain()
    args = u.indepSymbs
    st = applyRecur(u, func, args)

    return st

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
