"""Convert an LED parsetree to a SL program."""

############################################################
"""Import."""

from debugtools.debug_tool import *

############################################################
"""Python global variables."""

isGame = False

defedFuncs = ()
defedConsts = () # ('c1', 'c2',...)

auxFuncNum = 0
auxFuncDefs = '' # 'aux1 := 1; aux2 := 2;...'

############################################################
"""LED datum."""

class LedDatum:
    indepSymbs = () # ('i1',...)
    depSymbs = () # ('d1',...)

    def getNumIndepSymbs(self) -> int:
        n = len(self.indepSymbs)
        return n

    def getNumDepSymbs(self) -> int:
        n = len(self.depSymbs)
        return n

    def getSymbs(self) -> tuple:
        T = self.indepSymbs + self.depSymbs
        return T

    def getAnotherInst(self, isNext=False):
        if isNext:
            symbs = self.getNextIndepSymbs()
        else:
            symbs = self.indepSymbs
        dat = LedDatum()
        dat.indepSymbs = symbs
        return dat

    def getNextIndepSymbs(self) -> tuple:
        T = self.getSymbs()
        return T

    def appendToAux(
        self, extraAppend: str, isNext=False
    ) -> str:
        num = auxFuncNum
        if isNext:
            num += 1
        st = 'AUX_' + str(num) + '_' + extraAppend + '_'
        return st

    """Fields specific to aggregation."""
    # must assign immediately when instantiating
    aCateg = None # str
    # must assign later by calling function aDefFunc
    aFunc = None # 'AUX_3_(x, y)'

    aVal = ''
    # ground: 'x < y'
    # eq:     'x + 1'
    # set:    'x...2*x'


    # term
    aTerm = None # 'x + y'
    condInst = None # LedDatum

    # conj/disj
    subInst1 = None # LedDatum
    subInst2 = None # LedDatum

    def aCheckCateg(self) -> None:
        if self.aCateg not in aCategs:
            raiseError('INVALID AGGREGATE CATEGORY')

    def aDefFunc(self) -> str:
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

    def aDefFuncAggr(self) -> str:
        ind = 'i_'

        func = self.aFunc
        letCls = self.aGetAggrLetClauses(ind)
        inCl = self.aTerm

        st = defRecur(
            self, func, (), inCl,
            letCls=letCls, inds = (ind,), moreSpace=True
        )
        return st

    def aGetAggrLetClauses(self, ind: str) -> str:
        binding = 'b_'
        expr = applyRecur(
            self, self.condInst.aFunc, (), inds = (ind,)
        )
        letCls = defRecur(self, binding, (), expr),
        for i in range(self.getNumDepSymbs()):
            num = str(i + 1)
            expr = applyRecur(
                self, binding, (), inds = (num,)
            )
            letCls += defRecur(
                self, self.depSymbs[i], (), expr
            ),
        return letCls

    def aDefFuncLib(self) -> str:
        expr = applyRecur(
            self, self.aCateg, self.aGetArgsLib()
        )
        st = defRecur(
            self, self.aFunc, (), expr, moreSpace=True
        )
        return st

    def aGetArgsLib(self) -> tuple:
        if self.aCateg == 'solDisj':
            return self.subInst1.aFunc, self.subInst2.aFunc
        elif self.aCateg in aCategsLib:
            return self.aVal,
        else:
            raiseError('NOT IN LIBRARY')

    def aDefFuncConj(self) -> str:
        func = 'join'
        args = self.aGetFuncConjDeep(),
        expr = applyRecur(self, func, args)
        st = defRecur(
            self, self.aFunc, (), expr, moreSpace=True
        )
        st = self.aDefFuncConjDeep() + st
        return st

    def aDefFuncConjDeep(self) -> str:
        bindings = 'b1_', 'b2_'
        inds = 'i1_', 'i2_'

        func = self.aGetFuncConjDeep()
        expr = applyRecur(self, 'unnBinds', bindings)
        letCls = self.aGetConjLetClauses(bindings, inds)

        st = defRecur(
            self, func, (), expr, letCls=letCls,
            inds = inds, moreSpace=True
        )
        return st

    def aGetConjLetClauses(
        self, bindings: tuple, inds: tuple
    ) -> tuple:
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
            expr = applyRecur(
                self, workaround, (), inds = (ind,)
            )
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

    def aGetFuncConjDeep(self) -> str:
        func = self.appendToAux('DEEP')
        args = self.indepSymbs
        st = applyRecur(self, func, args)
        return st

    """Fields specific to quantification."""
    isUniv = None # bool
    qSet = '' # '{1, 2,...}'
    qPred = '' # 'all y in S. y > x'

    def qDefFuncs(self) -> str:
        st = (
            self.qDefFuncMain() + self.qDefFuncPred() +
            self.qDefFuncSet()
        )
        return st

    def qDefFuncMain(self) -> str:
        global auxFuncNum
        auxFuncNum += 1

        S = self.indepSymbs

        funcPred = self.qGetFuncPred()
        argsQuant = applyRecur(self, funcPred, S),

        funcQuant = self.qGetFuncQuant()
        expr = applyRecur(self, funcQuant, argsQuant)

        funcMain = self.qGetFuncMain()
        st = defRecur(
            self, funcMain, S, expr, moreSpace=True
        )
        return st

    def qDefFuncPred(self) -> str:
        ind = 'i_'

        letCls = self.qGetPredLetClause(ind),

        func = self.qPred
        if funcIsAux(func):
            args = self.getNextIndepSymbs()
            func = applyRecur(self, func, args)
        expr = func

        func2 = self.qGetFuncPred()
        args2 = self.indepSymbs

        st = defRecur(
            self, func2, args2, expr,
            inds = (ind,), letCls=letCls
        )
        return st

    def qGetPredLetClause(self, ind: str) -> str:
        """Return 'y := S(x)[i_];'."""
        expr = applyRecur(
            self, self.qGetFuncSet(), self.indepSymbs,
            inds = (ind,)
        )
        st = defRecur(self, self.depSymbs[0], (), expr)
        return st

    def qDefFuncSet(self) -> str:
        func = self.qGetFuncSet()
        args = self.indepSymbs
        expr = applyRecur(self, 'valToSet', (self.qSet,))
        st = defRecur(
            self, func, args, expr, moreSpace=True
        )
        return st

    def qGetFuncQuant(self) -> str:
        if self.isUniv:
            func = 'allSet'
        else: # universal
            func = 'someSet'
        return func

    def qGetFuncMain(self) -> str:
        st = self.appendToAux('A')
        return st

    def qGetFuncPred(self) -> str:
        st = self.appendToAux('B')
        return st

    def qGetFuncSet(self) -> str:
        st = self.appendToAux('C')
        return st

