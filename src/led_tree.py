"""Define labels appearing in an LED parsetree."""

################################################################################

DEF_WHERE_LABELS = {'funDefWhere', 'relDefWhere'}
DEF_LABELS = DEF_WHERE_LABELS | {'funDefNoWhere', 'relDefNoWhere'}

CMNT_LABEL = 'ledCmnt'

################################################################################

def is_led_def(prog_el):
    return prog_el[0] in DEF_LABELS # != CMNT_LABEL
