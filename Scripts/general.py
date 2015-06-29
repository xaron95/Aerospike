from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()
x = []
y = []
files = []
temp1 = es.search(index='logstash*',size=100000000)
temp2 = temp1['hits']['hits']
for t in temp2:
	files.append(t['_source']['filename'])
file_set = set(files)
files = list(file_set)
for j in range(1,8):
	temp = 'flag:'+str(j)
	x.append(es.search(index='logstash*',size=100000000,q=temp))
	y.append(x[j-1]['hits']['hits'])
	if j==1:
		self_htbt = []
		self_htbt_diff = []
		other_htbt = []
		other_htbt_diff = []
		for z in y[j-1]:
			self_htbt.append([z['_source']['self_heartbeats'],z['_source']['@timestamp'],z['_source']['filename']])
			other_htbt.append([z['_source']['other_heartbeats'],z['_source']['@timestamp'],z['_source']['filename']])
		self_htbt = sorted(self_htbt, key=lambda x:x[1])
		other_htbt = sorted(other_htbt, key=lambda x:x[1])
		self_temp = []
		other_temp = []
		for k in range(0,len(files)):
			l = 0
			while l < len(self_htbt):
				if self_htbt[l][2] == files[k]:
					temp = l
					break
				l+=1
			i = temp+1
			while i < len(self_htbt):
				if self_htbt[temp][2] == self_htbt[i][2]:
					self_htbt_diff.append([self_htbt[i][0]-self_htbt[temp][0],self_htbt[temp][2]])
					other_htbt_diff.append([other_htbt[i][0]-other_htbt[temp][0],other_htbt[temp][2]])
					temp = i
				i+=1
		while i < len(self_htbt):
			self_htbt_diff.append(self_htbt[i][0]-self_htbt[i-1][0])
			other_htbt_diff.append(other_htbt[i][0]-other_htbt[i-1][0])
			i += 1
		index = "logstash-meta"
		for i in range(0,len(self_htbt_diff)):
			es.create(index="logstash-meta",doc_type="info",body={"self_diff":int(self_htbt_diff[i][0]),"other_diff":int(other_htbt_diff[i][0]),"@timestamp":self_htbt[i][1],"tag":'htbt',"filename":self_htbt[i][2]})
#for i in range(1,len(self_htbt)):
#	if self_htbt[i]<self_htbt[i-1]:
#		print self_htbt[i-1],self_htbt[i]
#print self_htbt_diff
#print other_htbt_diff
#print x
#print y
#for i in range(1,len(self_htbt)):
data = {"title":"htbt-diff-sc","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"other_diff\"}},{\"id\":\"2\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"self_diff\"}},{\"id\":\"3\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a1\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a2\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-m*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="htbt_diff_script",body=data)
data = {"title":"trans_in_progress-sc","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"4\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"wr\"}},{\"id\":\"5\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"prox\"}},{\"id\":\"6\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"bq\"}},{\"id\":\"7\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"dq\"}},{\"id\":\"8\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"wait\"}},{\"id\":\"9\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"q\"}},{\"id\":\"10\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"iq\"}},{\"id\":\"11\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fab_ever_closed\"}},{\"id\":\"12\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fab_recent_open\"}},{\"id\":\"13\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fab_ever_opened\"}},{\"id\":\"14\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fds_ever_closed\"}},{\"id\":\"15\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fds_ever_opened\"}},{\"id\":\"16\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"fab_recent_open\"}},{\"id\":\"17\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a2\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a1\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="trans_in_progress_script",body=data)
data = {"title":"nsup_viz-sc","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"nsup_records\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"4\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"0-vt\"}},{\"id\":\"5\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"current_expired\"}},{\"id\":\"6\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"total_expired\"}},{\"id\":\"7\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"current_evicted\"}},{\"id\":\"8\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"total_evicted\"}},{\"id\":\"9\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"current_setdeletes\"}},{\"id\":\"10\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"total_setdeletes\"}},{\"id\":\"11\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"current_setevicted\"}},{\"id\":\"12\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"total_setevicted\"}},{\"id\":\"13\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"total_nsup_time_ms\"}},{\"id\":\"14\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a2\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a1\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="nsup_viz_script",body=data)
data = {"title":"histogram_viz-sc","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"total_hist_time_msec\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"5\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"reads\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"writes_master\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"proxy\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"udf\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"query\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"query_rec_count\\\"\",\"analyze_wildcard\":true}}}}]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a1\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a2\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}},{\"id\":\"6\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"total_query_count\"}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="hist_viz_script",body=data)
data = {"title":"memory_usage-sc","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"10\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"mem_namespace:\\\"cache\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"mem_namespace:\\\"persistent\\\"\",\"analyze_wildcard\":true}}}}]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a1\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a2\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}},{\"id\":\"6\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"disk_inuse\"}},{\"id\":\"7\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"memory_inuse_bytes\"}},{\"id\":\"8\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"sindex_memory_inuse\"}},{\"id\":\"9\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"avail_pct\"}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="mem_usage_script",body=data)
data = {"title":"migrations_mig-sc","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"incoming_mig\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"4\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"outgoing_mig\"}},{\"id\":\"5\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a1\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a2\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="migration_script",body=data)
data = {"title":"data_obj_mig-sc","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"data_objects\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a1\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a2\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="data_obj_mig_script",body=data)
data = {"title":"cluster_mig-sc","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"cluster_size\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a1\\\"\",\"analyze_wildcard\":true}}}},{\"input\":{\"query\":{\"query_string\":{\"query\":\"filename:\\\"a2\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="cluster_mig_script",body=data)


data = {"title":"temp_dashboard","hits":0,"description":"","panelsJSON":"[{\"col\":1,\"id\":\"cluster_mig_script\",\"row\":1,\"size_x\":4,\"size_y\":5,\"type\":\"visualization\"},{\"col\":5,\"id\":\"data_obj_mig_script\",\"row\":1,\"size_x\":4,\"size_y\":5,\"type\":\"visualization\"},{\"col\":9,\"id\":\"migration_script\",\"row\":1,\"size_x\":4,\"size_y\":5,\"type\":\"visualization\"},{\"col\":1,\"id\":\"hist_viz_script\",\"row\":6,\"size_x\":12,\"size_y\":5,\"type\":\"visualization\"},{\"col\":1,\"id\":\"mem_usage_script\",\"row\":11,\"size_x\":12,\"size_y\":5,\"type\":\"visualization\"},{\"col\":1,\"id\":\"nsup_viz_script\",\"row\":16,\"size_x\":12,\"size_y\":5,\"type\":\"visualization\"},{\"col\":1,\"id\":\"trans_in_progress_script\",\"row\":21,\"size_x\":12,\"size_y\":7,\"type\":\"visualization\"},{\"id\":\"htbt_diff_script\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":6,\"col\":1,\"row\":28}]","version":1,"timeRestore":false,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}}}]}"}}
es.create(index=".kibana",doc_type="dashboard",id="temp_dashboard_script",body=data)