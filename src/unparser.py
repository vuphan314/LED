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
    st += '\n(pp: pretty-print)'
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

    u = UnparserInfo()
    st = unparseRecur(u, T)

    st = importLib() + st
    if auxFuncDefs != '':
        st += addBlockComment('AUXILIARY FUNCTIONS') + '\n\n' + auxFuncDefs
    st = markBeginEnd(st)
    st += printTest()
    return st

########## ########## ########## ########## ########## ##########
'''
recursion iterators
'''

# unparseRecur: UnparserInfo * tree -> str
def unparseRecur(u, T):
    if type(T) == str:
        return T
    if T[0] in lexemes:
        return unparseLexemes(u, T)
    if T[0] == 'userFR':
        st = applyRecur(u, T[1], T[2][1:])
        return st
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
    if T[0] in ifLabels:
        return unparseIfClauses(u, T)
    if T[0] in defLabels:
        return unparseDef(u, T)
    else:
        return recurStr(unparseRecur, u, T)

# defRecur: UnparserInfo * tree * tuple(tree) * tree -> str
def defRecur(u, func, args, expr, moreSpace = False, inds = (), letCls = ()):
    head = applyRecur(u, func, args, inds = inds)
    expr = unparseRecur(u, expr)
    if letCls != ():
        letCls = writeLetClauses(letCls)
        inCl = writeInClause(expr)
        expr = letCls + inCl
    body = expr + ';\n'
    if moreSpace:
        body = '\t' + body
        if letCls == ():
            body = '\t' + body
        body = '\n' + body + '\n'
    st = head + ' := ' + body
    return st

# applyRecur: UnparserInfo * tree * tuple(tree) -> str
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

# recurStr: (UnparserInfo * tree -> str) * UnparserInfo * tree -> str
def recurStr(F, u, T):
    st = ''
    for t in T[1:]:
        st += F(u, t)
    return st

# recurTuple: (UnparserInfo * tree -> tuple(str)) * UnparserInfo * tree -> tuple(str)
def recurTuple(F, u, T):
    tu = ()
    for t in T[1:]:
        tu += F(u, t)
    return tu

# recurVoid: (UnparserInfo * tree -> void) * UnparserInfo * tree -> void
def recurVoid(F, u, T):
    for t in T[1:]:
        F(u, t)

# recurTree: (tree -> tree) * tree -> tree
def recurTree(F, T):
    T2 = T[:1]
    for t in T[1:]:
        T2 += F(t),
    return T2

########## ########## ########## ########## ########## ##########
'''
Easel
'''

paramInput = 'I'
paramState = 'S'

# addParams: tree -> tree
def addParams(T):
    if type(T) == str:
        return T
    #todo if T[0] in 
    else:
        return recurTree(addParams, T)

# getIds: str * tuple(str) -> tuple(str)
def getIds(label, ids):
    tu = ()
    for id in ids:
        st = 'id', id
        st = label, st
        tu += st,
    return tu

########## ########## ########## ########## ########## ##########
'''
unparse constant/function/relation definitions
'''

defLabels = {'constDef', 'funDef', 'relDef'}

# unparseDef: UnparserInfo * tree -> str
def unparseDef(u, T):
    func = unparseRecur(u, T[1][1])
    u2 = u.getAnotherInst()

    if T[0] == 'constDef':
        global defedConsts
        defedConsts += func,
    else: # in {'funDef', 'relDef'}
        u2.indepSymbs = getSymbsFromSyms(T[1][2])

    letCls = ()
    if len(T) > 3: # where clauses
        letCls = unparseWhereClauses(u2, T[3][1])

    st = defRecur(u2, func, u2.indepSymbs, T[2], moreSpace = True, letCls = letCls)
    return st

ifLabels = {'tIfBTs', 'tIfBTsO'}

# unparseIfClauses: UnparserInfo * tree -> str
def unparseIfClauses(u, T):
    if T[0] == 'tOther':
        st = unparseRecur(u, T[1])
        st = writeElseClause(st)
        return st
    if T[0] == 'tIfBT':
        st1 = unparseRecur(u, T[1])
        st2 = unparseRecur(u, T[2])
        st2 = applyRecur(u, 'valToTrth', (st2,))
        st = st1 + ' when ' + st2
        return st
    if T[0] == 'tIfBTs':
        st = unparseIfClauses(u, T[1])
        for t in T[2:]:
            st2 = unparseIfClauses(u, t)
            st += writeElseClause(st2)
        return st
    if T[0] == 'tIfBTsO':
        return recurStr(unparseIfClauses, u, T)
    else:
        err('INVALID IF CLAUSES')

# unparseWhereClauses: UnparserInfo * tree -> tuple(str)
def unparseWhereClauses(u, T):
    if T[0] == 'eq':
        st = defRecur(u, T[1], (), T[2])
        return st,
    if T[0] == 'conj':
        return recurTuple(unparseWhereClauses, u, T)
    else:
        err('INVALID WHERE CLAUSES')

########## ########## ########## ########## ########## ##########
'''
information for unparsing
'''

