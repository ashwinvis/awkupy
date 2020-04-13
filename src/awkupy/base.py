import cmd
import os
import sys
try:
    from os import system as call
except ImportError:
    from subprocess import call


class BasePrompt(cmd.Cmd):
    cmd_name = 'Cmd'
    cmd_count = 0
    history = []

    @classmethod
    def _update_prompt(cls):
        cls.cmd_count += 1
        cls.prompt = '\033[1;32m{0} [{1}]: \033[39m'.format(cls.cmd_name, cls.cmd_count)

    def preloop(self):
        self.do_reset()
        self._update_prompt()

    def precmd(self, line):
        if line:
            self._update_prompt()
            self.history.append(line)

        return line

    def emptyline(self):
        pass

    def do_shell(self, arg):
        """Execute shell commands."""
        call(arg)

    def do_ls(self, arg):
        """List information about the `arg` (the current directory by default)."""
        if not arg:
            arg = '.'

        path = self._expand_check_path(arg)
        if path:
            print(' '.join(os.listdir(path)))

    def do_cd(self, arg):
        """Change present working directory to `arg`."""
        if not arg:
            arg = '~'

        path = self._expand_check_path(arg)
        if path:
            os.chdir(path)

        print(path)

    def _expand_check_path(self, path):
        path = os.path.expandvars(path)
        path = os.path.expanduser(path)
        if os.path.exists(path):
            return path
        else:
            print('File/directory not found: ', path)
            return False

    def do_history(self, arg):
        """Print IAwk command history."""
        if not arg:
            s = slice(None, None)
        elif ':' in arg:
            s = slice(*[int(i) for i in arg.split(':')])
        else:
            s = slice(int(arg))

        for line in self.history[s]:
            print(line)

    do_hist = do_history
    do_exit = sys.exit

    def help_exit(self):
        print("Terminates the current IAwk session.")
        print("You can also use the Ctrl-D shortcut.")

    do_EOF = do_exit
    help_EOF = help_exit
