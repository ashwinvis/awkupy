"""IAwk Jupyter Kernel

$ python -m awkupy.kernel &
$ jupyter console --existing

"""
import sys
from contextlib import redirect_stderr
from metakernel import ProcessMetaKernel as Kernel

from . import IAwk, __version__


class IAwkKernel(Kernel):
    implementation = "IAwk"
    implementation_version = __version__
    language = "awk"
    language_version = "5.0"
    language_info = {
        "name": "Any text",
        "mimetype": "application/x-awk",
        "file_extension": ".awk",
    }
    banner = "IAwk version: " + __version__

    _awk_engine = None

    @property
    def engine(self):
        if not self._awk_engine:
            self._awk_engine = IAwk(
                #  error_handler=self.Error,
                stdin=self.raw_input,
                stdout=self.Print,
                #  stream_handler=self.Print,
                #  cli_options=self.cli_options,
                #  inline_toolkit=self.inline_toolkit,
                #  logger=self.log,
            )
            #  # Internals
            #  cmd = IAwk()
            #  #  cmd.use_rawinput = False
            #  cmd.preloop()
            self._awk_engine.preloop()

        return self._awk_engine

    def do_execute_direct(
        self, code, silent=False,
    ):
        return self.engine.onecmd(code)

if __name__ == "__main__":
    IAwkKernel.run_as_main()
