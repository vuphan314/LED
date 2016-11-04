"""LED engine.

Translate an LED program into
a semantically equivalent SL program.
"""

############################################################
"""Import."""

import sys

from vu_toolkit.vu_debugger import *
import led_parser
import led_translator

############################################################

def main() -> None:
    led = sys.argv[1]

    parsed = led_parser.parse_file(led)
    parsed = listToTree(parsed)

    sl = led_translator.translateTop(parsed)
    if led_translator.isGame:
        sl += easelFragment + getLibsStr()

    print(sl)

############################################################

def convert_tuple_to_str(T: tuple, tab_count=1) -> str:
    tabs = tree_tab * tab_count
    st = tabs
    if is_termimal(T):
        st += str(T)
    else:
        st += "('" + T[0] + "'"
        for t in T[1:]:
            st2 = ',\n'
            st2 += convert_tuple_to_str(
                    t, tab_count=tab_count+1
                )
            st += st2
        st += '\n' + tabs + ')'
    return st

tree_tab = ' ' * 4

def is_termimal(T: tuple) -> bool:
    boo = (
        isinstance(T, tuple) and
        len(T) > 1 and
        isinstance(T[1], str)
    )
    return boo

############################################################

def listToTree(L: list):
    if type(L) == str:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += listToTree(l),
        return T

############################################################
"""Copy LED library to end of easel output file."""

libName = 'led_lib.sl'

def getLibsStr() -> str:
    st = ''
    with open(libName) as libFile:
        stLib = libFile.read()
        mess = '''

{}

'''.format(blockComment('BELOW IS A COPY OF ' + libName))
        stLib = mess + stLib + '\n'
        stLib = markStartEnd(stLib) + '\n\n'
        st += stLib
    return st

############################################################

easelFragment = '''

/*
Easel fragment
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

if __name__ == '__main__':
    main()
