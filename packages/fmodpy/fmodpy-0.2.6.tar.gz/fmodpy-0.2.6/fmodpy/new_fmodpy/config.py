# File related maniplation arguments
CYTHON_EXT = ".pyx"
CYTHON_SUFFIX = ""
FORT_FILE_EXT = ".f90"
FORT_WRAPPER_SUFFIX = "_c_to_f"
FORT_WRAPPER_EXT = FORT_WRAPPER_SUFFIX + FORT_FILE_EXT
PREPROCESSED_FORTRAN_FILE = "simplified_fortran.f90"
# Get the local config file
import os
USER_HOME_DIRECTORY = os.path.expanduser("~")
FMODPY_CONFIG_FILE = ".fmodpy"

# Default configurable variables.
c_compiler          = 'gcc'
c_linker            = 'gcc'
f_compiler          = 'gfortran'
f_compile_arg       = '-c'
f_compiler_options  = '-fPIC -O3'
module_compile_args = '-O3'
module_link_args    = '-lgfortran'
link_blas           = '-lblas'
link_lapack         = '-lblas -llapack'
disallowed_options  = '-Wshorten-64-to-32'

# Automatically handle printing for status updates.
#   WARNING: Do not use this function for warnings. Use `warnings.warn`
#   WARNING: Do not use this function for errors. Use `raise(...)`
def fprint(file_name, *args, **kwargs):
    kwargs["flush"] = True
    print("FMODPY:", *args, **kwargs)

# Read a configuration file into a Python dictionary.
def read_config_file(path):
    with open(path) as f:
        # Get all lines that have one "=" split and stripped into nice strings.
        lines = ((' '.join(var.split()) for var in l.split('='))
                 for l in f.readlines() if (l.count('=') == 1))
    return dict(lines)

# Load local settings if they are available.
if os.path.exists(os.path.join(USER_HOME_DIRECTORY,LOCAL_FMODPY_CONFIG)):
    _ = read_config_file(
        os.path.join(USER_HOME_DIRECTORY,LOCAL_FMODPY_CONFIG))
else: _ = {}
# Make sure all provided settings are recognized (and allowable).
for var in _:
    if var not in globals():
        class UnrecognizedConfiguration(Exception): pass
        raise(UnrecognizedConfiguration(f"Setting named '{var}' is not recognized."))
# Update the configuration of fmodpy.
globals().update(_)


# Configure the current 'fmodpy' runtime.
def configure(**kwargs):
    import fmodpy

    # Set the default configuration as the current configuration.
    config = {k:getattr(fmodpy,k) for k in dir(fmodpy) if k[:1] != "_"}

    # Update the 'config' dictionary with the provided keyword arguments.
    config.update( kwargs )

    # Make sure the path names do not have spaces.
    if any(' ' in config[k] for k in ('f_compiler', 'c_linker', 'c_compiler')):
        class NotAllowedPath(Exception): pass
        raise(NotAllowedPath("Spaces cannot be included in compiler or linker paths"))

    # All of these variables should be lists.
    list_vars = ['f_compiler_options', 'module_compile_args',
                 'module_link_args', 'link_blas', 'link_lapack',
                 'disallowed_options']
    for var in list_vars:
        if (type(config[var]) is str):
            config[var] = config[var].split()

    # Convert the configuration variable that should be a boolean.
    if (type(config['autocompile_files']) is str):
        config['autocompile_files'] = config['autocompile_files'].lower() == 'true'

    # Make sure only allowed variables have been provided.
    allowed_variables = set(['f_compiler', 'f_compile_arg', 'c_linker',
                             'c_compiler', 'autocompile_files'] + list_vars)

    # Get the current configuration and return it.
    if (len(kwargs) == 0): return config

    # Set all of the configuration variables as module-wide globals.
    for var in config: setattr(fmodpy, var, config[var])

    # Return the current configuration.
    return config

