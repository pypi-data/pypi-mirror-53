
# Custom classes for handling lookup errors gracefully
class SizeMap(dict):
    def __missing__(self, f_type):
            raise(NotSupportedError("Type '%s' is not supported."%(f_type)))

class SizeDict(dict):
    def __init__(self, f_type, dictionary):
        self.f_type = f_type
        super(dict, self).__init__()
        self.update(dictionary)
        
    def __missing__(self, size):
        raise(SizeError("Size '%s' is not supported for type '%s'."%(
            size,self.f_type)))

# How to translate a fortran of a given type and size to a c type
FORT_C_SIZE_MAP = SizeMap(
    INTEGER = SizeDict("INTEGER", {
        "4":"int",
        "8":"long"
    }),
    REAL = SizeDict("REAL", {
        "4":"float",
        "8":"double"
    }),
    LOGICAL = SizeDict("LOGICAL", {
        "4":"bint"
    }),
    CHARACTER = SizeDict("CHARACTER", {
        "1":"char"
    }),
    PROCEDURE = SizeDict("PROCEDURE", {
        "":""
    }),
)

# How to translate a fortran of a given type and size to a numpy type
FORT_PY_SIZE_MAP = SizeMap(
    INTEGER = SizeDict("INTEGER", {
        "4":"numpy.int32",
        "8":"numpy.int64"
    }),
    REAL = SizeDict("REAL", {
        "4":"numpy.float32",
        "8":"numpy.float64"
    }),
    LOGICAL = SizeDict("LOGICAL", {
        "4":"numpy.uint32"
    }),
    CHARACTER = SizeDict("CHARATCTER", {
        "1":"numpy.uint8"
    }),
)

# Default sizes (in bytes) of fortran integer and logical types
DEFAULT_F_INT_SIZE = "4"
DEFAULT_F_LOG_SIZE = "4"
