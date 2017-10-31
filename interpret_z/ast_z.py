class ArrayNode:
    def __init__(self, arr):
        self.arr = arr

class AssignmentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BangNode:
    def __init__(self, child):
        self.child = child

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class BoolOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class BoolStatementNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class CompoundNode:
    def __init__(self, children):
        self.children = children

class DotNode:
    def __init__(self, var, prop):
        self.var = var
        self.prop = prop

class ForLoopNode:
    def __init__(self, arr, var, block):
        self.arr = arr
        self.var = var
        self.block = block

class FuncNode:
    def __init__(self, func, args):
        self.func = func
        self.args = args

class HtmlTextNode:
    def __init__(self, value):
        self.value = value

class IfNode:
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true 
        self.if_false = if_false 

class IntegerNode:
    def __init__(self, token):
        self.value = token.value

class RealNode:
    def __init__(self, token):
        self.value = token.value

class StringNode:
    def __init__(self, token):
        self.value = token.value

class SubscriptNode:
    def __init__(self, var, idx):
        self.var = var
        self.idx = idx

class TernaryNode:
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

class VarNode:
    def __init__(self, name):
        self.name = name

