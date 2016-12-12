"""
Copyright (c) 2014, Evgenii Balai
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY EVGENII BALAI "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL EVGENII BALAI OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.
"""

# modified by Vu Phan

############################################################

from os import path
import re
import sys

from debugtools.debug_tool import *
from genparser.src.astgen.parsing import lexer, parser

############################################################

LED_STR_TAB = ' ' * 2

############################################################

def parse_file(led_path, quiet=False) -> tuple:
    region_parser = RegionParser(led_path)
    syntax_list = region_parser.get_parsed_elements()
    syntax_list = ['prog'] + syntax_list
    syntax_tree = get_syntax_tree(syntax_list)
    if not quiet:
        syntax_str = get_syntax_str(syntax_tree)
        print(syntax_str)
    return syntax_tree

############################################################

def get_syntax_tree(L: list):
    if type(L) == str:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += get_syntax_tree(l),
        return T

def get_syntax_str(T: tuple, tab_count=1) -> str:
    tabs = LED_STR_TAB * tab_count
    st = tabs
    if is_termimal(T):
        st += str(T)
    else:
        st += "('" + T[0] + "'"
        for t in T[1:]:
            st2 = ',\n'
            st2 += get_syntax_str(
                    t, tab_count=tab_count+1
                )
            st += st2
        st += '\n' + tabs + ')'
    return st

def is_termimal(T: tuple) -> bool:
    boo = (
        isinstance(T, tuple) and
        len(T) > 1 and
        isinstance(T[1], str)
    )
    return boo

############################################################

class RegionParser:
    def __init__(self, led_path):
        with open(led_path) as file_object:
            self.program_str = file_object.read()

        file_names = 'led_lexicon.txt', 'led_grammar.txt'

        lexicon_file, grammar_file = [
            path.join(
                path.dirname(path.abspath(__file__)),
                file_name
            ) for file_name in file_names
        ]

        self.lexer_instance = lexer.Lexer(lexicon_file)

        self.parser_instance = parser.Parser(
            grammar_file,
            self.lexer_instance.lexicon_dict.keys()
        )

    def get_parsed_elements(self):
        # split the program into regions; parse each region
        all_regions_parsed = False
        parsed_elements = []
        unparsed_program_string = self.program_str
        cur_line = 1
        while not all_regions_parsed:
            # search for the start of
            # the next program region
            region_start = re.search(
                r'/\$',
                unparsed_program_string
            )
            if region_start is None:
                break

            # set cur_line to where the region starts
            pre_region = unparsed_program_string[
                :region_start.start()
            ]
            cur_line += pre_region.count('\n')

            # find the matching end of the program region
            end_delimiter = re.compile(r'\$/')
            region_end = end_delimiter.search(
                unparsed_program_string,
                region_start.end()
            )
            if region_end is None:
                raise UnmatchedRegion(cur_line)

            # get elements from the found region
            region = unparsed_program_string[
                region_start.end():
                region_end.start()
            ]

            parsed_elements.extend(
                self.get_elements_from_region(
                    region,
                    cur_line
                )
            )

            # update line number by adding the number of
            # lines inside the region
            cur_line += region.count('\n')

            # remove the current pre-region and
            # region from unparsed_program_string
            post_region = unparsed_program_string[
                region_end.end():
            ]
            unparsed_program_string = post_region

        return parsed_elements

    def get_elements_from_region(self, region, line_number):
        # obtain lexing sequence from
        # the region starting at line_number
        lexing_sequence = (
            self.lexer_instance.get_lexing_sequence(
                region
            )
        )

        # obtain parse tree
        ast = self.parser_instance.get_ast(lexing_sequence)
        if ast is None:
            raise InvalidRegion(region, line_number)

        # return cut_root (list of program elements) of
        # the parse tree
        lis = ast.children_list()
        return lis

class UnmatchedRegion(Exception):
    def __init__(self, line_number):
        super(UnmatchedRegion, self).__init__()
        self.line_number = line_number

    def __repr__(self):
        return '''

The program file contains an unmatched region
starting from line {}

'''.format(self.line_number)

    def __str__(self):
        return self.__repr__()

class InvalidRegion(Exception):
    def __init__(self, contents, line_number):
        super(InvalidRegion, self).__init__()
        self.contents = contents
        self.line_number = line_number

    def __repr__(self):
        return '''

The program file contains an invalid region
starting from line {}:

{}

'''.format(self.line_number, self.contents)

    def __str__(self):
        return self.__repr__()

############################################################

def main():
    led_path = sys.argv[1]
    syntax_dict = parse_file(led_path, quiet=False)

if __name__ == '__main__':
    print()
    main()
