from typing import List, Optional
import dataclasses
import re

# crosshair: off

def blow_up_noannot(n):
    # crosshair: on

    '''
    post: __return__ != 0
    '''
    return 2 * n + 10


def blow_up(n: int) -> int:
    # crosshair: on

    def blow_up_2(n: int) -> int:

        '''
        post: __return__ != 0
        '''
        return 2 * n + 10

    '''    
    post: __return__ > 0
    '''
    return blow_up_2(-10)
    # return 2 * n + 10


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
# Cross-check different implementations of logic

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



#-------------------------
# Example with classes


@dataclasses.dataclass
class AverageableQueue:
    '''
    A queue of numbers with a O(1) average() operation.
    inv: self._total == sum(self._values)
    '''
    _values: List[int]
    _total: int

    def push(self, val: int):
        self._values.append(val)
        self._total += val

    def pop(self) -> int:
        ''' pre: len(self._values) > 0 '''
        val = self._values.pop(0)
        # Oops. We are forgetting to do something here.
        return val

    def average(self) -> float:
        ''' pre: self._values '''
        return self._total / len(self._values)


# -----------------------
# Regex checking

def parse_year(yearstring: str) -> Optional[int]:
    # crosshair: on
    '''    
    post: __return__ is None or 1000 <= __return__ <= 9999
    '''
    
    # return int(yearstring) if re.match('[1-9][0-9][0-9][0-9]', yearstring.rstrip()) else None
    # """
    # Fix
    return int(yearstring) if re.match('^[1-9][0-9][0-9][0-9]$', yearstring.rstrip()) else None
    # """


# ------------------------
# Restrict possible inputs - Still not completing

def check_num_in_nums(num: int, numbers: list[int]) -> bool: 
    # crosshair: on
    '''
    pre: all([ x in (0,1) for x in numbers])
    pre: 0 <= len(numbers) < 3
    pre: 0 < num < 4
    post: True
    '''

    return num in numbers