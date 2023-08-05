# fmodpy is an automatic fortran wrapper for python.
# 
# This program is designed to processes a source fortran file into the
# following structure and wrap all contained code into a python module
# 
#   fimport()
#   build_py_mod()
#   configure()
# 

# Overwrite the "print" function to add "FMODPY" specific printouts.
from fmodpy.config import fprint as print
THIS_FILE = os.path.basename(__file__)


# Function for automating the entire fortran<->python wrapping
#   process. This is the top-level function built for standard usage.
#   This function automatically checks the modification times of the
#   output module as well as the source fortran in order to only
#   re-compile when necessary. Automatically wraps fortran, copies over
#   all files in the source directory as potential dependencies. 
# 
#  INPUTS:
#    input_fortran_file -- str, relative or absolute path to fortran source.
# 
#  OPTIONAL:
#    mod_name         -- str, name of output python module. Defaults
#                        to be before_dot(os.path.basename(input_fortran_file))
#    force_rebuild    -- True if you want to rebuild even though the
#                        input_fortran_file has not been modified
#                        since the last compilation of the module.
#    build_direcotry  -- The directory to store the wrapper code for
#                        input_fortran_file. If provided, it is
#                        assumed that the directory should not be
#                        removed automatically.
#    output_directory -- The directory to store the output python
#                        module. Defaults to os.getcwd()
# 
def fimport(input_fortran_file, name=None, build_dir=None,
            output_dir=None, force_rebuild=False, autocompile=True,
            **kwargs):
    # Import parsing functions.
    from fmodpy.parsing import before_dot, legal_module_name

    # Configure this runtime of fmodpy 
    pre_config = configure()
    if (len(kwargs) > 0): configure(kwargs)
    
    # Set the default output directory
    if (output_dir is None): output_dir = os.getcwd()
    output_dir = os.path.abspath(output_dir)

    # Get the source file and the source directory.
    source_file = os.path.basename(input_fortran_file)
    source_dir = os.path.dirname(os.path.abspath(input_fortran_file))

    # If the name is not defined, then try to automatically produce it.
    if (name is None): name = before_dot(source_file)

    # Check to make sure that the module name is lega.
    if not legal_module_name(name):
        from fmodpy.exceptions import NameError
        raise(NameError((f"'{name}' is not an allowed module name,\n"+
                         " must match the regexp `^[a-zA-z_]+"+
                         "[a-zA-Z0-9_]*`. Set the name with:\n"+
                         " fmodpy.fimport(<file>, name='<legal name>')"+
                         " OR\n $ fmodpy <file> name=<legal_name>")))

    # Create a build directory.
    if (build_dir is None):
        # Create a temporary directory for building.
        from tempfile import TemporaryDirectory
        build_dir = TemporaryDirectory()
        build_path = build_dir.name
    else:
        # Otherwise, assume a path was given, conver to absolute form.
        build_path = os.path.abspath(build_dir)
        # Create the directory for the build if it does not exist.
        if (not os.path.exists(build_path)): os.makedirs(build_path)


    # Determine whether or not the module needs to be rebuilt.
    should_rebuild = force_rebuild or should_rebuild_module(
        input_fortran_file, name, output_dir)
    if not should_rebuild:
        print("No new modifications to '%s' module, exiting."%(mod_name))
        return mod_name

    # Prepare the build directory, copy in necessary files
    build_dir = prepare_build_directory(
        source_file, source_dir, mod_name, output_directory,
        build_directory, verbose)

    # Automatically compile fortran files.
    if autocompile: autocompile_files(build_dir)

    # Generate the wrappers for going from python <-> fortran
    make_python_wrapper(input_fortran_file, build_dir, name, verbose)

    # Build the python module by compiling all components
    mod_path = make_python_module(source_file, build_dir, name, verbose=verbose)
    print(f"Finished making module '{name}'."))

    # Re-configure 'fmodpy' to work the way it did before this execution.
    if (len(kwargs) > 0): configure(pre_config)

    # Return the module to be stored as a variable.
    return importlib.import_module(mod_name)

