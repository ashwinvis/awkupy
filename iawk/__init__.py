from IPython.core.magic import Magics, magics_class, cell_magic, line_magic, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

from awkupy import Awk


@magics_class
class AwkMagics(Magics):
    "Provides the %awk line magic and %%awk cell magic."""

    @line_magic
    @cell_magic
    @magic_arguments()
    @argument("code", nargs="?", default="")
    @argument("input")
    def awk(self, line, cell=""):
        """Execute awk via awkupy API.

        Examples::

            %load_ext iawk

            %%awk LICENSE
            /^  [0-9]/{print $0}

            output = %awk '/^  [0-9]/{print $0}' LICENSE
            output.splitlines()[0]

        """
        args = parse_argstring(self.awk, line)

        api = Awk()
        api.INPUT = args.input
        args.code = args.code.strip("'")
        api.code = "".join((args.code, cell))
        return api.check_output().decode()


def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    magics = AwkMagics(ipython)
    ipython.register_magics(magics)

