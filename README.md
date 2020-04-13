awkupy and IAwk
===============
*AWK meets Python: API, CLI and magics*

[![PyPI](https://img.shields.io/pypi/v/awkupy)](https://pypi.org/project/awkupy/)
[![LICENSE](https://img.shields.io/badge/license-GPL-blue.svg)](/LICENSE)

A simple subprocess based Pythonic interface for Awk, which powers a
command-line REPL and Jupyter magics.


Installation
------------

```bash
pip install awkupy
```

Features
--------

- [x] Python class to call AWK via subprocess - see an [example](doc/examples/coins_histogram.py).
- [x] IPython / Jupyter magics: `%awk` and `%%awk`, enabling polyglot
      programming with Awk. See [example](doc/examples/coins_histogram.ipynb)
      and the [tutorial](doc/examples/tutorial.ipynb) for more details.

```awk
In [1]: %load_ext iawk

In [2]: cd doc/examples/
/home/avmo/src/projects/awkupy/doc/examples

In [3]: %%awk --stdout coins.txt
   ...: {
   ...:   country[$4]++
   ...: }
   ...:
   ...: END {
   ...:   for (i in country) print "Country: " i," count: ", country[i]
   ...: }
   ...:
   ...:
Country: USA  count:  7
Country: PRC  count:  1
Country: Austria-Hungary  count:  1
Country: Canada  count:  1
Country: Switzerland  count:  1
Country: RSA  count:  2
```

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

References
----------

- [To awk or not to ...](https://sites.google.com/site/toawkornot/home) -
  excellent tutorial on Awk
