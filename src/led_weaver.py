"""Convert an LED parsertree to a TeX program."""

############################################################
"""Import."""

from debugtools.debug_tool import *

############################################################

TEX_TOP = '''
\\documentclass[14pt]{extarticle}
\\usepackage[scale=0.9]{geometry}
\\usepackage{led_pkg}
\\begin{document}

LED Engine \\bigskip

'''
TEX_BOTTOM = '''
\\end{document}
'''

FUN_REL_DEFS = {'funDef', 'relDef'}
FUN_REL_EXPRS = {
    'funT', 'relT', 'symOrNullFunRel', 'nonnullFunRel'
}
COLLECTIONS = {'tpl'}
MANY = {'terms', 'symbol_s'}
PKG_CMDS = FUN_REL_DEFS | FUN_REL_EXPRS | COLLECTIONS | MANY

############################################################

def weave_top(T) -> str:
    st = weave_recur(T)
    return TEX_TOP + st + TEX_BOTTOM

############################################################

def weave_recur(T) -> str:
    if isinstance(T, str):
        return T
    elif T[0] == 'string':
        return '``' + T[1][1:-1] + '"'
    elif T[0] == 'truth':
        return get_cmd('textKeyword', T[1:])
    elif T[0] in MANY:
        return weave_many(T[1:])
    elif T[0] in FUN_REL_EXPRS:
        return weave_fun_rel_expr(T)
    elif T[0] in PKG_CMDS:
        return get_cmd(T[0], T[1:])
    else:
        return recur_str(weave_recur, T)

############################################################

def get_cmd(cmd_name, cmd_args: tuple) -> str:
    st = '\\' + weave_recur(cmd_name)
    for cmd_arg in cmd_args:
        st2 = weave_recur(cmd_arg)
        st += surround_str(st2, '{', '}')
    if cmd_name in FUN_REL_DEFS:
        st += '\n'
    return st

def apply_recur(func, args: tuple) -> str:
    st = weave_recur(func)
    if args:
        st2 = weave_many(args)
        st2 = get_cmd('parenthesize', [st2])
        st += ' ' + st2
    return st

def weave_many(args: tuple) -> str:
    st = weave_recur(args[0])
    for arg in args[1:]:
        st += ', ' + weave_recur(arg)
    return st

############################################################

def weave_fun_rel_expr(T) -> str:
    if len(T) > 2: # nonnullary
        args = T[2][1:]
    else:
        args = ()
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
