import sys
from pathlib import Path

f = Path(__file__).resolve()
parent, root = f.parent, f.parents[1]
sys.path.append(str(root))

__all__ = []

from interpret_z.token_z import TokenZ
from interpret_z.const_z import ReservedKeywords
from interpret_z.const_z import TypesZ
from interpret_z.const_z import ZephyrFuncs

from interpret_z.interpret_z import InterpreterZ
from interpret_z.parse_z import ParserZ
from interpret_z.scan_z import ScannerZ

def render(template, context):
    return InterpreterZ(
        ParserZ(ScannerZ(template)).parse(),
        context
    ).interpret()

