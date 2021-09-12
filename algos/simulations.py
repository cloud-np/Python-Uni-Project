from functools import wraps


def simulate_cell_pos(cell):
    """Do not let a function change the value of our cell.
    This decorator simply helps us simulate the new positions
    of the cell without changing it at the end.

    Parameters
    ----------
    cell : [type]
        [description]
    """
    def __simulate_cell_pos(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cell_old_pos = (cell.x, cell.y)
            func_return = func(*args, **kwargs)
            cell.set_position(*cell_old_pos)
            return func_return
        return wrapper
    return __simulate_cell_pos


def simulate_many_cells_pos(*cells):
    """Do not let a function change the value of any N cells.
    This decorator simply helps us simulate the new positions of N number
    of cells with keeping their positions intact in the end of the function.

    Parameters
    ----------
    cells : List[Node]
        The cells we cant to keep the same position for.
    """
    def __simulate_many_cell_pos(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            old_cell_info = [{'row': c.row, 'pos': (c.x, c.y)} for c in cells]
            func_return = func(*args, **kwargs)
            for info, c in zip(old_cell_info, cells):
                c.set_position(*info['pos'])
                c.row = info['row']

            return func_return
        return wrapper
    return __simulate_many_cell_pos
