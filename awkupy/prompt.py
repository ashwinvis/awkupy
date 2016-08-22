from __future__ import print_function

import cmd
import os
from sys import exit
try:
    from os import system as call
except ImportError:
    from subprocess import call

from .awk import Awk


class IAwk(cmd.Cmd):
    intro = 'Welcome to the IAwk shell. Type help or ? to list commands.\n'
    prompt = '\033[1;32m{0}\033[39m'.format('iawk > ')

    def preloop(self):
        self.do_reset()

    def do_reset(self, arg=None):
        """Reset the current IAwk session."""
        self.awk = Awk()

    def do_input(self, arg):
        """Specify input file/text."""
        self.awk.INPUT = arg

    def do_run(self, arg=None):
        """Execute AWK command set with BEGIN, PROGRAM, END code blocks with `run`.
        Use `run <script_file.awk>` to execute an awk script.

        """
        if(arg):
            self.awk.opts.f = arg

        self.awk()

    def do_set(self, args):
        """Set BEGIN, PROGRAM, and END code blocks in AWK language.
        Use `show code` to verify.

        """
        argv = args.split()
        if len(argv) == 1:
            self.awk.PROGRAM = argv[0]
        elif argv[0] in ['BEGIN', 'PROGRAM', 'END']:
            self.awk.__dict__[argv[0]] = ' '.join(argv[1])
        else:
            self.awk.PROGRAM = args

    def do_show(self, arg='code'):
        """Display equivalent AWK code `show code`/ command `show command`."""
        if not arg:
            self.awk.show_command()
            self.awk.show_code()

        if arg == 'command':
            self.awk.show_command()
        elif arg == 'code':
            self.awk.show_code()

    def do_shell(self, arg):
        """Execute shell commands."""
        call(arg)

    def do_ls(self, arg):
        if not arg:
            arg = '.'

        path = self._parse_path(arg)
        if path:
            print(' '.join(os.listdir(path)))

    def do_cd(self, arg):
        path = self._parse_path(arg)
        if path:
            os.chdir(path)

    def _parse_path(self, path):
        path = os.path.expandvars(path)
        path = os.path.expanduser(path)
        if os.path.exists(path):
            return path
        else:
            print('File/directory not found: ', path)
            return False

    def do_exit(self, arg):
        exit()

    def help_exit(self):
        print("Terminates the current IAwk session.")
        print("You can also use the Ctrl-D shortcut.")

    do_EOF = do_exit
    help_EOF = help_exit
