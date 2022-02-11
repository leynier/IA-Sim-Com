from compilation.enums import Enum, VariableType, MethodType
from compilation.context import Context


class NodeType(Enum):
    STRING = 0
    INT = 1
    DOUBLE = 2
    BOOL = 3
    ARRAY = 4
    OTHER = 5


def normaliza(typevar):
    if typevar in [VariableType.INT, MethodType.INT]:
        return "int"
    if typevar in [VariableType.BOOL, MethodType.BOOL]:
        return "bool"
    if typevar in [VariableType.DOUBLE, MethodType.DOUBLE]:
        return "double"
    if typevar in [VariableType.STRING, MethodType.STRING]:
        return "str"
    if typevar == MethodType.VOID:
        return "void"


class Node:
    def validate(self, context: Context):
        return True

    def checktype(self, context: Context):
        return None

    def eval(self, context: Context):
        return None

    def __repr__(self) -> str:
        return "NODE()"


class Statement(Node):
    @staticmethod
    def type() -> str:
        return "Statment"
