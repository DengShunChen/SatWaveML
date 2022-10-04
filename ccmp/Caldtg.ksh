#!/bin/ksh
#-------- document block --------------
#
#  Created by ????
#  Modified by Deng-Shun Chen 
#
# Log : 
#   2017-12-07 Deng-Shun  set defalut is plus sign(+) if not specificed  
#   2017-12-07 Deng-Shun  add flexiability to input a10 or a8 dtg format 
#
#-------end document block -------------

fun_Get_DD ()
{
  case ${mm} in
    01|03|05|07|08|10|12) DD=31 ;;
    04|06|09|11) DD=30 ;;
    02) DD=28 ;;
  esac
  let aa1=yy%400
  let aa2=yy%100
  let aa3=yy%4
  if [[ ${aa3} = 0 && ${aa2} != 0 ]] || [[ ${aa1} = 0 ]]
  then
    leap=1
  else
    leap=0
  fi
  [[ ${leap} = 1 && ${mm} = "02" ]] && DD=29
}

fun_YY ()
{
  let yy=yy${Sym}1
}

fun_MM ()
{
  let mm=mm${Sym}1
  fun_Get_DD $mm
  if [ $mm -le 0 ]
  then
    fun_YY - 1
    let mm=mm+12
  elif [ $mm -gt 12 ]
  then
    fun_YY + 1 
    let mm=mm-12
  fi
}

fun_DD ()
{
  Sym=$1
  TTd=$2
  let dd=dd${Sym}TTd
  while [ ${dd} -le 0 ]
  do
    fun_MM - 1
    let dd=dd+DD
  done
  while [ ${dd} -gt ${DD} ]
  do
    let dd=dd-DD
    fun_MM + 1
  done
  ddt=${dd}
}

##### main program
##set -x
if [ $# != 2 ] ; then
  echo "$0 yymmddhh [+|-]TT"
  echo " or "
  echo "$0 yyyymmddhh [+|-]TT"
  exit 0
fi
dtg=$1
TT=$2

test=`echo ${dtg} | cut -c9-10`
if [[ ${test} = '' ]] ; then
  # empty a8
  typeset -Z2 yy mm ddt hht
  yy=`echo ${dtg} | cut -c1-2`
  mm=`echo ${dtg} | cut -c3-4`
  dd=`echo ${dtg} | cut -c5-6`
  hh=`echo ${dtg} | cut -c7-8`
else
  # non-empty a10
  typeset -Z4 yy
  typeset -Z2 mm ddt hht
  yy=`echo ${dtg} | cut -c1-4`
  mm=`echo ${dtg} | cut -c5-6`
  dd=`echo ${dtg} | cut -c7-8`
  hh=`echo ${dtg} | cut -c9-10`
fi


fun_Get_DD $mm

let TTd=0
Sym=`echo ${TT} | cut -c1-1`
if [[ ${Sym} = "-" || ${Sym} = "+" ]] ; then
  TTh=`echo ${TT} | cut -c2-`
  TTh=`echo ${TTh} | sed 's/\([0]*\)\(.*\)/\2/g'`
else
  Sym="+"
  TTh=${TT}
  TTh=`echo ${TTh} | sed 's/\([0]*\)\(.*\)/\2/g'`
fi

typeset -i TTh=${TTh-:0}

if [ ${TTh} -ge 24 ] ; then
  let TTt=TTh%24
  let TTd=TTh/24
  fun_DD ${Sym} ${TTd}
  let hh=hh${Sym}TTt
else
  let hh=hh${Sym}TTh
fi

if [ ${hh} -lt 0 ] ; then
  let hh=hh+24
  fun_DD "-" 1
elif [ ${hh} -ge 24 ] ; then
  let hh=hh-24
  fun_DD "+" 1
else
  ddt=${dd}
fi
hht=${hh}

echo $yy$mm$ddt$hht 
exit 0
