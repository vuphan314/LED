"""Convert an LED parsetree into a SL program."""

############################################################
"""Import."""

from debugger import *

############################################################
"""Python global variables."""

isGame = False

defedFuncs = ()
defedConsts = () # ('c1', 'c2',...)

auxFuncNum = 0
auxFuncDefs = '' # 'aux1 := 1; aux2 := 2;...'

############################################################
"""Main function.

Unparse an LED parsetree into a string which
represents a SL program.

Note: Python pseudotype `tree` is
either type `tuple` or `str`.
"""

def unparseTop(L: list) -> str:
    T = listToTree(L)
    T = updateIsGame(T)

    T = addOtherwiseClause(T)
    updateDefedFuncsConsts(T)

    if isGame:
        updateFuncsAddParams(T)
        T = addEaselParams(T)

        # some constants were added parameters
        updateDefedConsts(T)

        imports = ''
        # Easel doesn't work well with imports.
        # Will write LED libraries at end of output file.

    else:
        imports = importLib()

    tests = '\n' + printTest()

    # for quantification
    T = expandSymsInS(T)

    dat = LedDatum()
    st = unparseRecur(dat, T)

    if auxFuncDefs != '':
        st += (
            blockComment('AUXILIARY FUNCTIONS') +
            '\n\n' + auxFuncDefs
        )

    st = tests + imports + st
    return st

############################################################
"""Recursion iterators."""

def unparseRecur(dat: LedDatum, T) -> str:
    if isinstance(T, str):
        return appendUnderscore(T)
    elif T[0] in lexemes:
        return unparseLexemes(dat, T)
    elif T[0] == 'userFR':
        st = applyRecur(dat, T[1], T[2][1:])
        return st
    elif T[0] == 'tpl':
        return unparseTuple(dat, T)
    elif T[0] == 'set':
        return unparseSet(dat, T)
    elif T[0] in aggrOps:
        return unparseAggr(dat, T)
    elif T[0] in quantOps:
        return unparseQuant(dat, T)
    elif T[0] in nonstrictOps:
        return unparseNonstrictOps(dat, T)
    elif T[0] in libOps:
        return unparseLibOps(dat, T)
    elif T[0] in ifLabels:
        return unparseIfClauses(dat, T)
    elif T[0] in defLabels:
        return unparseDef(dat, T)
    else:
        return recurStr(unparseRecur, dat, T)

# defRecur: LedDatum * tree * tuple(tree) * tree -> str
def defRecur(dat, func, args, expr, inds = (), letCls = (), moreSpace = False):
    head = applyRecur(dat, func, args, inds = inds)
    expr = unparseRecur(dat, expr)
    if letCls != ():
        letCls = writeLetClauses(letCls)
        inCl = writeInClause(expr)
        expr = letCls + inCl
        moreSpace = True
    body = expr + ';\n'
    if moreSpace:
        indent = '\n'
        if letCls == ():
            indent += '\t\t'
        body = indent + body + '\n'
    st = head + ' := ' + body
    return st

# applyRecur: LedDatum * tree * tuple(tree) -> str
def applyRecur(dat, func, args, isInLib = False, argsAreBracketed = False, inds = ()):
    func = unparseRecur(dat, func)
    if isInLib:
        func = prependLib(func)
    st = func
    if args != ():
        st2 = unparseRecur(dat, args[0])
        for arg in args[1:]:
            st2 += ', ' + unparseRecur(dat, arg)
        if argsAreBracketed:
            st2 = addBrackets(st2)
        st += addParentheses(st2)
    st = appendInds(st, inds)
    return st

############################################################
"""
recursion helpers
"""

# recurStr: (LedDatum * tree -> str) * LedDatum * tree -> str
def recurStr(F, dat, T):
    st = ''
    for t in T[1:]:
        st += F(dat, t)
    return st

# recurTuple: (LedDatum * tree -> tuple(str)) * LedDatum * tree -> tuple(str)
def recurTuple(F, dat, T):
    tu = ()
    for t in T[1:]:
        tu += F(dat, t)
    return tu

# recurVoid: (LedDatum * tree -> void) * LedDatum * tree -> void
def recurVoid(F, dat, T):
    for t in T[1:]:
        F(dat, t)

