'''
This translator converts an LED program into a semantically equivalent SL program.
'''

########## ########## ########## ########## ########## ########## ########## ##########

import sys

import ledparser
import modules.transformer
import modules.unparser

########## ########## ########## ########## ########## ########## ########## ##########

def main():
    led = sys.argv[1]
    parsed = ledparser.regparse_file(led)
    transformed = modules.transformer.main(parsed)
    sl = modules.unparser.main(transformed)
    print(sl)

if __name__ == '__main__':
    main()