# ====================================================================

# Function for compiling and creating a python module out of the
# prepared fortran + wrapper code.
def build_py_mod(file_name, working_dir, mod_name, verbose=True):
    ##################################################
    # These imports are only needed for this function!
    import numpy, sysconfig
    from distutils.extension import Extension
    from distutils.core import setup
    from Cython.Build import cythonize
    ##################################################

    # Store original directory to revert back after compilation
    original_dir = os.getcwd()
    os.chdir(working_dir)

    if not os.path.exists(os.path.join(working_dir,before_dot(file_name) + ".o")):
        if verbose: print("FMODPY: Compiling '%s'..."%(file_name))
        comp_code, stdout, stderr = run([fort_compiler,fort_compile_arg]+
                                        fort_compiler_options+[file_name])
        if comp_code != 0:
            raise(CompileError("Unexpected error in '%s'.\n"%(file_name)+
                               "\n".join(stderr)))

    # Compile the fortran wrapper 
    wrap_code = mod_name+FORT_WRAPPER_EXT
    if verbose: print("FMODPY: Compiling '%s'..."%(wrap_code))
    wrap_code, stdout, stderr = run([fort_compiler,fort_compile_arg]+
                                    fort_compiler_options+[wrap_code])
    if wrap_code != 0:
        print("\n".join(stderr))
        raise(CompileError("\nError in generated wrapper (fmodpy bug?)\n"))

    # Setup linking for creating the extension
    link_files = [f for f in os.listdir(working_dir) if 
                  (os.path.isfile(os.path.join(working_dir,f))
                   and (f[-2:] == ".o"))]
    if verbose: print("FMODPY: Linking %s..."%(link_files))
    cython_source = [mod_name+CYTHON_SUFFIX+CYTHON_EXT]

    if c_compiler != None:
        # Set the compiler
        os.environ["CC"] = c_compiler

    # Get the linker options used to build python
    linker_options = sysconfig.get_config_vars().get("BLDSHARED","").split(" ")[1:]
    # Remove linker options that cause trouble
    for bad_opt in module_disallowed_linker_options:
        if bad_opt in linker_options:
            linker_options.remove(bad_opt)
    # Set the linker, with appropriate options
    os.environ["LDSHARED"] = " ".join([c_linker]+linker_options)
    # Generate the extension module
    ext_modules = [ Extension(
        mod_name, cython_source,
        extra_compile_args=module_compile_args,
        extra_link_args=module_link_args+link_files,
        include_dirs = [numpy.get_include()])]

    if verbose:
        print("FMODPY: Compiling extension module using setup...")
        print("="*70)
        print()
    else:
        # Capture the output of setup so it doesn't bother the user
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")

    # Manually make this file always run as "build_ext" and "--inplace"
    # Capture the output of a dry run to get the command that would be
    # used to build this module. Modify the commands appropriately.
    actual_argv = sys.argv
    sys.argv = ['', 'build_ext', '--inplace']
    dist = setup( name = mod_name, ext_modules = cythonize(ext_modules) )
    sys.argv = actual_argv

    if verbose:
        print()
        print("="*70)
        print("FMODPY: Done setting up.")
    else:
        # Reset stdout back to its normal state
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    # Manipulate the path to test importing the module
    original_path = sys.path
    try:
        # First, invalidate any existing copies of the module
        try: del sys.modules[mod_name]
        except KeyError: pass
        # Second, try loading the newly created module
        sys.path = [working_dir]
        module = importlib.import_module(mod_name)
        # In case the module was already imported, reload it so that
        # the one left in memory is the most recent (so the user can
        # correctly import it later without any trouble)
        if sys.version_info >= (3,): module = importlib.reload(module)
        else:                        module = reload(module)
        module_path = os.path.abspath(module.__file__)
    except ImportError as exc:
        raise(LinkError("\n\n"+str(exc)+"\n\nUnable to successfully import module.\n Perhaps the "+
                        "relevant compiled fortran files were not available? See message above."))
    finally:
        # Rever the system path no matter what
        sys.path = original_path
    if verbose: print("FMODPY: Successfully built and imported module.")

    # Revert to the original directory
    os.chdir(original_dir)

    return module_path