# recurTree: (tree -> tree) * tree -> tree
def recurTree(F, T):
    T2 = T[:1]
    for t in T[1:]:
        T2 += F(t),
    return T2

############################################################
"""
update defined functions/constants
"""

# updateDefedFuncsConsts: tree -> void
def updateDefedFuncsConsts(prog):
    global defedFuncs
    global defedConsts
    for definition in prog[1:]:
        st = definition[1][1][1]
        defedFuncs += st,
        if definition[0] == 'constDef':
            defedConsts += st,

# updateDefedConsts: tree -> void
def updateDefedConsts(prog):
    global defedConsts
    defedConsts = ()
    for definition in prog[1:]:
        if definition[0] == 'constDef':
            st = definition[1][1][1]
            defedConsts += st,

############################################################
"""
Easel
"""

# addEaselParams: tree -> tree
def addEaselParams(T):
    if type(T) == str:
        return T
    elif T[0] == 'userSC':
        id = T[1]
        params = getParamsFromLexeme(id)
        if params != ():
            terms = getIdsTree('terms', 'userSC', params)
            T = 'userFR', id, terms
        return T
    elif T[0] == 'constN':
        id = T[1]
        params = getParamsFromLexeme(id)
        if params != ():
            syms = getIdsTree('syms', 'symN', params)
            T = 'funT', id, syms
        return T
    elif T[0] == 'constDef':
        root = T[0]
        head = addEaselParams(T[1])
        if head[0] == 'funT':
            root = 'funDef'
        expr = addEaselParams(T[2])
        T2 = root, head, expr
        if len(T) > 3:
            whereCl = addEaselParams(T[3])
            T2 += whereCl,
        return T2
    elif T[0] == 'userFR':
        params = getParamsFromLexeme(T[1])
        terms = T[2]
        terms += getIdsTuple('userSC', params)
        T = T[:2] + (terms,)
        return recurTree(addEaselParams, T)
    elif T[0] in {'funT', 'relT'}:
        params = getParamsFromLexeme(T[1])
        syms = T[2]
        syms += getIdsTuple('symN', params)
        T = T[:2] + (syms,)
        return T
    else:
        return recurTree(addEaselParams, T)

# getIdsTree: str * str * tuple(str) -> tree
def getIdsTree(label1, label2, ids):
    tu = getIdsTuple(label2, ids)
    tu = (label1,) + tu
    return tu

# getIdsTuple: str * tuple(str) -> tuple(str)
def getIdsTuple(label, ids):
    tu = ()
    for id in ids:
        st = 'id', id
        st = label, st
        tu += st,
    return tu

easelInput = 'I'
easelState = 'S'

easelParamsInput = easelInput,
easelParamsState = easelState,

easelParams = easelParamsInput + easelParamsState

# getParamsFromLexeme: tree -> tuple(str)
def getParamsFromLexeme(id):
    st = id[1]
    if type(st) != str:
        raiseError('MUST BE STRING')

    if not (st in defedFuncs or st in easelFuncs): # symbol
        return ()
    elif st in funcsAddParams['addNeither']:
        return ()
    elif st in funcsAddParams['addInput']:
        return easelParamsInput
    elif st in funcsAddParams['addState']:
        return easelParamsState
    else:
        return easelParams

# appendUnderscore: str -> str
def appendUnderscore(st):
    if st in easelFuncs and st not in easelFuncsGlobal:
        st += '_'
    return st

easelFuncsClick = {'mouseClicked', 'mouseX', 'mouseY'}
easelFuncsCurrentState = {'currentState'}
easelFuncsGlobal = easelFuncsClick | easelFuncsCurrentState

easelFuncsConstructor = {\
    'point', 'color', 'click', 'input', 'segment', 'circle', \
    'text', 'disc', 'fTri', 'graphic'}
easelFuncsAddNeither = easelFuncsConstructor | {'initialState'}

easelFuncsAddInput = easelFuncsClick

easelFuncsAddState = easelFuncsCurrentState | {'images'}

easelFuncsAddBoth = {'newState'}

easelFuncs = \
    easelFuncsAddNeither | easelFuncsAddInput | easelFuncsAddState | \
    easelFuncsAddBoth

funcsAddParams = {  'addNeither': easelFuncsAddNeither,
                    'addInput': easelFuncsAddInput,
                    'addState': easelFuncsAddState,
                    'addBoth': easelFuncsAddBoth}

