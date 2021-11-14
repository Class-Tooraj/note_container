# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT
import time
import hashlib
import pickle
import concurrent.futures

from datetime import datetime

# IMPORT TYPING
from typing import Callable, Iterator, Union



__all__ = ('now', 'perf_counter', 'monotonic', 'timestamp_to_str', 'md5', 'sha256', 'sha3_512', 'Crypting', 'RawData')
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

# NOW TIME
def now() -> float:
    return time.time()

# PERF COUNTER
def perf_counter() -> float:
    return time.perf_counter()

# MONOTONIC TIME
def monotonic() -> float:
    return time.monotonic()

# TIME STAMP TO STRING DATE
def timestamp_to_str(timstamp: float) -> str:
    return datetime.fromtimestamp(timstamp).strftime('%d/%m/%Y-%H:%M:%S')

# MD5 HASH
def md5(data: bytes) -> object:
    return hashlib.md5(data)

# SHA2 256
def sha256(data: bytes) -> object:
    return hashlib.sha256(data)

# SHA3 512
def sha3_512(data: bytes) -> object:
    return hashlib.sha3_512(data)


# BYTES CRYPTING
class Crypting:

    def __init__(self, key: Union[bytes, str], algorithm: Union[Callable, str] = None) -> None:
        """[Crypting Class]

        Args:
            key (Union[bytes, str]): [Key]
            algorithm (Union[Callable, str]): [Hash Algorithm]
                BUILT IN HASH SUPPORT WITH NAME: 'sha256', 'sha3_512', 'md5'
        """
        self.__hash_algorithm = {'sha256': sha256, 'sha3_512': sha3_512, 'md5': md5}
        
        if isinstance(algorithm, str):
            match algorithm in self.__hash_algorithm.keys():
                case True:
                    self.__algorithm = self.__hash_algorithm[algorithm]
                case False:
                    raise NameError
        
        elif isinstance(algorithm, Callable):
            self.__algorithm = algorithm
        else:
            self.__algorithm = sha3_512

        self.__key = self.__valid_key(key, self.__algorithm)

    def iter_crypto(self, data: bytes) -> Iterator[bytes]:
        """[Iterator Crypting]

        Args:
            data (bytes): [Data For Crypting]

        Yields:
            Iterator[bytes]: [EnCrypted or DeCrypted Iterator[bytes]]
        """
        key = self.__key_gen(self.__key)
        for it in data:
        # Generate New Bytes
            yield bytes([it ^ next(key)])

    def crypto(self, data: bytes) -> bytearray:
        """[Crypto]

        Args:
            data (bytes): [Data For Crypting]

        Returns:
            bytearray: [EnCrypted or DeCrypted Data]
        """
        return b''.join(self.iter_crypto(data))

    def update(self, key: Union[str, bytes], algorithm: Union[Callable, str] = None) -> None:
        """[Update Key]

        Args:
            key (Union[bytes, str]): [Updated Key]
            algorithm (Union[Callable, str]): [Hash Algorithm]
                BUILT IN HASH SUPPORT WITH NAME: 'sha256', 'sha3_512', 'md5'
        """
        if isinstance(algorithm, str):
            match algorithm in self.__hash_algorithm.keys():
                case True:
                    self.__algorithm = self.__hash_algorithm[algorithm]
                case False:
                    raise NameError
        
        elif isinstance(algorithm, Callable):
            self.__algorithm = algorithm
        else:
            self.__algorithm = sha3_512
        
        self.__key = self.__valid_key(key, self.__algorithm)

    @staticmethod
    def __key_gen(valid_key: list[int], limit: int = None) -> Iterator[int]:
        # Generate Unlimited Key
        # Limit For Limited Length
        run = True
        limit = -1 if limit is None else limit
        counter = 0
        while run:
            for i in valid_key:
                yield i
                
                if limit != -1:
                    if counter >= limit:
                        run = False
                        break
                
                    counter += 1

    @staticmethod
    def __valid_key(key: Union[str, bytes], hashing: Callable) -> list[int]:
        # Validate Key
        key = [*hashing(key.encode('utf-8') if isinstance(key, str) else key).digest()]
        r_key = reversed(key)
        res = [*r_key]
        res.extend(key)
        return res


# OBJECT TO RAW DATA
class RawData:

    @staticmethod
    def dumps(obj: object) -> bytes:
        with concurrent.futures.ThreadPoolExecutor() as executer:
            return executer.submit(pickle.dumps, obj).result()

    @staticmethod
    def loads(data: bytes) -> object:
        with concurrent.futures.ThreadPoolExecutor() as executer:
            return executer.submit(pickle.loads, data).result()

    @staticmethod
    def secure_dumps(obj: object, key: Union[str, bytes], algorithm: Union[Callable, str] = None) -> bytes:
        secure = Crypting(key, algorithm)
        with concurrent.futures.ThreadPoolExecutor() as executer:
            dump = executer.submit(pickle.dumps, obj).result()
            return executer.submit(secure.crypto, dump).result()

    @staticmethod
    def secure_loads(data: bytes, key: Union[str, bytes], algorithm: Union[Callable, str] = None) -> object:
        secure = Crypting(key, algorithm)
        with concurrent.futures.ThreadPoolExecutor() as executer:
            load = executer.submit(secure.crypto, data).result()
            return executer.submit(pickle.loads, load).result()


__dir__ = ('now', 'perf_counter', 'monotonic', 'timestamp_to_str', 'md5', 'sha256', 'sha3_512', 'Crypting', 'RawData')
