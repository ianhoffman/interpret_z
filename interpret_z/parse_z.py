from interpret_z import ast_z
from interpret_z import ReservedKeywords
from interpret_z.const_z import TypesZ

class ParserZ:
    def __init__(self, sz):
        self.sz = sz
        self.pos = 0
        self.tokens = []
        self.current_token = None

    def eat(self, token):
        if self.current_token != token:
            raise Exception('Expected type {}, got type {}'.format(
                token.name, self.current_token.z_type)
            )
        else:
            self.pos += 1
            if self.pos >= len(self.tokens):
                self.current_token = None
            else:
                self.current_token = self.tokens[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.tokens):
            return None
        else:
            return self.tokens[peek_pos]

    def parse(self):
        self.tokens = self.sz.scan()
        if len(self.tokens) >= 1:
            self.current_token = self.tokens[0]
        else:
            raise Exception('No tokens scanned')

        tree = self.compound()
        if self.current_token is not None:
            raise Exception(
                'After parsing, current_token should be None, '
                'instead got %s.' % self.current_token.z_type
            )
        return tree

    def compound(self):
        children = []
        while self.current_token == TypesZ.HTML_OR_TEXT or (
            self.current_token == TypesZ.LBRACE and
            self.peek() not in (
                ReservedKeywords.ENDFOR,
                ReservedKeywords.ENDIF,
                ReservedKeywords.ELSE
            )
        ):
            if self.current_token == TypesZ.LBRACE:
                children.append(self.zephyr())
            else:
                children.append(self.html_or_text())
        return ast_z.CompoundNode(children=children)

    def html_or_text(self):
        value = self.current_token.value
        self.eat(TypesZ.HTML_OR_TEXT)
        return ast_z.HtmlTextNode(value=value)
    
    def zephyr(self):
        self.eat(TypesZ.LBRACE)
        node = self.statement()
        self.eat(TypesZ.RBRACE)
        return node

    def statement(self):
        if self.current_token == ReservedKeywords.IF:
            return self.if_statement()
        elif self.current_token == ReservedKeywords.FORLOOP:
            return self.for_loop()
        elif self.current_token == TypesZ.VAR and self.peek() == TypesZ.EQ:
            return self.assignment_statement()
        else:
            return self.ternary_statement()

    def for_loop(self):
        self.eat(ReservedKeywords.FORLOOP)
        arr = self.var()
        self.eat(ReservedKeywords.AS)
        var = self.var() 
        self.eat(TypesZ.RBRACE)
        block = self.compound()
        self.eat(TypesZ.LBRACE)
        self.eat(ReservedKeywords.ENDFOR)
        return ast_z.ForLoopNode(
            arr=arr,
            var=var,
            block=block
        )

    def assignment_statement(self):
        token = self.current_token
        self.eat(TypesZ.VAR)
        self.eat(TypesZ.EQ)
        if self.current_token == TypesZ.LBRACKET:
            value = self.array()
        else: 
            value = self.ternary_statement()
        return ast_z.AssignmentNode(
            name=token.value,
            value=value
        )

    def if_statement(self):
        self.eat(ReservedKeywords.IF)
        condition = self.ternary_statement()
        self.eat(TypesZ.RBRACE)
        if_true = self.compound()
        self.eat(TypesZ.LBRACE)
        if_false = None
        
        if self.current_token == ReservedKeywords.ELSE:
            self.eat(ReservedKeywords.ELSE)
        if self.current_token == ReservedKeywords.IF:
            if_false = self.if_statement()
        elif self.current_token == ReservedKeywords.ENDIF:
            self.eat(ReservedKeywords.ENDIF)
        else:
            self.eat(TypesZ.RBRACE)
            if_false = self.compound()
            self.eat(TypesZ.LBRACE)
            self.eat(ReservedKeywords.ENDIF)

        return ast_z.IfNode(
            condition=condition,
            if_true=if_true,
            if_false=if_false
        )

    def ternary_statement(self):
        node = self.boolean_statement()
        if self.current_token.z_type == TypesZ.QUESTION:
            self.eat(TypesZ.QUESTION)
            if_true = self.boolean_statement()
            self.eat(TypesZ.COLON)
            if_false = self.boolean_statement()
            node = ast_z.TernaryNode(
                condition=node,
                if_true=if_true,
                if_false=if_false
            )
        return node

    def boolean_statement(self):
        node = self.boolean()
        while self.current_token.z_type in (
            TypesZ.AND, TypesZ.OR
        ):
            op_type = self.current_token
            self.eat(op_type)
            node = ast_z.BoolStatementNode(
                left=node,
                op=op_type,
                right=self.boolean()
            )
        return node

    def boolean(self):
        node = self.expr()
        while self.current_token.z_type in (
            TypesZ.EQEQ,
            TypesZ.NEQ,
            TypesZ.GT,
            TypesZ.GTE,
            TypesZ.LT,
            TypesZ.LTE
        ):
            op_type = self.current_token
            self.eat(op_type)
            node = ast_z.BoolOpNode(
                left=node,
                op=op_type,
                right=self.expr()
            )
        return node

    def expr(self):
        node = self.term()
        while self.current_token.z_type in (
            TypesZ.PLUS, TypesZ.MINUS
        ):
            op_type = self.current_token
            self.eat(op_type)
            node = ast_z.BinOpNode(
                left=node,
                op=op_type,
                right=self.term()
            )
        return node

    def term(self):
        node = self.factor()
        while self.current_token.z_type in (
            TypesZ.MUL, TypesZ.DIV, TypesZ.MOD
        ):
            op_type = self.current_token
            self.eat(op_type)
            node = ast_z.BinOpNode(
                left=node,
                op=op_type,
                right=self.factor()
            )
        return node

    def factor(self):
        node = None
        if self.current_token == TypesZ.INTEGER:
            node = ast_z.IntegerNode(self.current_token)
            self.eat(TypesZ.INTEGER)
        elif self.current_token == TypesZ.REAL:
            node = ast_z.RealNode(self.current_token)
            self.eat(TypesZ.REAL)
        elif self.current_token == TypesZ.LPAREN:
            self.eat(TypesZ.LPAREN)
            node = self.ternary_statement()
            self.eat(TypesZ.RPAREN)
        elif self.current_token == TypesZ.BANG:
            self.eat(TypesZ.BANG)
            node = ast_z.BangNode(
                self.boolean()
            )
        elif self.current_token == TypesZ.STRING:
            node = ast_z.StringNode(self.current_token)
            self.eat(TypesZ.STRING)
        elif self.current_token == TypesZ.VAR:
            node = self.var()
        elif self.current_token == TypesZ.FUNC:
            node = self.func()
        return node

    def var(self):
        node = ast_z.VarNode(name=self.current_token.value)
        self.eat(TypesZ.VAR)
        while self.current_token in (
            TypesZ.DOT, TypesZ.LBRACKET
        ):
            if self.current_token == TypesZ.DOT:
                self.eat(TypesZ.DOT)
                node = ast_z.DotNode(
                    var=node,
                    prop=self.current_token.value
                )
                self.eat(TypesZ.VAR)
            else:
                self.eat(TypesZ.LBRACKET)
                node = ast_z.SubscriptNode(
                    var=node,
                    idx=self.ternary_statement()
                )
                self.eat(TypesZ.RBRACKET)
        return node

    def func(self):
        func = self.current_token.value
        args = []
        self.eat(TypesZ.FUNC)
        self.eat(TypesZ.LPAREN)
        if self.current_token != TypesZ.RPAREN:
            while True:
                args.append(self.ternary_statement())
                if self.current_token != TypesZ.COMMA:
                    break
                self.eat(TypesZ.COMMA)
        self.eat(TypesZ.RPAREN)
        return ast_z.FuncNode(
            func=func,
            args=args
        )
    
    def array(self):
        arr = []
        self.eat(TypesZ.LBRACKET)
        if self.current_token != TypesZ.RBRACKET:
            arr.append(self.ternary_statement())
            while self.current_token == TypesZ.COMMA:
                self.eat(TypesZ.COMMA)
                arr.append(self.ternary_statement())
        self.eat(TypesZ.RBRACKET)
        return ast_z.ArrayNode(arr=arr)

