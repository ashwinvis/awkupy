from IPython.core.magic import Magics, magics_class, cell_magic, line_magic, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

from awkupy import Awk


@magics_class
class AwkMagics(Magics):

    @line_magic
    @cell_magic
    @magic_arguments()
    @argument("input")
    def awk(self, line, cell):
        args = parse_argstring(self.awk, line)

        api = Awk()
        api.INPUT = args.input
        api.code = cell
        api()


def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    magics = AwkMagics(ipython)
    ipython.register_magics(magics)

