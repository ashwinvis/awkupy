awkupy
======
AWK meets Python: bindings and interactive shell for AWK
--------------------------------------------------------

[![alpha](https://img.shields.io/badge/awkupy-v0.0.2a0-green.svg)](https://github.com/ashwinvis/awkupy/releases/tag/0.0.2a0)
[![LICENSE](https://img.shields.io/badge/license-GPL-blue.svg)](/LICENSE)

No reinventing the AWK wheel, and thus, no compromise in speed (I guess).


Installation
------------

```bash
pip install https://github.com/ashwinvis/awkupy/archive/0.0.2a0.tar.gz
```

Features
--------

- [x] Python class to call AWK via subprocess - see an [example](doc/examples/coins_histogram.py).
- [x] IPython / Jupyter magics: `%awk` and `%%awk` by loading extension `iawk`.
      See [example](doc/examples/coins_histogram.ipynb)
- [x] IAwk: interactive AWK prompt modelled after IPython.

```awk
❯❯❯ iawk                                                                                                                                        (awkupy)
Welcome to the IAwk shell. Type help or ? to list commands.
Prefix ! to run system commands

iawk [1]: help

Documented commands (type help <topic>):
========================================
EOF  cd  exit  help  hist  history  input  ls  reset  run  set  shell  show

iawk [2]: cd doc/examples/
doc/examples/
iawk [3]: ls
coins.txt coins_histogram.py coins_histogram.awk
iawk [4]: set pattern /gold/
iawk [5]: set action print $0
iawk [6]: input coins.txt
iawk [7]: show
#!/usr/bin/awk -f
/gold/ {print $0}

iawk [8]: run
iawk [9]:    gold     1    1986  USA                 American Eagle
   gold     1    1908  Austria-Hungary     Franz Josef 100 Korona
   gold     1    1984  Switzerland         ingot
   gold     1    1979  RSA                 Krugerrand
   gold     0.5  1981  RSA                 Krugerrand
   gold     0.1  1986  PRC                 Panda
   gold     0.25 1986  USA                 Liberty 5-dollar piece
   gold     0.25 1987  USA                 Constitution 5-dollar piece
   gold     1    1988  Canada              Maple Leaf

iawk [9]: exit
```
