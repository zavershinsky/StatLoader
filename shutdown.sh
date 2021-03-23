#!/bin/bash
#SEARCH_PID=`ps -aef | grep "daemon_mediation_device.py" | grep -v grep | awk '{print $2}'`
#if [ ! -z $SEARCH_PID ]
#then
#echo "MediationDevice daemon is not running."
#else
APP_NAME=InvoiceStatistics
PID_FILE=./PID/$APP_NAME.pid
CUR_PID=`cat $PID_FILE`
kill $CUR_PID
#for i in $SEARCH_PID;do 
#kill $i
#done
rm -f $PID_FILE

if ! [ -z $VIRTUAL_ENV ]; then
    deactivate
fi
#echo "Stopping MediationDevice daemon. PID: $CUR_PID"
#fi
