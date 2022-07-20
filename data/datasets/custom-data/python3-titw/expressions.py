from pytype_extensions import assert_type
# Syntactic convenience to avoid Python interpreter error

def check_indexing(i):
    
    li = [42, 'parrot']
    reveal_type(li)
    # Pytype: List[Union[int, str]]
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
    b = a

    i = input()
    if (i == 'coconut'):
        a.attr = 'coconut'
    else:
        a.attr = 1
    
    reveal_type(a.attr)
    # Pytype;  Union[int, str]
    # MyPy: object

    reveal_type(b.attr)
    # Pytype:  Union[int, str]
    # MyPy: Any

    # HiTyper
    # "category": "local",
    # "name": "a_",
    # "type": [
    #     "typing.Text",
    #     "int"
    # ]
