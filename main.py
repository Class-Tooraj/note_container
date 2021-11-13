# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #

# IMPORT
import os
import sys
import argparse

# IMPORT LOCAL
from note_container.note import NoteContainer
from note_container.container import Container
from note_container.utils import monotonic, sha256, sha3_512, md5, now, timstamp_to_str
from note_container.uniqueize import unique_key

# IMPORT TYPING
from typing import Sequence

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

_PROGRAM = 'Note Container'
_DESCRIPTION = 'Simple Data Container Based On Zip With Secure Data'
_VERSION = 0.1

_OTHER_COMMAND = ('hash', 'now', 'key', 'container', 'archive')


# CONTAINER `ARCHIVE` HANDLE
def _container_handle(parser: argparse.ArgumentParser) -> int:
    parser.add_argument(
        'path',
        type= str,
        help= 'Container `Archive` Path'
    )

    parser.add_argument(
        '--replace',
        '-R',
        default= True,
        action = 'store_true',
        help = ''
    )

    parser.add_argument(
        '--delete',
        '-D',
        type=str,
        help= 'Delete Member From Container !![NO RECOVERY]!!'
    )

    parser.add_argument(
        '--add',
        '-a',
        type=str,
        nargs=2,
        help= 'Add Member Need `Name` & `TEXT`'
    )

    parser.add_argument(
        '--all_member',
        '-A',
        default=False,
        action = 'store_true',
        help = 'All Container Member Names'
    )

    parser.add_argument(
        '--extract',
        '-e',
        type= str,
        nargs= 2,
        help= 'Extract Member From Container Need `Name` & `Path`'
    )

    parser.add_argument(
        '--get',
        '-g',
        type=str,
        help= 'Grab Data From Container Need `Name`'
    )

    parser.add_argument(
        '--append',
        '-ap',
        type=str,
        nargs= 2,
        help= 'Append Data To Existed Member or Create Member Need `Name` & `Data or Path`'
    )

    parser.add_argument(
        '--update',
        '-u',
        type= str,
        nargs = 2,
        help= 'Update `Replace` Data To Existed Member Need `Name` & `Data or Path`'
    )

    parser.add_argument(
        '--clear',
        '-C',
        default=False,
        action = 'store_true',
        help = 'Clear Container From Any Members !![NO RECOVERY]!!'
    )

    argus = vars(parser.parse_args())
    container = Container(argus['path'], argus['replace'])
    work = lambda x: print(x) if argus['verbose'] is True else None
    t0 = monotonic()

    if x:= argus['add']:
        try:
            container[x[0]] = x[1].encode('utf-8')
            work(f'Add {x[0]} Into Container')
        except Exception as err:
            work(f'ADD ERR\t{type(err).__name__}({err})')

    if x:= argus['append']:
        try:
            container.append(x[0], x[1].encode('utf-8'))
            work(f'APPEND {x[0]} Into Container')
        except Exception as err:
            work(f'APPEND ERR\t{type(err).__name__}({err})')

    if x:= argus['get']:
        try:
            get = container[x]
            print(f'{x} -> {get}')
        except Exception as err:
            work(f'GET ERR\t{type(err).__name__}({err})')

    if x:= argus['extract']:
        try:
            path = os.path.abspath(x[1])
            get = container[x[0]]
            work(f'GET {x[0]} From Container')
            try:
                with open(path, 'wb') as f:
                    f.write(get)
            except Exception as err:
                work(f'WRITE ERR\t{type(err).__name__}({err})')
        except Exception as err:
            work(f'GET ERR\t{type(err).__name__}({err})')

    if x:= argus['delete']:
        del container[x]
        work(f'DELETED {x} IF EXISTS NOW GONE :)')

    if x:= argus['update']:
        try:
            container.update(x[0], x[1].encode('utf-8'))
            work(f'UPDATE {x[0]} Member Of Container')
        except Exception as err:
            work(f'UPDATE ERR\t{type(err).__name__}({err})')

    if argus['clear']:
        container.clear()
        work(f'Container `Archive` [{argus["path"]}] CLEARED')

    if argus['time']:
        print(f'Finished in {monotonic() - t0:.4}')

    return 0

# NOW `TIME` HANDLE
def _now_handle(order: dict) -> str:
    if order['timestamp']:
        return f'{now()}'
    return timstamp_to_str(now())

# KEY GENERATE HANDLE
def _key_handle(order: dict) -> str:
    keys = (unique_key(order['length'], order['packsize'], order['chars']) for _ in range(0, order['many']))
    if order['file']:
        path = os.path.abspath(order['file'])
        with open(path, 'w') as f:
            f.write('\n'.join(keys))
        return f"Generated {order['many']} Key Saved To {path}"
    
    return '\n'.join(keys)

