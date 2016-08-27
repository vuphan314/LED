'''
print test string
'''

# tst: object -> print
def tst(o = 'DEFAULT TEST STRING'):
    st = str(o)
    st = markerComment + '\nTEST\n' + st + '\n' + markerComment + '\n'
    print(st)

########## ########## ########## ########## ########## ##########
'''
raise error
'''

# raiseError: raise
def raiseError(o = 'DEFAULT ERROR MESSAGE'):
    st = str(o)
    raise NameError(st)
err = raiseError

########## ########## ########## ########## ########## ##########
'''
mark begin and end of wanted string
'''

markerComment = \
'////////// ////////// ////////// ////////// ////////// //////////'

# markBeginEnd: str -> str
def markBeginEnd(st):
    st = markerComment + '\n\n' + st + markerComment
    return st
