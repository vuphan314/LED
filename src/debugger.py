"""
print test string
"""

# tst: object -> print
def tst(o = 'DEFAULT TEST STRING'):
    st = str(o)
    st = markerComment + '\nTEST\n' + st + '\n' + markerComment + '\n'
    print(st)

############################################################
"""
raise error
"""

# raiseError: raise
def raiseError(o = 'DEFAULT ERROR MESSAGE'):
    raise LedError(o)
err = raiseError

class LedError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return '''

{}
'''.format(self.error_message)

############################################################
"""
mark start and end of wanted string
"""

# markStartEnd: str -> str
def markStartEnd(st):
    st = startComment + st + endComment
    return st

# blockComment: str -> str
def blockComment(st):
    return '/* ' + st + ' */'

markerComment = \
    blockComment('********** ********** ********** ********** ********** **********')

startComment = markerComment + '\n' + blockComment('SECTION START')
endComment = blockComment('SECTION END') + '\n' + markerComment
