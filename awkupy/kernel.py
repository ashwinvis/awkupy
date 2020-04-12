"""IAwk Jupyter Kernel

$ python -m awkupy.kernel &
$ jupyter console --existing

"""
import sys
import subprocess
from io import StringIO
from pathlib import Path
from metakernel import ProcessMetaKernel as Kernel, REPLWrapper, pexpect, u
#  from metakernel.process_metakernel import BashKernel

from . import IAwk, __version__


class AwkREPLWrapper(REPLWrapper):

    #  def run_command(
    #      self,
    #      command,
    #      timeout=None,
    #      stream_handler=None,
    #      line_handler=None,
    #      stdin_handler=None,
    #  ):
    pass


class IAwkKernel(Kernel):
    implementation = "IAwk"
    implementation_version = __version__
    language = "awk"
    language_version = "5.0"
    language_info = {
        "language": language,
        "mimetype": "text/x-awk",
        "file_extension": ".awk",
    }

    kernel_json = {
        "argv": [
            sys.executable,
            "-m",
            "awkupy.kernel",
            "-f",
            "{connection_file}",
        ],
        "display_name": "IAwk",
        "language": "awk",
        "name": "iawk",
    }

    _awk_engine = None
    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            awk_version = subprocess.check_output(["awk", "--version"]).decode(
                "utf-8"
            )
            self._banner = "\n".join(awk_version.splitlines()[:2])
            self._banner += "\nIAwk version: " + __version__
        return self._banner

    def do_execute_direct(
        self, code, silent=False,
    ):
        try:
            last_arg = code.split()[-1]
            if Path(last_arg).is_file():
                file = last_arg
                code = code.rstrip(last_arg)
                print('last_arg: ', last_arg)
                print('code: ', code, type(code), type(last_arg), code.rstrip(last_arg.strip()))
                print('file: ', file)
            else:
                file = None

            code = '/def/'
            text = """
def this
def that
duf tho
            """
            if not self.wrapper:
                self.wrapper = self.makeWrapper(code)

            #  result = super().do_execute_direct(text, silent)
            result = self.wrapper.run_command(text)
            #  self.Print(stdout)
            return result #  if (result and result.output) else None
        except Exception as exc:
            self.Error(exc)

    def makeWrapper(self, code, file=None):
        if pexpect.which("awk"):
            program = "awk"
        else:
            raise OSError("awk not found.")

        # We don't want help commands getting stuck,
        # use a non interactive PAGER
        #  if file:
        #      command = f"{program} --source '{code}' {file}"
        #  else:
        #      command = f"{program} --source '{code}'"

        #  print(command)
        #  child = pexpect.spawn(program, ['--source', code], echo=False, encoding='utf-8')
        d = dict(cmd_or_spawn=child, prompt_regex=u(""), prompt_change_cmd=None)
        wrapper = AwkREPLWrapper(**d)
        # No sleeping before sending commands to gnuplot
        wrapper.child.delaybeforesend = 0
        return wrapper


if __name__ == "__main__":
    IAwkKernel.run_as_main()
    #  BashKernel.run_as_main()

    #  from IPython.kernel.zmq.kernelapp import IPKernelApp
    #  IPKernelApp.launch_instance(kernel_class=IAwkKernel)
