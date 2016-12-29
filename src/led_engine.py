"""LED engine.

Translate an LED program into
a semantically equivalent SL program.
"""

############################################################
"""Import."""

import argparse
import os
import sys
import time

from debugtools.debug_tool import *
import led_parser
import led_translator
import led_weaver

############################################################

def write_output_files(led_path: str, force: bool) -> None:
    syntax_tree = led_parser.parse_file(led_path, quiet=True)
    sl_path, tex_path = [
        append_base_path(led_path, ext)
        for ext in ['.sl', '.tex']
    ]
    # write_sl(syntax_tree, sl_path, force) #todo
    write_tex(syntax_tree, tex_path, force)

def write_sl(
    syntax_tree: tuple, sl_path: str, force: bool
) -> None:
    sl_str = led_translator.translateTop(syntax_tree)
    write_output_str(sl_str, sl_path, force)

def write_tex(
    syntax_tree: tuple, tex_path: str, force: bool
) -> None:
    tex_str = led_weaver.weave_top(syntax_tree)
    write_output_str(tex_str, tex_path, force)

def write_output_str(
    output_str: str, output_path: str, force: bool
) -> None:
    write_mode = 'w' if force else 'x'
    with open(output_path, write_mode) as output_file:
        output_file.write(output_str)

def append_base_path(
    led_path: str, base_appendage: str
) -> str:
    base_path = os.path.splitext(led_path)[0]
    appended_path = base_path + base_appendage
    return appended_path

############################################################

class ArgvParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument('LED_file')
        self.add_argument(
            '-f', '--force', action='store_true',
            help='OVERWRITE existing .sl and .tex files'
        )

############################################################

def main() -> None:
    time_start = time.time()
    argv_parser = ArgvParser()
    if len(sys.argv) == 1:
        argv_parser.print_help()
    else:
        parsed_argv = argv_parser.parse_args()
        led_path = parsed_argv.LED_file
        force = parsed_argv.force
        write_output_files(led_path, force)
    time_taken = int(time.time() - time_start)
    print(
        '\n' 'LED engine took: {} secs.\n'.format(
            time_taken
        )
    )

if __name__ == '__main__':
    main()
