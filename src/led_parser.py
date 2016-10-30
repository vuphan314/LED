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

###########################################################

from optparse import OptionParser
from os import path
import re

from genparser.src.astgen.parsing import lexer, parser

###########################################################

def optparse_arguments():
    """Return arguments parsed from sys.argv."""
    optParser = OptionParser()
    return optParser.parse_args()[1]

def parse_file(program_file):
    region_parser = RegionParser(program_file)

    # get the list of program elements
    parsed_file = region_parser.get_parsed_elements()

    parsed_file = ['prog'] + parsed_file
    return parsed_file

def main():
    # read arguments
    args = optparse_arguments()
    program_file = args[0]

    # parse file
    parsed_file = parse_file(program_file)

    return parsed_file

###########################################################

class RegionParser:
    def __init__(self, program_file):
        with open(program_file) as file_object:
            self.program_string = file_object.read()

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
        # split the program into regions and
        # parse each region
        all_regions_parsed = False
        parsed_elements = []
        unparsed_program_string = self.program_string
        cur_line = 1
        while not all_regions_parsed:
            # search for the start of
            # the next program region
            region_start = re.search(
                '/\$',
                unparsed_program_string
            )
            if region_start is None:
                break

            # set cur_line to the line where
            # the region starts
            pre_region = unparsed_program_string[
                :region_start.start()
            ]
            cur_line += pre_region.count('\n')

            # find the matching end of the program region
            end_delimiter = re.compile('\$/')
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
        return ast.children_list()

class UnmatchedRegion(Exception):
    def __init__(self, line_number):
        super(UnmatchedRegion, self).__init__()
        self.line_number = line_number

    def __repr__(self):
        return """

The program file contains an unmatched region
starting from line: {}

'''.format(self.line_number)

    def __str__(self):
        return self.__repr__()

class InvalidRegion(Exception):
    def __init__(self, contents, line_number):
        super(InvalidRegion, self).__init__()
        self.contents = contents
        self.line_number = line_number

    def __repr__(self):
        return """

The program file contains an invalid region
starting from line: {}:

{}

'''.format(self.line_number, self.contents)

    def __str__(self):
        return self.__repr__()

############################################################

if __name__ == '__main__':
    parsed_file = main()
    print(parsed_file)
