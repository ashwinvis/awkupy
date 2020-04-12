import subprocess
import os
import fileinput


class AwkError(IOError):
    pass


class Awk(object):
    """A subprocess interface for AWK."""

    def __init__(self):
        self.opts = _Options()
        del self.code
        self.INPUT = None

    def __call__(self, stdin=None, stdout=None):
        cmd = self.command

        if not stdin:
            if os.path.isfile(self.INPUT):
                with open(self.INPUT, "rb") as fp:
                    text = fp.read()
            elif self.INPUT:
                text = (
                    self.INPUT.encode()
                    if isinstance(self.INPUT, str)
                    else self.INPUT
                )
            else:
                raise AwkError("Cannot awk without input / stdin")

            proc = subprocess.run(cmd, input=text, stdout=stdout)
        else:
            proc = subprocess.run(cmd, stdin=stdin, stdout=stdout)

    def __repr__(self):
        cmd = self.command
        return " ".join(cmd)

    @property
    def command(self):
        cmd = ["awk"]
        cmd.extend(self.opts.args)
        if not self.opts.f:
            cmd.append(self.code)

        if self.INPUT and os.path.isfile(self.INPUT):
            cmd.append(self.INPUT)

        return cmd

    @property
    def code(self):
        if not (self.BEGIN or self.PATTERN or self.ACTION or self.END):
            return self._code

        code = ""
        if self.BEGIN:
            code += "BEGIN" + self._bracket(self.BEGIN)

        inner_code = ""
        if self.PATTERN:
            inner_code += self.PATTERN

        if self.ACTION:
            inner_code += " " + self._bracket(self.ACTION)

        code += inner_code

        if self.END:
            code += "\nEND" + self._bracket(self.END)

        return code

    @code.setter
    def code(self, source_code):
        del self.code
        self._code = source_code

    @code.deleter
    def code(self):
        self.BEGIN = None
        self.PATTERN = None
        self.ACTION = None
        self.END = None

        self._code = ""

    def _bracket(self, code):
        bcode = "{"
        if isinstance(code, list):
            bcode += "; ".join(code)
        elif isinstance(code, str):
            bcode += code

        return bcode + "}\n"


class _Options(object):
    def __init__(self):
        self.f = None
        self.F = None
        self.v = []

    def __repr__(self):
        return " ".join(self.args)

    @property
    def args(self):
        args = []
        if self.F:
            args.extend(["-F", self.F])

        if self.v:
            args.extend(["-v", self.v])

        if self.f:
            args.extend(["-f", self.f])

        return args
