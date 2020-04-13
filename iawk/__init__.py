from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
    line_magic,
    line_cell_magic,
    needs_local_scope,
)
from IPython.core.magic_arguments import (
    argument,
    magic_arguments,
    parse_argstring,
)
from IPython.display import display_javascript

from awkupy import Awk


@magics_class
class AwkMagics(Magics):
    "Provides the %awk line magic and %%awk cell magic." ""

    def __init__(self, shell):
        super().__init__(shell)
        self._input = ""

    @cell_magic
    def awk_input(self, line, cell):
        """Sets input text data."""
        self._input = cell

    @needs_local_scope
    @line_cell_magic
    @magic_arguments()
    @argument("-f", "--file", default=None, help="external awk program")
    @argument("-F", "--field-separator", default=None, help="separate column using a string")
    @argument("-p", "--print-output", action="store_true", help="print output to stdout")
    @argument("-s", "--save-as", default=None, help="save output to a file")
    @argument("-d", "--debug", action="store_true", help="debug awk code")
    @argument(
        "-v",
        "--variable",
        # FIXME: multiple variables
        #  nargs="*",
        help="pass variables to awk, for example, var={value}",
    )
    @argument("-e", "--source", default="", help="program text for oneliners")
    @argument("input", nargs="?", default="")
    def awk(self, line, cell="", local_ns={}):
        """Execute awk via awkupy API.

        Examples::

            %load_ext iawk

            %%awk LICENSE
            /^  [0-9]/{print $0}

            output = %awk -e '/^  [0-9]/{print $0}' LICENSE
            output.splitlines()[0]

        """
        args = parse_argstring(self.awk, line)
        args.source = args.source.strip("'")

        #  api = self.api
        api = Awk()

        if args.file:
            api.opts.f = args.file

        if args.field_separator:
            api.opts.F = args.field_separator

        if args.variable:
            api.opts.v = args.variable.format(**local_ns)

        api.INPUT = args.input or self._input

        api.code = args.source or cell

        if args.debug:
            print("\n\r".join(["Code:", api.code, "Input:", str(api.INPUT)]))

        if args.print_output:
            return api()
        else:
            output = api.check_output().decode()
            if args.save_as:
                with open(args.save_as, "w") as fp:
                    fp.write(output)
            else:
                return output


def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    js = "IPython.CodeCell.options_default.highlight_modes['magic_awk'] = {'reg':[/^%%awk/]};"
    display_javascript(js, raw=True)
    magics = AwkMagics(ipython)
    ipython.register_magics(magics)
