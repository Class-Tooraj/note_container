# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT STANDARD LIB
import random

# IMPORT TYPE
from typing import Iterable, Union, Generator

# IMPORT LOCAL
try:
    from utils import now
except ImportError:
    from note_container.utils import now


__all__ = ("rand_char", "unique_key")

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# RANDOM
def rand_char(letters: str = None) -> chr:
    """[Random Choice Char From Letter Sequence if None Use UpperCase & LowerCase Alphabet]

    Args:
        letters (str, optional): [Letter Sequence For Choice]. Defaults to None.

    Returns:
        chr: [Random Choice Returned]
    """
    letters = letters or "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return random.choice(letters)


# CUSTOMIZE BINARY
def custom_bin(value: Union[str, int]) -> str:
    if isinstance(value, str):
        try:
            value = int(value)
        except (BaseException, Exception) as err:
            raise err

    assert isinstance(value, int)

    return bin(value).removeprefix('0b')


# VALIDATE TO PACK SIZE
def packing(value: str, ped_size: int = 16, str_ret: bool = False) -> Generator[Union[int, str], None, None]:
    _dec = [*value]
    _active = True
    _resval = lambda x: str(int(x, 2)) if str_ret else int(x, 2)
    while _active:
        _ped = ""

        if len(_dec) >= ped_size:

            for _ in range(0, ped_size):
                _ped += _dec.pop(0)
            yield _resval(_ped)

        elif 0 < len(_dec) < ped_size:
            _ped = "".join(_dec)
            _dec.clear()
            yield _resval(_ped)

        else:
            _active = False
            break

    return None


# START PROGRAM TIME
STARTS: float = now()


# PROCESSING
def process_chars(pack_size: int = 16, letter: str = None) -> Iterable[str]:
    _mul = lambda x,y: int(x) * int(y)
    _add = lambda x,y: int(x) + int(y)
    _rec = f"{now()}.{STARTS}.{now()}".split('.')
    _bins = ''.join((custom_bin(i) for i in _rec))
    _revbins = reversed(_bins)
    _pack_one = packing(_bins, pack_size, True)
    _pack_tow = packing(_revbins, pack_size, True)
    _insertletter = (
        f"{rand_char(letter)}{_add(o,t)}{rand_char(letter)}{o}{rand_char(letter)}{t}{rand_char(letter)}{_mul(o,t)}{rand_char(letter)}"
        for o,t in zip(_pack_one, _pack_tow)
        )
    return _insertletter


# MAKE UNIQUE KEY
def unique_key(length: int = 32, pack_size: int = 16, letter: str = None) -> str:
    """[Unique Key]

    Args:
        length (int, optional): [Key Length]. Defaults to 32.
        pack_size (int, optional): [Pack Intiger Size]. Defaults to 16.

    Returns:
        str: [Generated Unique Key]
    """
    _choice = lambda x: rand_char(x)
    _pr = ''.join(process_chars(pack_size, letter))
    _in_size = [_choice(_pr) for _ in range(0, length)]
    return ''.join(_in_size)



__dir__ = ("rand_char", "unique_key")
