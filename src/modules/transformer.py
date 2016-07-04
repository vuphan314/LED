'''
This module transforms an LED parse-forest to a SL parse-tree.
'''

########## ########## ########## ########## ########## ########## ########## ##########

from . import helper

########## ########## ########## ########## ########## ########## ########## ##########

def main(L):
    L = ['prog'] + L
    T = helper.tupleFromList(L)
    transformed = transform(T)
    return transformed
    
def transform(T):
    if type(T) != tuple:
        return T
    else:
        T2 = T[:1]
        for t in T[1:]:
            T2 += transform(t),
        return T2
