# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #


# IMPORT
import os
import shutil
import tempfile
from zipfile import ZipFile, ZIP_BZIP2, ZIP64_LIMIT, ZIP_LZMA, ZIP_STORED, ZIP_DEFLATED, ZipInfo


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #

__all__ = ("UZip", "ZIP_BZIP2", "ZIP64_LIMIT", "ZIP_LZMA", "ZIP_STORED", "ZIP_DEFLATED", "ZipInfo")

# UPDATABLE ZIP FILE
class UZip(ZipFile):

    class DeleteMarker(object):
        pass

    def __init__(self, file, mode="r", compression=ZIP_DEFLATED, allowZip64=True) -> None:
        # Init base
        super(UZip, self).__init__(file, mode=mode, compression=compression, allowZip64=allowZip64)
        # track file to override in zip
        self._replace = {}
        # Whether the with statement was called
        self._allow_updates = False

    def writestr(self, zipinfo_or_arcname, bytes, compress_type=None, compresslevel = None) -> None:
        if isinstance(zipinfo_or_arcname, ZipInfo):
            name = zipinfo_or_arcname.filename
        else:
            name = zipinfo_or_arcname
        # If the file exits, and needs to be overridden,
        # mark the entry, and create a temp-file for it
        # we allow this only if the with statement is used
        if self._allow_updates and name in self.namelist():
            temp_file = self._replace[name] = self._replace.get(name, tempfile.TemporaryFile())
            temp_file.write(bytes)
        # Otherwise just act normally
        else:
            super(UZip, self).writestr(zipinfo_or_arcname, bytes, compress_type=compress_type, compresslevel=compresslevel)

    def write(self, filename, arcname=None, compress_type=None, compresslevel = None) -> None:
        arcname = arcname or filename
        # If the file exits, and needs to be overridden,
        # mark the entry, and create a temp-file for it
        # we allow this only if the with statement is used
        if self._allow_updates and arcname in self.namelist():
            temp_file = self._replace[arcname] = self._replace.get(arcname, tempfile.TemporaryFile())
            with open(filename, "rb") as source:
                shutil.copyfileobj(source, temp_file)
        # Otherwise just act normally
        else:
            super(UZip, self).write(filename, arcname=arcname, compress_type=compress_type, compresslevel=compresslevel)

    def __enter__(self) -> object:
        # Allow updates
        self._allow_updates = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # call base to close zip file, organically
        try:
            super(UZip, self).__exit__(exc_type, exc_val, exc_tb)
            if len(self._replace) > 0:
                self._rebuild_zip()
        finally:
            # In case rebuild zip failed,
            # be sure to still release all the temp files
            self._close_all_temp_files()
            self._allow_updates = False

    def _close_all_temp_files(self) -> None:
        for temp_file in self._replace.values():
            if hasattr(temp_file, 'close'):
                temp_file.close()

    def remove_file(self, path) -> None:
        self._replace[path] = self.DeleteMarker()

    def _rebuild_zip(self) -> None:
        tempdir = tempfile.mkdtemp()
        try:
            temp_zip_path = os.path.join(tempdir, 'new.zip')
            with ZipFile(self.filename, 'r') as zip_read:
                # Create new zip with assigned properties
                with ZipFile(temp_zip_path, 'w', compression=self.compression, allowZip64=self._allowZip64) as zip_write:
                    for item in zip_read.infolist():
                        # Check if the file should be replaced / or deleted
                        replacement = self._replace.get(item.filename, None)
                        # If marked for deletion, do not copy file to new zipfile
                        if isinstance(replacement, self.DeleteMarker):
                            del self._replace[item.filename]
                            continue
                        # If marked for replacement, copy temp_file, instead of old file
                        elif replacement is not None:
                            del self._replace[item.filename]
                            # Write replacement to archive,
                            # and then close it (deleting the temp file)
                            replacement.seek(0)
                            data = replacement.read()
                            replacement.close()
                        else:
                            data = zip_read.read(item.filename)
                        zip_write.writestr(item, data)
            # Override the archive with the updated one
            shutil.move(temp_zip_path, self.filename)
        finally:
            shutil.rmtree(tempdir)



__dir__ = ("UZip", "ZIP_BZIP2", "ZIP64_LIMIT", "ZIP_LZMA", "ZIP_STORED", "ZIP_DEFLATED", "ZipInfo")
