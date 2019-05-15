#!/usr/bin/awk -f
/gold/ {
  country[$4]++
}

END {
  for (i in country) print "Country: " i," count: ", country[i]
}
