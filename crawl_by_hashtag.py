#!/usr/bin/env python

import os
import argparse

from utility import crawl_one_url


def get_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tag", default="fashion", help="which hashtag to crawl")
    parser.add_argument("-d", "--data_path", default="./data/hashtags", help="path to save crawled user data")
    parser.add_argument("-i", "--image_path", default="./data/hashtags_images", help="path to save crawled images")
    args = parser.parse_args()
    return args


def main():
    paras = get_cmd()

    hashtag = paras.tag

    data_path = paras.data_path
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    img_save_path = paras.image_path
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)

    url = "https://www.instagram.com/explore/tags/" + hashtag + "/"
    crawl_one_url(url, data_path, img_save_path, hashtag)


if __name__ == '__main__':
    main()
