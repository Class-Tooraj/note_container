# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #

# IMPORT
import sys
import argparse

# IMPORT LOCAL
from note_container.note import NoteContainer
from note_container.utils import monotonic

# IMPORT TYPING
from typing import Sequence

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

_PROGRAM = 'Note Container'
_DESCRIPTION = 'Simple Data Container Based On Zip With Secure Data'
_VERSION = 'A:0.1'


def handle(commands: dict) -> None:
    t0 = monotonic()
    work = lambda x: print(x) if commands['verbose'] else None
    
    _active = NoteContainer(commands['path'], commands['key'], commands['hash_algorithm'])
    
    work(f"Note Container `{commands['path']}` Is Active")
    
    if commands['all_names']:
        print("\n".join(_active.all_member()))
    
    if commands['all_updated']:
        print("\n".join(_active.all_updated()))
    
    if commands['all_note_updated']:
        print("\n".join(_active.all_note_updated()))
    
    if commands['all_section_updated']:
        print("\n".join(_active.all_section_updated()))
    
    if commands['all_update_history']:
        for it in _active.all_update_list(False):
            print(f"{it[0]} -> {it[1]}")
    
    if x := commands['history']:
        print(f"{x} -> {_active.update_list(x, False)}")
    
    if x := commands['name_filter']:
        match x:
            case 'note':
                print(f'FILTER ---- {x} ----\n{[*_active.name_filter_note()]}')
            case 'section':
                print(f'FILTER ---- {x} ----\n{[*_active.name_filter_section()]}')
    
    if x := commands['sorted']:
        match x:
            case 'make':
                srt = _active.make_time_sort(commands['sort_type'], reverse=commands['reverse_sort'])
                print(f'FILTER:{commands["sort_type"]} -- SORTED ---- {x} ----\n{srt}')
            case 'update':
                srt = _active.update_time_sort(commands['sort_type'], reverse=commands['reverse_sort'])
                print(f'FILTER:{commands["sort_type"]} -- SORTED ---- {x} ----\n{srt}')

    if x := commands['add_note']:
        _active.add_note(x[0], x[1])
        work(f'Add Note `{x[0]}` Into The Container')
    
    if x := commands['get']:
        get = _active[x]
        print(f"{x} -> {get}")
    
    if x := commands['update_note']:
        _active.update_note(x[0], x[1])
        work(f'Updated Note `{x[0]}`')

    if x := commands['append_note']:
        _active.append_note(x[0], x[1])
        work(f"Appending New Note To `{x[0]}`")

    if x := commands['get_info']:
        print(f"{x} > {_active.get_obj_info(x)}")

    if x := commands['info']:
        print(f"INFO > {_active.get_info()}")

    if x := commands['add_section']:
        _active.add_section(x[0], eval(x[1]))
        work(f"Add Section `{x[0]}` Into The Container")

    if x := commands['update_section']:
        _active.update_section(x[0], eval(x[1]))
        work(f'Updated Section `{x[0]}`')

    if x := commands['append_section']:
        _active.append_section(x[0], eval(x[1]))
        work(f"Appending Section `{x[0]}`")

    if x := commands['delete']:
        _active.delete(x)
        work(f"Deleted `{x}` From Container")

    if x := commands['clear']:
        _active.clear()
        work(f"Container `{commands['path']}` is Cleared")

    if commands['time']:
        print(f'Finished in {monotonic() - t0:.4}')
    
    work(f"Note Container `{commands['path']}` Deactivate")


