'''
This module unparses a SL tree into a string which represents a SL program.
'''

########## ########## ########## ########## ########## ########## ########## ##########

# from tester import *

########## ########## ########## ########## ########## ########## ########## ##########

# main: tuple -> str
def main(T):
    st = importLib + unparse(T)
    st = markBeginEnd(st)
    return st

# unparse: tuple -> str
def unparse(T):
    if T[0] == 'id':
        return T[1]
    if T[0] == 'atom':
        func = 'atmToVal'
        arg = addDoubleQuotes(T[1])
        st = operate(func, arg)
        return st
    if T[0] == 'numl':
        func = 'n'
        arg = addDoubleQuotes(T[1])
        st = operate(func, arg)
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
        
# unparseArOps: tuple -> str
def unparseArOps(T):
    func = T[0]
    st = unparseOperate(func, T[1:])
    return st
    
########## ########## ########## ########## ########## ########## ########## ##########

arOps = {'add', 'biMinus', 'uMinus', 'mult', 'div', 'flr', 'clng', 'ab', 'md', 'exp'}

# operate: str * str -> str
def operate(func, arg):
    func = prependLib(func)
    st = func + '(' + arg + ')'
    return st

# unparseOperate: str * tuple -> str
def unparseOperate(func, args):
    func = prependLib(func)
    st = func + '(' + unparse(args[0])
    for arg in args[1:]:
        st += ', ' + unparse(arg)
    st += ')'
    return st
    
########## ########## ########## ########## ########## ########## ########## ##########

# recurStr: function * tuple -> str
def recurStr(func, tupl):
    st = ''
    for t in tupl:
        st += func(t)
    return st
    
# addDoubleQuotes: str -> str
def addDoubleQuotes(st):
    st = '"' + st + '"'
    return st
    
########## ########## ########## ########## ########## ########## ########## ##########

libName = 'll'

importLib = 'import * from "../' + libName + '.sl" as *;\n\n'

# str -> str
def prependLib(st):
    # st = libName + "::" + st
    return st

########## ########## ########## ########## ########## ########## ########## ##########

marker = \
    '/* ********** ********** ********** ********** ********** ********** ********** */'

# markBeginEnd: str -> str
def markBeginEnd(st):
    st = marker + '\n\n' + st + marker
    return st
