#!/usr/bin/python3

"""Copyright (c) 2014, Evgenii Balai
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY EVGENII BALAI "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL EVGENII BALAI OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project."""

# modified by Vu Phan

################################################################################

import sys
sys.path.append('..')
from debugtools.debug_tool import *

from os import path
import re

from genparser.src.astgen.parsing import lexer, parser

from led_tree import *

################################################################################

PRETTY_STR_TAB = ' ' * 2

################################################################################

def parse_file(led_path: str, verbose: bool) -> tuple:
    region_parser = RegionParser(led_path)
    syntax_list = region_parser.get_parsed_elements()
    syntax_list = ['prog'] + syntax_list
    syntax_tree = get_syntax_tree(syntax_list)
    if verbose:
        syntax_str = get_syntax_str(syntax_tree)
        print(syntax_str)
    return syntax_tree

################################################################################

def get_syntax_tree(L: list) -> tuple:
    if type(L) == str:
        return L
    else:
        T = L[0],
        for l in L[1:]:
            T += get_syntax_tree(l),
        return T

def get_syntax_str(T: tuple, tab_count=0) -> str:
    tabs = PRETTY_STR_TAB * tab_count
    st = tabs
    if is_termimal(T):
        st += str(T)
    else:
        st += "('" + T[0] + "'"
        for t in T[1:]:
            st2 = ',\n'
            st2 += get_syntax_str(t, tab_count=tab_count+1)
            st += st2
        st += '\n' + tabs + ')'
    return st

def is_termimal(T: tuple) -> bool:
    boo = isinstance(T, tuple) and len(T) == 2 and isinstance(T[1], str)
    return boo

################################################################################

class RegionParser:
    def __init__(self, led_path: str):
        with open(led_path) as file_object:
            self.prog_str = file_object.read()

        file_names = 'led_lexicon.gen', 'led_grammar.gen'
        lexicon_file, grammar_file = [
            path.join(path.dirname(path.abspath(__file__)), file_name)
            for file_name in file_names
        ]

        self.lexer_instance = lexer.Lexer(lexicon_file)
        self.parser_instance = parser.Parser(
            grammar_file, self.lexer_instance.lexicon_dict.keys()
        )

    def get_parsed_elements(self) -> list:
        # split the program into regions; parse each region
        unparsed_remainder = self.prog_str
        parsed_elements = []
        cur_line = 1
        while True:
            # find the start of the next program region
            region_start = re.search(r'/\$', unparsed_remainder)
            if region_start is None:
                self.append_cmnt_tree(parsed_elements, unparsed_remainder)
                break

            # pre_region is comment
            pre_region = unparsed_remainder[:region_start.start()]
            cur_line += pre_region.count('\n')
            self.append_cmnt_tree(
                parsed_elements, pre_region
            )

            # find the matching end of the program region
            end_delimiter = re.compile(r'\$/')
            region_end = end_delimiter.search(
                unparsed_remainder, region_start.end()
            )
            if region_end is None:
                raise UnmatchedRegion(cur_line)

            # get elements from the found region
            region = unparsed_remainder[region_start.end():region_end.start()]
            parsed_elements.extend(
                self.get_elements_from_region(region, cur_line)
            )
            cur_line += region.count('\n')

            # remove pre_region & region
            # from unparsed_remainder
            unparsed_remainder = unparsed_remainder[region_end.end():]

        return parsed_elements

    def append_cmnt_tree(self, base_list: list, cmnt_str: str) -> None:
        if cmnt_str and not cmnt_str.isspace():
            base_list.append(self.get_cmnt_tree(cmnt_str))

    def get_cmnt_tree(self, cmnt_str: str) -> tuple:
        return CMNT_LABEL, cmnt_str.strip()

    def get_elements_from_region(self, region: str, line_number: int) -> list:
        # obtain lexing_sequence from
        # region (starting at line_number)
        lexing_sequence = self.lexer_instance.get_lexing_sequence(region)

        # obtain ast
        ast = self.parser_instance.get_ast(lexing_sequence)
        if ast is None:
            raise InvalidRegion(line_number, region)

        # return cut_root (list of program elements) of ast
        return ast.children_list()

class ParserError(Exception):
    def __init__(self, line_number: int, contents=''):
        self.contents = contents.strip()
        self.line_number = line_number

    def __str__(self):
        return (
            '\nThe LED program contains '
            'an unmatched/invalid region starting from '
            'line {}:\n{}'.format(self.line_number, self.contents)
        )

class UnmatchedRegion(ParserError):
    pass

class InvalidRegion(ParserError):
    pass

################################################################################

def main():
    if len(sys.argv) == 2:
        led_path = sys.argv[1]
        syntax_dict = parse_file(led_path, verbose=True)
    else:
        print('must provide exactly 1 arg: <led_path>')

if __name__ == '__main__':
    main()
