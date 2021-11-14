# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT
import os
import concurrent.futures

# IMPORT LOCAL
try:
    from container import Container
    from utils import RawData, sha256, md5, now, timestamp_to_str
    from exceptions import *
except ImportError:
    from note_container.container import Container
    from note_container.utils import RawData, sha256, md5, now, timestamp_to_str
    from note_container.exceptions import *

# IMPORT TYPING
from typing import Union, Callable, Iterable


__all__ = ("NoteContainer",)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #


# NOTE_CONTAINER
class NoteContainer:
    # TODO: Multi Action Method (all method starts with `iter`) is Slow Now Must Some Changes or Changes Algorithm For SpeedUp
    # NOTE: This Container Created For Little Data For Bigger Data Use Container Class From container

    REPLACE = True
    HEADER = '*'

    def __init__(self, path: str, key: Union[str, bytes], algorithm: Union[Callable, str] = None) -> None:
        """[Note Container Collectable Object Based On Zip File Standard Modules]

        Args:
            path (str): [Container Path]
            key (Union[str, bytes]): [Secure Key]
            algorithm (Union[Callable, str], optional): [Hash Key Algorithm default 'sha3_512']. Defaults to None.
                ALGORITHM SUPPORTS BY NAME ['md5', 'sha256', 'sha3_512'] or Custom Callable Algorithm
        """
        self.__container = Container(path, self.REPLACE)
        self.__header = None
        self.__dump = lambda x: RawData.secure_dumps(x, key, algorithm)
        self.__load = lambda x: RawData.secure_loads(x, key, algorithm)

        self.__ready()

    def __ready(self) -> None:
        # READY CONTAINER
        # LOAD OR CREATE HEADER
        match self.HEADER in self.__container:
            
            case True:
                try:
                    self.__header = self.__load(self.__container['*'])
                    if self.__header.get('info', None) is None:
                        del self
                        raise CorruptedError
                except (BaseException, Exception):
                    del self
                    raise CorruptedError
            
            case False:
                self.__head_make()
                self.__ready()

    def __head_make(self) -> None:
        # CREATE HEADER FIRST TIME
        head = {
            'info': {'create': now(), 'count': 0, 'note_count': 0, 'section_count': 0},
            'obj': {}
        }
        self.__container[self.HEADER] = self.__dump(head)

    def __head_update(self) -> None:
        # HARD UPDATE HEAD UPDATE CHANGES IN CONTAINER
        self.__container.update(self.HEADER, self.__dump(self.__header))

    def all_member(self) -> Iterable[str]:
        """[All Member Name In Container]

        Returns:
            Iterable[str]: [Object Names]

        Yields:
            Iterator[Iterable[str]]: [name]
        """
        for name in self.__header['obj'].keys():
            yield name

    def all_updated(self) -> Iterable[str]:
        """[All Updated Object Name]

        Returns:
            Iterable[str]: [Object Names]

        Yields:
            Iterator[Iterable[str]]: [name]
        """
        for name in self.__header['obj'].keys():
            if len(self.get_obj_info(name)['update']) > 0:
                yield name

    def all_note_updated(self) -> Iterable[str]:
        """[All Note Updated Names]

        Returns:
            Iterable[str]: [Note Object Updated Names]

        Yields:
            Iterator[Iterable[str]]: [name]
        """
        for name in self.__header['obj'].keys():
            info = self.get_obj_info(name)
            if info['type'] == 'N':
                if len(info['update']) > 0:
                    yield name
                else:
                    continue
            else:
                continue

    def all_section_updated(self) -> Iterable[str]:
        """[All Section Updated Names]

        Returns:
            Iterable[str]: [Section Object Updated Names]

        Yields:
            Iterator[Iterable[str]]: [name]
        """
        for name in self.__header['obj'].keys():
            info = self.get_obj_info(name)
            if info['type'] == 'S':
                if len(info['update']) > 0:
                    yield name
                else:
                    continue
            else:
                continue

    def update_list(self, name: str, timestamp: bool = False) -> list:
        """[Update History List]

        Args:
            name (str): [Object Name]
            timestamp (bool): [False Mean Time Humanize or True Mean TimeStamp Float Type] Defaults to False.

        Raises:
            NameNotExistsError: [If Name Not Exists in Container]

        Returns:
            list: [Update History list[tuple[time, old_hash, now_hash]]]
        """
        info = self.get_obj_info(name, None)
        match info:
            case None:
                raise NameNotExistsError
        match timestamp:
            case False:
                return [(timestamp_to_str(t), o, n) for t, o, n in info['update']]
            case True:
                return info['update']

    def all_update_list(self, timestamp: bool = False) -> Iterable[tuple[str,list]]:
        """[summary]

        Args:
            timestamp (bool): [False Mean Time Humanize or True Mean TimeStamp Float Type] Defaults to False.

        Returns:
            Iterable[tuple[str,list]]: [Update History Tuple(Name, HistoryList)]

        Yields:
            Iterator[Iterable[tuple[str,list]]]: [Tuple Name and History Update]
        """
        for name in self.all_updated():
            try:
                yield self.update_list(name, timestamp)
            except NameNotExistsError:
                continue

    def name_filter_note(self) -> Iterable[str]:
        """[All Name Note Object]

        Returns:
            Iterable[str]: [Names Note Objects]

        Yields:
            Iterator[Iterable[str]]: [name]
        """
        for name in self.__header['obj'].keys():
            if self.__header['obj'][name]['type'] == 'N':
                yield name

    def name_filter_section(self) -> Iterable[str]:
        """[All Name Section Object]

        Returns:
            Iterable[str]: [Names Section Object]

        Yields:
            Iterator[Iterable[str]]: [name]
        """
        for name in self.__header['obj'].keys():
            if self.__header['obj'][name]['type'] == 'S':
                yield name

    def make_time_sort(self, type_filter: str = None, reverse: bool = False) -> list[str]:
        """[Create Time Sort]

        Args:
            type_filter (str, optional): [Filter Object 'note' or 'section' or None for all]. Defaults to None.
            reverse (bool, optional): [Reversed Sort]. Defaults to False.

        Returns:
            list[str]: [Sorted List]
        """
        match type_filter:
            case None:
                return sorted(self.all_member(), key= lambda x: self.get_obj_info(x)['create'], reverse=reverse)
            case 'note':
                return sorted(self.name_filter_note(), key= lambda x: self.get_obj_info(x)['create'], reverse=reverse)
            case 'section':
                return sorted(self.name_filter_section(), key= lambda x: self.get_obj_info(x)['create'], reverse=reverse)

    def update_time_sort(self, type_filter: str = None, reverse: bool = False) -> list[str]:
        """[Update Time Sort]

        Args:
            type_filter (str, optional): [Filter Object 'note' updated or 'section' updated or None for all updated]. Defaults to None.
            reverse (bool, optional): [Reversed Sort]. Defaults to False.

        Returns:
            list[str]: [Sorted List]
        """
        match type_filter:
            case None:
                return sorted(self.all_updated(), key= lambda x: self.get_obj_info(x)['update'][-1][0], reverse=reverse)
            case 'note':
                return sorted(self.all_note_updated(), key= lambda x: self.get_obj_info(x)['update'][-1][0], reverse=reverse)
            case 'section':
                return sorted(self.all_section_updated(), key= lambda x: self.get_obj_info(x)['update'][-1][0], reverse=reverse)

    def get_info(self) -> dict:
        """[Data Head Info]

        Returns:
            dict: [info]
        """
        return self.__header['info']

    def get_obj_info(self, name: str, alt: object = None) -> Union[dict, object]:
        """[Object Info]

        Args:
            name (str): [Member Name]
            alt (object, optional): [Alternative if not exists name return alt]. Defaults to None.

        Returns:
            Union[dict, object]: [Member Info or alt]
        """
        return self.__header['obj'].get(name, alt)

    def add_note(self, name: str, note: str) -> None:
        """[Add Note]

        Args:
            name (str): [Note Name Must Unique]
            note (str): [Note]

        Raises:
            AddTypeError: [Type Error When Try Section Add To Note]
            NameExistsError: [Name Is Already Exists]
        """
        match not isinstance(note, str):
            case True:
                raise AddTypeError
        
        with concurrent.futures.ThreadPoolExecutor() as executer:
            _hash_name = executer.submit(md5, name.encode('utf-8')).result().hexdigest()
            _hash_note = executer.submit(sha256, note.encode('utf-8')).result().hexdigest()
            _note = executer.submit(self.__dump, note).result()

        match _hash_name in self.__container:
            case True:
                raise NameExistsError
        
        self.__header['obj'][name] = {'member': _hash_name, 'create': now(),'type': 'N', 'length': len(note), 'sha256':_hash_note, 'update': []}
        self.__header['info']['note_count'] += 1
        self.__header['info']['count'] += 1
        self.__container[_hash_name] = _note
        self.__head_update()

    def iter_add_note(self, notes: Iterable[tuple[str, str]]) -> None:
        """[Add Multi Notes]
        
        !! FOR NOW IS SLOW !!

        Args:
            notes (Iterable[tuple[str, str]]): [Get Iterable of Tuple(name, note)]
        """
        with concurrent.futures.ThreadPoolExecutor() as executer:
            [executer.submit(self.add_note, name, note).result() for name, note in notes if name not in self]

    def update_note(self, name: str, note: str) -> None:
        """[Update Replace Exists Name]

        Args:
            name (str): [Name]
            note (str): [Note]

        Raises:
            NameNotExistsError: [Name Not Exists]
            UpdateTypeError: [Update Section With Update Note]
            NewNoteSameExistsNote: [Nothing Changed For Update]
        """
        info = self.get_obj_info(name, None)
        _hash_note = sha256(note.encode('utf-8')).hexdigest()
        
        match info:
            case None:
                raise NameNotExistsError
        
        match info['type']:
            case 'S':
                raise UpdateTypeError

        member = info['member']
        old_hash = info['sha256']
        
        match _hash_note == old_hash:
            case True:
                raise NewNoteSameExistsNote

        upd = info['update']
        upd.append((now(), old_hash, _hash_note))
        self.__header['obj'][name].update({'length': len(note),'sha256':_hash_note, 'update': upd})
        self.__container.update(member, self.__dump(note))

        self.__head_update()

    def iter_update_note(self, notes: Iterable[tuple[str, str]]) -> None:
        """[Multi Update Note]

        !! FOR NOW IS SLOW !!

        Args:
            notes (Iterable[tuple[str, str]]): [Iterable Tuple(name, note)]
        """
        with concurrent.futures.ThreadPoolExecutor() as executer:
            [executer.submit(self.update_note, name, note).result() for name, note in notes if name in self]

    def append_note(self, name: str, append_note: str) -> None:
        """[Append Note]

        Args:
            name (str): [Name For Appending]
            append_note (str): [Note Append After Old Note]

        Raises:
            NameNotExistsError: [Name Not Exists]
            AppendingTypeError: [Type Error if Try Appending Section]
        """
        info = self.get_obj_info(name, None)
        
        match info:
            case None:
                raise NameNotExistsError
        
        match info['type']:
            case 'S':
                raise AppendingTypeError
        
        member = info['member']
        old_hash = info['sha256']
        _notes = self.__load(self.__container[member])
        _notes += append_note

        _hash_note = sha256(_notes.encode('utf-8')).hexdigest()
        upd = info['update']
        upd.append((now(), old_hash, _hash_note))
        self.__header['obj'][name].update({'length': len(_notes), 'sha256':_hash_note, 'update': upd})
        self.__container.update(member, self.__dump(_notes))

        self.__head_update()

    def iter_append_note(self, notes: Iterable[tuple[str, str]]) -> None:
        """[Multi Append Note]

        !! FOR NOW IS SLOW !!

        Args:
            notes (Iterable[tuple[str, str]]): [Iterable Tuple(name, note) for appending]
        """
        with concurrent.futures.ThreadPoolExecutor() as executer:
            [executer.submit(self.append_note, name, note).result() for name, note in notes if name in self]

    def get_note(self, name:str) -> str:
        """[Get Note]

        Args:
            name (str): [Note Member Name]

        Raises:
            NameNotExistsError: [Not Exists Name]
            GetDataTypeError: [Try Get Section With this Method]
            CorruptedError: [Key Error Or Other Connecting issue]

        Returns:
            [str]: [Note]
        """
        info = self.get_obj_info(name, None)
        
        match info:
            case None:
                raise NameNotExistsError
        
        match info['type']:
            case 'S':
                raise GetDataTypeError

        member = info['member']
        getnote = self.__load(self.__container[member])
        match sha256(getnote.encode('utf-8')).hexdigest() == info['sha256']:
            case False:
                raise CorruptedError
        return getnote

    def remove(self, name: str) -> None:
        """[Remove Member Any type Section or Note]

        Args:
            name (str): [Object Name For Removing] 
        """
        info = self.get_obj_info(name, None)
        match info:
            case None:
                return
        
        member = info['member']
        _type = info['type']
        del self.__container[member]
        self.__header['info']['count'] -= 1
        
        match _type:
            case 'N':
                self.__header['info']['note_count'] -= 1
            case 'S':
                self.__header['info']['section_count'] -= 1
        
        del self.__header['obj'][name]
        self.__head_update()

    def iter_remove(self, names: Iterable[str]) -> None:
        """[Multi Removing]

        !! FOR NOW IS SLOW !!

        Args:
            names (Iterable[str]): [Iterable Name for Removing]
        """
        with concurrent.futures.ThreadPoolExecutor() as executer:
            [executer.submit(self.remove, name).result() for name in names]

    def iter_get(self, names: Iterable[str]) -> Iterable[tuple[str, Union[str, dict]]]:
        """[Multi Get Any Object Section or Note]

        Args:
            names (Iterable[str]): [Iterable of Member Name]

        Returns:
            Iterable[tuple[str, Union[str, dict]]]: [Tuple(name, data)]

        Yields:
            Iterator[Iterable[tuple[str, Union[str, dict]]]]: [Iterable tuple(name, data)]
        """
        with concurrent.futures.ThreadPoolExecutor() as executer:
            res = [(name, executer.submit(self.__getitem__, name).result()) for name in names if name in self]
        for item in res:
            yield item

    def add_section(self, name: str, section_data: dict) -> None:
        """[Add Section]

        Args:
            name (str): [Section Name]
            section_data (dict): [Section Data]

        Raises:
            AddTypeError: [Try Add Note With This Method]
            NameExistsError: [Name Already Exists]
        """
        match not isinstance(section_data, dict):
            case True:
                raise AddTypeError
        with concurrent.futures.ThreadPoolExecutor() as executer:
            _hash_name = executer.submit(md5, name.encode('utf-8')).result().hexdigest()
            _data = executer.submit(self.__dump, section_data).result()
            _hash_section = executer.submit(sha256, _data).result().hexdigest()

        match _hash_name in self.__container:
            case True:
                raise NameExistsError
        
        self.__header['obj'][name] = {'member': _hash_name, 'create': now(),'type': 'S', 'length': len(section_data), 'sha256':_hash_section, 'update': []}
        self.__header['info']['section_count'] += 1
        self.__header['info']['count'] += 1
        self.__container[_hash_name] = _data
        self.__head_update()

    def iter_add_section(self, data: Iterable[tuple[str, dict]]) -> None:
        """[Multi Add Section]

        !! FOR NOW IS SLOW !!

        Args:
            data (Iterable[tuple[str, dict]]): [Iterable Tuple(name, section)]
        """
        with concurrent.futures.ThreadPoolExecutor() as executer:
            [executer.submit(self.add_section, name, val).result() for name, val in data if name not in self]

    def get_section(self, name: str) -> dict:
        """[Get Data From Section Object]

        Args:
            name (str): [Section Name]

        Raises:
            NameNotExistsError: [Name Not Exists]
            GetDataTypeError: [Try Get Note With This Method]
            CorruptedError: [Key Error Or Other Connecting issue]

        Returns:
            dict: [Section]
        """
        info = self.get_obj_info(name, None)
        
        match info:
            case None:
                raise NameNotExistsError
        
        match info['type']:
            case 'N':
                raise GetDataTypeError
        
        member = info['member']
        getsection = self.__container[member]
        match sha256(getsection).hexdigest() == info['sha256']:
            case False:
                raise CorruptedError
        return self.__load(getsection)

    def update_section(self, name: str, update_data: dict) -> None:
        """[Update or Replace Exists Section]

        Args:
            name (str): [Section Name]
            update_data (dict): [New Section Data for Replace]

        Raises:
            NameNotExistsError: [Name Not Exists]
            UpdateTypeError: [Try Update Note with This Method]
            NewNoteSameExistsNote: [Nothing Changed For Update]
        """
        info = self.get_obj_info(name, None)
        _data = self.__dump(update_data)
        _hash_section = sha256(_data).hexdigest()
        
        match info:
            case None:
                raise NameNotExistsError
        
        match info['type']:
            case 'N':
                raise UpdateTypeError
        
        member = info['member']
        old_hash = info['sha256']
        
        match _hash_section == old_hash:
            case True:
                raise NewNoteSameExistsNote

        upd = info['update']
        upd.append((now(), old_hash, _hash_section))
        self.__header['obj'][name].update({'length': len(update_data),'sha256':_hash_section, 'update': upd})
        self.__container.update(member, _data)

        self.__head_update()

    def iter_update_section(self, data: Iterable[tuple[str, str]]) -> None:
        """[Multi Update Section]

        !! FOR NOW IS SLOW !!

        Args:
            data (Iterable[tuple[str, dict]]): [Iterable Tuple(name, section)]
        """
        with concurrent.futures.ThreadPoolExecutor() as executer:
            [executer.submit(self.update_section, name, val).result() for name, val in data if name in self]

    def append_section(self, name: str, append_data: dict) -> None:
        """[Appending Section Update Section data With New Data Any changed new Section or Change old Section]

        Args:
            name (str): [Section Name]
            append_data (dict): [Data For Update Section]

        Raises:
            NameNotExistsError: [Name Not Exists]
            AppendingTypeError: [Try Note With This Method]
        """
        info = self.get_obj_info(name, None)
        
        match info:
            case None:
                raise NameNotExistsError
        
        match info['type']:
            case 'N':
                raise AppendingTypeError

        member = info['member']
        old_hash = info['sha256']
        data = self.__load(self.__container[member])
        data.update(append_data)

        _data = self.__dump(data)

        _hash_section = sha256(_data).hexdigest()
        upd = info['update']
        upd.append((now(), old_hash, _hash_section))
        self.__header['obj'][name].update({'length': len(data), 'sha256':_hash_section, 'update': upd})
        self.__container.update(member, _data)

        self.__head_update()

    def iter_append_section(self, data: Iterable[tuple[str, dict]]) -> None:
        """[Multi Appending Section]

        !! FOR NOW IS SLOW !!

        Args:
            data (Iterable[tuple[str, dict]]): [Iterable Tuple(name, section)]
        """
        with concurrent.futures.ThreadPoolExecutor() as executer:
            [executer.submit(self.append_section, name, val).result() for name, val in data if name in self]

    def get(self, name: str, alt: object = None) -> Union[str, dict, object]:
        """[Get Method Can Handle Any Type Section or None]

        Args:
            name (str): [Object Name]
            alt (object, optional): [Alternative if not exists Name]. Defaults to None.

        Returns:
            Union[str, dict, object]: [Note or Section or Alternative]
        """
        try:
            return self.__getitem__(name)
        except NameNotExistsError:
            return alt

    def clear(self) -> None:
        """[Clear All Activity In Container And Clean Head File]
        ## ANY THING DELETING WITH THIS METHOD BE ##
        """
        temp = self.get_info()
        temp.update({'count': 0, 'note_count': 0, 'section_count': 0})
        self.__container.clear()
        self.__head_make()
        self.__header['info'].update(temp)
        self.__header['obj'].clear()
        self.__head_update()

    def __setitem__(self, name: str, data: Union[str, dict]) -> None:
        """[Dynamic Set Handle Note & Section]

        Args:
            name (str): [Object Name]
            data (Union[str, dict]): [Note String & Section Dict]

        Raises:
            NameExistsError: [Name Exists Error If Replace False]
            DataTypeError: [Data Type Not Support]
        """
        info = self.get_obj_info(name, None)
        match self.REPLACE:
            case False:
                if info is not None:
                    raise NameExistsError
                else:
                    if isinstance(data, str):
                        self.add_note(name, data)
                    elif isinstance(data, dict):
                        self.add_section(name, data)
                    else:
                        raise DataTypeError
            case True:
                if info is None:
                    if isinstance(data, str):
                        self.add_note(name, data)
                    elif isinstance(data, dict):
                        self.add_section(name, data)
                    else:
                        raise DataTypeError
                else:
                    if isinstance(data, str):
                        self.update_note(name, data)
                    elif isinstance(data, dict):
                        self.update_section(name, data)
                    else:
                        raise DataTypeError

    def __getitem__(self, name: str) -> Union[str, dict]:
        """[Dynamic Get Handle Note & Section]

        Args:
            name (str): [Object Name]

        Raises:
            NameNotExistsError: [Name Not Exists]

        Returns:
            Union[str, dict]: [Note or Section]
        """
        info = self.get_obj_info(name, None)
        
        if info is None:
            raise NameNotExistsError
        
        match info['type']:
            case 'N':
                return self.get_note(name)
            case 'S':
                return self.get_section(name)

    def __delitem__(self, name: str) -> None:
        """[Dynamic Del Item]

        Args:
            name (str): [Name Object For Deleting]
        """
        info = self.get_obj_info(name, None)
        
        match info:
            case None:
                return
            case _:
                self.remove(name)

    def __contains__(self, name: str) -> bool:
        """[Contains Name in the Container]

        Args:
            name (str): [Name For Check Into The Container]

        Returns:
            bool: [True if exists other False]
        """
        info = self.get_obj_info(name, None)
        match info:
            case None:
                return False
        return True



__dir__ = ("NoteContainer",)
