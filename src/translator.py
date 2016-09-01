'''
translate an LED program into a semantically equivalent SL program
'''

########## ########## ########## ########## ########## ##########
'''
importing
'''

import sys

from tester import *

import ledparser
import unparser

########## ########## ########## ########## ########## ##########

# translate: print
def translate(preparsed = False):
    if preparsed:
        parsed = preparsedTree
    else:
        led = sys.argv[1]
        parsed = ledparser.regparse_file(led)
    sl = unparser.unparseTop(parsed)
    if unparser.isGame:
        n = 2
        # n = 0 #toggle
        sl += getLibsStr(n)
    print(sl)

########## ########## ########## ########## ########## ##########
'''
copy libraries to easel output file
'''

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

########## ########## ########## ########## ########## ##########
'''
preparsed tree
'''

preparsedTree = \
['prog', ('hashIsGame', '#isGame'), ['constDef', ['constT', ('id', 'initialState')], ['setT', ['set']]], ['relDef', ['relT', ('id', 'occupies'), ['syms', ['symN', ('id', 'p')], ['symN', ('id', 'c')]]], ['boolT', ['setMem', ['tupT', ['tup', ['terms', ['userSC', ('id', 'p')], ['userSC', ('id', 'c')]]]], ['setT', ['setUT', ['userSC', ('id', 'currentState')]]]]]], ['relDef', ['relT', ('id', 'occupied'), ['syms', ['symN', ('id', 'c')]]], ['boolT', ['disj', ['boolUT', ['userFR', ('id', 'occupies'), ['terms', ['atomT', ('atom', '`x')], ['userSC', ('id', 'c')]]]], ['boolUT', ['userFR', ('id', 'occupies'), ['terms', ['atomT', ('atom', '`o')], ['userSC', ('id', 'c')]]]]]]], ['constDef', ['constT', ('id', 'rows')], ['setT', ['unn', ['unn', ['setUT', ['userSC', ('id', 'hRows')]], ['setUT', ['userSC', ('id', 'vRows')]]], ['setUT', ['userSC', ('id', 'diagonals')]]]], ['boolT', ['conj', ['conj', ['eq', ['userSC', ('id', 'hRows')], ['setT', ['set', ['terms', ['setT', ['set', ['terms', ['arT', ('numl', '1')], ['arT', ('numl', '2')], ['arT', ('numl', '3')]]]], ['setT', ['set', ['terms', ['arT', ('numl', '4')], ['arT', ('numl', '5')], ['arT', ('numl', '6')]]]], ['setT', ['set', ['terms', ['arT', ('numl', '7')], ['arT', ('numl', '8')], ['arT', ('numl', '9')]]]]]]]], ['eq', ['userSC', ('id', 'vRows')], ['setT', ['set', ['terms', ['setT', ['set', ['terms', ['arT', ('numl', '1')], ['arT', ('numl', '4')], ['arT', ('numl', '7')]]]], ['setT', ['set', ['terms', ['arT', ('numl', '2')], ['arT', ('numl', '5')], ['arT', ('numl', '8')]]]], ['setT', ['set', ['terms', ['arT', ('numl', '3')], ['arT', ('numl', '6')], ['arT', ('numl', '9')]]]]]]]]], ['eq', ['userSC', ('id', 'diagonals')], ['setT', ['set', ['terms', ['setT', ['set', ['terms', ['arT', ('numl', '1')], ['arT', ('numl', '5')], ['arT', ('numl', '9')]]]], ['setT', ['set', ['terms', ['arT', ('numl', '3')], ['arT', ('numl', '5')], ['arT', ('numl', '7')]]]]]]]]]]], ['relDef', ['relT', ('id', 'threeInRow'), ['syms', ['symN', ('id', 'p')]]], ['boolT', ['exist', ['symsInSet', ['syms', ['symN', ('id', 'R')]], ['setT', ['setUT', ['userSC', ('id', 'rows')]]]], ['univ', ['symsInSet', ['syms', ['symN', ('id', 'c')]], ['setT', ['setUT', ['userSC', ('id', 'R')]]]], ['boolUT', ['userFR', ('id', 'occupies'), ['terms', ['userSC', ('id', 'p')], ['userSC', ('id', 'c')]]]]]]]], ['constDef', ['constT', ('id', 'boardFull')], ['boolT', ['eq', ['arT', ['pipesOp', ['arT', ['arUT', ['userSC', ('id', 'currentState')]]]]], ['arT', ('numl', '9')]]]], ['constDef', ['constT', ('id', 'gameOver')], ['boolT', ['disj', ['disj', ['boolUT', ['userSC', ('id', 'boardFull')]], ['boolUT', ['userFR', ('id', 'threeInRow'), ['terms', ['atomT', ('atom', '`x')]]]]], ['boolUT', ['userFR', ('id', 'threeInRow'), ['terms', ['atomT', ('atom', '`o')]]]]]]], ['constDef', ['constT', ('id', 'playerToMove')], ['tIfBTsO', ['tIfBTs', ['tIfBT', ['atomT', ('atom', '`x')], ['boolT', ['boolUT', ['userFR', ('id', 'even'), ['terms', ['arT', ['pipesOp', ['arT', ['arUT', ['userSC', ('id', 'currentState')]]]]]]]]]]], ['tOther', ['atomT', ('atom', '`o')]]]], ['relDef', ['relT', ('id', 'even'), ['syms', ['symN', ('id', 'n')]]], ['boolT', ['eq', ['arT', ['md', ['arUT', ['userSC', ('id', 'n')]], ('numl', '2')]], ['arT', ('numl', '0')]]]], ['relDef', ['relT', ('id', 'legalToMoveIn'), ['syms', ['symN', ('id', 'c')]]], ['boolT', ['conj', ['neg', ['boolUT', ['userFR', ('id', 'occupied'), ['terms', ['userSC', ('id', 'c')]]]]], ['neg', ['boolUT', ['userSC', ('id', 'gameOver')]]]]]], ['constDef', ['constT', ('id', 'BLACK')], ['userFR', ('id', 'color'), ['terms', ['arT', ('numl', '0')], ['arT', ('numl', '0')], ['arT', ('numl', '0')]]]], ['constDef', ['constT', ('id', 'WHITE')], ['userFR', ('id', 'color'), ['terms', ['arT', ('numl', '255')], ['arT', ('numl', '255')], ['arT', ('numl', '255')]]]], ['constDef', ['constT', ('id', 'BLUE')], ['userFR', ('id', 'color'), ['terms', ['arT', ('numl', '0')], ['arT', ('numl', '0')], ['arT', ('numl', '255')]]]], ['constDef', ['constT', ('id', 'GREEN')], ['userFR', ('id', 'color'), ['terms', ['arT', ('numl', '0')], ['arT', ('numl', '255')], ['arT', ('numl', '0')]]]], ['constDef', ['constT', ('id', 'RED')], ['userFR', ('id', 'color'), ['terms', ['arT', ('numl', '255')], ['arT', ('numl', '0')], ['arT', ('numl', '0')]]]], ['constDef', ['constT', ('id', 'gridDisplay')], ['setT', ['set', ['terms', ['userSC', ('id', 'L1')], ['userSC', ('id', 'L2')], ['userSC', ('id', 'L3')], ['userSC', ('id', 'L4')]]]], ['boolT', ['conj', ['conj', ['conj', ['eq', ['userSC', ('id', 'L1')], ['userFR', ('id', 'segment'), ['terms', ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '200')], ['arT', ('numl', '700')]]], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '200')], ['arT', ('numl', '400')]]], ['userSC', ('id', 'BLACK')]]]], ['eq', ['userSC', ('id', 'L2')], ['userFR', ('id', 'segment'), ['terms', ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '300')], ['arT', ('numl', '700')]]], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '300')], ['arT', ('numl', '400')]]], ['userSC', ('id', 'BLACK')]]]]], ['eq', ['userSC', ('id', 'L3')], ['userFR', ('id', 'segment'), ['terms', ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '100')], ['arT', ('numl', '600')]]], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '400')], ['arT', ('numl', '600')]]], ['userSC', ('id', 'BLACK')]]]]], ['eq', ['userSC', ('id', 'L4')], ['userFR', ('id', 'segment'), ['terms', ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '100')], ['arT', ('numl', '500')]]], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '400')], ['arT', ('numl', '500')]]], ['userSC', ('id', 'BLACK')]]]]]]], ['constDef', ['constT', ('id', 'fontSize')], ['arT', ('numl', '36')]], ['funDef', ['funT', ('id', 'centerX'), ['syms', ['symN', ('id', 'c')]]], ['arT', ['plusOp', ('numl', '150'), ['starOp', ('numl', '100'), ['arT', ['md', ['arT', ['bMns', ['arUT', ['userSC', ('id', 'c')]], ('numl', '1')]], ('numl', '3')]]]]]], ['funDef', ['funT', ('id', 'centerY'), ['syms', ['symN', ('id', 'c')]]], ['arT', ['bMns', ('numl', '650'), ['starOp', ('numl', '100'), ['arT', ['flr', ['arT', ['div', ['arT', ['bMns', ['arUT', ['userSC', ('id', 'c')]], ('numl', '1')]], ('numl', '3')]]]]]]]], ['funDef', ['funT', ('id', 'xImage'), ['syms', ['symN', ('id', 'c')]]], ['userFR', ('id', 'text'), ['terms', ['strT', ('string', '"x"')], ['userFR', ('id', 'point'), ['terms', ['userFR', ('id', 'centerX'), ['terms', ['userSC', ('id', 'c')]]], ['userFR', ('id', 'centerY'), ['terms', ['userSC', ('id', 'c')]]]]], ['userSC', ('id', 'fontSize')], ['userSC', ('id', 'BLUE')]]]], ['funDef', ['funT', ('id', 'oImage'), ['syms', ['symN', ('id', 'c')]]], ['userFR', ('id', 'text'), ['terms', ['strT', ('string', '"o"')], ['userFR', ('id', 'point'), ['terms', ['userFR', ('id', 'centerX'), ['terms', ['userSC', ('id', 'c')]]], ['userFR', ('id', 'centerY'), ['terms', ['userSC', ('id', 'c')]]]]], ['userSC', ('id', 'fontSize')], ['userSC', ('id', 'GREEN')]]]], ['funDef', ['funT', ('id', 'cellDisplay'), ['syms', ['symN', ('id', 'c')]]], ['tIfBTsO', ['tIfBTs', ['tIfBT', ['setT', ['set', ['terms', ['userFR', ('id', 'xImage'), ['terms', ['userSC', ('id', 'c')]]]]]], ['boolT', ['setMem', ['tupT', ['tup', ['terms', ['atomT', ('atom', '`x')], ['userSC', ('id', 'c')]]]], ['setT', ['setUT', ['userSC', ('id', 'currentState')]]]]]], ['tIfBT', ['setT', ['set', ['terms', ['userFR', ('id', 'oImage'), ['terms', ['userSC', ('id', 'c')]]]]]], ['boolT', ['setMem', ['tupT', ['tup', ['terms', ['atomT', ('atom', '`o')], ['userSC', ('id', 'c')]]]], ['setT', ['setUT', ['userSC', ('id', 'currentState')]]]]]]], ['tOther', ['setT', ['set']]]]], ['constDef', ['constT', ('id', 'gameBoard')], ['setT', ['iv', ['arT', ('numl', '1')], ['arT', ('numl', '9')]]]], ['constDef', ['constT', ('id', 'cellDisplays')], ['setT', ['aggrUnn', ['boolT', ['setMem', ['userSC', ('id', 'c')], ['setT', ['setUT', ['userSC', ('id', 'gameBoard')]]]]], ['setUT', ['userFR', ('id', 'cellDisplay'), ['terms', ['userSC', ('id', 'c')]]]]]]], ['constDef', ['constT', ('id', 'currentPlayerDisplay')], ['tIfBTsO', ['tIfBTs', ['tIfBT', ['setT', ['set', ['terms', ['userFR', ('id', 'text'), ['terms', ['strT', ('string', '"x\'s turn"')], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '100')], ['arT', ('numl', '750')]]], ['userSC', ('id', 'fontSize')], ['userSC', ('id', 'BLACK')]]]]]], ['boolT', ['eq', ['userSC', ('id', 'playerToMove')], ['atomT', ('atom', '`x')]]]]], ['tOther', ['setT', ['set', ['terms', ['userFR', ('id', 'text'), ['terms', ['strT', ('string', '"o\'s turn"')], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '100')], ['arT', ('numl', '750')]]], ['userSC', ('id', 'fontSize')], ['userSC', ('id', 'BLACK')]]]]]]]]], ['constDef', ['constT', ('id', 'restartLeft')], ['arT', ('numl', '350')]], ['constDef', ['constT', ('id', 'restartRight')], ['arT', ('numl', '550')]], ['constDef', ['constT', ('id', 'restartBottom')], ['arT', ('numl', '725')]], ['constDef', ['constT', ('id', 'restartTop')], ['arT', ('numl', '775')]], ['constDef', ['constT', ('id', 'restartBottomLeftPoint')], ['userFR', ('id', 'point'), ['terms', ['userSC', ('id', 'restartLeft')], ['userSC', ('id', 'restartBottom')]]]], ['constDef', ['constT', ('id', 'restartBottomRightPoint')], ['userFR', ('id', 'point'), ['terms', ['userSC', ('id', 'restartRight')], ['userSC', ('id', 'restartBottom')]]]], ['constDef', ['constT', ('id', 'restartTopLeftPoint')], ['userFR', ('id', 'point'), ['terms', ['userSC', ('id', 'restartLeft')], ['userSC', ('id', 'restartTop')]]]], ['constDef', ['constT', ('id', 'restartTopRightPoint')], ['userFR', ('id', 'point'), ['terms', ['userSC', ('id', 'restartRight')], ['userSC', ('id', 'restartTop')]]]], ['funDef', ['funT', ('id', 'mid'), ['syms', ['symN', ('id', 'a')], ['symN', ('id', 'b')]]], ['arT', ['div', ['arT', ['plusOp', ['arUT', ['userSC', ('id', 'a')]], ['arUT', ['userSC', ('id', 'b')]]]], ('numl', '2')]]], ['constDef', ['constT', ('id', 'restartMidX')], ['userFR', ('id', 'mid'), ['terms', ['userSC', ('id', 'restartLeft')], ['userSC', ('id', 'restartRight')]]]], ['constDef', ['constT', ('id', 'restartMidY')], ['userFR', ('id', 'mid'), ['terms', ['userSC', ('id', 'restartBottom')], ['userSC', ('id', 'restartTop')]]]], ['constDef', ['constT', ('id', 'restartButton')], ['setT', ['set', ['terms', ['userSC', ('id', 'A1')], ['userSC', ('id', 'A2')], ['userSC', ('id', 'A3')], ['userSC', ('id', 'A4')], ['userSC', ('id', 'txt')]]]], ['boolT', ['conj', ['conj', ['conj', ['conj', ['eq', ['userSC', ('id', 'A1')], ['userFR', ('id', 'segment'), ['terms', ['userSC', ('id', 'restartBottomLeftPoint')], ['userSC', ('id', 'restartBottomRightPoint')], ['userSC', ('id', 'BLACK')]]]], ['eq', ['userSC', ('id', 'A2')], ['userFR', ('id', 'segment'), ['terms', ['userSC', ('id', 'restartTopLeftPoint')], ['userSC', ('id', 'restartTopRightPoint')], ['userSC', ('id', 'BLACK')]]]]], ['eq', ['userSC', ('id', 'A3')], ['userFR', ('id', 'segment'), ['terms', ['userSC', ('id', 'restartBottomLeftPoint')], ['userSC', ('id', 'restartTopLeftPoint')], ['userSC', ('id', 'BLACK')]]]]], ['eq', ['userSC', ('id', 'A4')], ['userFR', ('id', 'segment'), ['terms', ['userSC', ('id', 'restartBottomRightPoint')], ['userSC', ('id', 'restartTopRightPoint')], ['userSC', ('id', 'BLACK')]]]]], ['eq', ['userSC', ('id', 'txt')], ['userFR', ('id', 'text'), ['terms', ['strT', ('string', '"restart"')], ['userFR', ('id', 'point'), ['terms', ['userSC', ('id', 'restartMidX')], ['userSC', ('id', 'restartMidY')]]], ['userSC', ('id', 'fontSize')], ['userSC', ('id', 'BLACK')]]]]]]], ['constDef', ['constT', ('id', 'gameResultDisplay')], ['tIfBTsO', ['tIfBTs', ['tIfBT', ['setT', ['set', ['terms', ['userFR', ('id', 'text'), ['terms', ['strT', ('string', '"x won"')], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '200')], ['arT', ('numl', '750')]]], ['userSC', ('id', 'fontSize')], ['userSC', ('id', 'BLUE')]]]]]], ['boolT', ['boolUT', ['userFR', ('id', 'threeInRow'), ['terms', ['atomT', ('atom', '`x')]]]]]], ['tIfBT', ['setT', ['set', ['terms', ['userFR', ('id', 'text'), ['terms', ['strT', ('string', '"o won"')], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '200')], ['arT', ('numl', '750')]]], ['userSC', ('id', 'fontSize')], ['userSC', ('id', 'GREEN')]]]]]], ['boolT', ['boolUT', ['userFR', ('id', 'threeInRow'), ['terms', ['atomT', ('atom', '`o')]]]]]]], ['tOther', ['setT', ['set', ['terms', ['userFR', ('id', 'text'), ['terms', ['strT', ('string', '"cat got it"')], ['userFR', ('id', 'point'), ['terms', ['arT', ('numl', '200')], ['arT', ('numl', '750')]]], ['userSC', ('id', 'fontSize')], ['userSC', ('id', 'RED')]]]]]]]]], ['constDef', ['constT', ('id', 'images')], ['tIfBTsO', ['tIfBTs', ['tIfBT', ['userSC', ('id', 'gameOverDisplay')], ['boolT', ['boolUT', ['userSC', ('id', 'gameOver')]]]]], ['tOther', ['userSC', ('id', 'inPlayDisplay')]]], ['boolT', ['conj', ['conj', ['eq', ['userSC', ('id', 'alwaysDisplay')], ['setT', ['unn', ['unn', ['setUT', ['userSC', ('id', 'gridDisplay')]], ['setUT', ['userSC', ('id', 'cellDisplays')]]], ['setUT', ['userSC', ('id', 'restartButton')]]]]], ['eq', ['userSC', ('id', 'inPlayDisplay')], ['setT', ['unn', ['setUT', ['userSC', ('id', 'alwaysDisplay')]], ['setUT', ['userSC', ('id', 'currentPlayerDisplay')]]]]]], ['eq', ['userSC', ('id', 'gameOverDisplay')], ['setT', ['unn', ['setUT', ['userSC', ('id', 'alwaysDisplay')]], ['setUT', ['userSC', ('id', 'gameResultDisplay')]]]]]]]], ['funDef', ['funT', ('id', 'xMin'), ['syms', ['symN', ('id', 'c')]]], ['arT', ['plusOp', ('numl', '100'), ['starOp', ('numl', '100'), ['arT', ['md', ['arT', ['bMns', ['arUT', ['userSC', ('id', 'c')]], ('numl', '1')]], ('numl', '3')]]]]]], ['funDef', ['funT', ('id', 'xMax'), ['syms', ['symN', ('id', 'c')]]], ['arT', ['plusOp', ('numl', '200'), ['starOp', ('numl', '100'), ['arT', ['md', ['arT', ['bMns', ['arUT', ['userSC', ('id', 'c')]], ('numl', '1')]], ('numl', '3')]]]]]], ['funDef', ['funT', ('id', 'yMin'), ['syms', ['symN', ('id', 'c')]]], ['arT', ['bMns', ('numl', '600'), ['starOp', ('numl', '100'), ['arT', ['flr', ['arT', ['div', ['arT', ['bMns', ['arUT', ['userSC', ('id', 'c')]], ('numl', '1')]], ('numl', '3')]]]]]]]], ['funDef', ['funT', ('id', 'yMax'), ['syms', ['symN', ('id', 'c')]]], ['arT', ['bMns', ('numl', '700'), ['starOp', ('numl', '100'), ['arT', ['flr', ['arT', ['div', ['arT', ['bMns', ['arUT', ['userSC', ('id', 'c')]], ('numl', '1')]], ('numl', '3')]]]]]]]], ['relDef', ['relT', ('id', 'cellClicked'), ['syms', ['symN', ('id', 'c')]]], ['boolT', ['conj', ['conj', ['conj', ['conj', ['boolUT', ['userSC', ('id', 'mouseClicked')]], ['greater', ['arT', ['arUT', ['userSC', ('id', 'mouseX')]]], ['arT', ['arUT', ['userFR', ('id', 'xMin'), ['terms', ['userSC', ('id', 'c')]]]]]]], ['less', ['arT', ['arUT', ['userSC', ('id', 'mouseX')]]], ['arT', ['arUT', ['userFR', ('id', 'xMax'), ['terms', ['userSC', ('id', 'c')]]]]]]], ['greater', ['arT', ['arUT', ['userSC', ('id', 'mouseY')]]], ['arT', ['arUT', ['userFR', ('id', 'yMin'), ['terms', ['userSC', ('id', 'c')]]]]]]], ['less', ['arT', ['arUT', ['userSC', ('id', 'mouseY')]]], ['arT', ['arUT', ['userFR', ('id', 'yMax'), ['terms', ['userSC', ('id', 'c')]]]]]]]]], ['constDef', ['constT', ('id', 'restartClicked')], ['boolT', ['conj', ['conj', ['conj', ['conj', ['boolUT', ['userSC', ('id', 'mouseClicked')]], ['greater', ['arT', ['arUT', ['userSC', ('id', 'mouseX')]]], ['arT', ['arUT', ['userSC', ('id', 'restartLeft')]]]]], ['less', ['arT', ['arUT', ['userSC', ('id', 'mouseX')]]], ['arT', ['arUT', ['userSC', ('id', 'restartRight')]]]]], ['greater', ['arT', ['arUT', ['userSC', ('id', 'mouseY')]]], ['arT', ['arUT', ['userSC', ('id', 'restartBottom')]]]]], ['less', ['arT', ['arUT', ['userSC', ('id', 'mouseY')]]], ['arT', ['arUT', ['userSC', ('id', 'restartTop')]]]]]]], ['relDef', ['relT', ('id', 'moveMadeIn'), ['syms', ['symN', ('id', 'c')]]], ['boolT', ['conj', ['boolUT', ['userFR', ('id', 'cellClicked'), ['terms', ['userSC', ('id', 'c')]]]], ['boolUT', ['userFR', ('id', 'legalToMoveIn'), ['terms', ['userSC', ('id', 'c')]]]]]]], ['constDef', ['constT', ('id', 'movesMade')], ['setT', ['setCompr', ['tupT', ['tup', ['terms', ['userSC', ('id', 'playerToMove')], ['userSC', ('id', 'c')]]]], ['boolT', ['conj', ['setMem', ['userSC', ('id', 'c')], ['setT', ['setUT', ['userSC', ('id', 'gameBoard')]]]], ['boolUT', ['userFR', ('id', 'moveMadeIn'), ['terms', ['userSC', ('id', 'c')]]]]]]]]], ['constDef', ['constT', ('id', 'newState')], ['tIfBTsO', ['tIfBTs', ['tIfBT', ['userSC', ('id', 'initialState')], ['boolT', ['boolUT', ['userSC', ('id', 'restartClicked')]]]]], ['tOther', ['setT', ['unn', ['setUT', ['userSC', ('id', 'currentState')]], ['setUT', ['userSC', ('id', 'movesMade')]]]]]]]]

########## ########## ########## ########## ########## ##########
'''
initialize
'''

if __name__ == '__main__':
    preparsed = False

    preparsed = True #toggle

    translate(preparsed = preparsed)
