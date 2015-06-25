#!/bin/bash
#64-bit MAC
who &> temp
USER=$(cat temp | awk '{print $1}' | uniq)
rm -rf temp
if (java -version &> temp); then
	x=`cat temp | grep "java version" | awk '{print $3}'`
	y=`echo "$x" |awk -F'.' '{print $2}'`
	rm temp
	if [[ $y < 7 ]]; then
		echo "Installing java8..."
		curl -v -j -k -L -H "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u20-b26/jdk-8u20-macosx-x64.dmg > jdk-8u20-macosx-x64.dmg
		hdiutil mount jdk-8u20-macosx-x64.dmg
		installer -package /Volumes/JDK\ 8\ Update\ 20/JDK\ 8\ Update\ 20.pkg -target "/Volumes/Macintosh HD"
		cd ~
		hdiutil unmount "/Volumes/JDK 8 Update 20/"
		rm -rf jdk-8u20-macosx-x64.dmg
	else
		echo "Java version okay"
	fi
else
	echo "Installing java8..."
	curl -v -j -k -L -H "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u20-b26/jdk-8u20-macosx-x64.dmg"
	hdiutil mount jdk-8u20-macosx-x64.dmg
	installer -package /Volumes/JDK\ 8\ Update\ 20/JDK\ 8\ Update\ 20.pkg -target "/Volumes/Macintosh HD"
	cd ~
	hdiutil unmount "/Volumes/JDK 8 Update 20/"
	rm -rf jdk-8u20-macosx-x64.dmg
fi
if [[ ! -d /usr/local/elk ]]; then
	mkdir /usr/local/elk
	chown -R $USER /usr/local/elk
	curl -L -O https://download.elasticsearch.org/logstash/logstash/logstash-1.5.0.tar.gz
	tar -zxvf logstash-1.5.0.tar.gz -C /usr/local/elk
	chown -R $USER /usr/local/elk/logstash-1.5.0/
	rm -rf logstash-1.5.0.tar.gz
	curl -L -O https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.5.1.tar.gz
	tar -zxvf elasticsearch-1.5.1.tar.gz -C /usr/local/elk
	chown -R $USER /usr/local/elk/elasticsearch-1.5.1/
	rm -rf elasticsearch-1.5.1.tar.gz
	curl -L -O https://download.elastic.co/kibana/kibana/kibana-4.1.0-darwin-x64.tar.gz
	tar -zxvf kibana-4.1.0-darwin-x64.tar.gz -C /usr/local/elk
	chown -R $USER /usr/local/elk/kibana-4.1.0-darwin-x64/
	rm -rf kibana-4.1.0-darwin-x64.tar.gz
else
	echo "ELK stack already installed"
fi