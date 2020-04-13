from __future__ import print_function

from .awk import Awk
from .base import BasePrompt


class IAwk(BasePrompt):
    intro = ('Welcome to the IAwk shell. Type help or ? to list commands.\n'
             'Prefix ! to run system commands\n')
    cmd_name = 'iawk'

    def do_reset(self, arg=None):
        """Reset the current IAwk session."""
        self.awk = Awk()

    def do_input(self, arg):
        """Specify input file/text."""
        self.awk.INPUT = arg

    def do_run(self, arg=None):
        """Execute AWK command set with BEGIN, ACTION, END code blocks with `run`.
        Use `run <script_file.awk>` to execute an awk script.

        """
        if arg:
            self.awk.opts.f = arg

        self.awk()

    def do_set(self, args):
        """Set BEGIN, PATTERN, ACTION, and END code blocks in AWK language. If
        unspecified sets ACTION with whatever follows. Use `show code` to
        verify.

        """
        argv = args.split()
        if argv[0].upper() in ['BEGIN', 'PATTERN', 'ACTION', 'END']:
            self.awk.__dict__[argv[0].upper()] = ' '.join(argv[1:])
        else:
            self.awk.ACTION = args

    def do_show(self, arg):
        """Display equivalent AWK code `show code`/ command `show command`."""
        if arg == 'command':
            print(repr(self.awk))
        else:
            print(self.awk.code)