############################################################
"""Main function.

Translate an LED parsetree into a string which
represents a SL program.

Note: Python pseudotype `tree` is
either type `tuple` or `str`.
"""

def translateTop(T: tuple) -> str:
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
        # Will write LED library at end of output file.

    else:
        imports = importLib()

    tests = '\n' + printTest()

    # for quantification
    T = expandSymsInS(T)

    dat = LedDatum()
    st = translateRecur(dat, T)

    if auxFuncDefs != '':
        st += (
            blockComment('AUXILIARY FUNCTIONS') +
            '\n\n' + auxFuncDefs
        )

    st = tests + imports + st
    return st

############################################################
"""Recursion iterators."""

def translateRecur(dat: LedDatum, T) -> str:
    if isinstance(T, str):
        return appendUnderscore(T)
    elif T[0] in lexemes:
        return translateLexemes(dat, T)
    elif T[0] == 'nonnullFunRel':
        st = applyRecur(dat, T[1], T[2][1:])
        return st
    elif T[0] == 'tpl':
        return translateTuple(dat, T)
    elif T[0] == 'set':
        return translateSet(dat, T)
    elif T[0] in aggrOps:
        return translateAggr(dat, T)
    elif T[0] in quantOps:
        return translateQuant(dat, T)
    elif T[0] in nonstrictOps:
        return translateNonstrictOps(dat, T)
    elif T[0] in libOps:
        return translateLibOps(dat, T)
    elif T[0] in ifLabels:
        return translateIfClauses(dat, T)
    elif T[0] in defLabels:
        return translateDef(dat, T)
    else:
        return recurStr(translateRecur, dat, T)

def defRecur(
    dat: LedDatum, func, args: tuple, expr,
    inds=(), letCls=(), moreSpace=False
) -> str:
    head = applyRecur(dat, func, args, inds = inds)
    expr = translateRecur(dat, expr)
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

