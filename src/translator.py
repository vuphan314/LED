'''
translate an LED program into a semantically equivalent SL program
'''

########## ########## ########## ########## ########## ########## 

import sys

import ledparser
import unparser

########## ########## ########## ########## ########## ########## 

# translate: print
def translate():
    led = sys.argv[1]
    parsed = ledparser.regparse_file(led)
    sl = unparser.unparse(parsed)
    print(sl)

if __name__ == '__main__':
    translate()
