#!/bin/bash

HTMLFILE1="/openhab/conf/html/openhablog.html"
LOGFILE1="/openhab/userdata/logs/openhab.log"
HTMLFILE2="/openhab/conf/html/eventlog.html"
LOGFILE2="/openhab/userdata/logs/events.log"

echo '<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">' > ${HTMLFILE1}
echo "<html>" >> ${HTMLFILE1}
echo "<Body bgcolor=#303030>" >> ${HTMLFILE1}
echo "<pre style='color:white; width:100%'>" >> ${HTMLFILE1}
cat ${LOGFILE1} | tail -n30 >> ${HTMLFILE1}
echo "</pre>" >> ${HTMLFILE1}
echo "</Body>" >> ${HTMLFILE1}
echo "</html>" >> ${HTMLFILE1}

echo '<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">' > ${HTMLFILE2}
echo "<html>" >> ${HTMLFILE2}
echo "<Body bgcolor=#303030>" >> ${HTMLFILE2}
echo "<pre style='color:white; width:100%'>" >> ${HTMLFILE2}
cat ${LOGFILE2} | tail -n30 >> ${HTMLFILE2}
echo "</pre>" >> ${HTMLFILE2}
echo "</Body>" >> ${HTMLFILE2}
echo "</html>" >> ${HTMLFILE2}