# MAIN FUNCTION
def main(argv: Sequence[str] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(_PROGRAM, description = _DESCRIPTION)
    parser.add_argument(
        '--version',
        '-V',
        action = 'version',
        version=f'%(prog)s {_VERSION}'
    )

    parser.add_argument(
        'path',
        type= str,
        help= 'Container File Path',
    )

    parser.add_argument(
        'key',
        type= str,
        help= 'Secure Data Key',
    )

    parser.add_argument(
        '--all_names',
        '-A',
        default= False,
        action = 'store_true',
        help = 'Get All Member Names'
    )

    parser.add_argument(
        '--all_updated',
        '-Au',
        default= False,
        action = 'store_true',
        help = 'Get All Updated Member Names'
    )

    parser.add_argument(
        '--all_note_updated',
        '-Nu',
        default= False,
        action = 'store_true',
        help = 'Get All Note Updated Names'
    )

    parser.add_argument(
        '--all_section_updated',
        '-Su',
        default= False,
        action = 'store_true',
        help = 'Get All Section Updated Names'
    )

    parser.add_argument(
        '--all_update_history',
        '-Uh',
        default= False,
        action = 'store_true',
        help = 'All Updated History'
    )

    parser.add_argument(
        '--history',
        '-h',
        type= str,
        help= 'Object Update History Need `Name`'
    )

    parser.add_argument(
        '--name_filter',
        '-nf',
        default= None,
        choices=['section', 'note'],
        help = "All Named Filter With Object Chose `section` or `note`"
    )

    parser.add_argument(
        '--add_note',
        '-an',
        type= str,
        nargs= 2,
        help= 'Add Note To Container Need `Name` & `Note`'
    )

    parser.add_argument(
        '--get',
        '-g',
        type= str,
        help= 'Get Note or Section From Container Need `Name`'
    )

    parser.add_argument(
        '--get_info',
        '-gi',
        type= str,
        help= 'Get Object Info'
    )

    parser.add_argument(
        '--update_note',
        '-un',
        type= str,
        nargs=2,
        help= 'Update or Replace Existed Name Need `Name` & `New Note`'
    )

    parser.add_argument(
        '--sorted',
        '-S',
        default = None,
        choices= ['make', 'update'],
        help= 'Sorted chose `make` or `update`'
    )

    parser.add_argument(
        '--reverse_sort',
        '-R',
        default = False,
        action = 'store_true',
        help = 'Reverse Sort'
    )

    parser.add_argument(
        '--sort_type',
        '-T',
        default=None,
        choices= ['section', 'note'],
        help = 'Filter Type Sorted Default is All member chose `note` or `section`'
    )

    parser.add_argument(
        '--append_note',
        '-pn',
        type= str,
        nargs= 2,
        help= 'Appends Note To Existed Note Need `Name` & `Appending Note`'
    )

    parser.add_argument(
        '--add_section',
        '-as',
        type = str,
        nargs = 2,
        help= 'Add Section Need `Name` and `StrDictionary`'
    )

    parser.add_argument(
        '--update_section',
        '-us',
        type= str,
        nargs=2,
        help= 'Update or Replace Existed Name Need `Name` & `New Section`'
    )

    parser.add_argument(
        '--append_section',
        '-ps',
        type= str,
        nargs= 2,
        help= 'Appends & Update Section To Existed Section Need `Name` & `Appending Section`'
    )

    parser.add_argument(
        '--info',
        '-i',
        default= False,
        action = 'store_true',
        help = 'Get Container Info'
    )

    parser.add_argument(
        '--delete',
        '-D',
        type= str,
        help= 'Delete <Remove> Member From Container Need `Name` [NO RECOVERY]'
    )

    parser.add_argument(
        '--clear',
        '-C',
        default=False,
        action='store_true',
        help= 'Clear Container From Any Members [NO RECOVERY]'
    )

    parser.add_argument(
        '--hash_algorithm',
        '-H',
        type= str,
        default= 'sha3_512',
        help = 'Hash Algorithm Support `sha256`, `md5`, `sha3_512`'
    )

    parser.add_argument(
        '--time',
        '-t',
        default= False,
        action = 'store_true',
    )

    parser.add_argument(
        '--verbose',
        '-v',
        default= False,
        action = 'store_true',
    )

    argus = vars(parser.parse_args())
    # print(argus)
    handle(argus)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())