# updateFuncsAddParams: tree -> void
def updateFuncsAddParams(prog):
    for definition in prog[1:]:
        head = definition[1][1][1]
        if head not in easelFuncs:
            body = definition[2]
            if needBoth(body):
                key = 'addBoth'
            elif needInput(body):
                key = 'addInput'
            elif needState(body):
                key = 'addState'
            else:
                key = 'addNeither'
            global funcsAddParams
            funcsAddParams[key] |= {head}

# needBoth: tree -> bool
def needBoth(body):
    return \
        someStrFound(body, funcsAddParams['addBoth']) or \
        eachStrFound(body, easelParams) or \
        needInput(body) and needState(body)

# needInput: tree * bool
def needInput(body): # provided: not someStrFound(body, funcsAddParams['addBoth'])
    return \
        someStrFound(body, funcsAddParams['addInput']) or \
        someStrFound(body, easelParamsInput)

# needState: tree * bool
def needState(body): # provided: not someStrFound(body, funcsAddParams['addBoth'])
    return \
        someStrFound(body, funcsAddParams['addState']) or \
        someStrFound(body, easelParamsState)

# eachStrFound: tree * strs -> bool
def eachStrFound(T, sts):
    for st in sts:
        sts2 = {st}
        if not someStrFound(T, sts2):
            return False
    return True

# someStrFound: tree * strs -> bool
def someStrFound(T, sts):
    if type(T) == str:
        return T in sts
    else:
        for t in T[1:]:
            if someStrFound(t, sts):
                return True
        return False

############################################################
"""
unparse constant/function/relation definitions
"""

defLabels = {'constDef', 'funDef', 'relDef'}

# unparseDef: LedDatum * tree -> str
def unparseDef(dat, T):
    func = unparseRecur(dat, T[1][1])
    u2 = dat.getAnotherInst()

    if T[0] in {'funDef', 'relDef'}:
        u2.indepSymbs = getSymbsFromSyms(T[1][2])

    letCls = ()
    if len(T) > 3: # where-clauses
        letCls = unparseWhereClauses(u2, T[3][1])

    st = defRecur(u2, func, u2.indepSymbs, T[2], moreSpace = True, letCls = letCls)
    return st

ifLabels = {'tIfBTs', 'tIfBTsO'}

# unparseIfClauses: LedDatum * tree -> str
def unparseIfClauses(dat, T):
    if T[0] == 'tOther':
        st = unparseRecur(dat, T[1])
        st = writeElseClause(st)
        return st
    elif T[0] == 'tIfBT':
        st1 = unparseRecur(dat, T[1])
        st2 = unparseRecur(dat, T[2])
        st2 = applyRecur(dat, 'valToTrth', (st2,))
        st = st1 + ' when ' + st2
        return st
    elif T[0] == 'tIfBTs':
        st = unparseIfClauses(dat, T[1])
        for t in T[2:]:
            st2 = unparseIfClauses(dat, t)
            st += writeElseClause(st2)
        return st
    elif T[0] == 'tIfBTsO':
        return recurStr(unparseIfClauses, dat, T)
    else:
        raiseError('INVALID IF CLAUSES')

# unparseWhereClauses: LedDatum * tree -> tuple(str)
def unparseWhereClauses(dat, T):
    if T[0] == 'eq':
        st = defRecur(dat, T[1], (), T[2])
        return st,
    elif T[0] == 'conj':
        return recurTuple(unparseWhereClauses, dat, T)
    else:
        raiseError('INVALID WHERE CLAUSES')

############################################################
"""
information for unparsing
"""

