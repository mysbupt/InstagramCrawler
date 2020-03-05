#!/usr/bin/env python
# coding: utf-8

import os
import json
from bs4 import BeautifulSoup
from dateutil.parser import parse

import time
import random
import urllib
import hashlib
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import reverse_geocoder as rg


def load_file(filepath):
    users = []
    for line in open(filepath):
        users.append(line.strip())
    return users


def download_image(img_src, img_url_md5, save_path):
    img_path = os.path.join(save_path, img_url_md5+".jpg")
    try:
        urllib.urlretrieve(img_src, img_path)
    except:
        print('download image fail', img_src)


def parse_one_page(html_doc):
    res = {}

    soup = BeautifulSoup(html_doc, "lxml")

    try:
        like_comments = soup.find("meta", {"name": "description"})["content"].split("-")[0].strip()
        tmp_like_comments = like_comments.split(u'次赞、')
        res['likes'] = tmp_like_comments[0].strip()
        res['comments'] = tmp_like_comments[-1].split(u'条评论')[0].strip()
    except:
        res['likes'] = '0'
        res['comments'] = '0'

    try:
        username = soup.find("a", class_="FPmhX notranslate nJAzx").get_text()
        res['username'] = username
    except:
        res['username'] = ''

    try:
        location = soup.find("a", class_="O4GlU")
        res['location_name'] = location.get_text()
        res['location_url'] = location["href"]
        print(res['location_name'], res['location_url'])
    except:
        res['location_name'] = ""
        res['location_url'] = ""

    try:
        publish_time = soup.find("time", class_="_1o9PC Nzb55")["datetime"]
        publish_time = parse(publish_time).strftime('%Y-%m-%d %H:%M:%S')
        res['publish_time'] = publish_time
    except:
        res['publish_time'] = ''

    return res


def handle_detail_page(chrome_options, detail_driver, location_driver, detail_url_md5, detail_link, page_source_ori=None):
    detail_res = {}

    # here to download the detail html page
    if page_source_ori is None:
        try:
            print("download html page: ", detail_link)
            detail_driver.get(detail_link)
            page_source = detail_driver.page_source
        except:
            detail_driver.quit()
            time.sleep(random.randint(1, 2))
            detail_driver = webdriver.Chrome()
            detail_driver.set_page_load_timeout(10)
            time.sleep(random.randint(1,2))
            print("detail_driver error and restart")
            detail_driver.get(detail_link)
            page_source = detail_driver.page_source
    else:
        page_source = page_source_ori

    detail_res['detail_link_md5'] = detail_url_md5

    # parse the html page
    parse_res = parse_one_page(page_source)
    for k, v in parse_res.items():
        detail_res[k] = v

    # if has location field
    if detail_res["location_name"] != '':
        # download the location page
        m = hashlib.md5()
        m.update(detail_res["location_url"].encode('utf-8'))
        loc_url_md5 = m.hexdigest()
        loc_info_valid = False
        if not loc_info_valid:
            try:
                print("location_url: ", detail_res["location_url"])
                location_driver.get('https://www.instagram.com' + detail_res['location_url'])
                page_source = location_driver.page_source
            except:
                #pass
                print("location html download error")

            detail_res["latitude"] = ""
            detail_res["longitude"] = ""
            detail_res["parse_loc_name"] = ""
            detail_res["parse_cc"] = ""
            detail_res["parse_admin1"] = ""
            detail_res["parse_admin2"] = ""
            # parse location html to get latitude and longitude
            for line in page_source.split('\n'):
                if detail_res['latitude'] != "" and detail_res['longitude'] != "":
                    break
                if '<meta property="place:location:' in line:
                    key = line.strip().split(":")[2].split('"')[0]
                    value = line.strip().split('"')[3]
                    detail_res[key] = value

            # lookup latitude and longitude to get the info of this location
            if detail_res["latitude"] != "" and detail_res["longitude"] != "":
                parse_res = rg.search((float(detail_res["latitude"]), float(detail_res["longitude"])))
                parse_res = parse_res[0]
                detail_res["parse_loc_name"] = parse_res["name"]
                detail_res["parse_cc"] = parse_res["cc"]
                detail_res["parse_admin1"] = parse_res["admin1"]
                detail_res["parse_admin2"] = parse_res["admin2"]

    return detail_res, detail_driver, location_driver


