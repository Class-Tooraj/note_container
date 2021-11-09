# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT
import os

# IMPORT LOCAL
try:
    from zip_man import UZip, ZIP_LZMA
    from exceptions import *
except ImportError:
    from note_container.zip_man import UZip, ZIP_LZMA
    from note_container.exceptions import *


# IMPORT TYPING
from typing import Iterable


__all__ = ('Container',)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #


# CONTAINER
class Container:

    def __init__(self, path: str, replace: bool = True) -> None:
        self.__path = os.path.abspath(path)
        self.__archive: UZip = UZip
        self.__replace = replace

        self.__ready()

    def __ready(self) -> None:
        match os.path.isfile(self.__path):
            case False:
                self.__create()

    def __create(self) -> None:
        with self.__archive(self.__path, 'w', compression=ZIP_LZMA, allowZip64=True) as zf:
            zf.close()

    def all_member(self) -> list[str]:
        with self.__archive(self.__path, 'r', compression=ZIP_LZMA, allowZip64=True) as zf:
            return zf.namelist()

    def append(self, member: str, data: bytes) -> None:
        with self.__archive(self.__path, 'a', compression=ZIP_LZMA, allowZip64=True) as zf:
            if member in self:
                _data = zf.read(member) + data
                zf.writestr(member, _data)
            else:
                zf.writestr(member, data)

    def iter_remove(self, members: Iterable[str]) -> None:
        with self.__archive(self.__path, 'a', compression=ZIP_LZMA, allowZip64=True) as zf:
            for mem in members:
                zf.remove_file(mem)

    def iter_set(self, items: Iterable[tuple[str, bytes]]) -> None:
        with self.__archive(self.__path, 'a', compression=ZIP_LZMA, allowZip64=True) as zf:
            for mem, data in items:
                match self.__replace:
                    case True:
                        zf.writestr(mem, data)
                    case False:
                        match mem in self:
                            case True:
                                continue
                            case False:
                                zf.writestr(mem, data)

    def iter_get(self, members: Iterable[str]) -> Iterable[tuple[str, bytes]]:
        with self.__archive(self.__path, 'a', compression=ZIP_LZMA, allowZip64=True) as zf:
            for mem in members:
                match mem in self:
                    case True:
                        yield (mem, zf.read(mem))
                    case False:
                        continue

    def update(self, member: str, data: bytes) -> None:
        if not member in self:
            raise MemberNotExistsError

        with self.__archive(self.__path, 'a', compression=ZIP_LZMA, allowZip64=True) as zf:
            zf.writestr(member, data)
    
    def get(self, member: str, alt: object = None) -> object:
        try:
            return self.__getitem__(member)
        except MemberNotExistsError:
            return alt

    def clear(self) -> None:
        self.iter_remove(self.all_member())

    def __setitem__(self, member: str, data: bytes) -> None:
        match self.__replace:
            case True:
                with self.__archive(self.__path, 'a', compression=ZIP_LZMA, allowZip64=True) as zf:
                    zf.writestr(member, data)
            case False:
                if not member in self:
                    with self.__archive(self.__path, 'a', compression=ZIP_LZMA, allowZip64=True) as zf:
                        zf.writestr(member, data)
                else:
                    raise MemberExistsError

    def __getitem__(self, member: str) -> bytes:
        if not member in self:
            raise MemberNotExistsError

        with self.__archive(self.__path, 'r', compression=ZIP_LZMA, allowZip64=True) as zf:
            with zf.open(member, 'r') as mem:
                return mem.read()

    def __delitem__(self, member: str) -> None:
        with self.__archive(self.__path, 'a', compression=ZIP_LZMA, allowZip64=True) as zf:
            zf.remove_file(member)

    def __contains__(self, member: str) -> bool:
        with self.__archive(self.__path, 'r', compression=ZIP_LZMA, allowZip64=True) as zf:
            return member in zf.namelist()


__dir__ = ('Container',)
