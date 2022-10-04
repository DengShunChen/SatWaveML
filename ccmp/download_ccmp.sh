#!/bin/bash

#module add proxy

WGET="wget"
FLAGS=" --no-check-certificate --cut-dir=1 -l 20 -Y on -nH -np -m -r"

VERSION=2.1

ini_dtg=2021060400
end_dtg=2021060500

dtg=${ini_dtg}
while [ ${dtg} -le ${end_dtg} ] ; do
  
  YYYY=$(echo ${dtg} | cut -c1-4 )
  MM=$(echo ${dtg} | cut -c5-6 )
  DD=$(echo ${dtg} | cut -c7-8 )

  if [ ! -e v0${VERSION}.NRT/Y${YYYY}/M${MM}/CCMP_RT_Wind_Analysis_${YYYY}${MM}${DD}_V0${VERSION}_L3.0_RSS.nc ] ; then 
    $WGET ${FLAGS} http://data.remss.com/ccmp/v0${VERSION}.NRT/Y${YYYY}/M${MM}/CCMP_RT_Wind_Analysis_${YYYY}${MM}${DD}_V0${VERSION}_L3.0_RSS.nc
  fi

  dtg=$(./Caldtg.ksh ${dtg} +24)
done

#------
