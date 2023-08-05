# Custom errors that can be raised during the fmodpy process
class BadKeywordArgument(Exception): pass
class NotSupportedError(Exception):  pass
class CompileError(Exception):       pass
class FortranError(Exception):       pass
class LinkError(Exception):          pass
class SizeError(Exception):          pass
class NameError(Exception):          pass
