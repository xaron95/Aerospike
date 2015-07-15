from elasticsearch import Elasticsearch
es = Elasticsearch() 

#Getting lowest and highest timestamp
x = es.search(index="logstash-*",size=1,body={"sort":[{"@timestamp" : {"order" : "desc"}}]})
y = x['hits']['hits']
hi = y[0]['_source']['@timestamp']
x = es.search(index="logstash-*",size=1,body={"sort":[{"@timestamp" : {"order" : "asc"}}]})
y = x['hits']['hits']
lo = y[0]['_source']['@timestamp']
files = []
namespaces = []

#Getting maximum and minimum values for data objects
x = es.search(index="logstash-*",size=1,body={"sort":[{"data_objects" : {"order" : "desc"}}]})
y = x['hits']['hits']
hi_dataobj = y[0]['_source']['data_objects']
x = es.search(index="logstash-*",size=1,body={"sort":[{"data_objects" : {"order" : "asc"}}]})
y = x['hits']['hits']
lo_dataobj = y[0]['_source']['data_objects']

#Getting maximum and minimum values for other htbt diff
x = es.search(index="logstash-*",size=1,body={"sort":[{"other_htbt_diff" : {"order" : "desc"}}]})
y = x['hits']['hits']
hi_other_htbt = y[0]['_source']['other_htbt_diff']
x = es.search(index="logstash-*",size=1,body={"sort":[{"other_htbt_diff" : {"order" : "asc"}}]})
y = x['hits']['hits']
lo_other_htbt = y[0]['_source']['other_htbt_diff']

#Getting different filenames
x = es.search(index="logstash-*",body={"aggs": {"files":{"terms": {"field": "filename", "size": 0}}}})
y = x['aggregations']['files']['buckets']
for z in y:
	files.append(z['key'])

filestring = ""
for i in range(0,len(files)-1):
	filestring = filestring+"{\"input\":{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"filename:\\\""+str(files[i])+"\\\"\"}}}},"
filestring = filestring+"{\"input\":{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"filename:\\\""+str(files[-1])+"\\\"\"}}}}"

#Getting different namespaces
x = es.search(index="logstash-*",body={"aggs": {"namespaces":{"terms": {"field": "mem_namespace", "size": 0}}}})
y = x['aggregations']['namespaces']['buckets']
for z in y:
	namespaces.append(z['key'])

