"""LED engine.

Translate an LED program into
a semantically equivalent SL program.
"""

############################################################
"""Import."""

import sys

from debugger import *
import led_parser
import led_translator

############################################################

def main() -> None:
    led = sys.argv[1]
    parsed = led_parser.parse_file(led)
    sl = led_translator.translateTop(parsed)
    if led_translator.isGame:
        sl += getLibsStr()
    print(sl)

############################################################
"""Copy LED library to end of easel output file."""

libName = 'libName.sl'

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
