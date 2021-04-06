from antlr4 import InputStream, CommonTokenStream
import ast
import operator
from typing import Any
from storage.query.rsql.RSQLVisitor import RSQLVisitor
from storage.query.rsql.RSQLLexer import RSQLLexer
from storage.query.rsql.RSQLParser import RSQLParser
from storage.api import Predicate
from storage.var import Vars


def parse(rsql: str) -> Predicate[Any]:
    lexer = RSQLLexer(InputStream(rsql))
    parser = RSQLParser(CommonTokenStream(lexer))
    tree = parser.statement()
    return tree.accept(StorageQueryVisitor())


class StorageQueryVisitor(RSQLVisitor):

    def visitStatement(self, ctx: RSQLParser.StatementContext):
        if ctx.wrapped:
            return self.visit(ctx.wrapped)
        if ctx.node:
            return self.visit(ctx.node)
        if ctx.left or ctx.right:
            if ctx.op.type == RSQLParser.AND_OPERATOR:
                return self.visit(ctx.left) & self.visit(ctx.right)
            elif ctx.op.type == RSQLParser.OR_OPERATOR:
                return self.visit(ctx.left) | self.visit(ctx.right)
        return self.visit(ctx.node)

    def visitComparison(self, ctx: RSQLParser.ComparisonContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        comparator = self.visit(ctx.comparator())
        return comparator(left, right)

    def visitExpression(self, ctx: RSQLParser.ExpressionContext):
        if ctx.IDENTIFIER():
            return Vars.key(ctx.getText())
        return self.visit(ctx.value())

    def visitComparator(self, ctx: RSQLParser.ComparatorContext):
        if ctx.EQ():
            return operator.eq
        elif ctx.NE():
            return operator.ne
        elif ctx.CMP_IDENTIFIER():
            raise NotImplementedError()
        else:
            raise NotImplementedError()

    def visitValue(self, ctx: RSQLParser.ValueContext):
        if ctx.boolean:
            return self.visit(ctx.boolean)
        elif ctx.number:
            return self.visit(ctx.number)
        elif ctx.string:
            return self.visit(ctx.string)
        elif ctx.array:
            return self.visit(ctx.array)
        else:
            raise NotImplementedError(ctx)

    def visitArray_value(self, ctx: RSQLParser.Array_valueContext):
        return Vars.const(tuple([ self.visit(value) for value in ctx.value()]))

    def visitString_literal(self, ctx: RSQLParser.String_literalContext):
        if ctx.STRING_LITERAL():
            return Vars.const(ast.literal_eval(ctx.getText()))
        else:
            raise NotImplementedError(ctx)

    def visitBoolean_literal(self, ctx: RSQLParser.Boolean_literalContext):
        if ctx.TRUE():
            return Vars.const(True)
        elif ctx.FALSE():
            return Vars.const(False)
        else:
            raise NotImplementedError(ctx)

    def visitNumeric_literal(self, ctx: RSQLParser.Numeric_literalContext):
        textual = ctx.getText()
        if ctx.DECIMAL_LITERAL():
            return Vars.const(float(textual))
        elif ctx.INT_LITERAL():
            return Vars.const(int(textual))
        else:
            raise NotImplementedError(ctx)
