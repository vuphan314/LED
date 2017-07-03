"""Define labels appearing in an LED parsetree."""

################################################################################

from typing import Dict, Tuple

################################################################################

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

AGGR_OPS = {'setCompr', 'aggrUnn', 'aggrNrsec', 'aggrSum', 'aggrProd'}

################################################################################
"""library operations"""

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
"""lexemes"""

LEXEMES_DOUBLY_QUOTED = {'numl': 'nu', 'atom': 'at'}
LEXEMES = unionDicts((LEXEMES_DOUBLY_QUOTED, {'string': 'st', 'truth': 'tr'}))
