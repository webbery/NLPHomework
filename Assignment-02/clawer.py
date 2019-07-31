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

def search_detail(start,dest,search_map,cost):
    result = None
    pathes = [{'path':[start],'distance':0,'subways':[]}]

    # visited = []
    while pathes:
        path = pathes.pop(0)
        station_name = path['path'][-1]

        neighbors = search_map[station_name]['neighbor']
        for neighbor in neighbors:
            if neighbor['name'] in path['path']: continue   # exclude loop path
            new_path = path['path'] + [neighbor['name']]
            subway = list(set(search_map[station_name]['subway'])&set(search_map[neighbor['name']]['subway']))
            new_subway =path['subways'] + (subway if subway[0] not in path['subways'] else [])
            path_info = {
                'path':new_path,
                'distance': path['distance']+neighbor['distance'],
                'subways': new_subway
            }
            # exclude path which is badder than results
            if result and cost(path_info)>cost(result): continue
            pathes.append(path_info)

            if neighbor['name']==dest:
                # print(path_info)
                result = path_info
                break
    return result

class TransferNum:
    def __init__(self,transfer,station):
        self.transfer_count=transfer
        self.station_count=station

    def __gt__(self, value):
        if self.transfer_count>value.transfer_count: return True
        if self.station_count>value.station_count: return True
        return False

def station_count(obj):
    return len(obj['path'])

def transfer_count(obj):
    return TransferNum(len(obj['subways']),len(obj['path']))

def get_distance(obj):
    return obj['distance']

def is_exist(station):
    if not stations.__contains__(station):
        print(station+' not exist')
        return False
    return True

def search(src,dst):
    if not is_exist(src) or not is_exist(dst):
        return 
    result = search_detail(src,dst,stations,station_count)
    print('最少站点:',result)

    result = search_detail(src,dst,stations,transfer_count)
    print('最少换乘:',result)

    result = search_detail(src,dst,stations,get_distance)
    print('最短距离:',result)

# search('海淀五路居','平西路')

def a_star(start,dest,search_map,cost):
    result = None
    pathes = [{'path':[start],'distance':0,'subways':[]}]

    # visited = []
    while pathes:
        path = pathes.pop(0)
        station_name = path['path'][-1]

        neighbors = search_map[station_name]['neighbor']
        for neighbor in neighbors:
            if neighbor['name'] in path['path']: continue   # exclude loop path
            new_path = path['path'] + [neighbor['name']]
            subway = list(set(search_map[station_name]['subway'])&set(search_map[neighbor['name']]['subway']))
            new_subway =path['subways'] + (subway if subway[0] not in path['subways'] else [])
            path_info = {
                'path':new_path,
                'distance': path['distance']+neighbor['distance'],
                'subways': new_subway
            }
            # exclude path which is badder than results
            
            # if result and cost(path_info)>cost(result): continue
            # pathes.append(path_info)

            if neighbor['name']==dest:
                result = path_info
                break
    return result

# print(search('顺义','西土城'))