# ====================================================================

def autocompile_files(working_dir):
    # Store original directory to revert back after compilation
    original_dir = os.getcwd()
    os.chdir(working_dir)

    # Try and compile the rest of the files (that might be fortran) in
    # the working directory in case any are needed for linking.
    should_compile = []
    # Generate the list of files that we sould try to autocompile
    for f in os.listdir(working_dir):
        f = f.strip()
        # Skip the preprocessed file, the size program, and directories
        if ( (PREPROCESSED_FORTRAN_FILE in f) or
             (GET_SIZE_PROG_FILE in f) or
             (os.path.isdir(f)) or
             ("f" not in after_dot(f)) ):
            continue

        # Try opening the file, if it can't be decoded, then skip
        try:
            # Make sure the file does not have any immediate exclusions,
            # if it does then skip it
            with open(f) as fort_file:
                exclude_this_file = False
                # Read through the file, look for exclusions
                for line in fort_file.readlines():
                    line = line.strip().upper().split()
                    if (len(line) > 0) and (line[0] in IMMEDIATELY_EXCLUDE):
                        exclude_this_file = True
                        break
                if exclude_this_file:
                    if verbose:
                        print(("FMODPY: Skipping '%s' because it contains "+
                               "one of %s.")%(f, IMMEDIATELY_EXCLUDE))
                    continue
        except:
            # Some failure occurred while reading that file, skip it
            continue
        # No failures or obvious red-flags, this file might be useful
        should_compile.append(f)

    # Handle dependencies by doing rounds of compilation, presuming
    # only files with fewest dependencies will compile first
    errors = []
    successes = [None]
    # Continue rounds until (everything compiled) or (no success)
    while (len(should_compile) > 0) and (len(successes) > 0):
        successes = []
        for f in should_compile:
            # Try to compile all files that have "f" in the extension
            if verbose: print("FMODPY: Compiling '%s'..."%(f))
            code, stdout, stderr = run([fort_compiler,fort_compile_arg]+fort_compiler_options+[f])
            if code == 0: successes.append(f)
            else: errors.append(stderr)
        # Remove the files that were successfully compiled from
        # the list of "should_compile"
        for f in successes:
            should_compile.remove(f)

    # Revert to the original directory
    os.chdir(original_dir)

    # TODO:  Nothing is done with 'errors', should something be done?
    #        Perhaps they should be given in the case that the import
    #        of the completed module fails.

# ====================================================================

