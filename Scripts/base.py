from datetime import datetime
from elasticsearch import Elasticsearch
#DATA OBJECTS
es = Elasticsearch()
x = es.search(index='logstash*',size=100000000,q='flag:2')
y = x['hits']['hits']
data_objects = []
data_objects_diff = []
for z in y:
	data_objects.append([z['_source']['data_objects'],z['_source']['@timestamp']])
i = 1
data_objects = sorted(data_objects, key=lambda x:x[1])
while i < len(data_objects):
	data_objects_diff.append(data_objects[i][0]-data_objects[i-1][0])
	i += 1
#index = "logstash-"+temp[0]+"."+temp[1]+"."+temp[2]+"meta"
index = "logstash-meta"
for i in range(0,len(data_objects_diff)):
	es.create(index=index,doc_type="info",body={"data_objects_diff":data_objects_diff[i],"@timestamp":data_objects[i][1]})
for i in range(1,len(data_objects)):
	if data_objects[i][1]<data_objects[i-1][1]:
		print data_objects[i-1],data_objects[i]

#HISTOGRAM

es = Elasticsearch()
x = es.search(index='logstash*',size=100000000,q='flag:5')
y = x['hits']['hits']
hist_time = []
hist_time_diff = []
for z in y:
	if z['_source']['hist_type'] != "query_rec_count":
		hist_time.append([z['_source']['hist_type'],z['_source']['@timestamp'],z['_source']['total_hist_time_msec']])
	else:
		hist_time.append([z['_source']['hist_type'],z['_source']['@timestamp'],z['_source']['total_query_count']])
i = 1
hist_time = sorted(hist_time, key=lambda x:x[1])
hist_reads = []
hist_writes = []
hist_proxy = []
hist_udf = []
hist_query = []
hist_query_count = []
while i < len(hist_time):
	if hist_time[i][0]=="reads":
		hist_reads.append([hist_time[i][2],hist_time[i][1]])
	elif hist_time[i][0]=="writes_master":
		hist_writes.append([hist_time[i][2],hist_time[i][1]])
	elif hist_time[i][0]=="proxy":
		hist_proxy.append([hist_time[i][2],hist_time[i][1]])
	elif hist_time[i][0]=="udf":
		hist_udf.append([hist_time[i][2],hist_time[i][1]])
	elif hist_time[i][0]=="query":
		hist_query.append([hist_time[i][2],hist_time[i][1]])
	elif hist_time[i][0]=="query_rec_count":
		hist_query_count.append([hist_time[i][2],hist_time[i][1]])
	i+=1
for i in range(1,len(hist_query_count)):
	hist_time_diff.append([hist_query_count[i][0]-hist_query_count[i-1][0],hist_query_count[i][1],"query_rec_count"])
for i in range(1,len(hist_query)):
	hist_time_diff.append([hist_query[i][0]-hist_query[i-1][0],hist_query[i][1],"query"])
for i in range(1,len(hist_udf)):
	hist_time_diff.append([hist_udf[i][0]-hist_udf[i-1][0],hist_udf[i][1],"udf"])
for i in range(1,len(hist_proxy)):
	hist_time_diff.append([hist_proxy[i][0]-hist_proxy[i-1][0],hist_proxy[i][1],"proxy"])
for i in range(1,len(hist_writes)):
	hist_time_diff.append([hist_writes[i][0]-hist_writes[i-1][0],hist_writes[i][1],"writes_master"])
for i in range(1,len(hist_reads)):
	hist_time_diff.append([hist_reads[i][0]-hist_reads[i-1][0],hist_reads[i][1],"reads"])

for i in range(0,len(hist_time_diff)):
	es.create(index=index,doc_type="info",body={"hist_diff":int(hist_time_diff[i][0]),"hist_type_diff":str(hist_time_diff[i][2]),"@timestamp":hist_time_diff[i][1]})

#FDS PROTO

es = Elasticsearch()
x = es.search(index='logstash*',size=100000000,q='flag:3')
y = x['hits']['hits']
fds_recent_open = []
fds_recent_open_diff = []
fds_ever_opened = []
fds_ever_opened_diff = []
fds_ever_closed = []
fds_ever_closed_diff = []
for z in y:
	fds_recent_open.append([z['_source']['fds_recent_open'],z['_source']['@timestamp']])
	fds_ever_opened.append([z['_source']['fds_ever_opened'],z['_source']['@timestamp']])
	fds_ever_closed.append([z['_source']['fds_ever_closed'],z['_source']['@timestamp']])
i = 1
fds_recent_open = sorted(fds_recent_open, key=lambda x:x[1])
fds_ever_opened = sorted(fds_ever_opened, key=lambda x:x[1])
fds_ever_closed = sorted(fds_ever_closed, key=lambda x:x[1])
while i < len(fds_recent_open):
	fds_recent_open_diff.append(fds_recent_open[i][0]-fds_recent_open[i-1][0])
	fds_ever_opened_diff.append(fds_ever_opened[i][0]-fds_ever_opened[i-1][0])
	fds_ever_closed_diff.append(fds_ever_closed[i][0]-fds_ever_closed[i-1][0])
	i += 1
for i in range(0,len(fds_recent_open_diff)):
	es.create(index=index,doc_type="info",body={"fds_recent_open_diff":int(fds_recent_open_diff[i]),"fds_ever_opened_diff":int(fds_ever_opened_diff[i]),"fds_ever_closed_diff":int(fds_ever_closed_diff[i]),"@timestamp":fds_recent_open[i][1]})

#DASHBOARD

data = {"title":"data_objects","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"data_objects_diff\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}}],\"listeners\":{}}","description":"Average Rate of data_object change","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="data_objects_viz",body=data)
data = {"title":"histogram-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"hist_diff\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type_diff:\\\"reads\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type_diff:\\\"writes_master\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type_diff:\\\"query\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type_diff:\\\"udf\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type_diff:\\\"reads\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type_diff:\\\"proxy\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type_diff:\\\"query_rec_count\\\"\",\"analyze_wildcard\":true}}}}],\"row\":false}}],\"listeners\":{}}","description":"Average Rate of histogram for different types","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="histogram_viz",body=data)
data = {"title":"fds_proto_viz","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fds_ever_closed_diff\"}},{\"id\":\"2\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fds_ever_opened_diff\"}},{\"id\":\"3\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fds_recent_open_diff\"}},{\"id\":\"4\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}}],\"listeners\":{}}","description":"Average Rate of change of fds_proto states","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="fds_proto_viz",body=data)
data = {"title":"memory_space","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"memory_inuse_bytes\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"disk_inuse\"}},{\"id\":\"4\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"sindex_memory_inuse\"}},{\"id\":\"5\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"mem_namespace:\\\"cache\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"mem_namespace:\\\"persistent\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"Average memory usage for different namespaces","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="memory_namespace_viz",body=data)

data = {"title":"Base Dashboard","hits":0,"description":"Basic Dashboard","panelsJSON":"[{\"col\":1,\"id\":\"data_objects_viz\",\"row\":1,\"size_x\":12,\"size_y\":4,\"type\":\"visualization\"},{\"id\":\"fds_proto_viz\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":4,\"col\":1,\"row\":5},{\"id\":\"histogram_viz\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":6,\"col\":1,\"row\":9},{\"id\":\"memory_namespace_viz\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":5,\"col\":1,\"row\":15}]","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}}}]}"}}
es.create(index=".kibana",doc_type="dashboard",id="Base-Dashboard",body=data)
