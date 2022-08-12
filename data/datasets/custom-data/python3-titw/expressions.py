from pytype_extensions import assert_type
# Syntactic convenience to avoid Python interpreter error

def check_indexing(j):
    
    li = [42, 'parrot']
    reveal_type(li)
    # Pytype: List[Union[int, str]]
    # MyPy: list [object]
    # HiTyper: list[typing.Union[int,typing.Text]]
    
    a = li[0]
    reveal_type(a)
    # Pytype: int
    # MyPy: object
    # HiTyper: int
    
    b = li[j]
    reveal_type(b)
    # Pytype: Any
    # MyPy: object
    # HiTyper: int


def aliasing_and_attributes():

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

    # HiTyper
    # "category": "local",
    # "name": "a_",
    # "type": [
    #     "typing.Text",
    #     "int"
    # ]


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
    a = f(0)
    reveal_type(a)
    return l[i] 