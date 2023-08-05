#   FortranArgument()
#     .name = "<name>"
#     .type = "<type>"
#     .size = "<size>"
#     .kind = "<kind>"
#     .intent = "<intent>"
#     .message = "<messages to user>"
#     .defined = True / False
#     .allocatable = True / False
#     .optional = True / False
#     .dim = ["<dim 1>", ...]
#     ._is_optional()
#     ._is_present()
#     ._to_copy_args()
#     ._to_needed_dim()
#     .to_py_input_doc_string()
#     .to_py_output_doc_string()
#     .to_py_input()
#     .to_py_prepare()
#     .to_py_call()
#     .to_py_after()
#     .to_py_return()
#     .to_c_input()
#     .to_c_prepare()
#     .to_c_call()
#     .to_c_after()
#     .to_fort_input()
#     .to_fort_declare()
#     .to_fort_prepare()
#     .to_fort_call()
#     .to_fort_after()
#
#   Real(FortranArgument)
# 
#   Integer(FortranArgument)
# 
#   Logical(FortranArgument)
# 
#   Character(FortranArgument)
#     .len = "<len>"
# 
#   Procedure(FortranArgument)
#     .interface = Interface()
# 
#   DataType(FortranArgument)
#     .contains = [<FortranArgument>, ...]
#     
