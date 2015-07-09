#!/bin/bash
#Log file destination entered by user

function start {
	echo 'Enter path of log file(s)'
	read LOG_PATH
	LOGSTASH_PATH="/usr/local/elk/logstash-1.5.0"
	ELK_PATH="/usr/local/elk"
	if [[ -d $LOG_PATH ]]; then
	    echo "$LOG_PATH is a directory"
	    sed -i '' "s|	path => .*|	path => \"$LOG_PATH/\*.log\"|" $LOGSTASH_PATH/general.conf
	    LINENUM=$(cat $LOG_PATH/*.log | wc -l)
	elif [[ -f $LOG_PATH ]]; then
	    echo "$LOG_PATH is a file"
	    sed -i '' "s|	path => .*|	path => \"$LOG_PATH\"|" $LOGSTASH_PATH/general.conf
	    LINENUM=$(cat $LOG_PATH | wc -l)
	else
	    echo "$LOG_PATH is not valid"
	    exit 1
	fi
	#Making a directory that contains customized filters
	if [[ ! -d "$LOGSTASH_PATH/patterns" ]]; then
	    echo "making dir $LOGSTASH_PATH/patterns"
	    mkdir "$LOGSTASH_PATH/patterns"
	    echo "Writing extra patterns in $LOGSTASH_PATH/patterns/extra_patterns"
		echo 'SOURCE %{USER}\.%{WORD}
		TIME_LOG %{MONTH} %{MONTHDAY} %{YEAR} %{TIME} %{WORD}
		LOG_TYPE %{WORD}|(%{WORD}:%{WORD})' > $LOGSTASH_PATH/patterns/extra_patterns
	fi

	#Running elk stack afresh
	echo "Do you want to clear elasticsearch?(press y or n)"
	read OP
	$ELK_PATH/elasticsearch-1.6.0/bin/elasticsearch >/dev/null 2>&1 &
	#Waiting for elasticsearch to open completely
	if [[ "$OP" == 'y' ]]; then
		sleep 10
		curl -XDELETE 'http://localhost:9200/logstash*';
		curl -XDELETE 'http://localhost:9200/.kibana';
		echo "Elasticsearch cleared!"
	fi
	$ELK_PATH/kibana-4.1.0-darwin-x64/bin/kibana >/dev/null 2>&1 &
	$LOGSTASH_PATH/bin/logstash -f $LOGSTASH_PATH/general.conf >/dev/null 2>&1 &
	echo "$LINENUM" | python $LOGSTASH_PATH/check.py
	python $LOGSTASH_PATH/test.py
	echo "ELK stack started!"
	echo "Go to browser and type following url's to see ELK working:"
	echo "For Elasticsearch: localhost:9200/_search?pretty"
	echo "For Kibana: http://localhost:5601/"
}
function stop {
	ps -ef &> temp
	if grep -q "kibana" temp; then
		grep "kibana" temp | kill -KILL `awk '{print $2}'`
	fi
	if grep -q "elasticsearch" temp; then
		grep "elasticsearch" temp | kill -KILL `awk '{print $2}'`
	fi
	if grep -q "logstash" temp; then
		grep "logstash" temp | kill -KILL `awk '{print $2}'`
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