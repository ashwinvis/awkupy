import subprocess
import os


class Awk(object):
    """A subprocess interface for AWK."""

    def __init__(self):
        self.opts = _Options()
        self.BEGIN = None
        self.PATTERN = None
        self.ACTION = None
        self.END = None
        self.INPUT = None
        self.OUTPUT = None

    def __call__(self, stdin=None, stdout=None):
        args = self._command()

        if self.INPUT or stdin:
            if not os.path.exists(self.INPUT) and not stdin:
                echo = subprocess.Popen(['echo', self.INPUT], stdout=subprocess.PIPE)
                stdin = echo.stdout

            return subprocess.Popen(args, stdin=stdin, stdout=stdout)
        else:
            print('Cannot awk without input')

    def show_command(self):
        args = self._command()
        print(' '.join(args))

    def show_code(self):
        print('#!/usr/bin/awk -f')
        print(self._generate_code())

    def _command(self):
        args = ['awk']
        args = self.opts.get(args)
        if not self.opts.f:
            args.append(self._generate_code())

        if self.INPUT and os.path.isfile(self.INPUT):
            args.append(self.INPUT)

        return args

    def _generate_code(self):
        code = ''
        if self.BEGIN:
            code += 'BEGIN' + self._bracket(self.BEGIN)

        inner_code = ''
        if self.PATTERN:
            inner_code += self.PATTERN

        if self.ACTION:
            inner_code += ' ' + self._bracket(self.ACTION)

        code += inner_code

        if self.END:
            code += '\nEND' + self._bracket(self.END)

        return code

    def _bracket(self, code):
        bcode = '{'
        if isinstance(code, list):
            bcode += '; '.join(code)
        elif isinstance(code, str):
            bcode += code

        return bcode + '}\n'


class _Options(object):

    def __init__(self):
        self.f = None
        self.F = None
        self.v = []

    def get(self, args=[]):
        if self.F:
            args.extend(['-F', self.F])

        if self.v:
            args.extend(['-v', self.v])

        if self.f:
            args.extend(['-f', self.f])

        return args
