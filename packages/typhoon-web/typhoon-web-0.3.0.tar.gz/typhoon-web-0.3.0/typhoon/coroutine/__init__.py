"""
typhoon.coroutine module
"""
import sys

if sys.version < '3.3':
    from .gen_old import run_in_executor
elif sys.version < '3.5':
    from .gen_new import run_in_executor
else:
    from .native import run_in_executor
