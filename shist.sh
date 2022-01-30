#!/bin/bash
if [ "$#" -eq 1 ]
then
  date=${1}
else
  date=`date '+%F'`
fi

sacct --starttime $date --format 'WorkDir%200,JobName,JobId,State,End' | grep -v "batch\|extern\|orted"
