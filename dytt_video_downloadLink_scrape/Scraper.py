import json
import time

import requests
import re
from tqdm import tqdm


class Scraper:
    def __init__(self, domain, entry_url):
        self.domain = domain
        self.entry_url = entry_url
        self.result = []
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/93.0.4577.63 Safari/537.36 "
        }

    # send the requests, return the page content
    def send_req(self, url):
        resp = requests.get(url=url, headers=self.headers)
        resp.encoding = 'gb2312'
        resp.close()
        time.sleep(3)
        return resp.text

    # select the movie list
    @staticmethod
    def get_mvlist(page_content):
        pattern = re.compile(r'<td height="26">.*?<a href="(?P<movie_page>.*?)"', re.S)
        mv_links = pattern.findall(page_content)
        return mv_links

    # select the information of a single movie, return the dict
    @staticmethod
    def get_mvinfo(page_content):
        pattern = re.compile(r'<ul>.*?<strong class="rank">(?P<rate>.*?)</strong></span>'
                             r'.*?◎年　　代(?P<year>.*?)<br />.*?◎产　　地(?P<country>.*?)<br />'
                             r'.*?◎语　　言(?P<lang>.*?)<br />.*?◎字　　幕(?P<sub>.*?)<br />'
                             r'.*?<tbody>.*?<a href="(?P<download_link>.*?)">', re.S)
        # only one movie info will be found so we use search method
        mv_match = pattern.search(page_content)
        mv_dict = mv_match.groupdict()
        mv_dict['year'] = mv_dict['year'].strip()
        mv_dict['country'] = mv_dict['country'].strip()
        mv_dict['lang'] = mv_dict['lang'].strip()
        mv_dict['sub'] = mv_dict['sub'].strip()
        return mv_dict

    # save the data as json file
    @staticmethod
    def save_data(data):
        with open('./output/hot_movie_list.json', 'w', encoding='utf-8') as f:
            json_data = json.dumps(data)
            f.write(json_data)

    # run the process
    def run(self):
        maxPageNum = 20
        for i in range(0, maxPageNum+1):
            if i == 0:
                print("scraping the page %d ....." % i)
                page_content = self.send_req(url=self.entry_url)
                time.sleep(2)
                mv_links = self.get_mvlist(page_content)
                print("extracting the data from page %d ...." % i)
                for mv_link in tqdm(mv_links):
                    mv_page_url = self.domain + mv_link
                    mv_page_content = self.send_req(mv_page_url)
                    time.sleep(2)
                    mv_dict = self.get_mvinfo(mv_page_content)
                    self.result.append(mv_dict)
            elif i == 1:
                continue
            else:
                print("scraping the page %d ....." % i)
                entry_url = self.entry_url+'index_'+str(i)+'.html'
                page_content = self.send_req(url=entry_url)
                time.sleep(2)
                mv_links = self.get_mvlist(page_content)
                print("extracting the data from page %d ...." % i)
                for mv_link in tqdm(mv_links):
                    mv_page_url = self.domain + mv_link
                    mv_page_content = self.send_req(mv_page_url)
                    time.sleep(2)
                    mv_dict = self.get_mvinfo(mv_page_content)
                    self.result.append(mv_dict)
        print("Saving data ...")
        self.save_data(self.result)
        print("Done!")


if __name__ == "__main__":
    base_url = "https://www.dy2018.com"
    target_url = "https://www.dy2018.com/html/bikan/"
    scraper = Scraper(base_url, target_url)
    scraper.run()

