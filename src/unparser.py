'''
unparse an LED parse-forest (list) into a string which represents a SL program
'''

# unparse: list -> str
def unparse(L):
    T = forestToTree(L)
    st = importLib + unparseRecur(T)
    st = markBeginEnd(st)
    return st

# unparseRecur: tuple -> str
def unparseRecur(T):
    if T[0] == 'atom':
        func = 'a'
        arg = addDoubleQuotes(T[1])
        st = applyUnary(func, arg)
        return st
    if T[0] == 'truth':
        func = 'tr'
        arg = T[1]
        st = applyUnary(func, arg)
        return st
    if T[0] == 'numl':
        func = 'n'
        arg = addDoubleQuotes(T[1])
        st = applyUnary(func, arg)
        return st
    if T[0] == 'id':
        return T[1]
    if T[0] == 'cDef':
        st1 = unparseRecur(T[1])
        st2 = unparseRecur(T[2])
        st = st1 + ' := ' + st2 + ';\n\n'
        return st
    if T[0] in arOps:
        return unparseArOps(T)
    else:
        return recurStr(unparseRecur, T[1:])
        
########## ########## ########## ########## ########## ########## 
'''
unparse arithmetic operations
'''

arOps = {'add', 'biMinus', 'uMinus', 'mult', 'div', 'flr', 'clng', 'ab', 'md', 'exp'}

# unparseArOps: tuple -> str
def unparseArOps(T):
    func = T[0]
    st = applyNaryRecur(func, T[1:])
    return st
    
########## ########## ########## ########## ########## ########## 
'''
helper functions
'''

# applyUnary: str * str -> str
def applyUnary(func, arg):
    func = prependLib(func)
    st = func + '(' + arg + ')'
    return st

# applyNaryRecur: str * tuple -> str
def applyNaryRecur(func, args):
    func = prependLib(func)
    st = func + '(' + unparseRecur(args[0])
    for arg in args[1:]:
        st += ', ' + unparseRecur(arg)
    st += ')'
    return st
    
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
    
########## ########## ########## ########## ########## ########## 
'''
importing and using LED library
'''

libLoc = '../'

libName = 'ledlib'

libAs = ''

importLib = 'import * from "' + libLoc + libName + '.sl" as ' + libAs + '*;\n\n'

# str -> str
def prependLib(st):
    st = libAs + st
    return st

########## ########## ########## ########## ########## ########## 
'''
mark begin and end of output SL program
'''

markerSL = \
'////////// ////////// ////////// ////////// ////////// //////////'

# markBeginEnd: str -> str
def markBeginEnd(st):
    st = markerSL + '\n\n' + st + markerSL
    return st

########## ########## ########## ########## ########## ########## 
'''
transform a parse-forest (list) to a parse-tree (tuple)
'''

# forestToTree: list -> tuple
def forestToTree(L):
    L = ['prog'] + L
    T = listToTuple(L)
    transformed = listToTuple(T)
    return transformed
    
# listToTuple: list -> tuple
def listToTuple(L):
    if type(L) != list:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += listToTuple(l),
        return T
        
########## ########## ########## ########## ########## ########## 

from tester import *
