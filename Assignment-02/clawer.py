from requests_html import HTMLSession
import re

session = HTMLSession()
r = session.get("http://www.bjsubway.com/station/zjgls")

# for i in range(18):
# css = "#sub"+str(i)+" td"
css = "#sub"+str(0)+" tr"
data = r.html.find(css)
for idx in range(len(data)):
    if idx==1: continue     # do not process describe grid
    # here we can use regex or css selector to get data
    # print(data[idx].html)
    searchObj = re.search(r'.*<td colspan="5">(.*)线相邻站间距信息统计表</td>\n</tr>\n<tr>\n<th>(.+)——(.+)</th>\n<td width="146">(\w+)</td>\n<td width="148">上行/下行</td>\n</tr>',data[idx].html,re.M|re.S)
    if searchObj:
        print("searchObj.group(1) : ", searchObj.group())
        print("searchObj.group(1) : ", searchObj.group(1))
        # print("searchObj.group(1) : ", searchObj.group(2))
    else:
        print('Not found')