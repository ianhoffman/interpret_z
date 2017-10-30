def render(template, context):
    from lib.scan_z import ScannerZ
    from lib.parse_z import ParserZ
    from lib.interpret_z import InterpreterZ

    sz = ScannerZ(template)
    pz = ParserZ(sz)
    ast = pz.parse()
    iz = InterpreterZ(ast, context)
    return iz.interpret()

