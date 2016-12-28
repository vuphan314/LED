"""Convert an LED parsertree to a TeX program."""

############################################################
"""Import."""

from debugtools.debug_tool import *

############################################################

TEX_TOP = '''
\\documentclass{{article}}
\\usepackage{{led_pkg}}
\\begin{{document}}

'''
TEX_BOTTOM = '''
\\end{{document}}
'''

FUN_REL_DEFS = {'funDef', 'relDef'}
FUN_REL_EXPRS = {
    'funT', 'relT', 'symOrNullFunRel', 'nonnullFunRel'
}
PKG_CMDS = FUN_REL_DEFS | FUN_REL_EXPRS

############################################################

def weave_top(T) -> str:
    st = weave_recur(T)
    return TEX_TOP + st + TEX_BOTTOM

############################################################

def weave_recur(T) -> str:
    if isinstance(T, str):
        return T
    elif T[0] in FUN_REL_EXPRS:
        return weave_fun_rel(T)
    elif T[0] in PKG_CMDS:
        return get_cmd_recur(T[0], T[1:])
    else:
        return recur_str(weave_recur, T)

############################################################

def apply_recur(func, args: tuple) -> str:
    st = weave_recur(func)
    if args:
        st2 = weave_recur(args[0])
        for arg in args[1:]:
            st2 += ', ' + weave_recur(arg)
        st2 = get_cmd_recur('parenthesize', [st2])
        st += ' ' + st2
    return st

def get_cmd_recur(cmd_name, cmd_args: tuple) -> str:
    st = '\\' + weave_recur(cmd_name)
    for cmd_arg in cmd_args:
        st2 = weave_recur(cmd_arg)
        st += surround_str(st2, '{', '}')
    if cmd_name in FUN_REL_DEFS:
        st += '\n'
    return st

############################################################

def weave_fun_rel(T) -> str:
    if len(T) == 2: # nullary
        args = ()
    else:
        args = T[2][1:]
    return apply_recur(T[1], args)

############################################################

def surround_str(
    inner_str: str, left_str: str, right_str: str
) -> str:
    st = left_str + inner_str + right_str
    return st

############################################################

def recur_str(F, T) -> str:
    st = ''
    for t in T[1:]:
        st += F(t)
    return st
