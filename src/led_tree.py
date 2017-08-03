"""Define labels appearing in an LED parsetree."""

################################################################################

from typing import Dict, Tuple

################################################################################
"""miscellaneous"""

def unionDicts(ds: Tuple[Dict]) -> dict:
    D = {}
    for d in ds:
        D.update(d)
    return D

################################################################################
"""program element"""

CMNT_LABEL = 'ledCmnt'
DEF_WHERE_LABELS = {'funDefWhere', 'relDefWhere'}
DEF_LABELS = DEF_WHERE_LABELS | {'funDefNoWhere', 'relDefNoWhere'}

def is_led_def(prog_el) -> bool:
    return prog_el[0] in DEF_LABELS # != CMNT_LABEL

################################################################################
"""aggregation"""

SET_COMPR = 'setCompr'
AGGR_OPS = {SET_COMPR, 'aggrUnn', 'aggrNrsec', 'aggrSum', 'aggrProd'}

# aggregate categories:
GROUND_SOL = 'groundSol' # 1 + 2 < 3
EQ_SOL = 'eqSol' # x = 1
EQS_SOL = 'eqsSol' # (x, y) = (1, 2)
SET_MEM_SOL = 'setMemSol' # x in {1, 2}
DISJ_SOL = 'unnSols' # x = 1 V y in {2}
LIB_SOLS = {GROUND_SOL, EQ_SOL, EQS_SOL, SET_MEM_SOL, DISJ_SOL}
CONJ_SOL = 'conjSol' # x = 1 & y in {2}
AGGR_CATEGS = LIB_SOLS | {CONJ_SOL, 'isAggr'} # todo what is 'isAggr'

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

ACT_FUN_EXPR = 'actFunExpr'

################################################################################
"""lexeme"""

LEXEMES_DOUBLY_QUOTED = {'numl': 'nu', 'atom': 'at'}
LEXEMES = unionDicts((LEXEMES_DOUBLY_QUOTED, {'string': 'st', 'truth': 'tr'}))
