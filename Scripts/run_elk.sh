#!/bin/bash
#Log file destination entered by user

function start {
	echo 'Enter path of log file(s)'
	read LOG_PATH
	if [[ -d $LOG_PATH ]]; then
	    echo "$LOG_PATH is a directory"
	    LOG_PATH="$LOG_PATH/*log"
	elif [[ -f $LOG_PATH ]]; then
	    echo "$LOG_PATH is a file"
	else
	    echo "$LOG_PATH is not valid"
	    exit 1
	fi
	LOGSTASH_PATH="/usr/local/elk/logstash-1.5.0"
	ELK_PATH="/usr/local/elk"
	#if [[ -d $LOGSTASH_PATH ]]; then
	#	echo "$LOGSTASH_PATH is a directory"
	#else
	#	echo "$LOGSTASH_PATH is not valid"
	#    exit 1
	#fi
	#Making a directory that contains customized filters
	if [[ ! -d "$LOGSTASH_PATH/patterns" ]]; then
	    echo "making dir $LOGSTASH_PATH/patterns"
	    mkdir "$LOGSTASH_PATH/patterns"
	else
		echo 'patterns directory already exists'
	fi
	'''echo "Writing extra patterns in $LOGSTASH_PATH/patterns/extra_patterns"
	echo 'ONLY_WARN (WARNING(.*))' > $LOGSTASH_PATH/patterns/extra_patterns
	#Configuration file
	echo "Writing configuration file for logstash,that is, $LOGSTASH_PATH/warning.conf"
	echo "input {
		file{
			sincedb_path => \"/dev/null\"
			path => \"$LOG_PATH\"
			start_position => \"beginning\"
		}
	}

	filter{
		grok{
			patterns_dir => \"./patterns\"
			match => {\"message\" =>\"%{ONLY_WARN:warning_msg}\"}
			tag_on_failure => []
		}
	}
	output {
	  	
		elasticsearch {
			host=>localhost
			protocol => \"http\"
		}
		stdout{ codec => rubydebug}
	}" > $LOGSTASH_PATH/warning.conf'''

	#Running elk stack afresh
	echo "Do you want to clear elasticsearch?(press y or n)"
	read OP
	$ELK_PATH/elasticsearch-1.5.1/bin/elasticsearch >/dev/null 2>&1 &
	#Waiting for elasticsearch to open completely
	sleep 10
	if [[ "$OP" == 'y' ]]; then
		curl -XDELETE 'http://localhost:9200/logstash*';
		curl -XDELETE 'http://localhost:9200/.kibana';
		echo "Elasticsearch cleared!"
	fi
	$LOGSTASH_PATH/bin/logstash -f $LOGSTASH_PATH/general.conf >/dev/null 2>&1 &
	$ELK_PATH/kibana-4.0.2-darwin-x64/bin/kibana >/dev/null 2>&1 &
	echo "ELK stack started!"
	echo "Go to browser and type following url's to see ELK working:"
	echo "For Elasticsearch: localhost:9200/_search?pretty"
	echo "For Kibana: localhost:5601"
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