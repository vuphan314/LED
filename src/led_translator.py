"""LED-SL translator.

Translate an LED program into
a semantically equivalent SL program.
"""

############################################################
"""Import."""

import sys

from debugger import *
import led_parser
import led_unparser

############################################################

def translate() -> None:
    led = sys.argv[1]
    parsed = led_parser.regparse_file(led)
    sl = led_unparser.unparseTop(parsed)
    if led_unparser.isGame:
        n = 2
        # n = 0 #toggle
        sl += getLibsStr(n)
    print(sl)

############################################################
"""
copy libraries to easel output file
"""

lib = 'lib.sl'
lib2 = 'lib2.sl'
libs = lib, lib2

# getLibsTuple: int -> tuple(str)
def getLibsTuple(n):
    return libs[:n][::-1]

# getLibsStr: int -> str
def getLibsStr(n):
    st = ''
    for l in getLibsTuple(n):
        with open(l) as myLib:
            stLib = myLib.read()
            mess = '\n\n' + blockComment('BELOW IS A COPY OF ' + l) + '\n\n'
            stLib = mess + stLib + '\n'
            stLib = markStartEnd(stLib) + '\n\n'
            st += stLib
    return st

############################################################

easel_lib = '''
/*
Easel library
*/

/* easel required functions */

initialState: State;
initialState :=
    valToState(initialState_);

newState: Input * State -> State;
newState(I, S) :=
    let
        v := newState_(I, S);
    in
        valToState(v);

images: State -> Image(1);
images(S) :=
    let
        v := images_(S);
    in
        valToImages(v);

/* easel default sound */
sounds: Input * State -> char(2);
sounds(I, S) := ["ding"] when I.iClick.clicked else [];
'''

############################################################
"""
initialize
"""

if __name__ == '__main__':
    translate()
