'''
This module transforms an LED parse-forest to a SL parse-tree
'''

########## ########## ########## ########## ########## ########## ########## ##########

from . import helper

########## ########## ########## ########## ########## ########## ########## ##########

def transform(L):
    L = ['prog'] + L
    T = helper.tupleFromList(L)
    transformed = convert(T)
    return transformed
    
def convert(T):
    if type(T) != tuple:
        return T
    else:
        T2 = T[:1]
        for t in T[1:]:
            T2 += convert(t),
        return T2
