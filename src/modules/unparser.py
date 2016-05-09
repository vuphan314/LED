'''
This module unparses a SL tree to a string which represents a SL program
'''

########## ########## ########## ########## ########## ########## ########## ##########

def unparse(T):
    imp = 'import "../' + libName + '.sl";\n\n'
    prog = convert(T)
    return imp + prog

def convert(T):
    if T[0] == 'id':
        return T[1]
    elif T[0] == 'num':
        ret = prependLib('numeral') + '("' + T[1] + '")'
        return ret
    elif T[0] == 'funDef':
        st1 = convert(T[1])
        st2 = convert(T[2])
        return st1 + ' := ' + st2 + ';\n\n'
        return ret
    elif T[0] in arOps:
        return unparseArOps(T)
    else:
        return recurStr(T[0], T[1:], convert)
        
def unparseArOps(T):    
    ret = prependLib(arOps[T[0]])
    ret += '(' + convert(T[1])
    if len(T) == 3:
        ret += ', ' + convert(T[2])
    ret += ')'    
    return ret
    
########## ########## ########## ########## ########## ########## ########## ##########

def recurStr(head, tail, func):
    # print(head)
    st = ''
    for t in tail:
        st += func(t)
    return st
    
########## ########## ########## ########## ########## ########## ########## ##########

arOps = {'exp': 'exp'}

libName = 'lib'

def prependLib(st):
    return libName + "::" + st
