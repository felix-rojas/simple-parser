from SymbolTable import *
from Type import *

class Node:
    def eval(self, env):
        pass

class Numeric(Node):
    def eval(self, env):
        pass

class Logic(Node):
    def eval(self, env):
        pass

class Void(Node):
    def eval(self, env):
        pass

# --- NUMERIC --- #
class Number(Numeric):
    def __init__(self, value):
        self.value = value
    
    def eval(self, env):
        return self.value

class Identifier(Numeric):
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def eval(self, env):
        result = env.lookup(self.name)
        if result != None:
            (_, value) = result
            return value
        else: 
            text = "Line " + str(self.line) + " - " + self.name + " has not been declared"
            raise Exception(text)

class Minus(Numeric):
    def __init__(self, right):
        self.right = right

    def eval(self, env):
        return -1 * float(self.right.eval(env))

class Add(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left + right

class Subtract(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left - right

class Multiply(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left * right


class Divide(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))

        if right != 0:
            return left / right
        else: 
            text = "Line " + str(self.line) + " - " +  "has division by zero"
            raise Exception(text)

class Modulo(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))

        if right != 0:
            return left % right
        else: 
            text = "Line " + str(self.line) + " - " +  "has division by zero"
            raise Exception(text)

# --- LOGIC ---
class Boolean(Logic):
    def __init__(self, value):
        self.value = value
    def eval(self, env):
        return self.value

class Not(Logic):
    def __init__(self, right):
        self.right = right
    def eval(self, env):
        return not(bool(self.right.eval(env))) 

class Lesser(Logic):
    def __init__(self,left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left < right

class LesserEqual(Logic):
    def __init__(self,left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left <= right

class Larger(Logic):
    def __init__(self,left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left > right

class LargerEqual(Logic):
    def __init__(self,left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left >= right

class Equal(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        return self.left.eval(env) == self.right.eval(env)

class NotEqual(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        return self.left.eval(env) != self.right.eval(env)

class And(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        return bool(self.left.eval(env)) and bool(self.right.eval(env))

class Or(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self, env):
        return bool(self.left.eval(env)) or bool(self.right.eval(env))

# --- Void classes ---
class Print(Void):
    def __init__(self,expression):
        self.expression = expression
    def eval(self,env):
        result = self.expression.eval(env)
        print(result)

class Assignment(Void):
    def __init__(self,expression):
        self.expression = expression
    def eval(self,env):
        result = self.expression.eval(env)
        _type = None
        if isinstance(self.expression,Numeric):
            _type = Type.NUMBER
            value = float(result)
        else:
            _type = Type.BOOLEAN
            value = bool(result)
        if not(env.set(self.id,_type,value)):
            text = f"Variable at line {line} was not declared"
            raise Exception(text)