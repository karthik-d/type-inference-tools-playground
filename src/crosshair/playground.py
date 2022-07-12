# crosshair: off

def make_bigger_noannot(n):
    # crosshair: off

    '''
    post: __return__ != 0
    '''
    return 2 * n + 10


def make_bigger(n: int) -> int:
    # crosshair: on

    '''
    post: __return__ != 0
    '''
    return 2 * n + 10