def applyRecur(
    dat: LedDatum, func, args: tuple,
    isInLib=False, argsAreBracketed=False, inds=()
) -> str:
    func = translateRecur(dat, func)

    if isInLib:
        func = prependLib(func)

    st = func

    if args != ():
        st2 = translateRecur(dat, args[0])
        for arg in args[1:]:
            st2 += ', ' + translateRecur(dat, arg)

        if argsAreBracketed:
            st2 = addBrackets(st2)

        st += addParentheses(st2)

    st = appendInds(st, inds)
    return st

############################################################
"""Recursion helpers."""

def recurStr(F, dat: LedDatum, T) -> str:
    """F: LedDatum * tree -> str."""
    st = ''
    for t in T[1:]:
        st += F(dat, t)
    return st

def recurTuple(F, dat: LedDatum, T) -> tuple:
    """F: LedDatum * tree -> tuple."""
    tu = ()
    for t in T[1:]:
        tu += F(dat, t)
    return tu

def recurVoid(F, dat: LedDatum, T) -> None:
    """F: LedDatum * tree -> None."""
    for t in T[1:]:
        F(dat, t)

def recurTree(F, T):
    """F: tree -> tree."""
    T2 = T[:1]
    for t in T[1:]:
        T2 += F(t),
    return T2

############################################################
"""Update defined functions/constants."""

def updateDefedFuncsConsts(prog) -> None:
    global defedFuncs
    global defedConsts
    for definition in prog[1:]:
        st = translateRecur(LedDatum(), definition[1][1])
        defedFuncs += st,
        if definition[0] == 'constDef':
            defedConsts += st,

def updateDefedConsts(prog) -> None:
    global defedConsts
    defedConsts = ()
    for definition in prog[1:]:
        if definition[0] == 'constDef':
            st = translateRecur(LedDatum(), definition[1])
            defedConsts += st,

############################################################
"""Easel."""

def addEaselParams(T):
    if isinstance(T, str):
        return T
    elif T[0] == 'symOrNullFunRel':
        id = T[1]
        params = getParamsFromLexeme(id)
        if params != ():
            terms = getIdsTree('terms', 'symOrNullFunRel', params)
            T = 'nonnullFunRel', id, terms
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
    elif T[0] == 'nonnullFunRel':
        params = getParamsFromLexeme(T[1])
        terms = T[2]
        terms += getIdsTuple('symOrNullFunRel', params)
        T = T[:2] + (terms,)
        return recurTree(addEaselParams, T)
    elif T[0] in {'funT', 'relT'}:
        params = getParamsFromLexeme(T[1])
        # tst(params)
        syms = T[2]
        syms += getIdsTuple('symN', params)
        T = T[:2] + (syms,)
        return T
    else:
        return recurTree(addEaselParams, T)

def getIdsTree(label1: str, label2: str, ids: tuple):
    tu = getIdsTuple(label2, ids)
    tu = (label1,) + tu
    return tu

def getIdsTuple(label: str, ids: tuple) -> tuple:
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

def getParamsFromLexeme(id) -> tuple:
    st = translateRecur(LedDatum(), id)
    if not isinstance(st, str):
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

def appendUnderscore(st: str) -> str:
    if st in easelFuncs and st not in easelFuncsGlobal:
        st += '_'
    return st

easelFuncsClick = {'mouseClicked', 'mouseX', 'mouseY'}
easelFuncsCurrentState = {'currentState'}
easelFuncsGlobal = easelFuncsClick | easelFuncsCurrentState

easelFuncsConstructor = {
    'point', 'color', 'click', 'input', 'segment', 'circle',
    'text', 'disc', 'fTri', 'graphic'
}
easelFuncsAddNeither = easelFuncsConstructor | {
    'initialState'
}

easelFuncsAddInput = easelFuncsClick

easelFuncsAddState = easelFuncsCurrentState | {'images'}

easelFuncsAddBoth = {'newState'}

easelFuncs = (
    easelFuncsAddNeither | easelFuncsAddInput |
    easelFuncsAddState | easelFuncsAddBoth
)

funcsAddParams = {
    'addNeither': easelFuncsAddNeither,
    'addInput': easelFuncsAddInput,
    'addState': easelFuncsAddState,
    'addBoth': easelFuncsAddBoth
}

def updateFuncsAddParams(prog) -> None:
    for definition in prog[1:]:
        head = translateRecur(LedDatum(), definition[1][1])
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

def needBoth(body) -> bool:
    return (
        someStrFound(body, funcsAddParams['addBoth']) or
        eachStrFound(body, easelParams) or
        needInput(body) and needState(body)
    )

