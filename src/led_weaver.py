"""Convert an LED parsertree to TeX program."""

############################################################

def weave_top(T: tuple) -> str:
    st = weave_recur(T)
    return st

def weave_recur(T: tuple) -> str:
    pass

############################################################

"""
T[0] == 'constDef'

st ==
"""
