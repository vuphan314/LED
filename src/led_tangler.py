#!/usr/bin/python3

"""Convert an LED parsetree into a SL program."""

################################################################################

from typing import Dict, Tuple
from debugtools.debug_tool import *

################################################################################
"""Python global variables."""

defedFuncs = () # defined functions
defedConsts = () # ('c1', 'c2',...)

auxFuncNum = 0
auxFuncDefs = '' # 'auxFunc1 := 1; auxFunc2 := [2];...'

# Easel:
isGame = False
funcsAddParams = {} # set by setFuncsAddParams

################################################################################

class LedDatum:
    indepSymbs = () # ('i1',...)
    depSymbs = () # ('d1',...)

    def getNumIndepSymbs(self) -> int:
        return len(self.indepSymbs)

    def getNumDepSymbs(self) -> int:
        return len(self.depSymbs)

    def getSymbs(self) -> tuple:
        return self.indepSymbs + self.depSymbs

    def getAnotherInst(self, isNext=False):
        if isNext:
            symbs = self.getNextIndepSymbs()
        else:
            symbs = self.indepSymbs
        dat = LedDatum()
        dat.indepSymbs = symbs
        return dat

    def getNextIndepSymbs(self) -> tuple:
        return self.getSymbs()
            # current dependent symbols will be next independent symbols

    def appendToAux(self, postfix: str, isNext=False) -> str:
        num = auxFuncNum
        if isNext:
            num += 1
        st = 'AUX_' + str(num) + '_' + postfix + '_'
        return st

    """Fields specific to aggregation."""
    # must assign immediately when instantiating:
    aCateg = None # str
    # must assign later by calling aDefFunc:
    aFunc = None # 'AUX_3_(x, y)'

    aVal = ''
        # ground: 'x < y'
        # eq:     'x + 1'
        # set:    'x...2*x'

    # term:
    aTerm = None # 'x + y'
    condInst = None # condition instance (LedDatum)

    # conj/disj:
    subInst1 = None # LedDatum
    subInst2 = None # LedDatum

    def aCheckCateg(self):
        if self.aCateg not in AGGR_CATEGS:
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
        elif self.aCateg in AGGR_LIB_CATEGS:
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
            self, func, (), inCl, letCls=letCls, inds=(ind,), moreSpace=True
        )
        return st

    def aGetAggrLetClauses(self, ind: str) -> str:
        binding = 'b_'
        expr = applyRecur(self, self.condInst.aFunc, (), inds=(ind,))
        letCls = defRecur(self, binding, (), expr),
        for i in range(self.getNumDepSymbs()):
            num = str(i + 1)
            expr = applyRecur(self, binding, (), inds=(num,))
            letCls += defRecur(self, self.depSymbs[i], (), expr),
        return letCls

    def aDefFuncLib(self) -> str:
        expr = applyRecur(self, self.aCateg, self.aGetArgsLib())
        st = defRecur(self, self.aFunc, (), expr, moreSpace=True)
        return st

    def aGetArgsLib(self) -> tuple:
        if self.aCateg == 'solDisj':
            return self.subInst1.aFunc, self.subInst2.aFunc
        elif self.aCateg in AGGR_LIB_CATEGS:
            return self.aVal,
        else:
            raiseError('NOT IN LIBRARY')

    def aDefFuncConj(self) -> str:
        func = 'join'
        args = self.aGetFuncConjDeep(),
        expr = applyRecur(self, func, args)
        st = defRecur(self, self.aFunc, (), expr, moreSpace=True)
        st = self.aDefFuncConjDeep() + st
        return st

    def aDefFuncConjDeep(self) -> str:
        bindings = 'b1_', 'b2_'
        inds = 'i1_', 'i2_'

        func = self.aGetFuncConjDeep()
        expr = applyRecur(self, 'unnBinds', bindings)
        letCls = self.aGetConjLetClauses(bindings, inds)

        st = defRecur(
            self, func, (), expr, letCls=letCls, inds=inds, moreSpace=True
        )
        return st

    def aGetConjLetClauses(self, bindings: tuple, inds: tuple) -> tuple:
        workarounds = 'workaround1_', 'workaround2_'
            # Bryant's solution to avoid SL bug
        funcs = self.subInst1.aFunc, self.subInst2.aFunc
        letCls = ()
        for i in range(2):
            workaround = workarounds[i]
            func = funcs[i]
            letCls += defRecur(self, workaround, (), func),

            ind = inds[i]
            expr = applyRecur(self, workaround, (), inds=(ind,))
            binding = bindings[i]
            letCls += defRecur(self, binding, (), expr),

        n = int(len(letCls) / 2)

        sts = ()
        for i in range(self.subInst1.getNumDepSymbs()):
            symb = self.subInst1.depSymbs[i]
            func = bindings[0]
            num = str(i + 1)
            expr = applyRecur(self, func, (), inds=(num,))
            sts += defRecur(self, symb, (), expr),

        return letCls[:n] + sts + letCls[n:]

    def aGetFuncConjDeep(self) -> str:
        func = self.appendToAux('DEEP')
        args = self.indepSymbs
        return applyRecur(self, func, args)

    """Fields specific to quantification."""
    isUniv = None # bool
    qSet = '' # '{1, 2,...}'
    qPred = '' # 'all y in S. y > x'

    def qDefFuncs(self) -> str:
        st = self.qDefFuncMain() + self.qDefFuncPred() + self.qDefFuncSet()
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
            inds=(ind,), letCls=letCls
        )
        return st

    def qGetPredLetClause(self, ind: str) -> str:
        """Return 'y := S(x)[i_];'."""
        expr = applyRecur(
            self, self.qGetFuncSet(), self.indepSymbs,
            inds=(ind,)
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

################################################################################
"""Top-level function.

Convert an LED parsetree into a string which
represents a SL program.

Python pseudotype `Tree` is either type `tuple` or `str`.
"""

def tangleTop(T: tuple) -> str:
    T = setIsGame(T)
    T = addOtherwiseClauses(T)
    updateDefedFuncsConsts(T)
    if isGame:
        setFuncsAddParams(T)
        T = addEaselParams(T)
        updateDefedConsts(T)
            # parameters were added to some constants,
            # making them non-constants
        imports = ''
            # Easel doesn't work well with imports,
            # so I will append a copy of the LED library to
            # the output SL file
    else:
        imports = importLib()
    T = expandSymsInS(T)
    st = tangleRecur(LedDatum(), T)
    if auxFuncDefs != '':
        st += (
            blockComment('AUXILIARY FUNCTIONS') +
            '\n\n' + auxFuncDefs
        )
    st = printTest() + imports + st
    if isGame:
        st += EASEL_FRAGMENT + getLibsStr()
    return st + '\n'

################################################################################
"""Appened the LED library to the output SL file."""

LIB_NAME = 'led_lib.sl'

def getLibsStr() -> str:
    st = ''
    with open(LIB_NAME) as libFile:
        stLib = libFile.read()
        msg = '''

{}

'''.format(blockComment('BELOW IS A COPY OF ' + LIB_NAME))
        stLib = msg + stLib + '\n'
        stLib = markStartEnd(stLib) + '\n\n'
        st += stLib
    return st

################################################################################

EASEL_FRAGMENT = '''

/*
Easel fragment
*/

/* easel required functions */

initialState: State;
initialState :=
    valToState(initialState_);

newState: Input * State -> State;
newState(I, S) :=
    let
        v := newState_(I, S);
    in
        valToState(v);

images: State -> Image(1);
images(S) :=
    let
        v := images_(S);
    in
        valToImages(v);

/* easel default sound */
sounds: Input * State -> char(2);
sounds(I, S) := ["ding"] when I.iClick.clicked else [];

'''

################################################################################
"""Recursion iterators."""

def tangleRecur(dat: LedDatum, T) -> str:
    if isinstance(T, str):
        return appendUnderscore(T)
    elif T[0] in LEXEMES:
        return tangleLexemes(dat, T)
    elif T[0] == 'actFunExpr':
        args = T[2][1:] if len(T) > 2 else ()
        return applyRecur(dat, T[1], args)
    elif T[0] == 'tpl':
        return tangleTuple(dat, T)
    elif T[0] in SET_LABELS:
        return tangleSet(dat, T)
    elif T[0] in AGGR_OPS:
        return tangleAggr(dat, T)
    elif T[0] in QUANT_OPS:
        return tangleQuant(dat, T)
    elif T[0] in NONSTRICT_OPS:
        return tangleNonstrictOps(dat, T)
    elif T[0] in LIB_OPS:
        return tangleLibOps(dat, T)
    elif T[0] in IF_LABELS:
        return tangleIfClauses(dat, T)
    elif T[0] in DEF_LABELS:
        return tangleDef(dat, T)
    elif T[0] == 'ledCmnt':
        return ''
    else:
        return recurStr(tangleRecur, dat, T)

def defRecur(
    dat: LedDatum, func, args: tuple, expr,
    inds=(), letCls=(), moreSpace=False
) -> str:
    head = applyRecur(dat, func, args, inds=inds)
    expr = tangleRecur(dat, expr)
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
    func = tangleRecur(dat, func)
    if isInLib:
        func = prependLib(func)
    st = func
    if args != ():
        st2 = tangleRecur(dat, args[0])
        for arg in args[1:]:
            st2 += ', ' + tangleRecur(dat, arg)
        if argsAreBracketed:
            st2 = addBrackets(st2)
        st += addParentheses(st2)
    st = appendInds(st, inds)
    return st

################################################################################
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

def recurVoid(F, dat: LedDatum, T):
    """F: LedDatum * tree."""
    for t in T[1:]:
        F(dat, t)

def recurTree(F, T):
    """F: tree -> tree."""
    T2 = T[:1]
    for t in T[1:]:
        T2 += F(t),
    return T2

################################################################################
"""Update defined functions/constants."""

def updateDefedFuncsConsts(prog):
    global defedFuncs
    global defedConsts
    for led_def in prog[1:]:
        st = tangleRecur(LedDatum(), led_def[1][1])
        defedFuncs += st,
        if isConstDef(led_def):
            defedConsts += st,

def updateDefedConsts(prog):
    global defedConsts
    defedConsts = ()
    for led_def in prog[1:]:
        if isConstDef(led_def):
            st = tangleRecur(LedDatum(), led_def[1])
            defedConsts += st,

def isConstDef(led_def):
    formFunExpr = led_def[1][1]
    return len(formFunExpr) == 2 # no 'terms'

################################################################################
"""Easel."""

def addEaselParams(T):
    if isinstance(T, str):
        return T
    elif T[0] == 'namedTermNoParenth':
        id = T[1]
        params = getEaselParamsFromLexeme(id)
        if params != ():
            terms = getIdsTree('terms', 'namedTermNoParenth', params)
            T = 'actFunExpr', id, terms
        return T
    elif T[0] == 'constDef':
        # todo!
        root = T[0]
        head = addEaselParams(T[1])
        if head[0] == 'formFunExpr':
            root = 'funDef'
        expr = addEaselParams(T[2])
        T2 = root, head, expr
        if len(T) > 3:
            whereCl = addEaselParams(T[3])
            T2 += whereCl,
        return T2
    elif T[0] == 'actFunExpr':
        params = getEaselParamsFromLexeme(T[1])
        terms = T[2]
        terms += getIdsTuple('namedTermNoParenth', params)
        T = T[:2] + (terms,)
        return recurTree(addEaselParams, T)
    elif T[0] == 'formFunExpr':
        params = getEaselParamsFromLexeme(T[1])
        if params != ():
            syms = getIdsTuple('id', params)
            if len(T) == 2: # nullary
                syms = ('syms',) + syms
                T += syms,
            else:
                syms = T[2] + syms
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

EASEL_INPUT = 'I'
EASEL_STATE = 'S'

EASEL_PARAMS_INPUT = EASEL_INPUT,
EASEL_PARAMS_STATE = EASEL_STATE,

EASEL_PARAMS = EASEL_PARAMS_INPUT + EASEL_PARAMS_STATE

def getEaselParamsFromLexeme(id) -> tuple:
    st = tangleRecur(LedDatum(), id)
    if not isinstance(st, str):
        raiseError('MUST BE STRING')
    if not (st in defedFuncs or st in EASEL_FUNCS): # symbol
        return ()
    elif st in funcsAddParams['addNeither']:
        return ()
    elif st in funcsAddParams['addInput']:
        return EASEL_PARAMS_INPUT
    elif st in funcsAddParams['addState']:
        return EASEL_PARAMS_STATE
    else:
        return EASEL_PARAMS

def appendUnderscore(st: str) -> str:
    if st in EASEL_FUNCS and st not in EASEL_FUNCS_GLOBAL:
        st += '_'
    return st

EASEL_FUNCS_CLICK = {'mouseClicked', 'mouseX', 'mouseY'}
EASEL_FUNCS_CURRENT_STATE = {'currentState'}
EASEL_FUNCS_GLOBAL = EASEL_FUNCS_CLICK | EASEL_FUNCS_CURRENT_STATE

EASEL_FUNCS_CONSTRUCTOR = {
    'point', 'color', 'click', 'input', 'segment', 'circle', 'text', 'disc',
    'fTri', 'graphic'
}
EASEL_FUNCS_ADD_NEITHER = EASEL_FUNCS_CONSTRUCTOR | {'initialState'}

EASEL_FUNCS_ADD_INPUT = EASEL_FUNCS_CLICK

EASEL_FUNCS_ADD_STATE = EASEL_FUNCS_CURRENT_STATE | {'images'}

EASEL_FUNCS_ADD_BOTH = {'newState'}

EASEL_FUNCS = (
    EASEL_FUNCS_ADD_NEITHER | EASEL_FUNCS_ADD_INPUT | EASEL_FUNCS_ADD_STATE |
    EASEL_FUNCS_ADD_BOTH
)

def setFuncsAddParams(prog):
    global funcsAddParams
    funcsAddParams = {
        'addNeither': EASEL_FUNCS_ADD_NEITHER,
        'addInput': EASEL_FUNCS_ADD_INPUT,
        'addState': EASEL_FUNCS_ADD_STATE,
        'addBoth': EASEL_FUNCS_ADD_BOTH
    }
    for prog_el in prog[1:]:
        if prog_el[0] in DEF_LABELS: # != 'ledCmnt'
            fun_name = tangleRecur(LedDatum(), prog_el[1][1][1]) # no 'syms'
            if fun_name not in EASEL_FUNCS:
                body = prog_el[1][2]
                if needBoth(body):
                    key = 'addBoth'
                elif needInput(body):
                    key = 'addInput'
                elif needState(body):
                    key = 'addState'
                else:
                    key = 'addNeither'
                funcsAddParams[key] |= {fun_name}

def needBoth(body) -> bool:
    return (
        someStrFound(body, funcsAddParams['addBoth']) or
        eachStrFound(body, EASEL_PARAMS) or
        needInput(body) and needState(body)
    )

def needInput(body) -> bool:
    """Assumption:

    not someStrFound(body, funcsAddParams['addBoth'])
    """
    return (
        someStrFound(body, funcsAddParams['addInput']) or
        someStrFound(body, EASEL_PARAMS_INPUT)
    )

def needState(body) -> bool:
    """Assumption:

    not someStrFound(body, funcsAddParams['addBoth'])
    """
    return (
        someStrFound(body, funcsAddParams['addState']) or
        someStrFound(body, EASEL_PARAMS_STATE)
    )

def eachStrFound(T, sts) -> bool:
    for st in sts:
        sts2 = {st}
        if not someStrFound(T, sts2):
            return False
    return True

def someStrFound(T, sts) -> bool:
    if isinstance(T, str):
        return T in sts
    else:
        for t in T[1:]:
            if someStrFound(t, sts):
                return True
        return False

################################################################################
"""Tangle function definitions."""

DEF_LABELS = {'funDef', 'relDef'}
DEF_WHERE_LABELS = {'funDefWhere', 'relDefWhere'}

def tangleDef(dat: LedDatum, T) -> str:
    T = T[1]

    func = tangleRecur(dat, T[1][1])

    dat2 = dat.getAnotherInst()
    if len(T[1]) > 2: # non-constant function
        dat2.indepSymbs = getSymbsFromSyms(T[1][2])

    if T[0] in DEF_WHERE_LABELS:
        letCls = tangleWhereClauses(dat2, T[3])
    else:
        letCls = ()

    st = defRecur(
        dat2, func, dat2.indepSymbs, T[2],
        moreSpace=True, letCls=letCls
    )
    return st

IF_LABELS = {'condTerms', 'termIfBoolTerm', 'termOw'}

def tangleIfClauses(dat: LedDatum, T) -> str:
    if T[0] == 'termOw':
        st = tangleRecur(dat, T[1])
        return st
    elif T[0] == 'termIfBoolTerm':
        st1 = tangleRecur(dat, T[1])
        st2 = tangleRecur(dat, T[2])
        st2 = applyRecur(dat, 'valToTrth', (st2,))
        st = st1 + ' when ' + st2
        return st
    elif T[0] == 'condTerms':
        st = tangleIfClauses(dat, T[1])
        for t in T[2:]:
            st2 = tangleIfClauses(dat, t)
            st += writeElseClause(st2)
        return st
    else:
        raiseError('INVALID IF-CLAUSES')

def tangleWhereClauses(dat: LedDatum, T) -> Tuple[str]:
    if T[0] == 'eq':
        st = defRecur(dat, T[1], (), T[2])
        return st,
    elif T[0] == 'conj':
        return recurTuple(tangleWhereClauses, dat, T)
    else:
        raiseError('INVALID WHERE-CLAUSES')

################################################################################
"""Tangle collections."""

def tangleTuple(dat: LedDatum, T) -> str:
    func = 'tu'
    terms = T[1]
    st = applyRecur(
        dat, func, terms[1:], isInLib=True,
        argsAreBracketed=True
    )
    return st

SET_LABELS = {'setEmpty', 'setNonempty'}

def tangleSet(dat: LedDatum, T) -> str:
    func = 'se'
    if T[0] == 'setEmpty':
        args = '',
    else:
        terms = T[1]
        args = terms[1:]
    st = applyRecur(
        dat, func, args, isInLib=True,
        argsAreBracketed=True
    )
    return st

################################################################################
"""Nonstrict operations."""

NONSTRICT_OPS = {'impl', 'conj'}

def tangleNonstrictOps(dat: LedDatum, T):
    st1 = tangleRecur(dat, T[1])
    st2 = tangleRecur(dat, T[2])
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

################################################################################
"""Tangle LED library operations."""

AR_OPS = {
    'binaryMinus', 'unaryMinus',
    'div', 'flr', 'clng', 'md', 'exp'
}
BOOL_OPS = {'equiv', 'disj', 'neg'}
EQUALITY_OPS = {'eq', 'uneq'}
OVERLOADED_OPS = {'pipesOp', 'plusOp', 'starOp'}
RELATIONAL_OPS = {'less', 'greater', 'lessEq', 'greaterEq'}
SET_OPS = {
    'setMem', 'sbset', 'unn', 'nrsec', 'diff',
    'powSet', 'iv'
}
TUPLE_OPS = {'tuIn', 'tuSl'}

LIB_OPS = (
    AR_OPS | BOOL_OPS | EQUALITY_OPS | OVERLOADED_OPS |
    RELATIONAL_OPS | SET_OPS | TUPLE_OPS
)

def tangleLibOps(dat: LedDatum, T) -> str:
    st = applyRecur(dat, T[0], T[1:], isInLib=True)
    return st

################################################################################
"""SequenceL helpers."""

def writeLetClauses(tup: tuple) -> str:
    st = '\tlet\n'
    for t in tup:
        st += '\t\t' + t
    return st

def writeInClause(st: str) -> str:
    st = '\tin\n\t\t' + st
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

################################################################################
"""Miscellaneous."""

def unionDicts(ds: Tuple[Dict]) -> dict:
    D = {}
    for d in ds:
        D.update(d)
    return D

################################################################################
"""Add otherwise-clase."""

def addOtherwiseClauses(T):
    if isinstance(T, str):
        return T
    elif T[0] == 'condTerms':
        if T[-1][0] == 'termIfBoolTerm': # != 'termOw'
            t = 'valNull'
            t = 'id', t
            t = 'namedTermNoParenth', t
            t = 'termOw', t
            T += t,
        return T
    else:
        return recurTree(addOtherwiseClauses, T)

################################################################################
"""Expand quantifying symbols."""

QUANT_OPS = {'exist', 'univ'}

def expandSymsInS(T):
    if isinstance(T, str):
        return T
    elif T[0] in QUANT_OPS:
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

################################################################################
"""Aggregation."""

AGGR_OPS = {
    'setCompr', 'aggrUnn', 'aggrNrsec',
    'aggrSum', 'aggrProd'
}

AGGR_LIB_CATEGS = {
    'solGround', 'solEq', 'solEqs', 'solSet', 'solDisj'
}
AGGR_CATEGS = AGGR_LIB_CATEGS | {'isAggr', 'solConj'}

def tangleAggr(dat: LedDatum, T) -> str:
    if T[0] in AGGR_OPS:
        dat.aCateg = 'isAggr'
        if T[0] == 'setCompr':
            termTree = T[1]
            condTree = T[2]
        else:
            termTree = T[2]
            condTree = T[1]

        updateDepSymbsRecur(dat, condTree)
        uTerm = dat.getAnotherInst(isNext=True)
        dat.aTerm = tangleRecur(uTerm, termTree)

        uCond = dat.getAnotherInst()
        tangleAggr(uCond, condTree)
        dat.condInst = uCond

        args = dat.aDefFunc(),
        st = applyRecur(dat, T[0], args)
        return st
    elif isGround(dat, T):
        dat.aCateg = 'solGround'
        dat.aVal = tangleRecur(dat, T)
        st = dat.aDefFunc()
        return st
    elif T[0] in {'eq', 'setMem'}:
        if T[0] == 'eq':
            if T[1][0] == 'namedTermNoParenth':
                dat.aCateg = 'solEq'
            else: # 'tupT'
                dat.aCateg = 'solEqs'
        else: # 'setMem'
            dat.aCateg = 'solSet'
        updateDepSymbsRecur(dat, T[1])
        dat.aVal = tangleRecur(dat, T[2])
        st = dat.aDefFunc()
        return st
    elif T[0] == 'disj':
        dat.aCateg = 'solDisj'

        dat1 = dat.getAnotherInst()
        tangleAggr(dat1, T[1])
        dat.subInst1 = dat1

        dat2 = dat.getAnotherInst()
        tangleAggr(dat2, T[2])
        dat.subInst2 = dat2

        st = dat.aDefFunc()
        return st
    elif T[0] == 'conj':
        dat.aCateg = 'solConj'

        dat1 = dat.getAnotherInst()
        tangleAggr(dat1, T[1])
        dat.subInst1 = dat1

        dat2 = dat1.getAnotherInst(isNext=True)
        tangleAggr(dat2, T[2])
        dat.subInst2 = dat2

        st = dat.aDefFunc()
        return st
    else:
        return recurStr(tangleAggr, dat, T)

def updateDepSymbsRecur(dat: LedDatum, T):
    if isinstance(T, tuple):
        if T[0] == 'namedTermNoParenth':
            st = T[1][1]
            if isNewDepSymb(dat, st):
                dat.depSymbs += st,
        else:
            recurVoid(updateDepSymbsRecur, dat, T)

def isGround(dat: LedDatum, T) -> bool:
    return not newDepSymbFound(dat, T)

def newDepSymbFound(dat: LedDatum, T) -> bool:
    if isinstance(T, str):
        return False
    elif T[0] == 'namedTermNoParenth':
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

################################################################################
"""Quantification."""

def tangleQuant(dat: LedDatum, T) -> str:
    dat.isUniv = T[0] == 'univ'

    symsInSet = T[1]
    dat.depSymbs = getSymbsFromSyms(symsInSet[1])

    dat2 = dat.getAnotherInst()
    dat.qSet = tangleRecur(dat2, symsInSet[2])

    dat3 = dat.getAnotherInst(isNext=True)
    dat.qPred = tangleRecur(dat3, T[2])

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
        symb = sym[1]
        symbs += symb,
    return symbs

################################################################################
"""Tangle lexemes."""

LEXEMES_DOUBLY_QUOTED = {'numl': 'nu', 'atom': 'at'}
LEXEMES = unionDicts(
    (LEXEMES_DOUBLY_QUOTED, {'string': 'st', 'truth': 'tr'})
)

def tangleLexemes(dat: LedDatum, T) -> str:
    lex = T[0]
    func = LEXEMES[lex]
    arg = T[1]
    if lex in LEXEMES_DOUBLY_QUOTED:
        arg = addDoubleQuotes(arg)
    args = arg,
    st = applyRecur(dat, func, args, isInLib=True)
    return st

################################################################################
"""Import and use LED library."""

LIB_PATH = '../src/led_lib.sl'
LIB_AS = ''

def importLib() -> str:
    st = 'import * from {} as '.format(
        addDoubleQuotes(LIB_PATH)
    )
    if LIB_AS != '':
        st += LIB_AS + '::'
    st += '*;\n\n'
    return st

def prependLib(st: str) -> str:
    st = LIB_AS + st
    return st

################################################################################
"""Test SL constants."""

def printTest() -> str:
    st = ''
    for const in defedConsts:
        if (
            const == 'initialState' or
            const not in EASEL_FUNCS
        ):
            func = applyRecur(None, 'pp', (const,))
            st += func + '\n'
    if st != '':
        head = 'Test with SequenceL interpreter:\n\n'
        tail = '\n(pp: pretty-print)'
        st = head + st + tail
        st = blockComment(st)
        st += '\n\n'
    return st

################################################################################
"""Check whether the LED program is an Easel game.

For each keyword #isGame found in the LED program:
- set the Python global variable isGame to True
- delete that keyword from the parsetree
"""

def setIsGame(prog):
    prog2 = prog[:1]
    for el in prog[1:]:
        if el[0] == 'hashIsGame':
            global isGame
            isGame = True
        else:
            prog2 += el,
    return prog2
