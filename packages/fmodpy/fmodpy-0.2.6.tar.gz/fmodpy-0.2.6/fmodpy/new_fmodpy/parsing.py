
# Functions for identifying the strings before and after the last "."
before_dot = lambda name: name[:len(name) - 1 - name[::-1].find(".")];
after_dot = lambda name: name[min(-name[::-1].find("."),0):]
legal_module_name = lambda name: (name.replace("_","")[0].isalpha() and
                                  name.replace("_","")[1:].isalnum() and
                                  (len(name) > 0))
