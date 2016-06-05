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

import os
from genparser.src.astgen.parsing.lexer import *
from genparser.src.astgen.parsing.parser import *

class RegionParser:
    """ 
    """

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
        Get the list of parse trees corresponding
        to the elements of the given program
        """

        # split the program into regions
        # call the parser for every region separately
        all_regions_parsed= False
        parsed_elements = []
        unparsed_program_string = self.program_string
        cur_line = 1 
        while not all_regions_parsed: 
            # search for the start of the next program region
            region_start = re.search(r"/\$", unparsed_program_string)
            if region_start is None:
                all_regions_parsed = True
                break
            # set cur_line to the line where the regions start
            cur_line += unparsed_program_string[:region_start.start()].count('\n')

            # find matching end of the program region
            region_end = re.search(r"\$/", unparsed_program_string)

            if region_end.start() is None:
                raise UnmatchedRegionComment(cur_line)

            # get the elements from the found region
            region = unparsed_program_string[  region_start.end() + 1 : \
                                    region_end.start()]
            parsed_elements.extend(self.get_elements_from_region(region, cur_line))

            # update line numbers, add the number of lines inside the region
            cur_line += unparsed_program_string[:region_end.start()].count('\n')

            # remove the region from the beginning of unparsed_program_string
            unparsed_program_string = unparsed_program_string[region_end.end() + 1 :]
        return parsed_elements



    def get_elements_from_region(self, region, line_number):
        # obtain lexing sequence from the region starting at line_number
        lexing_sequence = self.lexer.get_lexing_sequence(region)
        # obtain parse tree
        ast = self.parser.get_ast(lexing_sequence)
        # get the children of the root of the tree (which correspond to program elements)
        if ast is None:
            raise InvalidProgramRegion(region, line_number)
        return ast.children_list()


class UnmatchedRegionComment(Exception):
    """
    Defines a class for representing exceptions which are thrown in the event of
    an invalid lexeme declaration in the lexicon file
    """

    def __init__(self, line_number):
        super(UnmatchedRegionComment, self).__init__()
        self.line_number = line_number

    def __repr__(self):
        return "The program contains " \
               "a region starting from line " \
               "number " + str(self.line_number) + "."\
               "which does not end"

    def __str__(self):
        return self.__repr__()


class InvalidProgramRegion(Exception):
    """
    Defines a class for representing exceptions which are thrown in the event of
    a (syntactically) invalid program element in the program file
    """

    def __init__(self, contents, line_number):
        super(InvalidProgramElement, self).__init__()
        self.contents = contents
        self.line_number = line_number

    def __repr__(self):
        return  "\n\nThe program file contains an invalid program region: \n\n" + \
                self.contents + "\n\n starting from line number " + \
                str(self.line_number) + "."

    def __str__(self):
        return self.__repr__()
