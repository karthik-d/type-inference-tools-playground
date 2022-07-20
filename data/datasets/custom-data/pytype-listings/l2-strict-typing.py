# https://github.com/google/pytype

from typing import List
def get_list() -> List[str]:
    lst = ["PyCon"]
    lst.append(2019)
    return [str(x) for x in lst]

# mypy: line 4: error: Argument 1 to "append" of "list" has
# incompatible type "int"; expected "str"