from interpret_z import ast_z
from interpret_z import ZephyrFuncs
from interpret_z import TypesZ

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_{}'.format(node.__class__.__name__)
        method = getattr(self, method_name, 'generic_visit')
        return method(node)

    def generic_visit(self, node):
        raise Exception(
            'No visit method implemented for node class {}'.format(
                node.__class__.__name__
            )
        )

class InterpreterZ(NodeVisitor):
    def __init__(self, ast, context=None):
        self.ast = ast
        self.context = context or {} 

    def visit_ArrayNode(self, node):
        arr = []
        for child in node.arr:
            arr.append(self.visit(child))
        return arr
    
    def visit_AssignmentNode(self, node):
        self.context[node.name] = self.visit(node.value)

    def visit_BangNode(self, node):
        return not self.visit(node.child)

    def visit_BinOpNode(self, node):
        left_val = self.visit(node.left)
        if node.op == TypesZ.MUL:
            if type(left_val) is str:
                return 0
            return left_val * self.visit(node.right)
        if node.op == TypesZ.DIV:
            if type(left_val) is str:
                return 0
            return left_val / self.visit(node.right)
        if node.op == TypesZ.PLUS:
            if type(left_val) is str:
                return left_val + str(self.visit(node.right)) 
            return left_val + self.visit(node.right)
        if node.op == TypesZ.MINUS:
            if type(left_val) is str:
                return 0
            return left_val - self.visit(node.right)
        if node.op == TypesZ.MOD:
            if type(left_val) is str:
                return 0
            return left_val - self.visit(node.right)
        raise NotImplemented('op %s not implemented' % node.op)

    def visit_BoolOpNode(self, node):
        if node.op == TypesZ.EQEQ:
            return self.visit(node.left) == self.visit(node.right)
        if node.op == TypesZ.NEQ:
            return self.visit(node.left) != self.visit(node.right)
        if node.op == TypesZ.GTE:
            return self.visit(node.left) >= self.visit(node.right)
        if node.op == TypesZ.GT:
            return self.visit(node.left) > self.visit(node.right)
        if node.op == TypesZ.LTE:
            return self.visit(node.left) <= self.visit(node.right)
        if node.op == TypesZ.LT:
            return self.visit(node.left) < self.visit(node.right)
        raise NotImplemented('op %s not implemented' % node.op)

    def visit_BoolStatementNode(self, node):
        if node.op == TypesZ.AND:
            return self.visit(node.left) and self.visit(node.right)
        if node.op == TypesZ.OR:
            return self.visit(node.left) or self.visit(node.right)
        raise NotImplemented('op %s not implemented' % node.op)

    def visit_CompoundNode(self, node):
        visited_children = []
        for child in node.children:
            res = self.visit(child)
            if str(res) == 'True':
                visited_children.append('true')
            elif str(res) == 'False':
                visited_children.append('false')
            elif res is None:
                continue
            else:
                visited_children.append(str(res))
        return ''.join(visited_children)

    def visit_DotNode(self, node):
        var = self.visit(node.var)
        while type(node.prop) is ast_z.DotNode:
            node = node.prop
            var = var[node.var.name]
        return var[node.prop]

    def visit_ForLoopNode(self, node):
        result = []
        for item in self.visit(node.arr):
            self.context[node.var.name] = item
            result.append(self.visit(node.block))
        return ''.join(result)

    def visit_FuncNode(self, node):
        args = []
        func = ZephyrFuncs[node.func]
        for arg in node.args:
            args.append(self.visit(arg))
        return func(*args)

    def visit_IfNode(self, node):
        if self.visit(node.condition):
            return self.visit(node.if_true)
        elif node.if_false:
            return self.visit(node.if_false)
        else:
            return None

    def visit_IntegerNode(self, node):
        return node.value

    def visit_RealNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_SubscriptNode(self, node):
        return self.visit(node.var)[self.visit(node.idx)]

    def visit_TernaryNode(self, node):
        if self.visit(node.condition):
            return self.visit(node.if_true)
        else:
            return self.visit(node.if_false)

    def visit_HtmlTextNode(self, node):
        return node.value

    def visit_VarNode(self, node):
        value = self.context.get(node.name)
        if value is None:
            raise Exception('Var %s referenced before assignment' % node.name)
        return value 

    def interpret(self):
        return self.visit(self.ast)
