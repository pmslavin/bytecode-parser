import ply.lex
import ply.yacc
import dis
import copy

from pprint import pprint
from bytecode import CodeLine

"""
EBNF for Python bytecode as output by dis, with
lineno and offset made optional...

    code_object	::=	lines
    lines		::=	line NEWLINE lines
    line		::=	prefix OPNAME operand?
    prefix		::=	lineno? offset
    offset		::=	NUMBER
    NUMBER		::=	[0-9]
                |	[1-9][0-9]+

    lineno		::=	[1-9]+
    operand		::=	NUMBER OPERAND_DISPLAY?
    OPERAND_DISPLAY	::=	'(' \w+ ')'
    OPNAME		::=	[ n for n in dis.opname ]
"""

def parse_bytecode(src):

    tokens = ('NUMBER', 'OPNAME', 'OPERAND_DISPLAY', 'NEWLINE')
    t_ignore = " \t"
    t_ignore_CHEVRONS = r">>"

    def t_error(t):
        raise SyntaxError("Unknown symbol '{0}': line {1}".format(t.value.split()[0], t.lexer.lineno))
        print "Skipping", repr(t.value[0])
        t.lexer.skip(1)

    def t_NEWLINE(t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        return t

    def t_NUMBER(t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_OPNAME(t):
        return t

# Generatated 'regex' for token match
    t_OPNAME.__doc__ = "|".join(dis.opmap.keys())

    def t_OPERAND_DISPLAY(t):
        r"\(.+\)"
        t.value = t.value[1:-1]
        return t

    def p_error(p):
        print("Parse error: {0}".format(p))
        raise ValueError("Syntax error, line {0}: {1}".format(p.lineno + 1, p.type))

    def p_CODE_OBJECT(p):
        """code_object	:	lines"""
        p[0] = p[1]

    def p_LINES(p):
        """lines	:	line NEWLINE lines
                    |	line"""

        if len(p) == 4:
            if p[1]:
                p[0] =  [p[1]] + p[3] 
            else:
                p[0] = p[3]
        elif len(p) == 2:
            if p[1]:
                p[0] = [p[1]]
            else:
                p[0] = []

    def p_PREFIX(p):
        """prefix	: lineno offset
                    | offset"""

        if len(p) == 3:
            p[0] = [ p[1], p[2] ]
        elif len(p) == 2:
            p[0] = [p[1]]

    def p_LINENO(p):
        """lineno	: NUMBER"""

        p[0] = p[1]

    def p_LINE(p):
        """line		: prefix OPNAME operand
                    | prefix OPNAME
                    | """

        if len(p) == 4:
            p[0] = CodeLine(p[1], p[2], p[3])
#           p[0] = [ p[1], p[2], p[3] ]
        elif len(p) == 3:
            p[0] = CodeLine(p[1], p[2])
#           p[0] = [ p[1], p[2] ]
        elif len(p) == 1:
            pass

    def p_OFFSET(p):
        """offset	: NUMBER"""

        p[0] = p[1]

    def p_OPERAND(p):
        """operand	: NUMBER OPERAND_DISPLAY
                    | NUMBER """

        if len(p) == 3:
            p[0] = [ p[1], p[2] ]
        elif len(p) == 2:
            p[0] = [p[1]]


    lexer = ply.lex.lex()
#   lexer.input(src)
    parser = ply.yacc.yacc()

    try:
        return parser.parse(src, lexer=lexer)
    except ValueError as err:
        print("[ValueError] {0}".format(err))
        return []

#   for token in lexer:
#       print("[T] {0}".format(token))


if __name__ == "__main__":

    pbc = """
    2           0 LOAD_FAST                0 (a)
                3 LOAD_FAST                1 (b)
                6 BINARY_ADD
                7 RETURN_VALUE
    """

    ret = parse_bytecode(pbc)
    pprint(ret)
