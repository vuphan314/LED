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

########## ########## ########## ########## ########## ########## 

import os

from genparser.src.astgen.parsing.lexer import *
from genparser.src.astgen.parsing.parser import *

########## ########## ########## ########## ########## ########## 

class RegionParser:
    def __init__(self, program_file):
        """ 
        Read the program file; initialize lexer and parser instances
        """
        with open(program_file) as lf:
            self.program_string = lf.read()

        #initialize lexer and parser
        lexicon_file = \
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "lexicon.txt")
        grammar_file = \
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "grammar.txt")
        self.lexer = Lexer(lexicon_file, False)
        self.parser = Parser(grammar_file, self.lexer.lexicon_dict.keys())
        
    def get_parsed_elements(self):
        """ 
        Get the list of parse trees corresponding to the elements of the given program
        """
        # split the program into regions and parse each region
        all_regions_parsed = False
        parsed_elements = []
        unparsed_program_string = self.program_string
        cur_line = 1
        while not all_regions_parsed: 
            # search for the start of the next program region
            region_start = re.search(r"/\$", unparsed_program_string)
            if region_start is None:
                break
                
            # set cur_line to the line where the region starts
            pre_region = unparsed_program_string[:region_start.start()]
            cur_line += pre_region.count('\n')
            
            # find the matching end of the program region
            end_delimiter = re.compile(r"\$/")
            region_end = \
                end_delimiter.search(unparsed_program_string, region_start.end())
            if region_end is None:
                raise UnmatchedRegion(cur_line)
            
            # get elements from the found region
            region = unparsed_program_string[region_start.end():region_end.start()]
            parsed_elements.extend(self.get_elements_from_region(region, cur_line))

            # update line number by adding the number of lines inside the region
            cur_line += region.count('\n')

            # remove the current pre-region and region from unparsed_program_string
            post_region = unparsed_program_string[region_end.end():]
            unparsed_program_string = post_region
            
        return parsed_elements

    def get_elements_from_region(self, region, line_number):
        # obtain lexing sequence from the region starting at line_number
        lexing_sequence = self.lexer.get_lexing_sequence(region)
        
        # obtain parse tree
        ast = self.parser.get_ast(lexing_sequence)
        if ast is None:
            raise InvalidRegion(region, line_number)
            
        # return cut_root (list of program elements) of the parse tree
        return ast.children_list()

class UnmatchedRegion(Exception):
    def __init__(self, line_number):
        super(UnmatchedRegion, self).__init__()
        self.line_number = line_number

    def __repr__(self):
        return \
            "\n\nThe program file contains an unmatched region starting from line " + \
            str(self.line_number)

    def __str__(self):
        return self.__repr__()


class InvalidRegion(Exception):
    """
    Defines a class for representing exceptions which are thrown in the event of
    a (syntactically) invalid program element in a region
    """

    def __init__(self, contents, line_number):
        super(InvalidRegion, self).__init__()
        self.contents = contents
        self.line_number = line_number

    def __repr__(self):
        return  "\n\nThe program file contains an invalid region " + \
                "starting from line " + str(self.line_number) + ":\n\n" + \
                self.contents + "\n\n"

    def __str__(self):
        return self.__repr__()
