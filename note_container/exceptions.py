# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> #
#           < IN THE NAME OF GOD >           #
# ------------------------------------------ #
__AUTHOR__ = "ToorajJahangiri"
__EMAIL__ = "Toorajjahangiri@gmail.com"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #



# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\^////////////////////////////// #


class MemberNotExistsError(Exception):
    pass

class MemberExistsError(Exception):
    pass

class NameExistsError(Exception):
    pass

class NameNotExistsError(Exception):
    pass

class NewNoteSameExistsNote(Exception):
    pass

class CorruptedError(Exception):
    pass

class AddTypeError(Exception):
    pass

class GetDataTypeError(Exception):
    pass

class AppendingTypeError(Exception):
    pass

class UpdateTypeError(Exception):
    pass

class DataTypeError(Exception):
    pass
