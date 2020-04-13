from IPython.conftest import get_ipython


def test_magics():
    ip = get_ipython()
    ip.run_line_magic('load_ext', 'iawk')
    ip.run_cell_magic('awk_input', '', 'Pat   100 97 58\nSandy  84 72 93\nChris  72 92 89\n\n')
    ip.run_line_magic('awk', "--debug --stdout -e '{print $1+$2*$3}'")
