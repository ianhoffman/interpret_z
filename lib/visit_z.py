from lib.const_z import TypesZ

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_{}'.format(node.__class__.__name__)
        import pdb; pdb.set_trace()
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(
            'No visit method implemented for node class {}'.format(
                node.__class__.__name__
            )
        )

class InterpreterZ(NodeVisitor):
    def __init__(self, ast):
        self.ast = ast

    def visit_BinOpNode(self, node):
        if node.op == TypesZ.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op == TypeZ.DIV:
            return self.visit(node.left) * self.visit(node.right)

    def visit_IntegerNode(self, node):
        return node.value

    def visit_RealNode(self, node):
        return node.value

    def interpret(self):
        return self.visit(self.ast)
        
