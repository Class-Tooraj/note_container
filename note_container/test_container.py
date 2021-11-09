# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #

# IMPORT
import random

# IMPORT TYPING
from typing import Iterable

# LOCAL IMPORT
from container import Container


def IterMember(many: int = 20) -> Iterable[tuple[str, bytes]]:
    for i in range(0, many):
        tic = random.randint(10, 30)
        yield (f'MEM_{i}', random.randbytes(tic))

def test(path: str, many: int = 20):
    members = [*IterMember(many)]
    mid = [members[i] for i in range(0, many//2)]
    last = [members[i] for i in range(many//2, many)]
    container = Container(path)
    for mem, data in mid:
        container[mem] = data
    
    container.iter_set(last)

    for name, val in mid:
        check = container[name]
        assert val == check
    
    for get, it in zip(container.iter_get([i[0] for i in last]), last):
        n_get = get[0]
        v_get = get[1]
        n = it[0]
        v = it[1]
        if n_get == n:
            assert v_get == v
    
    for name, *_ in mid:
        del container[name]
    container.iter_remove((i[0] for i in last))

    print('Passed')
    return True


if __name__ == "__main__":
    import os
    _d = os.path.dirname(__file__)
    _path = os.path.realpath(os.path.join(_d, './test/test.zip'))
    test(_path, 40)
    os.remove(_path)
