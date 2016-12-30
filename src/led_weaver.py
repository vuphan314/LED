"""Convert an LED parsertree to a TeX program."""

############################################################
"""Import."""

from debugtools.debug_tool import *

############################################################

TEX_TOP = (
    '\\documentclass[14pt]{extarticle}' '\n'
    '\\usepackage{led_pkg}' '\n'
    '\\begin{document}' '\n'
    'LED Engine' '\n'
)
TEX_BOTTOM = '\n' '\\end{document}' '\n'

DEF_LABELS = {
    'funDefNoWhere', 'relDefNoWhere', 'funDefWhere', 'relDefWhere'
}
COND_LABELS = {'tIfBT', 'tOther'}
QUANT_OPS = {'exist', 'univ'}
AGGR_OPS = {
    'setCompr', 'aggrUnn', 'aggrNrsec', 'aggrSum', 'aggrProd'
}
OVERLOADED_OPS = {'pipesOp', 'plusOp', 'starOp'}
BOOL_OPS = {
    'equiv', 'impl', 'disj', 'conj', 'neg', 'eq', 'uneq', 'less', 'greater', 'lessEq', 'greaterEq'
}
AR_OPS = {'uMns', 'bMns', 'div', 'md', 'exp', 'flr', 'clng'}
TUPLE_LABELS = {'tpl', 'tuIn', 'tuSl'}
SET_LABELS = {
    'powSet', 'set', 'setEmpty', 'iv', 'unn', 'diff', 'nrsec', 'sbset', 'setMem', 'symsInSet'
}
PKG_CMDS = (
    DEF_LABELS | COND_LABELS | QUANT_OPS | AGGR_OPS | OVERLOADED_OPS | BOOL_OPS | AR_OPS | TUPLE_LABELS | SET_LABELS
)

FUN_REL_EXPRS = {
    'funT', 'relT', 'symOrNullFunRel', 'nonnullFunRel'
}
MANY_LABELS = {'terms', 'syms'}

############################################################

def weave_top(T) -> str:
    T = change_label(T)
    st = weave_recur(T)
    return surround_str(st, TEX_TOP, TEX_BOTTOM)

def change_label(T):
    if isinstance(T, str):
        return T
    elif T[0] == 'set' and len(T) < 2: # empty
        T2 = ('setEmpty',) + T[1:]
        return change_label(T2)
    elif T[0] == 'tIfBTsO':
        tIfBTs = T[1]
        tOther = T[2]
        T2 = tIfBTs + (tOther,)
        return change_label(T2)
    else:
        return recur_tree(change_label, T)

############################################################

def weave_recur(T) -> str:
    if isinstance(T, str):
        return T
    elif T[0] == 'hashIsGame':
        return ''
    elif T[0] == 'string':
        return '``' + T[1][1:-1] + '"'
    elif T[0] == 'truth':
        return get_cmd('textKeyword', T[1:])
    elif T[0] == 'tIfBTs':
        return weave_tIfBTs(T)
    elif T[0] in MANY_LABELS:
        return weave_many(T[1:])
    elif T[0] in FUN_REL_EXPRS:
        return weave_fun_rel_expr(T)
    elif T[0] in {'funDef', 'relDef'}:
        return weave_def(T)
    elif T[0] in PKG_CMDS:
        return get_cmd(T[0], T[1:])
    else:
        return recur_str(weave_recur, T)

############################################################

def weave_def(T) -> str:
    if len(T) > 3: # where-clause
        postfix = 'Where'
    else:
        postfix = 'NoWhere'
    T = (T[0] + postfix,) + T[1:]
    st = get_env('ledDef', [T])
    return st

def weave_fun_rel_expr(T) -> str:
    if len(T) > 2: # nonnullary
        args = T[2][1:]
    else:
        args = ()
    return weave_call(T[1], args)

def weave_many(args: tuple) -> str:
    st = weave_recur(args[0])
    for arg in args[1:]:
        st += ', ' + weave_recur(arg)
    return st

############################################################

def weave_tIfBTs(T) -> str:
    st = get_env('cases', T[1:])
    return st

def weave_call(func, args: tuple) -> str:
    st = weave_recur(func)
    if args:
        st2 = weave_many(args)
        st2 = get_cmd('parentheses', [st2])
        st += ' ' + st2
    return st

############################################################

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

############################################################

def surround_str(
    inner_str: str, left_str: str, right_str: str
) -> str:
    st = left_str + inner_str + right_str
    return st

############################################################

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
