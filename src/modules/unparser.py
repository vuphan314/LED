'''
This module unparses a SL tree to a string which represents a SL program.
'''

########## ########## ########## ########## ########## ########## ########## ##########

# from tester import *

########## ########## ########## ########## ########## ########## ########## ##########

# tuple -> str
def main(T):
    st = 'import * from "../' + libName + '.sl" as *;\n\n'
    st += unparse(T)
    return st

# tuple -> str
def unparse(T):
    if T[0] == 'id':
        return T[1]
    if T[0] == 'numl':
        fun = prependLib('n')
        st = fun + '("' + T[1] + '")'
        return st
    if T[0] == 'cDef':
        st1 = unparse(T[1])
        st2 = unparse(T[2])
        st = st1 + ' := ' + st2 + ';\n\n'
        return st
    if T[0] in arOps:
        return unparseArOps(T)
    else:
        return recurStr(unparse, T[1:])
        
# tuple -> str
def unparseArOps(T):
    func = prependLib(T[0])
    st = operate(func, T[1:])
    return st
    
########## ########## ########## ########## ########## ########## ########## ##########

arOps = {'add', 'biMinus', 'uMinus', 'mult', 'div', 'flr', 'clng', 'ab', 'md', 'exp'}

# str * tuple -> str
def operate(func, args):
    st = func + '(' + unparse(args[0])
    for arg in args[1:]:
        st += ', ' + unparse(arg)
    st += ')'
    return st
    
########## ########## ########## ########## ########## ########## ########## ##########

# function * tuple -> str
def recurStr(func, tupl):
    st = ''
    for t in tupl:
        st += func(t)
    return st
    
########## ########## ########## ########## ########## ########## ########## ##########

libName = 'll'

def prependLib(st):
    # st = libName + "::" + st
    return st
