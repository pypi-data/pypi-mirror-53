# TODO:  Assign the defaults for compilation based on a settings file

class Fortran:
    file_name = ""
    docs      = ""
    # Build
    build_directory = ""
    # Contents
    types       = []
    modules     = []
    functions   = []
    subroutines = []
    # Compilation
    f_compiler         = ""
    f_compiler_options = []
    c_compiler         = ""
    c_compiler_options = []
    c_linker           = ""
    c_linker_options   = []

    # Scan the contents of this module for symantic errors
    def check_errors(self):
        pass

    # Given a configuration file, load it and set the internal options
    # for this module accordingly.
    def config(self, config_file="fmodpy.config"):
        pass

    # Do all necessary compilation steps (cython -> c, c compile, f
    # compile, link and build module).
    def build(self):
        pass

    # Cleanup the build directory (remove all intermediate compiled
    # files)
    def cleanup(self):
        pass