def needInput(body) -> bool:
    """Assumption:

    not someStrFound(body, funcsAddParams['addBoth']).
    """
    return (
        someStrFound(body, funcsAddParams['addInput']) or
        someStrFound(body, easelParamsInput)
    )

def needState(body) -> bool:
    """Assumption:

    not someStrFound(body, funcsAddParams['addBoth']).
    """
    return (
        someStrFound(body, funcsAddParams['addState']) or
        someStrFound(body, easelParamsState)
    )

def eachStrFound(T, sts) -> bool:
    for st in sts:
        sts2 = {st}
        if not someStrFound(T, sts2):
            return False
    return True

def someStrFound(T, sts) -> bool:
    if type(T) == str:
        return T in sts
    else:
        for t in T[1:]:
            if someStrFound(t, sts):
                return True
        return False

############################################################
"""Translate constant/function/relation definitions."""

defLabels = {'constDef', 'funDef', 'relDef'}

def translateDef(dat: LedDatum, T) -> str:
    func = translateRecur(dat, T[1][1])
    dat2 = dat.getAnotherInst()

    if T[0] in {'funDef', 'relDef'}:
        dat2.indepSymbs = getSymbsFromSyms(T[1][2])

    letCls = ()
    if len(T) > 3: # where-clauses
        letCls = translateWhereClauses(dat2, T[3])

    st = defRecur(
        dat2, func, dat2.indepSymbs, T[2],
        moreSpace=True, letCls=letCls
    )
    return st

ifLabels = {'tIfBTs', 'tIfBTsO'}

def translateIfClauses(dat: LedDatum, T) -> str:
    if T[0] == 'tOther':
        st = translateRecur(dat, T[1])
        st = writeElseClause(st)
        return st
    elif T[0] == 'tIfBT':
        st1 = translateRecur(dat, T[1])
        st2 = translateRecur(dat, T[2])
        st2 = applyRecur(dat, 'valToTrth', (st2,))
        st = st1 + ' when ' + st2
        return st
    elif T[0] == 'tIfBTs':
        st = translateIfClauses(dat, T[1])
        for t in T[2:]:
            st2 = translateIfClauses(dat, t)
            st += writeElseClause(st2)
        return st
    elif T[0] == 'tIfBTsO':
        return recurStr(translateIfClauses, dat, T)
    else:
        raiseError('INVALID IF CLAUSES')

# translateWhereClauses: LedDatum * tree -> tuple(str)
def translateWhereClauses(dat, T):
    if T[0] == 'eq':
        st = defRecur(dat, T[1], (), T[2])
        return st,
    elif T[0] == 'conj':
        return recurTuple(translateWhereClauses, dat, T)
    else:
        raiseError('INVALID WHERE CLAUSES')

############################################################
"""Translate collections."""

def translateTuple(dat: LedDatum, T) -> str:
    func = 'tu'
    terms = T[1]
    st = applyRecur(
        dat, func, terms[1:], isInLib=True,
        argsAreBracketed=True
    )
    return st

def translateSet(dat: LedDatum, T) -> str:
    func = 'se'
    if len(T) == 1: # empty set
        args = '',
    else:
        terms = T[1]
        args = terms[1:]
    st = applyRecur(
        dat, func, args, isInLib=True,
        argsAreBracketed=True
    )
    return st

############################################################
"""Nonstrict operations."""

nonstrictOps = {'impl', 'conj'}

def translateNonstrictOps(dat: LedDatum, T):
    st1 = translateRecur(dat, T[1])
    st2 = translateRecur(dat, T[2])
    if T[0] == 'conj':
        mainSt = 'valFalse'
        whenSt = 'not ' + applyRecur(
            dat, 'valToTrth', (st1,)
        )
    elif T[0] == 'impl':
        mainSt = 'valTrue'
        whenSt = 'not ' + applyRecur(
            dat, 'valToTrth', (st1,)
        )
    else:
        raiseError('MUST BE NON-STRICT OPERATION')
    elseSt = st2
    st = writeWhenElseClause(mainSt, whenSt, elseSt)
    return st

def writeWhenElseClause(
    mainSt: str, whenSt: str, elseSt: str
) -> str:
    st = mainSt + ' when ' + whenSt + ' else ' + elseSt
    st = addParentheses(st)
    return st

############################################################
"""Translate LED library operations."""

