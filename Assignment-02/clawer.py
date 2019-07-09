from requests_html import HTMLSession
import re

session = HTMLSession()
r = session.get("http://www.bjsubway.com/station/zjgls")

# structure of stations: {
#   xxx_station:{
#       neighbor:[{name:xxx,distance:xxx}],
#       subway:subway_name
#   }
# }
stations={}

def add_station_detail(subway,station1,station2,distance):
    if station1 in stations:
        subways = stations[station1]['subway']
        if subway not in subways:
            subways.append(subway)
        stations[station1]['neighbor'].append({
            'name':station2,
            'distance':distance
        })
    else:
        stations[station1]={
            'subway':[subway],
            'neighbor':[{
                'name':station2,
                'distance':distance
            }]
        }

def add_station(subway,station1,station2,distance):
    add_station_detail(subway,station1,station2,distance)
    add_station_detail(subway,station2,station1,distance)

for i in range(18):
    regex_table = "#sub"+str(i)+" table"
    # regex_table = "#sub"+str(9)+" table"
    tables = r.html.find(regex_table)
    for i_table in range(len(tables)):
        data = tables[i_table].find("tr")
        subway_name = ''
        for idx in range(len(data)):
            # print(data[idx].html)
            if idx==1: continue     # do not process describe grid
            
            # here we can use regex or css selector to get data
            if idx==0:
                searchObj = re.search(r'.*<td .*>(.*)相邻站间距信息统计表</td>',data[idx].html,re.M|re.S)
                if searchObj:
                    subway_name = searchObj.group(1)
                    # print("searchObj.group(1) : ", searchObj.group(1))
            else:
                searchObj = re.search(r'<th>(.*)——(.*)</th>\n<td(.*?)>(\w+)</td>',data[idx].html,re.M|re.S)
                if searchObj:
                    station1 = searchObj.group(1)
                    station2 = searchObj.group(2)
                    distance = int(searchObj.group(4))
                    add_station(subway_name,station1,station2,distance)
# print(stations)

def BFS(start,dest):
    station1 = stations[start]

    path = []
    seen = []
    neighbors = station1['neighbor'][:]
    while len(neighbors)>0:
        front = neighbors.pop(0)
        if front['name'] in seen: continue
        
        seen.append(front['name'])
        print(front['name'])
        # print(front['name'],neighbors)
        if front['name']==dest:
            break
        neighbors = neighbors + stations[front['name']]['neighbor']
        
# BFS('西单','呼家楼')

def search(start,dest,map,sort_candidate):
    results = []
    pathes = [{'path':[start],'distance':0,'subways':[]}]

    visited = []
    while pathes:
        path = pathes.pop(0)
        station_name = path['path'][-1]
        if station_name in visited: continue
        visited.append(station_name)

        neighbors = map[station_name]['neighbor']
        for neighbor in neighbors:
            new_path = path['path'] + [neighbor['name']]
            subway = list(set(map[station_name]['subway'])&set(map[neighbor['name']]['subway']))
            new_subway =path['subways'] + (subway if subway[0] not in path['subways'] else [])
            path_info = {
                'path':new_path,
                'distance': path['distance']+neighbor['distance'],
                'subways': new_subway
            }
            pathes.append(path_info)

            if neighbor['name']==dest:
                results.append(path_info)
                break
    return sort_candidate(results)[0]

def get_stations_count(obj):
    # print(obj)
    return sorted(obj,key=lambda info: len(info['path']))

def get_distance(obj):
    return sorted(obj,key=lambda info: info['distance'])

def get_transfer_count(obj):
    return sorted(obj,key = lambda info: len(info['subways']))

result = search('古城','望京',stations,get_stations_count)
print(result)

result = search('古城','望京',stations,get_transfer_count)
print(result)
