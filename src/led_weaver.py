#!/usr/bin/python3

"""Convert an LED parsertree into a TeX program."""

################################################################################

from debugtools.debug_tool import *

from led_tree import *

################################################################################

TEX_TOP = (
    '\\documentclass{../src/led_doc}' '\n'
    '\\begin{document}' '\n'
)
TEX_BOTTOM = '\n' '\\end{document}' '\n'


IF_CLAUSES = {'termIfBoolTerm', 'termOw'}
QUANT_OPS = {'exist', 'univ'}
AGGR_OPS = {'setCompr', 'aggrUnn', 'aggrNrsec', 'aggrSum', 'aggrProd'}
OVERLOADED_OPS = {'pipesOp', 'plusOp', 'starOp'}
BOOL_OPS = {
    'impl', 'disj', 'conj', 'neg', 'eq', 'uneq', 'less', 'greater', 'lessEq',
    'greaterEq'
}
AR_OPS = {'unaryMinus', 'binaryMinus', 'div', 'md', 'exp', 'flr', 'clng'}
TUPLE_LABELS = {'tpl', 'tuIn', 'tuSl'}
SET_LABELS = {
    'powSet', 'setEmpty', 'setNonempty', 'iv', 'unn', 'diff', 'nrsec', 'sbset',
    'setMem', 'symsInSet'
}
CLS_CMDS = (
    DEF_LABELS | IF_CLAUSES | QUANT_OPS | AGGR_OPS | OVERLOADED_OPS | BOOL_OPS |
    AR_OPS | TUPLE_LABELS | SET_LABELS
)

################################################################################

def weave_top(prog) -> str:
    st = ''
    for prog_el in prog[1:]:
        if is_led_def(prog_el):
            st += get_env('ledDef', (prog_el,))
        elif is_game_flag(prog_el):
            st += r' \textbf{isGame} '
        else:
            st += get_env(CMNT_LABEL, prog_el[1:])
    return surround_str(st, TEX_TOP, TEX_BOTTOM)

################################################################################

def weave_recur(T) -> str:
    if isinstance(T, str):
        return T
    elif T[0] == 'string':
        return get_cmd('texttt', T[1:])
    elif T[0] == 'truth':
        return get_cmd('textKeyword', T[1:])
    elif T[0] == 'equiv':
        return get_cmd('equivLED', T[1:])
    elif T[0] in MANY_LABELS:
        return weave_many(T[1:])
    elif T[0] in FUN_EXPRS:
        return weave_fun_expr(T)
    elif T[0] in CLS_CMDS:
        return get_cmd(T[0], T[1:])
    elif T[0] == 'condTerms':
        return get_env('cases', T[1:])
    else:
        return recur_str(weave_recur, T)

################################################################################

def weave_fun_expr(T) -> str:
    args = ()
    if not isConstFunExpr(T):
        args = T[2][1:]
    return weave_call(T[1], args)

def weave_many(args: tuple) -> str:
    st = weave_recur(args[0])
    for arg in args[1:]:
        st += ', ' + weave_recur(arg)
    return st

################################################################################

def weave_call(func, args: tuple) -> str:
    st = weave_recur(func)
    if args:
        st2 = weave_many(args)
        st2 = get_cmd('parentheses', [st2])
        st += ' ' + st2
    return st

################################################################################

def get_env(env_name: str, env_items: tuple) -> str:
    st = ''
    for env_item in env_items:
        st += weave_recur(env_item) + '\n'
    env_name = surround_str(env_name, '{', '}')
    env_start = surround_str(env_name, '\n' '\\begin', '\n')
    env_end = surround_str(env_name, '\\end', '\n')
    st = surround_str(st, env_start, env_end)
    return st

def get_cmd(cmd_name: str, cmd_args: tuple) -> str:
    st = '\\' + cmd_name
    for cmd_arg in cmd_args:
        st2 = weave_recur(cmd_arg)
        st += surround_str(st2, '{', '}')
    return st

################################################################################

def surround_str(inner_str: str, left_str: str, right_str: str) -> str:
    st = left_str + inner_str + right_str
    return st

################################################################################

def recur_tree(F, T):
    T2 = T[:1]
    for t in T[1:]:
        T2 += F(t),
    return T2

def recur_str(F, T) -> str:
    st = ''
    for t in T[1:]:
        st += F(t)
    return st
