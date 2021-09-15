# get the page source code ---> requerst
# get the target content ---> regex

import requests
import re

url = "https://movie.douban.com/top250"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.63 Safari/537.36 "
}
# response is null means we have to add the headers to let the website know we are using browser instead of program
resp = requests.get(url, headers=headers)
page_content = resp.text

# parse data
obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>'
                 r'.*?<p class="">.*?<br>(?P<year>.*?)&nbsp'
                 r'.*?<div class="star">.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>'
                 r'.*?<span>(?P<rateNum>.*?)人评价</span>', re.S)
# start to find the obj
result = obj.finditer(page_content)
for it in result:
    print(it.group("name"), end='-')
    print(it.group("year").strip(), end='-')
    print(it.group("score"), end='-')
    print(it.group("rateNum"))
    # group single video info to dict
    dic = it.groupdict()
    # process date
    dic["date"] = dic["date"].strip()
