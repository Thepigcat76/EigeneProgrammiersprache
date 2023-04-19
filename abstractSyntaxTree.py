import lexer
from environment import Env
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Tuple

class NullException(Exception):
    pass

class ASTError(Exception):
    pass


@dataclass
class Stmt(ABC):
    pass

@dataclass
class Program(Stmt):
    body: List[Stmt]
    def generate_code(self, env: Env) -> str:
        code = """
# Program:
        .text
        """
        for stmt in self.body:
            code += stmt.generate_code(env)
        code += env.generate_data()
        return code

@dataclass
class Expr(Stmt, ABC):
    pass

@dataclass
class VarDecl(Stmt):
    const: bool
    identifier: str
    value: Expr
    def generate_code(self, env: Env) -> str:
        if isinstance(self.value, NullLiteral):
            env.deklGlobalVar(self.identifier, None)
            return f"""
        # Var {self.identifier} decl in .data
            """
        elif isinstance(self.value, NumericLiteral):
            env.deklGlobalVar(self.identifier, self.value.value)
            return f"""
        # Var {self.identifier} decl in .data with value {self.value.value}
            """
        else:
            env.deklGlobalVar(self.identifier, None)
            code = self.value.generate_code(env)
            code += f"""
        lw $t8, ($sp)  # init variable {self.identifier}
        sw $t8, {self.identifier}
            """
            return code


@dataclass
class FunctionDeclaration(Stmt):
    name: str
    parameters: List[str]
    body: List[Stmt]

@dataclass
class Return(Stmt):
    return_value: Expr

@dataclass
class If(Stmt):
    condition: Expr
    body: List[Stmt]

@dataclass
class IfElifElse(Stmt):
    cases: List[If]

@dataclass
class While(Stmt):
    condition: Expr
    has_do: bool
    body: List[Stmt]

@dataclass
class Break(Stmt):
    pass

@dataclass
class BinaryExpr(Expr):
    left: Expr
    right: Expr
    operator: str
    def generate_code(self, env: Env) -> str:
        code = self.left.generate_code(env)
        code += self.right.generate_code(env)
        if self.operator == "+":
            code += """
        lw $t8, ($sp)  # Binary + operation
        addi $sp, $sp, 4
        lw $t9, ($sp)
        add $t8, $t8, $t9
        sw $t8, ($sp)
            """
        else:
            raise ASTError("BinaryExpr has invalid operator")
        return code
    
@dataclass
class UnaryExpr(Expr):
    arg: Expr
    operator: str
    def generate_code(self, env: Env) -> str:
        code = self.arg.generate_code(env)
        if self.operator == "-":
            code += """
        lw $t8, ($sp)  # Unary - operation
        neg $t8, $t8
        sw $t8, ($sp)
            """
        elif self.operator in ["!", "~"]:
            goto = env.getGoto()
            code += f"""
        lw $t8, ($sp)  # Unary ! operation
        beq $zero, $t8, negate{goto}
        li $t8, 0
        b exitNegate{goto}
negate{goto}:
        li $t8, 1
exitNegate{goto}:
            """
        else:
            raise ASTError("UnaryExpr has invalid operator")
        return code

@dataclass
class Identifier(Expr):
    symbol: str
    def generate_code(self, env: Env) -> str:
        env.useGlobalVar(self.symbol)
        return f"""
        lw $t8, {self.symbol}  # Identifier {self.symbol} to stack
        addi $sp, $sp, -4
        sw $t8, ($sp)
        """

@dataclass
class NumericLiteral(Expr):
    value: float
    def generate_code(self, env: Env) -> str:
        return f"""
        li $t8, {self.value}  # Num {self.value} to stack
        addi $sp, $sp, -4
        sw $t8, ($sp)
        """
@dataclass
class String(Expr):
    value: str

@dataclass
class NullLiteral(Expr):
    def generate_code(self, env: Env):
        raise NullException("Null Literal can not be evaluated")

@dataclass
class AssignmentExpr(Expr):
    assigne: Expr
    value: Expr

@dataclass
class Property(Expr):
    arg: str
    value: Expr

@dataclass
class ObjectLiteral(Expr):
    properties: List[Property]

@dataclass
class CallExpr(Expr):
    args: List[Expr]
    caller: Expr

@dataclass
class MemberExpr(Expr):
    obj: Expr
    property: Expr
    computed: bool

@dataclass
class Comparator(Expr):
    left: Expr
    right: Expr
    operator: str

@dataclass
class For(Stmt):
    start: NumericLiteral
    end: NumericLiteral
    step: NumericLiteral
    body: List[Stmt]