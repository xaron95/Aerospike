from elasticsearch import Elasticsearch
from time import sleep

es = Elasticsearch()
x = input()
e = es.search(index='logstash-*',size=1)
y = e['hits']['total']
print "Loading..."
while(y<x):
	print "..."
	sleep(5)
	e = es.search(index='logstash-*',size=1)
	y = e['hits']['total']