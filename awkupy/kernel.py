"""IAwk Jupyter Kernel

$ python -m awkupy.kernel &
$ jupyter console --existing

"""
import sys
from contextlib import redirect_stderr
from ipykernel.kernelbase import Kernel

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

    # Internals
    cmd = IAwk()
    cmd.use_rawinput = False
    cmd.preloop()



    def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        if not silent:
            try:
                payload = []
                if code.strip() in ("exit", "quit"):
                    result = ""
                    payload.append(
                        {
                            "source": "ask_exit",
                            # whether the kernel should be left running, only closing
                            # the client
                            "keepkernel": False,
                        }
                    )
                else:
                    result = self.cmd.onecmd(code)

                status = "ok"
                stream_content = {
                    "name": 'stdout',
                    "text": result if result else "",
                }

                self.send_response(self.iopub_socket, "stream", stream_content)

                return {
                    "status": status,
                    # The base class increments the execution count
                    "execution_count": self.execution_count,
                    "payload": payload,
                    "user_expressions": {},
                }
            except IOError as e:
                status = "error"

                return {
                    "status": status,
                    "execution_count": self.execution_count,
                    "ename": e.__class__.__name__,
                    "traceback": str(e),
                }


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=IAwkKernel)
