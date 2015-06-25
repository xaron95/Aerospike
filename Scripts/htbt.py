from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()
x = es.search(index='logstash*',size=10000,q='flag:1')
y = x['hits']['hits']
self_htbt = []
self_htbt_diff = []
other_htbt = []
other_htbt_diff = []
for z in y:
	self_htbt.append([z['_source']['self_heartbeats'],z['_source']['@timestamp']])
	other_htbt.append([z['_source']['other_heartbeats'],z['_source']['@timestamp']])
i = 1
self_htbt = sorted(self_htbt, key=lambda x:x[1])
other_htbt = sorted(other_htbt, key=lambda x:x[1])
while i < len(self_htbt):
	self_htbt_diff.append(self_htbt[i][0]-self_htbt[i-1][0])
	other_htbt_diff.append(other_htbt[i][0]-other_htbt[i-1][0])
	i += 1
temp = datetime.now()
temp = str(temp)
temp = temp.split()
temp = temp[0].split('-')
#index = "logstash-"+temp[0]+"."+temp[1]+"."+temp[2]+"meta"
index = "logstash-meta"
for i in range(0,len(self_htbt_diff)):
	es.create(index=index,doc_type="info",body={"self_diff":self_htbt_diff[i],"other_diff":other_htbt_diff[i],"@timestamp":self_htbt[i][1]})
#for i in range(1,len(self_htbt)):
#	if self_htbt[i]<self_htbt[i-1]:
#		print self_htbt[i-1],self_htbt[i]
#print self_htbt_diff
#print other_htbt_diff
#print x
#print y