# Given the path to the file that we are creating an extension for,
# create and prepare a working directory for the project compilation
def prepare_build_directory(source_file, source_dir, project_name,
                            output_direcotry, working_direcotry="",
                            verbose=False):
    if len(working_direcotry) == 0:
        working_dir = os.path.join(source_dir, FMODPY_DIR_PREFIX+project_name)
    else:
        working_dir = os.path.abspath(os.path.expanduser(working_direcotry))

    # Generate the names of files that will be created by this
    # program, so that we can copy them to an "old" directory if necessary.
    fort_wrapper_file = project_name+FORT_WRAPPER_EXT
    cython_file = project_name+CYTHON_SUFFIX+CYTHON_EXT

    if verbose:
        print()
        print("="*60)
        print("Input file directory: ",source_dir)
        print("Input file name:      ",source_file)
        print("Base module name:     ",project_name)
        print("Using working dir:    ",working_dir)
        print("  fortran wrapper:    ",fort_wrapper_file)
        print("  cython file:        ",cython_file)
        print("Output file directory:",output_direcotry)
        print("="*60)
        print()

    #      Prepare a working directory     
    # =====================================
    if not os.path.exists(working_dir):
        # Otherwise, create the initial working directory
        os.makedirs(working_dir)
    elif len(working_direcotry) == 0:
        # Otherwise the user didn't give a directory, but it exists
        # for some reason (probably failure?) So save contents.
        # 
        # Identify a viable name for the old project contents
        num = 1
        while os.path.exists( os.path.join(
                working_dir, OLD_PROJECT_NAME(project_name, num))): num += 1
        old_proj_name = OLD_PROJECT_NAME(project_name, num)
        # Create the directory for old project contents
        old_proj_dir = os.path.join(working_dir,old_proj_name)
        os.makedirs(os.path.join(working_dir,old_proj_name))
        # Move the files that would've been created by this project
        # before into an "OLD" directory
        for f in os.listdir(working_dir):
            f = os.path.join(working_dir, f)
            if not os.path.isdir(f):
                shutil.move(f,os.path.join(old_proj_dir,os.path.basename(f)))
        if verbose:
            print("FMODPY:  Moved existing working directory contents to\n  '%s'"%(
                os.path.join(working_dir,old_proj_name) ))

    # If the working directory is not the same as the file directory,
    # copy all the contents of the file directory into the working
    # directory (in case any of them are used by the fortran project)
    if source_dir != working_dir:
        for f in os.listdir(source_dir):
            source = os.path.join(source_dir,f)
            extension = after_dot(f)
            # WARNING: If the user wants files to be in the module
            # that do not have the standard extensions then this will
            # accidentally exclude them.
            maybe_relevant = ("f" in extension) or (extension in {"mod", "o"})
            is_directory = os.path.isdir(source)
            is_py_module = (f[-3] == ".so")
            if maybe_relevant and (not (is_directory or is_py_module)):
                destination = os.path.join(working_dir,f)
                if verbose:
                    print("FMODPY: Copying '%s' to '%s'"%(source, destination))
                shutil.copyfile(source, destination)
    
    # Return the prepared working directory
    return working_dir

# ====================================================================

# Return True if a module should be rebuilt, False otherwise.
def should_rebuild_module(file_path, mod_name, output_directory):
    # Get the last modification time of the module (if it exists already)
    # Make sure that the output directory is in the sys path so that
    # the time-check import will work correctly.
    sys.path = [output_directory] + sys.path
    try:
        # Import the module, get the modification time
        mod = importlib.import_module(mod_name)
        module_mod_time = os.path.getmtime(mod.__file__)
    except ImportError:
        module_mod_time = 0
    except:
        # TODO: Existing module was corrupt, should we warn the user or ignore?
        module_mod_time = 0
    # Reset the sys path
    sys.path = sys.path[1:]

    # Exit if the module has been built since the last update of the
    # source file and the user does *not* want to force a reconstruction.
    source_file_mod_time = os.path.getmtime(file_path)
    return source_file_mod_time < module_mod_time):


def set_globals(kwargs):
    # Add **kwargs that captures any global settings temporarily
    # for this execution of the function.
    unknown = set(kwargs.keys())
    for arg_name in kwargs:
        if (arg_name in globals()):
            globals()[arg_name] = kwargs[arg_name]
            unknown.remove(arg_name)
    # Check for invalid keyword arguments
    if len(unknown) > 0:
        error = ", ".join(sorted(unknown))
        raise(BadKeywordArgument("Invalid keyword argument%s: %s\n\nSee 'help' documentation."%(
            ("s" if len(unknown) > 1 else ""), error)))




# These must be the last declared globals for them to include
# everything, allows for automatically parsing command line arguments
# the same way as the user would set the variables in practice.
USER_GLOBAL_CASTS = {
    type(None) : lambda s: s,
    str        : lambda s: s,
    list       : lambda s: s[1:-1].split(","),
    bool       : lambda s: bool(s.lower().strip("false").replace("0","")),
}

# The list of globals that users can modify at execution time.
USER_MODIFIABLE_GLOBALS = [n for n,v in globals().items() if
                           (n.lower() == n) and (n[:1] != "_") and
                           (type(v) in USER_GLOBAL_CASTS)]


