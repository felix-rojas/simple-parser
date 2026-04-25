from SymbolTable import *
from Type import *
from BaseNodes import Logic, Numeric, Void

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
    def __init__(self, id_name, expression, line):
        self.id_name = id_name
        self.expression = expression
        self.line = line

    def eval(self,env):
        result = self.expression.eval(env)
        _type = None
        
        if isinstance(self.expression,Numeric):
            _type = Type.NUMBER
            value = float(result)
        else:
            _type = Type.BOOLEAN
            value = bool(result)
            
        if not(env.set(self.id_name, _type, value)):
            text = f"Line {self.line} - Variable '{self.id_name}' was not declared"
            raise Exception(text)

class Sequence(Void):
    def __init__(self, statements):
        self.statements = statements
    def eval(self, env):
        for stmt in self.statements:
            stmt.eval(env)