'''
'''
# current version
#==============================================================================
VERSION = (0, 0, 4, "b", 1)


# PEP440 Format
#==============================================================================
__version__ = "%d.%d.%d.%s%d" % VERSION if len(VERSION) == 5 else \
              "%d.%d.%d" % VERSION


# all submodules
#==============================================================================
__all__ = ['solvers', 'utils', 
           'examples.langford', 'examples.disjunction', 'examples.parity_board']
