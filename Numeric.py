from dataclasses import dataclass, field
from typing import Optional, Tuple, Any

from Type import *
from BaseNodes import Numeric


@dataclass
class Number(Numeric):
    """Base class for numeric types. All numeric types are treated as floats."""
    value: float

    def eval(self, env) -> float:
        return self.value


@dataclass
class Identifier(Numeric):
    name: str
    line: int

    def eval(self, env) -> float:
        result: Optional[Tuple[Any, Any]] = env.lookup(self.name)
        if result is None:
            raise Exception(f"Line {self.line} - Variable '{self.name}' not declared")
        _, value = result
        if value is None:
            raise Exception(f"Line {self.line} - '{self.name}' is uninitialized")
        return value


@dataclass
class Minus(Numeric):
    right: Numeric

    def eval(self, env) -> float:
        return -1.0 * float(self.right.eval(env))


@dataclass
class BinaryNumericOp(Numeric):
    left: Numeric
    right: Numeric
    line: int = field(default=None, kw_only=True)

    @staticmethod
    def operation(left: float, right: float) -> float:
        raise NotImplementedError

    def eval(self, env) -> float:
        left_val = float(self.left.eval(env))
        right_val = float(self.right.eval(env))
        return self.operation(left_val, right_val)


class Add(BinaryNumericOp):
    @staticmethod
    def operation(left: float, right: float) -> float:
        return left + right


class Subtract(BinaryNumericOp):
    @staticmethod
    def operation(left: float, right: float) -> float:
        return left - right


class Multiply(BinaryNumericOp):
    @staticmethod
    def operation(left: float, right: float) -> float:
        return left * right


class Divide(BinaryNumericOp):
    def __init__(self, left, right, line: int):
        super().__init__(left=left, right=right, line=line)

    @staticmethod
    def operation(left: float, right: float) -> float:
        if right == 0:
            raise Exception("Division by zero")
        return left / right

    def eval(self, env) -> float:
        left_val = float(self.left.eval(env))
        right_val = float(self.right.eval(env))
        if right_val == 0 or right_val == float(0):
            raise Exception(f"Line {self.line} - division by zero")
        return left_val / right_val


class Modulo(BinaryNumericOp):
    def __init__(self, left, right, line: int):
        super().__init__(left=left, right=right, line=line)

    @staticmethod
    def operation(left: float, right: float) -> float:
        if right == 0:
            raise Exception("Division by zero")
        return left % right

    def eval(self, env) -> float:
        left_val = float(self.left.eval(env))
        right_val = float(self.right.eval(env))
        if right_val == 0:
            raise Exception(f"Line {self.line} - division by zero")
        return left_val % right_val