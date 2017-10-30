from lib.interpret_z import InterpreterZ
from lib.parse_z import ParserZ
from lib.scan_z import ScannerZ

def render(template, context):
    sz = ScannerZ(template)
    pz = ParserZ(sz)
    ast = pz.parse()
    iz = InterpreterZ(ast, context)
    return iz.interpret()

