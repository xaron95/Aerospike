Run installer_mac.sh to install ELK.
Default directory for ELK stack is /usr/local/elk which contains logstash,elasticsearch and kibana.

Before running run_elk.sh do the following:
Put general.conf,patterns directory,base.py and check.py in logstash folder.
Install gem by executing /usr/local/elk/bin/plugin install path_to_gem/logstash-filter-simpledelta-0.2.0.gem.
To install python elasticsearch api use pip install elasticsearch.

Run the running script run_elk.sh.

Go to kibana page, that is, http://localhost:9200
Click Create
Go to Dashboard on top and select Open dashboard on top right with folder sign.
Select main-dash

NOTE: As running script is based on location of files and directories in computer, do not change the name or location of directory.