def get_multi_images(chrome_options, detail_driver, detail_url_md5, detail_link, img_save_path):
    multi_img_res = []

    try:
        print("download html page: ", detail_link)
        detail_driver.get(detail_link)
    except:
        detail_driver.close()
        time.sleep(random.randint(1,2))
        detail_driver = webdriver.Chrome()
        detail_driver.set_page_load_timeout(10)
        print("detail_driver error and restart")
        detail_driver.get(detail_link)

    # here download all the images in the detail page
    finish_flag = False
    while not finish_flag:
        each_img_res = None

        try:
            per_img_div = detail_driver.find_element_by_xpath('//div[contains(@class, "tN4sQ zRsZI")]')
        except Exception as e:
            print(e)
        per_img = per_img_div.find_element_by_xpath('//div/div/div/img')
        per_img_src = per_img.get_attribute('src')
        if per_img_src is None or per_img_src == "":
            continue
        per_img_alt = per_img.get_attribute('alt')
        if not per_img_alt:
            per_img_alt = ""

        m = hashlib.md5()
        m.update(per_img_src)
        per_img_url_md5 = m.hexdigest()

        download_image(per_img_src, per_img_url_md5, img_save_path)

        try:
            next_img_button = per_img_div.find_element_by_xpath('./button[@class="  _6CZji"]')
        except selenium.common.exceptions.NoSuchElementException as e:
            finish_flag = True
            break

        next_img_button.click()
        time.sleep(random.randint(1, 2))

    return multi_img_res, detail_driver, detail_driver.page_source


def crawl_one_url(url, data_path, img_save_path, user_name):
    # chrome for crawling image list and detail page by tagname
    chrome_options = Options()
    browse_driver = webdriver.Chrome()
    detail_driver = webdriver.Chrome()
    location_driver = webdriver.Chrome()
    browse_driver.set_page_load_timeout(10)
    detail_driver.set_page_load_timeout(10)
    location_driver.set_page_load_timeout(10)

    # get image list page
    try:
        browse_driver.get(url)
    except:
        time.sleep(random.randint(1, 2))
        browse_driver.quit()
        browse_driver = webdriver.Chrome()
        browse_driver.set_page_load_timeout(10)
        browse_driver.get(url)

    time.sleep(2)
    browse_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    last_height = browse_driver.execute_script("return document.body.scrollHeight")

    # scroll to get the image list
    cnt_total = 0
    cnt_saved_img = 0
    cnt_saved_new_img = 0
    cnt_saved_html = 0
    cnt_saved_new_html = 0

    finish_flag = False
    output = open(os.path.join(data_path, user_name), "a")
    while not finish_flag:
        print("user_name: %s" %(user_name))
        browse_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(2,4))

        new_height = browse_driver.execute_script("return document.body.scrollHeight")
        # if the scroll reach the end, sroll up a little to mock the website
        if new_height == last_height:
            finish_flag = True
            continue
        last_height = new_height

        # parse the html and get all the images
        imgs = browse_driver.find_elements_by_xpath('//div/div/a/div/div/img')
        print("\n\n\n\ start a new scroll \n\n\n", len(imgs))
        for num, img in enumerate(imgs):
            result = {}
            result['src_site'] = 'instagram'
            result['alt'] = img.get_attribute('alt')
            result['img_src'] = img.get_attribute('src')
            result['detail_link'] = img.find_element_by_xpath('./ancestor::a').get_attribute('href')
            print("original detail link is: ", result['detail_link'])

            m = hashlib.md5()
            m.update(result['img_src'])
            img_url_md5 = m.hexdigest()

            download_image(result["img_src"], img_url_md5, img_save_path)

            m = hashlib.md5()
            m.update(result['detail_link'].encode("utf-8"))
            detail_url_md5 = m.hexdigest()

            # here first judge the type of this posts: single image, multi images, or video
            result['post_type'] = 'single_img'

            try:
                post_type = img.find_element_by_xpath('./ancestor::a/div[@class="u7YqG"]')
                post_type = post_type.find_element_by_xpath('./span').get_attribute('aria-label')
                result['post_type'] = post_type
            except selenium.common.exceptions.NoSuchElementException as e:
                print("cannot detect post_type")

            print("post_type: %s" %(result['post_type']))
            if result['post_type'] == u'视频':
                print("post_type hit video")
            elif result['post_type'] == 'single_img':
                print("hit post_type with single_img")
                detail_res, detail_driver, location_driver = handle_detail_page(chrome_options, detail_driver, location_driver, detail_url_md5, result['detail_link'])
                for k, v in detail_res.items():
                    result[k] = v
            elif result['post_type'] == u'轮播':
                multi_img_res, detail_driver, page_source = get_multi_images(chrome_options, detail_driver, detail_url_md5, result['detail_link'], img_save_path)
                if len(multi_img_res) > 0:
                    result["multi_imgs"] = multi_img_res
                    detail_res, detail_driver, location_driver = handle_detail_page(chrome_options, detail_driver, location_driver, detail_url_md5, result['detail_link'], page_source_ori=page_source)
                    for k, v in detail_res.items():
                        result[k] = v
                else:
                    continue
            else:
                print("match none of the options")

            output.write(json.dumps(result).encode("utf-8") + "\n")

    browse_driver.quit()
    detail_driver.quit()
    location_driver.quit()