equalityOps = {'eq', 'uneq'}
relationalOps = {'less', 'greater', 'lessEq', 'greaterEq'}
boolOps = {'equiv', 'disj', 'neg'}
overloadedOps = {'pipesOp', 'plusOp', 'starOp'}
arOps = {'bMns', 'uMns', 'div', 'flr', 'clng', 'md', 'exp'}
setOps = {
    'setMem', 'sbset', 'unn', 'nrsec', 'diff', 'powSet',
    'iv'
}
tupleOps = {'tuIn', 'tuSl'}

libOps = (
    overloadedOps | equalityOps | relationalOps | arOps |
    setOps | boolOps | tupleOps
)

def translateLibOps(dat: LedDatum, T) -> str:
    st = applyRecur(dat, T[0], T[1:], isInLib=True)
    return st

############################################################
"""SequenceL helpers."""

def writeLetClauses(tup: tuple) -> str:
    st = '\tlet\n'
    for t in tup:
        st += '\t\t' + t
    return st

def writeInClause(st: str) -> str:
    st = '\tin\n\t\t' + st;
    return st

def writeElseClause(st: str) -> str:
    st = ' else\n\t\t' + st
    return st

def appendInds(st: str, tup: tuple) -> str:
    if tup != ():
        st2 = tup[0]
        for t in tup[1:]:
            st2 += ', ' + t
        st2 = addBrackets(st2)
        st += st2
    return st

def addBrackets(st: str) -> str:
    st = '[' + st + ']'
    return st

def addDoubleQuotes(st: str) -> str:
    st = '"' + st + '"'
    return st

def addParentheses(st: str) -> str:
    st = '(' + st + ')'
    return st

def funcIsAux(st: str) -> bool:
    b = st[-1] == '_'
    return b

############################################################
"""Miscellaneous."""

def unionDicts(ds) -> dict:
    """Note: ds: tuple(dict)."""
    D = {}
    for d in ds:
        D.update(d)
    return D

############################################################
"""Add otherwise-clase."""

def addOtherwiseClause(T):
    if type(T) == str:
        return T
    elif T[0] == 'tIfBTs':
        return tIfBTsToTIfBTsO(T)
    elif T[0] == 'tIfBTsO':
        return T
    else:
        return recurTree(addOtherwiseClause, T)

def tIfBTsToTIfBTsO(tIfBTs):
    t = 'valNull'
    t = 'id', t
    t = 'symOrNullFunRel', t
    t = 'tOther', t
    T = 'tIfBTsO', tIfBTs, t
    return T

############################################################
"""Expand quantifying symbols."""

quantOps = {'exist', 'univ'}

def expandSymsInS(T):
    if type(T) == str:
        return T
    elif T[0] in quantOps:
        T2 = symsInSetToSymbInSet(T)
        return T2
    else:
        return recurTree(expandSymsInS, T)

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
"""Aggregation."""

aggrOps = {
    'setCompr', 'aggrUnn', 'aggrNrsec', 'aggrSum',
    'aggrProd'
}

aCategsLib = {
    'solGround', 'solEq', 'solEqs', 'solSet', 'solDisj'
}
aCategs = aCategsLib | {'isAggr', 'solConj'}

def translateAggr(dat: LedDatum, T) -> str:
    if T[0] in aggrOps:
        dat.aCateg = 'isAggr'
        if T[0] == 'setCompr':
            termTree = T[1]
            condTree = T[2]
        else:
            termTree = T[2]
            condTree = T[1]

        updateDepSymbsRecur(dat, condTree)
        uTerm = dat.getAnotherInst(isNext=True)
        dat.aTerm = translateRecur(uTerm, termTree)

        uCond = dat.getAnotherInst()
        translateAggr(uCond, condTree)
        dat.condInst = uCond

        args = dat.aDefFunc(),
        st = applyRecur(dat, T[0], args)
        return st
    elif isGround(dat, T):
        dat.aCateg = 'solGround'
        dat.aVal = translateRecur(dat, T)
        st = dat.aDefFunc()
        return st
    elif T[0] in {'eq', 'setMem'}:
        if T[0] == 'eq':
            if T[1][0] == 'symOrNullFunRel':
                dat.aCateg = 'solEq'
            else: # 'tupT'
                dat.aCateg = 'solEqs'
        else: # 'setMem'
            dat.aCateg = 'solSet'
        updateDepSymbsRecur(dat, T[1])
        dat.aVal = translateRecur(dat, T[2])
        st = dat.aDefFunc()
        return st
    elif T[0] == 'disj':
        dat.aCateg = 'solDisj'

        dat1 = dat.getAnotherInst()
        translateAggr(dat1, T[1])
        dat.subInst1 = dat1

        dat2 = dat.getAnotherInst()
        translateAggr(dat2, T[2])
        dat.subInst2 = dat2

        st = dat.aDefFunc()
        return st
    elif T[0] == 'conj':
        dat.aCateg = 'solConj'

        dat1 = dat.getAnotherInst()
        translateAggr(dat1, T[1])
        dat.subInst1 = dat1

        dat2 = dat1.getAnotherInst(isNext=True)
        translateAggr(dat2, T[2])
        dat.subInst2 = dat2

        st = dat.aDefFunc()
        return st
    else:
        return recurStr(translateAggr, dat, T)

