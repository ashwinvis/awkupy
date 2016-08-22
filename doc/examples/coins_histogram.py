from awkupy import Awk

awk = Awk()
awk.PROGRAM = 'country[$4]++'
awk.END = 'for (i in country) print "Country: " i," count: ", country[i]'
awk.INPUT = 'coins.txt'

awk.show_code()

awk()
