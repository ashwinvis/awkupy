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
    @argument("-d", "--debug", action="store_true", help="debug awk code")
    @argument("-f", "--file", default=None, help="external awk program")
    @argument(
        "-F",
        "--field-separator",
        default=None,
        help="separate column using a string",
    )
    @argument(
        "-o",
        "--pretty-print",
        nargs="?",
        const=True,
        default=False,
        help=(
            "pretty print program to a file; if no file is mentioned "
            "the program is saved to awkprof.out"
        ),
    )
    @argument("-s", "--save-as", default=None, help="save output to a file")
    @argument("-u", "--stdout", action="store_true", help="print to stdout")
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
            # TODO: use
            print(
                "\n  ".join(
                    [
                        "\r- Code:",
                        api.code,
                        "\n\r- Input:",
                        *str(api.INPUT).splitlines(),
                        "\n\r- Output:",
                        "stdout" if args.stdout else args.save_as,
                        "\r",
                    ]
                )
            )

        if args.pretty_print:
            api.opts.o = args.pretty_print

        if args.stdout:
            if self.shell.__class__.__name__ == "ZMQInteractiveShell":
                # NOTE: we need this, otherwise the stdout of the terminal
                # would be used!
                # https://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
                print(api.check_output().decode())
            else:
                api()
        elif args.save_as:
            with open(args.save_as, "wb") as fp:
                return api(stdout=fp)
        else:
            return api.check_output().decode()


def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    js = "IPython.CodeCell.options_default.highlight_modes['magic_awk'] = {'reg':[/^%%awk/]};"
    display_javascript(js, raw=True)
    magics = AwkMagics(ipython)
    ipython.register_magics(magics)
