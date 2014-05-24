import pytest

from parser import parse_bytecode
from bytecode import CodeLine


complete_test_file = "p.pbc"
fragment_test_file = "f.pbc"

@pytest.fixture
def add_fragment():
    return """2           0 LOAD_FAST                0 (a)
                          3 LOAD_FAST                1 (b)
                          6 BINARY_ADD
                          7 RETURN_VALUE"""
@pytest.fixture
def composite():
    return "5 LOAD_FAST 9 (x)\n3 BINARY_ADD\n1 LOAD_FAST 4 (z)\n127 RETURN_VALUE"

@pytest.fixture
def badline():
    return "77 55 TOAD_FAST        3 (ocelot)"

@pytest.fixture
def prolix_desc():
    return """26          40 LOAD_CONST               3 (<code object parse_bytecode at 0xb72a9d58, file "parser.py", line 26>)"""

@pytest.fixture
def referent():
    return "             73 LOAD_CONST               7 ('\t  2 LOAD_FAST                0 (xyz pqr)')"

def test_parse_add_fragment_lineno(add_fragment):
    ret = parse_bytecode(add_fragment)
    ret[1].lineno == 2

def test_parse_add_fragment_offset(add_fragment):
    ret = parse_bytecode(add_fragment)
    ret[3].offset == 7

def test_parse_add_fragment_opname(add_fragment):
    ret = parse_bytecode(add_fragment)
    ret[2].opname == "BINARY_ADD"

def test_parse_badline_syntaxerror(badline):
    with pytest.raises(SyntaxError):
        ret = parse_bytecode(badline)

def test_parse_prolix_desc(prolix_desc):
    ret = parse_bytecode(prolix_desc)

def test_parse_referent(referent):
    ret = parse_bytecode(referent)

def test_file_input():
    with open(complete_test_file, 'r') as fp:
        src = fp.read()

    ret = parse_bytecode(src)