# HASH HANDLE
def _hash_handle(order: dict) -> str:
    alg = order['algorithm']
    match alg:
        case 'sha256':
            if order['file']:
                path = os.path.abspath(order['input'])
                with open(path, 'rb') as f:
                    return sha256(f.read()).hexdigest()
            return sha256(order['input'].encode('utf-8')).hexdigest()
        
        case 'sha3_512':
            if order['file']:
                path = os.path.abspath(order['input'])
                with open(path, 'rb') as f:
                    return sha3_512(f.read()).hexdigest()
            return sha3_512(order['input'].encode('utf-8')).hexdigest()
        
        case 'md5':
            if order['file']:
                path = os.path.abspath(order['input'])
                with open(path, 'rb') as f:
                    return md5(f.read()).hexdigest()
            return md5(order['input'].encode('utf-8')).hexdigest()

# OTHER HANDLE ORDER HANDEL
def other_handle(cmd: str, parser: argparse.ArgumentParser) -> int:
    parser.add_argument(
        'cmd',
        choices=_OTHER_COMMAND
    )
    parser.add_argument(
        '--time',
        '-t',
        default=False,
        action = 'store_true',
        help = 'ExecuteTime Options'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        default=False,
        action = 'store_true',
        help = 'Verbose Options'
    )

    if cmd in ('container', 'archive'):
        return _container_handle(parser)

    match cmd:
        case 'now':
            parser.add_argument(
                '--timestamp',
                '-T',
                default=False,
                action = 'store_true',
                help = 'Type Return TimeStamp `float`'
            )
        
        case 'key':
            parser.add_argument(
                '--length',
                '-l',
                type= int,
                default=32,
                help= 'Generate Key With Length Default is `32`'
            )
            parser.add_argument(
                '--packsize',
                '-p',
                type= int,
                default= 16,
                help= 'Pack Size Generate Unit For Key'
            )
            parser.add_argument(
                '--many',
                '-m',
                type = int,
                default=1,
                help= 'How Many Key Generate'
            )
            parser.add_argument(
                '--file',
                '-f',
                type=str,
                default=None,
                help= 'Path File For Save Generated Key'
            )
            parser.add_argument(
                '--chars',
                '-c',
                type=str,
                default=None,
                help="Custom Characters Valid For Key"
            )
        
        case 'hash':
            parser.add_argument(
                'input',
                type= str,
                help= 'Input String For Hash'
                )
            parser.add_argument(
                '--algorithm',
                '-a',
                type= str,
                default='sha256',
                choices = ('sha256', 'sha3_512', 'md5'),
                help = 'Hash Algorithm Default Set `sha256` Support `sha3_512`, `sha256`, `md5`'
            )
            parser.add_argument(
                '--file',
                '-f',
                default=False,
                action = 'store_true',
                help = 'If Input Is File Path For File Hash'
            )
    
    argus = vars(parser.parse_args())
    work = lambda x: print(x) if argus['verbose'] else None
    t0 = monotonic()
    match cmd:
        case 'now':
            work(f'execute now `time` {"-Floating Point-" if argus["timestamp"] is True else "-Human Readable-"} order')
            handle = _now_handle(argus)
            print(handle)
        case 'key':
            work(f"execute key generator [length {argus['length']}, many {argus['many']}] order")
            handle = _key_handle(argus)
            print(handle)
        case 'hash':
            work(f"execute hash algorithm {argus['algorithm'].upper()} order")
            handle = _hash_handle(argus)
            print(handle)
    if argus['time']:
        print(f'Finished in {monotonic() - t0:.4}')

# NOTE_CONTAINER ORDER HANDLE
def note_handle(commands: dict) -> None:
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
    
    if x := commands['update_history']:
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
        del _active[x]
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

    if len(argv) > 0:
        if argv[0].lower() in _OTHER_COMMAND:
            parser = argparse.ArgumentParser('OTHER ORDER', description='Some Other Functionality')
            parser.add_argument(
            '--version',
            '-V',
            action = 'version',
            version=f'%(prog)s {_VERSION}'
            )
            cmd = argv.pop(0)
            return other_handle(cmd, parser)

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
        '--update_history',
        '-uh',
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
        help= 'Delete <Remove> Member From Container Need `Name` !![NO RECOVERY]!!'
    )

    parser.add_argument(
        '--clear',
        '-C',
        default=False,
        action='store_true',
        help= 'Clear Container From Any Members !![NO RECOVERY]!!'
    )

    parser.add_argument(
        '--hash_algorithm',
        '-ha',
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
    note_handle(argus)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
