'''
This file contains constructs for testing.
'''

########## ########## ########## ########## ########## ########## ########## ##########

# test: str -> print
def test(S):
    startD = '/*'
    endD = '*/'
    print(startD, S, endD, sep = '\n', end = '\n\n')
