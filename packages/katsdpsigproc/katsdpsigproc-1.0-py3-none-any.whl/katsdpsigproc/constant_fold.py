"""Utility to replace variables in a Python function with a fixed value.

This is intended as an aid to using numba, which requires certain things to
be constants and won't accept some things that really are constants (see
https://github.com/numba/numba/issues/2518).
"""

from __future__ import print_function, division, absolute_import
import ast
import inspect
import functools
import textwrap


class ConstantTransformer(ast.NodeTransformer):
    def __init__(self, constants):
        self._constants = constants

    def visit_Name(self, node):
        try:
            value = ast.Num(self._constants[node.id])
            return ast.copy_location(value, node)
        except KeyError:
            return node


def fold(func, **kwargs):
    """For each key in `kwargs`, replace references to that key in the code
    with the corresponding value (which must be a number).

    This is very hacky, and may not work in all cases. Some caveats:
    - The code will be interpreted under the __future__ imports in this
      module, rather than the one where the function is defined
    - The code needs to be available
    - It may go wrong if the function has a decorator

    The names in `kwargs` do not need to resolve to anything when the
    function is defined.
    """
    src = inspect.getsource(func)
    tree = ast.parse(textwrap.dedent(src))
    new_tree = ConstantTransformer(kwargs).visit(tree)
    compiled = compile(new_tree, inspect.getsourcefile(func), 'exec')
    lcls = {}
    exec(compiled, func.func_globals, lcls)
    out = lcls[func.func_name]
    functools.update_wrapper(out, func)
    return out