memorystring=""
size = [1,1+(5*len(namespaces)),1+(10*len(namespaces))]
#Memory usage viz
for i in range(0,len(namespaces)):
	if i < len(namespaces)-1:
		memorystring = memorystring+"{\"id\":\""+"memory-ns"+str(i+1)+"-viz"+"\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":5,\"col\":1,\"row\":"+str(size[0]+(5*i))+"},{\"id\":\""+"disk-ns"+str(i+1)+"-viz"+"\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":5,\"col\":1,\"row\":"+str(size[1]+(5*i))+"},{\"id\":\""+"sindex-ns"+str(i+1)+"-viz"+"\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":5,\"col\":1,\"row\":"+str(size[2]+(5*i))+"},"
	namespacestring = "{\"input\":{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"mem_namespace:\\\""+str(namespaces[i])+"\\\"\"}}}}"
	#Getting maximum and minimum values for disk usage 
	x = es.search(index="logstash-*",size=1,body={"query":{"match":{"mem_namespace":namespaces[i]}},"sort":[{"disk_inuse" : {"order" : "desc"}}]})
	y = x['hits']['hits']
	hi_temp = y[0]['_source']['disk_inuse']
	x = es.search(index="logstash-*",size=1,body={"query":{"match":{"mem_namespace":namespaces[i]}},"sort":[{"disk_inuse" : {"order" : "asc"}}]})
	y = x['hits']['hits']
	lo_temp = y[0]['_source']['disk_inuse']
	data = {"title":"disk-ns"+str(i+1)+"-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":true,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{\"max\":"+str(hi_temp)+",\"min\":"+str(lo_temp)+"}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"disk_inuse\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":["+namespacestring+"],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
	es.create(index=".kibana",doc_type="visualization",id="disk-ns"+str(i+1)+"-viz",body=data)
	#Getting maximum and minimum values for main memory usage
	x = es.search(index="logstash-*",size=1,body={"query":{"match":{"mem_namespace":namespaces[i]}},"sort":[{"disk_inuse" : {"order" : "desc"}}]})
	y = x['hits']['hits']
	hi_temp = y[0]['_source']['memory_inuse_bytes']
	x = es.search(index="logstash-*",size=1,body={"query":{"match":{"mem_namespace":namespaces[i]}},"sort":[{"disk_inuse" : {"order" : "asc"}}]})
	y = x['hits']['hits']
	lo_temp = y[0]['_source']['memory_inuse_bytes']
	data = {"title":"memory-ns"+str(i+1)+"-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":true,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{\"max\":"+str(hi_temp)+",\"min\":"+str(lo_temp)+"}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"memory_inuse_bytes\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":["+namespacestring+"],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
	es.create(index=".kibana",doc_type="visualization",id="memory-ns"+str(i+1)+"-viz",body=data)
	#Getting maximum and minimum values for sindex memory usage
	x = es.search(index="logstash-*",size=1,body={"query":{"match":{"mem_namespace":namespaces[i]}},"sort":[{"disk_inuse" : {"order" : "desc"}}]})
	y = x['hits']['hits']
	hi_temp = y[0]['_source']['sindex_memory_inuse']
	x = es.search(index="logstash-*",size=1,body={"query":{"match":{"mem_namespace":namespaces[i]}},"sort":[{"disk_inuse" : {"order" : "asc"}}]})
	y = x['hits']['hits']
	lo_temp = y[0]['_source']['sindex_memory_inuse']
	data = {"title":"sindex-ns"+str(i+1)+"-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":true,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{\"max\":"+str(hi_temp)+",\"min\":"+str(lo_temp)+"}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"sindex_memory_inuse\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":["+namespacestring+"],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
	es.create(index=".kibana",doc_type="visualization",id="sindex-ns"+str(i+1)+"-viz",body=data)
memorystring = memorystring+"{\"id\":\""+"memory-ns"+str(i+1)+"-viz"+"\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":5,\"col\":1,\"row\":"+str(size[0]+(5*i))+"},{\"id\":\""+"disk-ns"+str(i+1)+"-viz"+"\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":5,\"col\":1,\"row\":"+str(size[1]+(5*i))+"},{\"id\":\""+"sindex-ns"+str(i+1)+"-viz"+"\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":6,\"col\":1,\"row\":"+str(size[2]+(5*i))+"}"

'''#Getting source files and line numbers
x = es.search(index="logstash-*",q="log_level:INFO",body={"aggs": {"agg1": {"terms": {"field": "Source_file"},"aggs": {"agg2": {"terms": {"field": "Line_number"}}}}}})
source_file = []
lines = []
y = x['aggregations']['agg1']['buckets']
for z in y:
  source_file.append(z['key'])
  l = z['agg2']['buckets']
  for m in l:
  	lines.append(m['key'])

sourcestring = ""
for i in range(0,len(source_file)-1):
  sourcestring = sourcestring+"{\"input\":{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"Source_file:\\\""+str(source_file[i])+"\\\"\"}}}},"
sourcestring = sourcestring+"{\"input\":{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"Source_file:\\\""+str(source_file[-1])+"\\\"\"}}}}"

linestring = ""
for i in range(0,len(lines)-1):
  linestring = linestring+"{\"input\":{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"Line_number:\\\""+str(lines[i])+"\\\"\"}}}},"
linestring = linestring+"{\"input\":{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"Line_number:\\\""+str(lines[-1])+"\\\"\"}}}}"
'''
#Grouping filename,Source file and line number for warning messages
x = es.search(index="logstash-*",q="log_level:WARNING",body={
    "aggs": {
      "agg1": {
        "terms": {
          "field": "filename"
        },
      "aggs": {
        "agg2": {
          "terms": {
            "field": "Source_file"
          },
          "aggs": {
            "agg3": {
              "terms": {
                "field": "Line_number"
              }
            }
          }          
        }
      }
    }
  }
})
temp = []
y = x['aggregations']['agg1']['buckets']
for z in y:
  #print z['key'],z['doc_count']
  a = z['agg2']['buckets']
  for i in a:
    #print i['key'],i['doc_count']
    b = i['agg3']['buckets']
    for j in b:
      #print j['key'],j['doc_count']
      temp.append([z['key'],i['key'],j['key'],j['doc_count']])
statstring=""
for i in range(0,len(temp)):
  statstring = statstring+"|"+temp[i][0]+"|"+temp[i][1]+"|"+str(temp[i][2])+"|"+str(temp[i][3])+"|\\n"
data = {"title":"warning-stats","visState":"{\"type\":\"markdown\",\"params\":{\"markdown\":\"|&nbsp;&nbsp;&nbsp;Filename&nbsp;&nbsp;&nbsp;|&nbsp; &nbsp; &nbsp;Source file &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; Line number &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp;Count &nbsp; &nbsp; &nbsp; |\\n|:-----------:|:-------------:|:----------------:|:-----------:|\\n"+statstring+"\\n\"},\"aggs\":[],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="warning-stats",body=data)
#Warning stats
#data = {"title":"warning-stats","visState":"{\"type\":\"table\",\"params\":{\"perPage\":20,\"showPartialRows\":false,\"showMeticsAtAllLevels\":false},\"aggs\":[{\"id\":\"1\",\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"log_level:\\\"INFO\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"bucket\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"bucket\",\"params\":{\"filters\":["+sourcestring+"]}},{\"id\":\"5\",\"type\":\"filters\",\"schema\":\"bucket\",\"params\":{\"filters\":["+linestring+"]}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
#es.create(index=".kibana",doc_type="visualization",id="warning-stats",body=data)

#Migrations viz
data = {"title":"migrations-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"incoming_mig\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"outgoing_mig\"}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="migrations-viz",body=data)

#Histogram reads viz
data = {"title":"reads-hist","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"diff_reads_trans\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"reads\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="reads-hist",body=data)

#Histogram writes viz
data = {"title":"writes-hist","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"diff_writes_master_trans\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"writes_master\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="writes-hist",body=data)

#Histogram proxy viz
data = {"title":"proxy-hist","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"diff_proxy_trans\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"proxy\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="proxy-hist",body=data)

#Histogram query_rec_count viz
data = {"title":"query_count-hist","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"diff_query_count\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"query_rec_count\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="query_count-hist",body=data)

#Histogram query viz
data = {"title":"query-hist","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"diff_query_trans\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"query\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="query-hist",body=data)

#Histogram udf viz
data = {"title":"udf-hist","visState":"{\"type\":\"line\",\"params\":{\"shareYAxis\":true,\"addTooltip\":true,\"addLegend\":true,\"showCircles\":true,\"smoothLines\":false,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false,\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"diff_udf_trans\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":[{\"input\":{\"query\":{\"query_string\":{\"query\":\"hist_type:\\\"udf\\\"\",\"analyze_wildcard\":true}}}}],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="udf-hist",body=data)

#Data Objects viz
data = {"title":"data_obj-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":true,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{\"max\":"+str(hi_dataobj)+",\"min\":"+str(lo_dataobj)+"}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"data_objects\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="data_obj-viz",body=data)

#Data Objects diff viz
data = {"title":"data_obj_diff-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"data_obj_diff\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="data_obj_diff-viz",body=data)

#Self heartbeat diff viz
data = {"title":"htbt-self","visState":"{\"aggs\":[{\"id\":\"1\",\"params\":{\"field\":\"self_htbt_diff\"},\"schema\":\"metric\",\"type\":\"avg\"},{\"id\":\"2\",\"params\":{\"customInterval\":\"2h\",\"extended_bounds\":{},\"field\":\"@timestamp\",\"interval\":\"auto\",\"min_doc_count\":1},\"schema\":\"segment\",\"type\":\"date_histogram\"},{\"id\":\"3\",\"params\":{\"filters\":["+filestring+"]},\"schema\":\"group\",\"type\":\"filters\"}],\"listeners\":{},\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"type\":\"line\"}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="htbt-self",body=data)

#Other heartbeat diff viz
data = {"title":"htbt-other","visState":"{\"aggs\":[{\"id\":\"1\",\"params\":{\"field\":\"other_htbt_diff\"},\"schema\":\"metric\",\"type\":\"avg\"},{\"id\":\"2\",\"params\":{\"customInterval\":\"2h\",\"extended_bounds\":{},\"field\":\"@timestamp\",\"interval\":\"auto\",\"min_doc_count\":1},\"schema\":\"segment\",\"type\":\"date_histogram\"},{\"id\":\"3\",\"params\":{\"filters\":["+filestring+"]},\"schema\":\"group\",\"type\":\"filters\"}],\"listeners\":{},\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":true,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{\"max\":"+str(hi_other_htbt)+",\"min\":"+str(lo_other_htbt)+"}},\"type\":\"line\"}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="htbt-other",body=data)

#Sindex mem usage viz
data = {"title":"sindexmem_inuse-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"sindex_memory_inuse\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":["+namespacestring+"],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="sindexmem_inuse-viz",body=data)

#Memory inuse viz
data = {"title":"memory_inuse-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"memory_inuse_bytes\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":["+namespacestring+"],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="memory_inuse-viz",body=data)

#Disk inuse viz
data = {"title":"disk_inuse-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"disk_inuse\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}},{\"id\":\"4\",\"type\":\"filters\",\"schema\":\"split\",\"params\":{\"filters\":["+namespacestring+"],\"row\":true}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="disk_inuse-viz",body=data)

#Cluster size viz
data = {"title":"cluster-viz","visState":"{\"type\":\"line\",\"params\":{\"addLegend\":true,\"addTimeMarker\":false,\"addTooltip\":true,\"defaultYExtents\":false,\"drawLinesBetweenPoints\":true,\"interpolate\":\"linear\",\"radiusRatio\":9,\"scale\":\"linear\",\"setYExtents\":false,\"shareYAxis\":true,\"showCircles\":true,\"smoothLines\":false,\"times\":[],\"yAxis\":{}},\"aggs\":[{\"id\":\"1\",\"type\":\"avg\",\"schema\":\"metric\",\"params\":{\"field\":\"cluster_size\"}},{\"id\":\"2\",\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"type\":\"filters\",\"schema\":\"group\",\"params\":{\"filters\":["+filestring+"]}}],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"index\":\"logstash-*\",\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="cluster-viz",body=data)

#Other-graphs markdown
data = {"title":"Other graphs","visState":"{\"type\":\"markdown\",\"params\":{\"markdown\":\"####_Other graphs_:\\n1. [Warning stats][warndash] \\n2. [Histograms][histdash]\\n3. [Memory usage][memdash]\\n\\n\\n[memdash]:http://localhost:5601/#/dashboard/memory_usage-dash?_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),time:(from:\'"+str(lo)+"\',mode:absolute,to:\'"+str(hi)+"\'))\\n[histdash]:http://localhost:5601/#/dashboard/hist-dash?_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),time:(from:\'"+str(lo)+"\',mode:absolute,to:\'"+str(hi)+"\'))\\n[warndash]:http://localhost:5601/#/dashboard/warning-dash?_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),time:(from:\'"+str(lo)+"\',mode:absolute,to:\'"+str(hi)+"\'))\"},\"aggs\":[],\"listeners\":{}}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="Other-graphs",body=data)

#Network-graphs markdown
data = {"title":"Network graphs","visState":"{\"aggs\":[],\"listeners\":{},\"params\":{\"markdown\":\"####_Network graphs_:\\n1. [Heartbeats][htbtdash]\\n2. [Migrations][migdash]\\n\\n\\n[htbtdash]:http://localhost:5601/#/dashboard/htbt-dash?_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),time:(from:\'"+str(lo)+"\',mode:absolute,to:\'"+str(hi)+"\'))\\n[migdash]:http://localhost:5601/#/dashboard/migrations-dash?_g=(refreshInterval:(display:Off,pause:!f,section:0,value:0),time:(from:\'"+str(lo)+"\',mode:absolute,to:\'"+str(hi)+"\'))\"},\"type\":\"markdown\"}","description":"","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"query\":{\"query_string\":{\"analyze_wildcard\":true,\"query\":\"*\"}},\"filter\":[]}"}}
es.create(index=".kibana",doc_type="visualization",id="Network-graphs",body=data)

#Warning Dashboard
data = {"title":"warning-dash","hits":0,"description":"","panelsJSON":"[{\"id\":\"warning-stats\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":8,\"col\":1,\"row\":1}]","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}}}]}"}}
es.create(index=".kibana",doc_type="dashboard",id="warning-dash",body=data)

#Memory Usage Dashboard
data = {"title":"memory_usage-dash","hits":0,"description":"","panelsJSON":"["+memorystring+"]","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}}}]}"}}
es.create(index=".kibana",doc_type="dashboard",id="memory_usage-dash",body=data)

#Heartbeat Dashboard
data = {"title":"htbt-dash","hits":0,"description":"","panelsJSON":"[{\"id\":\"htbt-other\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":4,\"col\":1,\"row\":1},{\"id\":\"htbt-self\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":6,\"col\":1,\"row\":5}]","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}}}]}"}}
es.create(index=".kibana",doc_type="dashboard",id="htbt-dash",body=data)

#Migrations Dashboard
data = {"title":"migrations-dash","hits":0,"description":"","panelsJSON":"[{\"id\":\"data_obj-viz\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":5,\"col\":1,\"row\":6},{\"id\":\"cluster-viz\",\"type\":\"visualization\",\"size_x\":6,\"size_y\":5,\"col\":1,\"row\":1},{\"id\":\"migrations-viz\",\"type\":\"visualization\",\"size_x\":6,\"size_y\":5,\"col\":7,\"row\":1},{\"id\":\"data_obj_diff-viz\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":5,\"col\":1,\"row\":11}]","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}}}]}"}}
es.create(index=".kibana",doc_type="dashboard",id="migrations-dash",body=data)

#Histogram Dashboard
data = {"title":"hist-dash","hits":0,"description":"","panelsJSON":"[{\"id\":\"reads-hist\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":4,\"col\":1,\"row\":1},{\"id\":\"writes-hist\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":4,\"col\":1,\"row\":5},{\"id\":\"udf-hist\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":4,\"col\":1,\"row\":9},{\"id\":\"proxy-hist\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":4,\"col\":1,\"row\":13},{\"id\":\"query_count-hist\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":4,\"col\":1,\"row\":17},{\"id\":\"query-hist\",\"type\":\"visualization\",\"size_x\":12,\"size_y\":4,\"col\":1,\"row\":21}]","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}}}]}"}}
es.create(index=".kibana",doc_type="dashboard",id="hist-dash",body=data)

#Main Dashboard
data = {"title":"main-dash","hits":0,"description":"","panelsJSON":"[{\"id\":\"Network-graphs\",\"type\":\"visualization\",\"size_x\":6,\"size_y\":5,\"col\":1,\"row\":1},{\"id\":\"Other-graphs\",\"type\":\"visualization\",\"size_x\":6,\"size_y\":5,\"col\":7,\"row\":1}]","version":1,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}}}]}"}}
es.create(index=".kibana",doc_type="dashboard",id="Main Dashboard",body=data)

