
#   FortranCode()
#     .module = FortranModule()
#     .name = "<name>"
#     .docs = "<documentation>"
#     .arguments = [FortranArgument(), ...]
#     .parse_line( "<line of source fortran code>" )
#     .generate_cython()
#     .generate_fortran()
#     
#   Subroutine(FortranCode)
#     .parse_line( "<line of source fortran code>" )
#     .generate_cython()
#     .generate_fortran()
# 
#   Function(FortranCode)
#     .return = FortranArgument()
#     .parse_line( "<line of source fortran code>" )
#     .generate_cython()
#     .generate_fortran()
# 
#   Interface(FotranCode)
#     .parse_line( "<line of source fortran code>" )
#     .generate_cython()
#     .generate_fortran()
# 
# 
#   Module(FortranCode)
#     

class FortranCode:
    # Description
    name = ""
    docs = ""
    # Contents
    use         = []
    types       = []
    arguments   = []
    subroutines = []
    functions   = []
    interfaces  = []

    def parse(source):
        pass

    def generate_c():
        pass

    def generate_fortran():
        pass


class Subroutine(FortranCode):
    def parse_line(source):
        pass

    def generate_c():
        pass

    def generate_fortran():
        pass

class Function(FortranCode):
    result = None

    def parse_line(source):
        pass

    def generate_c():
        pass

    def generate_fortran():
        pass


class Module(FortranCode):
    public    = []
    private   = []
    is_public = True

    # Given source code (with an expected format), parse into FortranModule
    def parse(source):
        self = FortranModule()
        return self, rest

    # Recursively evaluate the sizes of all arguments for all contents
    def evaluate_sizes(self):
        pass

    # Generate the c-code that will act as a python module and allow
    # access to the fortran codes.
    def generate_c(self):
        pass

    # Generate the fortran wrapper code necessary to transfer
    # information from c into fortran code.
    def generate_fortran(self):
        pass
