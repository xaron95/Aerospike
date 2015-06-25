#/usr/local/elk/logstash-1.5.0/bin/logstash -f /usr/local/elk/logstash-1.5.0/general.conf < /tmp/log.s
#python /Users/kutemangesh/Desktop/scripts/htbt.py
#http://localhost:5601/#/visualize/create?type=line&indexPattern=logstash-m*&_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),time:(from:now-1d,mode:relative,to:now))&_a=(filters:!(),linked:!f,query:(query_string:(analyze_wildcard:!t,query:'*')),vis:(aggs:!((id:'1',params:(field:other_diff),schema:metric,type:avg),(id:'2',params:(field:self_diff),schema:metric,type:avg),(id:'3',params:(customInterval:'2h',extended_bounds:(),field:'@timestamp',interval:second,min_doc_count:1),schema:segment,type:date_histogram)),listeners:(),params:(addLegend:!t,addTimeMarker:!f,addTooltip:!t,defaultYExtents:!f,drawLinesBetweenPoints:!t,interpolate:linear,radiusRatio:9,scale:linear,setYExtents:!f,shareYAxis:!t,showCircles:!t,smoothLines:!f,times:!(),yAxis:()),type:line))

#!/bin/bash
#Log file destination entered by user

function start {
	FLAG=0
	echo 'Enter path of log file(s)'
	read LOG_PATH
	if [[ -d $LOG_PATH ]]; then
	    echo "$LOG_PATH is a directory"
	    FLAG=1
	elif [[ -f $LOG_PATH ]]; then
	    echo "$LOG_PATH is a file"
	else
	    echo "$LOG_PATH is not valid"
	    exit 1
	fi
	LOGSTASH_PATH="/usr/local/elk/logstash-1.5.0"
	ELK_PATH="/usr/local/elk"
	#Making a directory that contains customized filters
	if [[ ! -d "$LOGSTASH_PATH/patterns" ]]; then
	    echo "making dir $LOGSTASH_PATH/patterns"
	    mkdir "$LOGSTASH_PATH/patterns"
	    echo "Writing extra patterns in $LOGSTASH_PATH/patterns/extra_patterns"
		echo 'SOURCE %{WORD}\.%{WORD}
		TIME_LOG %{MONTH} %{MONTHDAY} %{YEAR} %{TIME} %{WORD}' > $LOGSTASH_PATH/patterns/extra_patterns
	fi

	#Running elk stack afresh
	echo "Do you want to clear elasticsearch?(press y or n)"
	read OP
	$ELK_PATH/elasticsearch-1.6.0/bin/elasticsearch >/dev/null 2>&1 &
	#Waiting for elasticsearch to open completely
	sleep 10
	if [[ "$OP" == 'y' ]]; then
		curl -XDELETE 'http://localhost:9200/logstash*';
		curl -XDELETE 'http://localhost:9200/.kibana';
		echo "Elasticsearch cleared!"
	fi
	$ELK_PATH/kibana-4.1.0-darwin-x64/bin/kibana >/dev/null 2>&1 &
	#if [[ $FLAG == 1 ]]; then
		#$LOGSTASH_PATH/bin/logstash -f $LOGSTASH_PATH/general.conf >/dev/null 2>&1 &
	#	cat $LOG_PATH/*.s | $LOGSTASH_PATH/bin/logstash -f $LOGSTASH_PATH/general.conf
	#else
	#	$LOGSTASH_PATH/bin/logstash -f $LOGSTASH_PATH/general.conf < $LOG_PATH
	#fi
	#python $LOGSTASH_PATH/htbt.py
	$LOGSTASH_PATH/bin/logstash -f $LOGSTASH_PATH/general.conf #>/dev/null 2>&1 &
	echo "ELK stack started!"
	echo "Go to browser and type following url's to see ELK working:"
	echo "For Elasticsearch: localhost:9200/_search?pretty"
	echo "For Kibana: http://localhost:5601/"
}
function stop {
	ps -ef &> temp
	if grep -q "logstash" temp; then
		grep "logstash" temp | kill -KILL `awk '{print $2}'`
		grep "elasticsearch" temp | kill -KILL `awk '{print $2}'`
		grep "kibana" temp | kill -KILL `awk '{print $2}'`
	fi
	rm -rf temp
	echo "Stopping ELK stack..."
}
function restart {
		stop
		start
}

OPTION="$1"
if [[ "$OPTION" == "start" ]]; then
	start
elif [[ "$OPTION" == "stop" ]]; then
	stop
elif [[ "$OPTION" == "restart" ]]; then
	restart
else
	echo "Invalid argument"
	exit 1
fi