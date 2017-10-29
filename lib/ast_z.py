class AssignmentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class CompoundNode:
    def __init__(self, children):
        self.children = children

class ForLoopNode:
    def __init__(self, arr, var, block):
        self.arr = arr
        self.var = var
        self.block = block

class IntegerNode:
    def __init__(self, token):
        self.value = token.value

class RealNode:
    def __init__(self, token):
        self.value = token.value

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

class TernaryNode:
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

class IfNode:
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true 
        self.if_false = if_false 

class BangNode:
    def __init__(self, child):
        self.child = child

class StringNode:
    def __init__(self, token):
        self.value = token.value

class VarNode:
    def __init__(self, name):
        self.name = name