def updateDepSymbsRecur(dat: LedDatum, T) -> None:
    if type(T) == tuple:
        if T[0] == 'symOrNullFunRel':
            st = T[1][1]
            if isNewDepSymb(dat, st):
                dat.depSymbs += st,
        else:
            recurVoid(updateDepSymbsRecur, dat, T)

def isGround(dat: LedDatum, T) -> bool:
    return not newDepSymbFound(dat, T)

def newDepSymbFound(dat: LedDatum, T) -> bool:
    if type(T) == str:
        return False
    elif T[0] == 'symOrNullFunRel':
        if isNewDepSymb(dat, T[1][1]):
            return True
        else:
            return False
    else:
        for t in T[1:]:
            if newDepSymbFound(dat, t):
                return True
        return False

def isNewDepSymb(dat: LedDatum, id: str) -> bool:
    return id not in dat.getSymbs() + defedConsts

############################################################
"""Quantification."""

def translateQuant(dat: LedDatum, T) -> str:
    dat.isUniv = T[0] == 'univ'

    symsInSet = T[1]
    dat.depSymbs = getSymbsFromSyms(symsInSet[1])

    dat2 = dat.getAnotherInst()
    dat.qSet = translateRecur(dat2, symsInSet[2])

    dat3 = dat.getAnotherInst(isNext=True)
    dat.qPred = translateRecur(dat3, T[2])

    global auxFuncDefs
    qFuncs = dat.qDefFuncs()
    auxFuncDefs += qFuncs

    func = dat.qGetFuncMain()
    args = dat.indepSymbs
    st = applyRecur(dat, func, args)

    return st

def getSymbsFromSyms(T) -> tuple:
    syms = T[1:]
    symbs = ()
    for sym in syms:
        symb = sym[1][1]
        symbs += symb,
    return symbs

############################################################
"""Translate lexemes."""

lexemesDoublyQuoted = {'numl': 'nu', 'atom': 'at'}
dicts = lexemesDoublyQuoted, {'string': 'st', 'truth': 'tr'}
lexemes = unionDicts(dicts)

def translateLexemes(dat: LedDatum, T) -> str:
    lex = T[0]
    func = lexemes[lex]
    arg = T[1]
    if lex in lexemesDoublyQuoted:
        arg = addDoubleQuotes(arg)
    args = arg,
    st = applyRecur(dat, func, args, isInLib=True)
    return st

############################################################
"""Import and use LED library."""

libPath = '../led_lib.sl'
libAs = ''

def importLib() -> str:
    st = 'import * from {} as '.format(
        addDoubleQuotes(libPath)
    )
    if libAs != '':
        st += libAs + '::'
    st += '*;\n\n'
    return st

def prependLib(st: str) -> str:
    st = libAs + st
    return st

############################################################
"""Test SL constants."""

def printTest() -> str:
    st = ''
    for const in defedConsts:
        if const == 'initialState' or const not in easelFuncs:
            func = applyRecur(None, 'pp', (const,))
            st += func + '\n'
    if st != '':
        head = '''
Copy/paste the block below into
the SequenceL interpreter to test:

'''
        tail = '\n(pp: pretty-print)'
        st = head + st + tail
        st = blockComment(st)
        st += '\n\n'
    return st

############################################################
"""
for each keyword *#isGame* found in LED input file
- make python global variable `isGame` true
- delete keyword from parsetree
"""

def updateIsGame(prog):
    prog2 = prog[:1]
    for el in prog[1:]:
        if el[0] == 'hashIsGame':
            global isGame
            isGame = True
        else:
            prog2 += el,
    return prog2
