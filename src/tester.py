'''
print test string
'''

# test: object -> print
def test(o):
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