class LedDatum:
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

    # getAnotherInst: LedDatum
    def getAnotherInst(self, isNext = False):
        if isNext:
            symbs = self.getNextIndepSymbs()
        else:
            symbs = self.indepSymbs
        dat = LedDatum()
        dat.indepSymbs = symbs
        return dat

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

    """
    fields specific to aggregation
    """
    # must assign immediately when instantiating
    aCateg = None # str
    # must assign later by calling function aDefFunc
    aFunc = None # 'AUX_3_(x, y)'

    aVal = ''
    """
    ground: 'x < y'
    eq:     'x + 1'
    set:    'x...2*x'
    """

    # term
    aTerm = None # 'x + y'
    condInst = None # LedDatum

    # conj/disj
    subInst1 = None # LedDatum
    subInst2 = None # LedDatum

    # aCheckCateg: void
    def aCheckCateg(self):
        if self.aCateg not in aCategs:
            raiseError('INVALID AGGREGATE CATEGORY')

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

        func = self.aFunc
        letCls = self.aGetAggrLetClauses(ind)
        inCl = self.aTerm

        st = defRecur(  self, func, (), inCl, letCls = letCls, \
                        inds = (ind,), moreSpace = True)
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
        elif self.aCateg in aCategsLib:
            return self.aVal,
        else:
            raiseError('NOT IN LIBRARY')

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

        func = self.aGetFuncConjDeep()
        expr = applyRecur(self, 'unnBinds', bindings)
        letCls = self.aGetConjLetClauses(bindings, inds)

        st = defRecur(  self, func, (), expr, letCls = letCls, \
                        inds = inds, moreSpace = True)
        return st

    # aGetConjLetClauses: tuple(str) * tuple(str) -> tuple(str)
    def aGetConjLetClauses(self, bindings, inds):
        workarounds = 'workaround1_', 'workaround2_'
        funcs = self.subInst1.aFunc, self.subInst2.aFunc
        letCls = ()
        for i in range(2):
            # assign workaround
            workaround = workarounds[i]
            func = funcs[i]
            letCls += defRecur(self, workaround, (), func),
            # call workaround
            ind = inds[i]
            expr = applyRecur(self, workaround, (), inds = (ind,))
            binding = bindings[i]
            letCls += defRecur(self, binding, (), expr),
        n = int(len(letCls) / 2)

        sts = ()
        for i in range(self.subInst1.getNumDepSymbs()):
            symb = self.subInst1.depSymbs[i]
            func = bindings[0]
            num = str(i + 1)
            expr = applyRecur(self, func, (), inds = (num,))
            sts += defRecur(self, symb, (), expr),

        sts = letCls[:n] + sts + letCls[n:]
        return sts

    # aGetFuncConjDeep: str
    def aGetFuncConjDeep(self):
        func = self.appendToAux('DEEP')
        args = self.indepSymbs
        st = applyRecur(self, func, args)
        return st

    """
    fields specific to quantification
    """
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

        S = self.indepSymbs

        funcPred = self.qGetFuncPred()
        argsQuant = applyRecur(self, funcPred, S),

        funcQuant = self.qGetFuncQuant()
        expr = applyRecur(self, funcQuant, argsQuant)

        funcMain = self.qGetFuncMain()
        st = defRecur(self, funcMain, S, expr, moreSpace = True)
        return st

    # qDefFuncPred: str
    def qDefFuncPred(self):
        ind = 'i_'

        letCls = self.qGetPredLetClause(ind),

        func = self.qPred
        if funcIsAux(func):
            args = self.getNextIndepSymbs()
            func = applyRecur(self, func, args)
        expr = func

        func2 = self.qGetFuncPred()
        args2 = self.indepSymbs

        st = defRecur(self, func2, args2, expr, inds = (ind,), letCls = letCls)
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

############################################################
"""
unparse collections
"""

# unparseTuple: LedDatum * tree -> str
def unparseTuple(dat, T):
    func = 'tu'
    terms = T[1]
    st = applyRecur(dat, func, terms[1:], isInLib = True, argsAreBracketed = True)
    return st

# unparseSet: LedDatum * tree -> str
def unparseSet(dat, T):
    func = 'se'
    if len(T) == 1: # empty set
        args = '',
    else:
        terms = T[1]
        args = terms[1:]
    st = applyRecur(dat, func, args, isInLib = True, argsAreBracketed = True)
    return st

############################################################
"""
non-strict operations
"""

nonstrictOps = {'impl', 'conj'}

# unparseNonstrictOps: LedDatum * tree -> tree
def unparseNonstrictOps(dat, T):
    st1 = unparseRecur(dat, T[1])
    st2 = unparseRecur(dat, T[2])
    if T[0] == 'conj':
        mainSt = 'valFalse'
        whenSt = 'not ' + applyRecur(dat, 'valToTrth', (st1,))
    elif T[0] == 'impl':
        mainSt = 'valTrue'
        whenSt = 'not ' + applyRecur(dat, 'valToTrth', (st1,))
    else:
        raiseError('MUST BE NON-STRICT OPERATION')
    elseSt = st2
    st = writeWhenElseClause(mainSt, whenSt, elseSt)
    return st