class UnparserInfo:
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

    # getAnotherInst: UnparserInfo
    def getAnotherInst(self, isNext = False):
        if isNext:
            symbs = self.getNextIndepSymbs()
        else:
            symbs = self.indepSymbs
        u = UnparserInfo()
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
    ground: 'x < y'
    eq:     'x + 1'
    set:    'x...2*x'
    '''

    # term
    aTerm = None # 'x + y'
    condInst = None # UnparserInfo

    # conj/disj
    subInst1 = None # UnparserInfo
    subInst2 = None # UnparserInfo

    # aCheckCateg: void
    def aCheckCateg(self):
        if self.aCateg not in aCategs:
            err('INVALID AGGREGATE CATEGORY')

    # aDefFunc: str
    def aDefFunc(self):
        global auxFuncNum
        auxFuncNum += 1

        func = self.appendToAux('AGGR')
        args = self.indepSymbs
        self.aFunc = applyRecur(self, func, args)

        self.aCheckCateg()
        if self.aCateg == 'isAggr':
            st = self.aDefFuncAggr()
        elif self.aCateg in aCategsLib:
            st = self.aDefFuncLib()
        else: # 'solConj'
            st = self.aDefFuncConj()
        global auxFuncDefs
        auxFuncDefs += st

        return self.aFunc

    # aDefFuncAggr: str
    def aDefFuncAggr(self):
        ind = 'i_'

        letCls = self.aGetAggrLetClauses(ind)
        expr = writeLetClauses(letCls)

        inCl = self.aTerm
        expr += writeInClause(inCl)

        st = defRecur(self, self.aFunc, (), expr, inds = (ind,), moreSpace = True)
        return st

    # aGetAggrLetClauses: str -> str
    def aGetAggrLetClauses(self, ind):
        binding = 'b_'
        expr = applyRecur(self, self.condInst.aFunc, (), inds = (ind,))
        letCls = defRecur(self, binding, (), expr),
        for i in range(self.getNumDepSymbs()):
            num = str(i + 1)
            expr = applyRecur(self, binding, (), inds = (num,))
            letCls += defRecur(self, self.depSymbs[i], (), expr),
        return letCls

    # aDefFuncLib: str
    def aDefFuncLib(self):
        expr = applyRecur(self, self.aCateg, self.aGetArgsLib())
        st = defRecur(self, self.aFunc, (), expr, moreSpace = True)
        return st

    # aGetArgsLib: tuple(str)
    def aGetArgsLib(self):
        if self.aCateg == 'solDisj':
            return self.subInst1.aFunc, self.subInst2.aFunc
        if self.aCateg in aCategsLib:
            return self.aVal,
        else:
            err('NOT IN LIBRARY')

    # aDefFuncConj: str
    def aDefFuncConj(self):
        func = 'join'
        args = self.aGetFuncConjDeep(),
        expr = applyRecur(self, func, args)
        st = defRecur(self, self.aFunc, (), expr, moreSpace = True)
        st = self.aDefFuncConjDeep() + st
        return st

    # aDefFuncConjDeep: str
    def aDefFuncConjDeep(self):
        bindings = 'b1_', 'b2_'
        inds = 'i1_', 'i2_'

        letCls = self.aGetConjLetClauses(bindings, inds)
        expr = writeLetClauses(letCls)

        inCl = applyRecur(self, 'unnBinds', bindings)
        expr += writeInClause(inCl)

        func = self.aGetFuncConjDeep()
        st = defRecur(self, func, (), expr, inds = inds, moreSpace = True)
        return st

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
        for i in range(self.subInst1.getNumDepSymbs()):
            symb = self.subInst1.depSymbs[i]
            func = bindings[0]
            num = str(i + 1)
            expr = applyRecur(self, func, (), inds = (num,))
            sts += defRecur(self, symb, (), expr),

        sts = letCls[:1] + sts + letCls[1:]
        return sts

    # aGetFuncConjDeep: str
    def aGetFuncConjDeep(self):
        func = self.appendToAux('DEEP')
        args = self.indepSymbs
        st = applyRecur(self, func, args)
        return st

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

# unparseTuple: UnparserInfo * tree -> str
def unparseTuple(u, T):
    func = 'tu'
    terms = T[1]
    st = applyRecur(u, func, terms[1:], isInLib = True, argsAreBracketed = True)
    return st

# unparseSet: UnparserInfo * tree -> str
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
boolOps = {'equiv', 'impl', 'disj', 'conj', 'neg'}
overloadedOps = {'pipesOp', 'plusOp', 'starOp'}
arOps = {'bMns', 'uMns', 'div', 'flr', 'clng', 'md', 'exp'}
setOps = {'setMem', 'sbset', 'unn', 'nrsec', 'diff', 'powSet', 'iv'}
tupleOps = {'tuIn', 'tuSl'}

libOps = \
    overloadedOps | equalityOps | relationalOps | arOps | setOps | boolOps | tupleOps

# unparseLibOps: UnparserInfo * tree -> str
def unparseLibOps(u, T):
    st = applyRecur(u, T[0], T[1:], isInLib = True)
    return st

########## ########## ########## ########## ########## ##########
'''
SequenceL helpers
'''

# writeLetClauses: tuple(str) -> str
def writeLetClauses(T):
    st = 'let\n'
    for t in T:
        st += '\t\t' + t
    return st

# writeInClause: str -> str
def writeInClause(st):
    st = '\tin\n\t\t' + st;
    return st

# writeElseClause: str -> str
def writeElseClause(st):
    st = ' else\n\t\t' + st
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
        return recurTree(transformTree, T)

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
    T2 = recurTree(transformTree, T2)
    return T2

########## ########## ########## ########## ########## ##########
'''
aggregation
'''

aCategsLib = {'solGround', 'solEq', 'solEqs', 'solSet', 'solDisj'}
aCategs = aCategsLib | {'isAggr', 'solConj'}

# unparseAggr: UnparserInfo * tree -> str
def unparseAggr(u, T):
    if T[0] in aggrOps:
        u.aCateg = 'isAggr'
        if T[0] == 'setCompr':
            termTree = T[1]
            condTree = T[2]
        else:
            termTree = T[2]
            condTree = T[1]

        updateDepSymbsRecur(u, condTree)
        uTerm = u.getAnotherInst(isNext = True)
        u.aTerm = unparseRecur(uTerm, termTree)

        uCond = u.getAnotherInst()
        unparseAggr(uCond, condTree)
        u.condInst = uCond

        args = u.aDefFunc(),
        st = applyRecur(u, T[0], args)
        return st
    if isGround(u, T):
        u.aCateg = 'solGround'
        u.aVal = unparseRecur(u, T)
        st = u.aDefFunc()
        return st
    if T[0] in {'eq', 'setMem'}:
        if T[0] == 'eq':
            if T[1][0] == 'userSVC':
                u.aCateg = 'solEq'
            else: # 'tupT'
                u.aCateg = 'solEqs'
        else: # 'setMem'
            u.aCateg = 'solSet'
        updateDepSymbsRecur(u, T[1])
        u.aVal = unparseRecur(u, T[2])
        st = u.aDefFunc()
        return st
    if T[0] == 'disj':
        u.aCateg = 'solDisj'

        u1 = u.getAnotherInst()
        unparseAggr(u1, T[1])
        u.subInst1 = u1

        u2 = u.getAnotherInst()
        unparseAggr(u2, T[2])
        u.subInst2 = u2

        st = u.aDefFunc()
        return st
    if T[0] == 'conj':
        u.aCateg = 'solConj'

        u1 = u.getAnotherInst()
        unparseAggr(u1, T[1])
        u.subInst1 = u1

        u2 = u1.getAnotherInst(isNext = True)
        unparseAggr(u2, T[2])
        u.subInst2 = u2

        st = u.aDefFunc()
        return st
    else:
        return recurStr(unparseAggr, u, T)

# updateDepSymbsRecur: UnparserInfo * tree -> void
def updateDepSymbsRecur(u, T):
    if type(T) == tuple:
        if T[0] == 'userSVC':
            st = T[1][1]
            if isNewDepSymb(u, st):
                u.depSymbs += st,
        else:
            recurVoid(updateDepSymbsRecur, u, T)

# isGround: UnparserInfo * tree -> bool
def isGround(u, T):
    return not newDepSymbFound(u, T)

# newDepSymbFound: UnparserInfo * tree -> bool
def newDepSymbFound(u, T):
    if type(T) == str:
        return False
    if T[0] == 'userSVC':
        if isNewDepSymb(u, T[1][1]):
            return True
        return False
    else:
        for t in T[1:]:
            if newDepSymbFound(u, t):
                return True
        return False

# isNewDepSymb: UnparserInfo * str -> bool
def isNewDepSymb(u, id):
    return id not in u.getSymbs() + defedConsts

########## ########## ########## ########## ########## ##########
'''
quantification
'''

# unparseQuant: UnparserInfo * tree -> str
def unparseQuant(u, T):
    u.isUniv = T[0] == 'univ'

    symsInSet = T[1]
    u.depSymbs = getSymbsFromSyms(symsInSet[1])

    u2 = u.getAnotherInst()
    u.qSet = unparseRecur(u2, symsInSet[2])

    u3 = u.getAnotherInst(isNext = True)
    u.qPred = unparseRecur(u3, T[2])

    global auxFuncDefs
    qFuncs = u.qDefFuncs()
    auxFuncDefs += qFuncs

    func = u.qGetFuncMain()
    args = u.indepSymbs
    st = applyRecur(u, func, args)

    return st

# getSymbsFromSyms: tree -> tuple(str)
def getSymbsFromSyms(T):
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

# unparseLexemes: UnparserInfo * tree -> str
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

libPath = '../lib.sl'
libAs = ''

# importLib: st
def importLib():
    st = 'import * from ' + addDoubleQuotes(libPath) + ' as '
    if libAs != '':
        st += libAs + '::'
    st += '*;\n\n'
    return st

# str -> str
def prependLib(st):
    st = libAs + st
    return st
