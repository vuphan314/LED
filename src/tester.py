'''
print test string
'''

# err: raise
def err(mess = 'error message'):
    raise NameError(mess)

# tst: object -> print
def tst(o = 'test string'):
    st = str(o)
    st = markerComment + '\nTEST\n' + st + '\n' + markerComment + '\n'
    print(st)
    
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
