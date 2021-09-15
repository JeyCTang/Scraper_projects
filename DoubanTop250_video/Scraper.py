import requests
import re
import json
from tqdm import tqdm


class Scraper:
    def __init__(self, url, headers):
        self.base_url = url
        self.headers = headers
        self.results = []

    # send requests to get the html source page
    def send_requests(self, url):
        resp = requests.get(url, headers=self.headers)
        page_content = resp.text
        if not page_content:
            raise Exception
        else:
            return page_content

    # select data by Regex
    def select_data(self, page_content):
        pattern = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>'
                             r'.*?<p class="">.*?<br>(?P<year>.*?)&nbsp'
                             r'.*?<div class="star">.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>'
                             r'.*?<span>(?P<rateNum>.*?)人评价</span>', re.S)
        movies = pattern.finditer(page_content)
        # process the collected movies
        for movie in movies:
            movie_dic = movie.groupdict()
            movie_dic['year'] = movie_dic['year'].strip()
            self.results.append(movie_dic)

    # save the data as json file
    def save_json(self):
        with open('./output/top_250_movie_Douban.json', 'w') as f:
            json_data = json.dumps(self.results, indent=2)
            f.write(json_data)

    # how to run this program
    def run(self):
        interval = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225]
        for num in tqdm(interval):
            target_url = self.base_url + '?start=' + str(num)
            page_content = self.send_requests(target_url)
            self.select_data(page_content)
        self.save_json()
        print("done!")


if __name__ == "__main__":
    # headers = {
    #     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
    #                   "Chrome/93.0.4577.63 Safari/537.36 "
    # }
    # scraper = Scraper("https://movie.douban.com/top250", headers=headers)
    # scraper.run()

    # evaluate
    with open('./output/top_250_movie_Douban.json', encoding='utf-8-sig') as f:
        video_data = json.load(f)
    print(len(video_data))
    for video in video_data:
        print("片名：%s --- 年代：%s --- 评分：%s --- 评论数：%s" % (video['name'], video['year'], video['score'], video['rateNum']))
