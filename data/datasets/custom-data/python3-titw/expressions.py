from pytype_extensions import assert_type
# Syntactic convenience to avoid Python interpreter error


"""
Accessing elements of a heterogeneous collection leads to poor inference
"""
def check_indexing(j):
    
    li = [42, 'parrot']
    reveal_type(li)
    # Pytype: List[Union[int, str]]
    # MyPy: list [object]
    # HiTyper: list[typing.Union[int,typing.Text]]
    
    a = li[1]
    reveal_type(a)
    # Pytype: int
    # MyPy: object
    # HiTyper: int (INCORRECT)
    
    b = li[j]
    reveal_type(b)
    # Pytype: Any
    # MyPy: object
    # HiTyper: int (INCORRECT)


"""
Types influenced by side-effects are not grouped under a common supertype
HiTyper still tries to be specific, and fails at times
"""
def attributes_and_sideeffects():

    class A():
        def __init__(self, x):
            self.attr = x
    
    a = A(1)
    b = A(2)

    i = input()
    if (i == 'coconut'):
        a.attr = 'coconut'
    else:
        a.attr = 1
    
    reveal_type(a.attr)
    # Pytype;  Union[int, str]
    # MyPy: object

    reveal_type(b.attr)
    # Pytype:  Union[int, str], int
    # MyPy: Any

    # HiTyper   (INCORRECT)
    # "category": "local",
    # "name": "a_",
    # "type": [
    #     "typing.Text",
    #     "int"
    # ]


def aliasing():
    
    class A():
        def __init__(self, x):
            self.attr = x
    
    a = A(1)
    b = a

    a.attr = "text"
    b.attr = b.attr
    reveal_type(a.attr)
    reveal_type(b.attr)


"""
- Argument type inference is not correct
    - Predicts a type for `x` and `y` -- incorrect
    - No types predicted for `other`
>> Suggests that the inference goes "forward" but not "backward"?
"""
def args(other, x, y):
    if hasattr(other,"__getitem__") and len(other)==2:
        return x != other[0] or y != other[1]
    else:
        return True

    # {
    #     "category": "arg",
    #     "name": "other",
    #     "type": []
    # },
    # {
    #     "category": "arg",
    #     "name": "x",
    #     "type": [
    #         "int",
    #         "tuple[typing.Union[float,float]]"
    #     ]
    # },
    # {
    #     "category": "arg",
    #     "name": "y",
    #     "type": [
    #         "int",
    #         "tuple[typing.Union[float,float]]"
    #     ]
    # }


def type_updation():

    li = [10, 20]
    reveal_type(li)
    # PyType:  List[int]
    # MyPy: List[int]

    li[1] = "string"
    reveal_type(li)
    # Pytype: List[Union[int, str]]
    # MyPy: ERROR
    # HiTyper (INCORRECT)
    # "type": [
    #     "list[int]",
    #     "list[typing.Union[int,typing.Text]]"
    # ]


def f(i):
    l = [1, 2, 3]
    reveal_type(i)
    reveal_type(l[i])
    
    # a = f(0)
    a = l[0] if i == 0 else f(i - 1)
    reveal_type(a)
    # HiTyper (INCORRECT)
    # "type": [
    #     "str",
    #     "dict[, ]",
    #     "int"
    # ]

    return l[i] 