# writeWhenElseClause: str * str * str -> str
def writeWhenElseClause(mainSt, whenSt, elseSt):
    st = mainSt + ' when ' + whenSt + ' else ' + elseSt
    st = addParentheses(st)
    return st

############################################################
"""
unparse library operations
"""

equalityOps = {'eq', 'uneq'}
relationalOps = {'less', 'greater', 'lessEq', 'greaterEq'}
boolOps = {'equiv', 'disj', 'neg'}
overloadedOps = {'pipesOp', 'plusOp', 'starOp'}
arOps = {'bMns', 'uMns', 'div', 'flr', 'clng', 'md', 'exp'}
setOps = {'setMem', 'sbset', 'unn', 'nrsec', 'diff', 'powSet', 'iv'}
tupleOps = {'tuIn', 'tuSl'}

libOps = \
    overloadedOps | equalityOps | relationalOps | arOps | setOps | boolOps | tupleOps

# unparseLibOps: LedDatum * tree -> str
def unparseLibOps(dat, T):
    st = applyRecur(dat, T[0], T[1:], isInLib = True)
    return st

############################################################
"""
SequenceL helpers
"""

# writeLetClauses: tuple(str) -> str
def writeLetClauses(T):
    st = '\tlet\n'
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

# funcIsAux: str -> bool
def funcIsAux(st):
    b = st[-1] == '_'
    return b

############################################################
"""
miscellaneous
"""

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

############################################################
"""
add otherwise-clase
"""

# addOtherwiseClause: tree -> tree
def addOtherwiseClause(T):
    if type(T) == str:
        return T
    elif T[0] == 'tIfBTs':
        return tIfBTsToTIfBTsO(T)
    elif T[0] == 'tIfBTsO':
        return T
    else:
        return recurTree(addOtherwiseClause, T)

# tIfBTsToTIfBTsO: tree -> tree
def tIfBTsToTIfBTsO(tIfBTs):
    t = 'printNull'
    t = 'id', t
    t = 'userSC', t
    t = 'tOther', t
    T = 'tIfBTsO', tIfBTs, t
    return T

############################################################
"""
expand quantifying symbols
"""

quantOps = {'exist', 'univ'}

# expandSymsInS: tree -> tree
def expandSymsInS(T):
    if type(T) == str:
        return T
    elif T[0] in quantOps:
        T2 = symsInSetToSymbInSet(T)
        return T2
    else:
        return recurTree(expandSymsInS, T)

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
    T2 = recurTree(expandSymsInS, T2)
    return T2

############################################################
"""
aggregation
"""

aggrOps = {'setCompr', 'aggrUnn', 'aggrNrsec', 'aggrSum', 'aggrProd'}

aCategsLib = {'solGround', 'solEq', 'solEqs', 'solSet', 'solDisj'}
aCategs = aCategsLib | {'isAggr', 'solConj'}

# unparseAggr: LedDatum * tree -> str
def unparseAggr(dat, T):
    if T[0] in aggrOps:
        dat.aCateg = 'isAggr'
        if T[0] == 'setCompr':
            termTree = T[1]
            condTree = T[2]
        else:
            termTree = T[2]
            condTree = T[1]

        updateDepSymbsRecur(dat, condTree)
        uTerm = dat.getAnotherInst(isNext = True)
        dat.aTerm = unparseRecur(uTerm, termTree)

        uCond = dat.getAnotherInst()
        unparseAggr(uCond, condTree)
        dat.condInst = uCond

        args = dat.aDefFunc(),
        st = applyRecur(dat, T[0], args)
        return st
    elif isGround(dat, T):
        dat.aCateg = 'solGround'
        dat.aVal = unparseRecur(dat, T)
        st = dat.aDefFunc()
        return st
    elif T[0] in {'eq', 'setMem'}:
        if T[0] == 'eq':
            if T[1][0] == 'userSC':
                dat.aCateg = 'solEq'
            else: # 'tupT'
                dat.aCateg = 'solEqs'
        else: # 'setMem'
            dat.aCateg = 'solSet'
        updateDepSymbsRecur(dat, T[1])
        dat.aVal = unparseRecur(dat, T[2])
        st = dat.aDefFunc()
        return st
    elif T[0] == 'disj':
        dat.aCateg = 'solDisj'

        u1 = dat.getAnotherInst()
        unparseAggr(u1, T[1])
        dat.subInst1 = u1

        u2 = dat.getAnotherInst()
        unparseAggr(u2, T[2])
        dat.subInst2 = u2

        st = dat.aDefFunc()
        return st
    elif T[0] == 'conj':
        dat.aCateg = 'solConj'

        u1 = dat.getAnotherInst()
        unparseAggr(u1, T[1])
        dat.subInst1 = u1

        u2 = u1.getAnotherInst(isNext = True)
        unparseAggr(u2, T[2])
        dat.subInst2 = u2

        st = dat.aDefFunc()
        return st
    else:
        return recurStr(unparseAggr, dat, T)

