import json
import os

import requests


def get_person(page):
    """
    :param page: page number
    :return:
    """
    # the website url we are going to crawl
    url = f'https://www.douyu.com/gapi/rknc/directory/yzRec/{page}'
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/95.0.4638.69 Safari/537.36 "
    }
    # send the request
    response = requests.get(url, headers=headers)

    # parse the response
    content = response.json()
    person_list = content["data"]["rl"]

    # extract the person name and image url
    extracted_info = []
    for person in person_list:
        username = person["nn"]
        user_image_url = person["rs1"]
        extracted_info.append({"username": username, "img_url": user_image_url})

    # save the extract data as json format
    with open('extract_person.json', 'a') as f:
        content = json.dumps(extracted_info, indent=4)
        f.write(content)


def download_image(json_file):
    with open(json_file, 'r') as f:
        content = f.read()



if __name__ == '__main__':
    get_person(1)
