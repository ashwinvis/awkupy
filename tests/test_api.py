from awkupy import Awk


def test_fileinput():
    awk = Awk()
    awk.code = '/^  [0-9]/{print $0}'
    awk.INPUT = "LICENSE"
    awk()


def test_textinput():
    awk = Awk()
    awk.PATTERN = '/^[a-c]/'
    awk.ACTION = 'print $2'
    awk.INPUT = """
a. First
b. Second
c. Third
d. Fourth
"""
    awk()
