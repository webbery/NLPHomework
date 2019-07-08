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
    css = "#sub"+str(i)+" tr"
    # css = "#sub"+str(0)+" tr"
    data = r.html.find(css)
    subway_name = ''
    for idx in range(len(data)):
        if idx==1: continue     # do not process describe grid
        # print(data[idx].html)
        # here we can use regex or css selector to get data
        if idx==0:
            searchObj = re.search(r'.*<td .*>(.*)相邻站间距信息统计表</td>',data[idx].html,re.M|re.S)
            if searchObj:
                subway_name = searchObj.group(1)
                # print("searchObj.group(1) : ", searchObj.group(1))
        else:
            searchObj = re.search(r'<th>(.*)——(.*)</th>\n<td(.*)>(\w+)</td>',data[idx].html,re.M|re.S)
            if searchObj:
                station1 = searchObj.group(1)
                station2 = searchObj.group(2)
                distance = int(searchObj.group(4))
                add_station(subway_name,station1,station2,distance)
            else:
                print(data[idx].html)
    print(subway_name)
    print('---------')
    # print(stations)