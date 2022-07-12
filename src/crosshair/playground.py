from typing import List

# crosshair: off

def blow_up_noannot(n):
    # crosshair: off

    '''
    post: __return__ != 0
    '''
    return 2 * n + 10


def blow_up(n: int) -> int:
    # crosshair: on

    '''
    post: __return__ != 0
    '''
    return 2 * n + 10


def identity(x):
    # crosshair: on
    '''
    post: True
    '''

    return x


# ---------------------

def average(numbers: list[float]) -> float:
    # crosshair: on
    '''
    pre: len(numbers) >= 0
    post: min(numbers)  <= __return__ <= max(numbers)
    '''

    return sum(numbers)/len(numbers)


# ---------------------
# Catch potential run-time errors (Set-> post: True)

def catch_index_error(numbers: list[int]) -> list[tuple[int, int]]:
    # crosshair: on
    '''
    post: True
    '''

    return [
        (numbers[i], numbers[i+1])
        for i in range(len(numbers))
    ]
    """
    # Fix
    return [
        (numbers[i], numbers[i+1])
        for i in range(len(numbers)-1)
    ]
    """

# ---------------------
# Cross-check different implementatios of logic

def get_first_column(text: str) -> str: 
    # crosshair: on
    '''
    post: __return__ == text.split(',')[0]
    '''
    try:
        return text[text.index(',')]
    except ValueError:
        # No ',' in text
        return text


# -------------------
# Nested functions -- ONLY top-level functions are checked

def outer_function():
    # crosshair: on
    '''
    post: True
    '''

    def inner_function():
        '''
        post: True
        '''

        raise IndexError 
    
    #raise IndexError
    return 10




# ------------------------
# Restrict possible inputs - Still not completing

def check_num_in_nums(num: int, numbers: list[int]) -> bool: 
    # crosshair: on
    '''
    pre: all([ x in (0,1) for x in numbers])
    pre: 0 < len(numbers) < 3
    pre: 0 < num < 4
    '''

    return num in numbers