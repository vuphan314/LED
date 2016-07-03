'''
This file contains miscellaneous constructs used by other files
'''

########## ########## ########## ########## ########## ########## ########## ##########

lexemes = {'id', 'num'}

########## ########## ########## ########## ########## ########## ########## ##########

def tupleFromList(L):
    if type(L) != list:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += tupleFromList(l),
        return T
        
########## ########## ########## ########## ########## ########## ########## ##########

def test(S):
    start = '/*'
    end = '*/'
    print(start, S, end, sep = '\n', end = '\n\n')
