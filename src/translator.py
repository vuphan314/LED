'''
This translator converts an LED program into a semantically equivalent SL program.
'''

########## ########## ########## ########## ########## ########## ########## ##########

import sys

import parser
import modules.transformer
import modules.unparser

########## ########## ########## ########## ########## ########## ########## ##########

if __name__ == '__main__':
    led = sys.argv[1]
    parsed = parser.parse_file(led)
    transformed = modules.transformer.transform(parsed)
    sl = modules.unparser.unparse(transformed)
    print(sl)
