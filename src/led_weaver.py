"""Convert an LED parsertree to a TeX program."""

############################################################

PKG_CMDS = {'funDef', 'relDef'}

############################################################

def weave_top(T: tuple) -> str:
    st = weave_recur(T)
    return st

############################################################

def weave_recur(T: tuple) -> str:
    if isinstance(T, str):
        return T
    elif T[0] in {'funT', 'relT'}:
        pass
    elif T[0] in PKG_CMDS:
        cmd_name = T[0]
        cmd_args = map(weave_recur, T[1:])
        cmd = get_cmd(cmd_name, cmd_args)
        return cmd
    else:
        return recur_str(weave_recur, T)

############################################################

def get_cmd(cmd_name: str, cmd_args: tuple) -> str:
    st = '\\' + cmd_name
    for cmd_arg in cmd_args:
        st2 = surround_str(cmd_arg, '{', '}')
        st += st2
    st = surround_str(st, '{', '}')
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

def recur_str(F: 'function', T: tuple) -> str:
    st = ''
    for t in T[1:]:
        st += F(t)
    return st
