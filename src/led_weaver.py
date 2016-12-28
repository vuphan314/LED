"""Convert an LED parsertree to a TeX program."""

############################################################

PKG_CMDS = {'funDef', 'relDef'}

############################################################

def weave_top(T) -> str:
    st = weave_recur(T)
    return st

############################################################

def weave_recur(T) -> str:
    if isinstance(T, str):
        return T
    elif T[0] in {'funT', 'relT'}:
        return apply_recur(T[1], T[2:])
    elif T[0] in PKG_CMDS:
        return get_cmd_recur(T[1], T[2:])
    else:
        return recur_str(weave_recur, T)

############################################################

def get_cmd_recur(cmd_name, cmd_args: tuple) -> str:
    st = '\\' + weave_recur(cmd_name)
    for cmd_arg in cmd_args:
        st2 = weave_recur(cmd_arg)
        st += surround_str(st2, '{', '}')
    st = surround_str(st, '{', '}')
    return st

def apply_recur(func, args: tuple) -> str:
    st = weave_recur(func)
    if args:
        st2 = weave_recur(args[0])
        for arg in args[1:]:
            st2 += ', ' + weave_recur(arg)
        st += parenthesize_str(st2)
    return st

############################################################

def parenthesize_str(inner_str: str) -> str:
    st = surround_str(inner_str, '\\left(', '\\right)')
    return st

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
