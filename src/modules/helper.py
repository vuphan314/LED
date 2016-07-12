'''
This file contains miscellaneous constructs used by other files.
'''

########## ########## ########## ########## ########## ########## 

lexemes = {'id', 'num'}

########## ########## ########## ########## ########## ########## 

# tupleFromList: list -> tuple
def tupleFromList(L):
    if type(L) != list:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += tupleFromList(l),
        return T        
