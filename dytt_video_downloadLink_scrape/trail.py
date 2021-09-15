import requests
import re

# send requests to the website
base_url = "https://www.dy2018.com"
target_url = "https://www.dy2018.com/html/bikan/"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.63 Safari/537.36 "
}
resp = requests.get(target_url, headers=headers)
resp.encoding = 'gb2312'
# print(resp.text)

# collect the link list
re_1 = re.compile(r'<td height="26">.*?<a href="(?P<movie_page>.*?)"', re.S)
links = re_1.finditer(resp.text)
for link in links:
    sub_link = link.group('movie_page')
    sub_resp = requests.get(url=base_url+sub_link, headers=headers)
    sub_resp.encoding = 'gb2312'
    # print(sub_resp.text)
    pattern = re.compile(r'<ul>.*?<strong class="rank">(?P<rate>.*?)</strong></span>'
                         r'.*?◎年　　代(?P<year>.*?)<br />.*?◎产　　地(?P<country>.*?)<br />'
                         r'.*?◎语　　言(?P<lang>.*?)<br />.*?◎字　　幕(?P<sub>.*?)<br />'
                         r'.*?<tbody>.*?<a href="(?P<download_link>.*?)">', re.S)
    mv_info = pattern.search(sub_resp.text)
    # for mv_info in mv_infos:
    print(mv_info.group('rate'))
    print(mv_info.group('year'))
    print(mv_info.group('country'))
    print(mv_info.group('lang'))
    print(mv_info.group('sub'))
    print(mv_info.group('download_link'))
    break

