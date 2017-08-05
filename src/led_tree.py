#!/usr/bin/python3

"""Define labels appearing in an LED parsetree."""

################################################################################

from typing import Dict, Tuple

################################################################################
"""program element"""

CMNT_LABEL = 'ledCmnt'
GAME_LABEL = 'ledGame'
DEF_WHERE_LABELS = {'funDefWhere', 'relDefWhere'}
DEF_LABELS = DEF_WHERE_LABELS | {'funDefNoWhere', 'relDefNoWhere'}

def is_led_cmnt(prog_el) -> bool:
    return prog_el[0] == CMNT_LABEL

def is_game_flag(prog_el) -> bool:
    return prog_el[0] == GAME_LABEL

def is_led_def(prog_el) -> bool:
    return prog_el[0] in DEF_LABELS

################################################################################
"""aggregation"""

SET_COMPR = 'setCompr'
AGGR_OPS = {SET_COMPR, 'aggrUnn', 'aggrNrsec', 'aggrSum', 'aggrProd'}

# aggregate categories:
GROUND_SOL = 'groundSol' # of `1 + 2 < 0` is `[]`
EQ_SOL = 'eqSol' # of `x = 1` is `[[1]]`
EQS_SOL = 'eqsSol' # of `(x, y) = (1, 2)` is `[[1, 2]]`
SET_MEM_SOL = 'setMemSol' # of `x in {1, 2}` is `[[1], [2]]`
DISJ_SOL = 'unnSols' # of solutions `[[1]]` and `[[2]]` is `[[1], [2]]`
    # for boolean term `x = 1 V x in {2}`
LIB_SOLS = {GROUND_SOL, EQ_SOL, EQS_SOL, SET_MEM_SOL, DISJ_SOL}
CONJ_SOL = 'conjSol' # of `x = 1 & y in {2}` is `[[1, 2]]`
READY_LIST = 'readyList'
    # of `{x^2 | x in {-2, 2}}` or `Sum[x in {-2, 2}](x^2)` is `[4, 4]`
AGGR_CATEGS = LIB_SOLS | {CONJ_SOL, READY_LIST}

################################################################################
"""collection"""

SET_LABELS = {'setEmpty', 'setNonempty'}

################################################################################
"""library operation"""

AR_OPS = {'binaryMinus', 'unaryMinus', 'div', 'flr', 'clng', 'md', 'exp'}
BOOL_OPS = {'equiv', 'disj', 'neg'}
EQUALITY_OPS = {'eq', 'uneq'}
OVERLOADED_OPS = {'pipesOp', 'plusOp', 'starOp'}
RELATIONAL_OPS = {'less', 'greater', 'lessEq', 'greaterEq'}
SET_OPS = {'setMem', 'sbset', 'unn', 'nrsec', 'diff', 'powSet', 'iv'}
TUPLE_OPS = {'tuIn', 'tuSl'}
LIB_OPS = (
    AR_OPS | BOOL_OPS | EQUALITY_OPS | OVERLOADED_OPS | RELATIONAL_OPS |
    SET_OPS | TUPLE_OPS
)

################################################################################
"""function expression"""

FORM_FUN_EXPR = 'formFunExpr'
ACT_FUN_EXPR = 'actFunExpr'
FUN_EXPRS = {FORM_FUN_EXPR, ACT_FUN_EXPR}

def isConstDef(led_def) -> bool:
    form_fun_expr = led_def[1]
    return isConstFunExpr(form_fun_expr)

def isConstFunExpr(fun_expr) -> bool:
    return len(fun_expr) == 2 # no: ('terms',...)

################################################################################
"""many"""

SYMS = 'syms'
TERMS = 'terms'
MANY_LABELS = {TERMS, SYMS}

################################################################################
"""lexeme"""

def unionDicts(ds: Tuple[Dict]) -> dict:
    D = {}
    for d in ds:
        D.update(d)
    return D

ID = 'id'
LEXEMES_DOUBLY_QUOTED = {'numl': 'nu', 'atom': 'at'}
LEXEMES = unionDicts((LEXEMES_DOUBLY_QUOTED, {'string': 'st', 'truth': 'tr'}))
