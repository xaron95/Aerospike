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
	echo "Logstash installation complete"
	curl -L -O https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.6.0.tar.gz
	tar -zxvf elasticsearch-1.6.0.tar.gz -C /usr/local/elk
	chown -R $USER /usr/local/elk/elasticsearch-1.6.0/
	rm -rf elasticsearch-1.6.0.tar.gz
	echo "Elasticsearch installation complete"
	curl -L -O https://download.elastic.co/kibana/kibana/kibana-4.1.0-darwin-x64.tar.gz
	tar -zxvf kibana-4.1.0-darwin-x64.tar.gz -C /usr/local/elk
	chown -R $USER /usr/local/elk/kibana-4.1.0-darwin-x64/
	rm -rf kibana-4.1.0-darwin-x64.tar.gz
	echo "Kibana installation complete"
else
	if [[ ! -d /usr/local/elk/logstash-1.5.0 ]]; then
		curl -L -O https://download.elasticsearch.org/logstash/logstash/logstash-1.5.0.tar.gz
		tar -zxvf logstash-1.5.0.tar.gz -C /usr/local/elk
		chown -R $USER /usr/local/elk/logstash-1.5.0/
		rm -rf logstash-1.5.0.tar.gz
	else
		echo "Logstash is already installed"
	fi

	if [[ ! -d /usr/local/elk/elasticsearch-1.6.0 ]]; then
		curl -L -O https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.6.0.tar.gz
		tar -zxvf elasticsearch-1.6.0.tar.gz -C /usr/local/elk
		chown -R $USER /usr/local/elk/elasticsearch-1.6.0/
		rm -rf elasticsearch-1.6.0.tar.gz
	else
		echo "Elasticsearch is already installed"
	fi
	if [[ ! -d /usr/local/elk/kibana-4.1.0-darwin-x64 ]]; then
		curl -L -O https://download.elastic.co/kibana/kibana/kibana-4.1.0-darwin-x64.tar.gz
		tar -zxvf kibana-4.1.0-darwin-x64.tar.gz -C /usr/local/elk
		chown -R $USER /usr/local/elk/kibana-4.1.0-darwin-x64/
		rm -rf kibana-4.1.0-darwin-x64.tar.gz
	else
		echo "Kibana is already installed"
	fi
fi
if [[ ! -d /usr/local/elk/logstash-1.5.0/patterns ]]; then
	cp -R logstash-1.5.0/* /usr/local/elk/logstash-1.5.0
fi

/usr/local/elk/logstash-1.5.0/bin/plugin install Ruby_gems/logstash-filter-simpledelta-0.2.0.gem &>/dev/null
sudo easy_install pip &>/dev/null
sudo pip install elasticsearch &>/dev/null 