# updateDepSymbsRecur: LedDatum * tree -> void
def updateDepSymbsRecur(dat, T):
    if type(T) == tuple:
        if T[0] == 'userSC':
            st = T[1][1]
            if isNewDepSymb(dat, st):
                dat.depSymbs += st,
        else:
            recurVoid(updateDepSymbsRecur, dat, T)

# isGround: LedDatum * tree -> bool
def isGround(dat, T):
    return not newDepSymbFound(dat, T)

# newDepSymbFound: LedDatum * tree -> bool
def newDepSymbFound(dat, T):
    if type(T) == str:
        return False
    elif T[0] == 'userSC':
        if isNewDepSymb(dat, T[1][1]):
            return True
        else:
            return False
    else:
        for t in T[1:]:
            if newDepSymbFound(dat, t):
                return True
        return False

# isNewDepSymb: LedDatum * str -> bool
def isNewDepSymb(dat, id):
    return id not in dat.getSymbs() + defedConsts

############################################################
"""
quantification
"""

# unparseQuant: LedDatum * tree -> str
def unparseQuant(dat, T):
    dat.isUniv = T[0] == 'univ'

    symsInSet = T[1]
    dat.depSymbs = getSymbsFromSyms(symsInSet[1])

    u2 = dat.getAnotherInst()
    dat.qSet = unparseRecur(u2, symsInSet[2])

    u3 = dat.getAnotherInst(isNext = True)
    dat.qPred = unparseRecur(u3, T[2])

    global auxFuncDefs
    qFuncs = dat.qDefFuncs()
    auxFuncDefs += qFuncs

    func = dat.qGetFuncMain()
    args = dat.indepSymbs
    st = applyRecur(dat, func, args)

    return st

# getSymbsFromSyms: tree -> tuple(str)
def getSymbsFromSyms(T):
    syms = T[1:]
    symbs = ()
    for sym in syms:
        symb = sym[1][1]
        symbs += symb,
    return symbs

############################################################
"""
unparse lexemes
"""

lexemesDoublyQuoted = {'numl': 'nu', 'atom': 'at'}
lexemes = unionDicts((lexemesDoublyQuoted, {'string': 'st', 'truth': 'tr'}))

# unparseLexemes: LedDatum * tree -> str
def unparseLexemes(dat, T):
    lex = T[0]
    func = lexemes[lex]
    arg = T[1]
    if lex in lexemesDoublyQuoted:
        arg = addDoubleQuotes(arg)
    args = arg,
    st = applyRecur(dat, func, args, isInLib = True)
    return st

############################################################
"""
importing and using LED library
"""

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

############################################################
"""
SL test constants
"""

# printTest: str
def printTest():
    st = ''
    for const in defedConsts:
        if const == 'initialState' or const not in easelFuncs:
            func = applyRecur(None, 'pp', (const,))
            st += func + '\n'
    if st != '':
        head = 'Copy/paste the block below into the SequenceL interpreter to test:\n\n'
        tail = '\n(pp: pretty-print)'
        st = head + st + tail
        st = blockComment(st)
        st += '\n\n'
    return st

############################################################
"""
for each keyword $#isGame$ found in LED input file
- make python global variable $isGame$ true
- delete keyword from parsetree
"""

# updateIsGame: tree -> tree
def updateIsGame(prog):
    prog2 = prog[:1]
    for el in prog[1:]:
        if el[0] == 'hashIsGame':
            global isGame
            isGame = True
        else:
            prog2 += el,
    return prog2
