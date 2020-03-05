#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from utility import load_file, crawl_one_url


def get_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user_list", default="./users.txt", help="user list file to crawl")
    parser.add_argument("-d", "--data_path", default="./data/users", help="path to save crawled user data")
    parser.add_argument("-i", "--image_path", default="./data/users_images", help="path to save crawled images")
    args = parser.parse_args()
    return args


def main():
    paras = get_cmd()

    user_names = load_file(paras.user_list)

    data_path = paras.data_path
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    img_save_path = paras.image_path
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)

    for i, user_name in enumerate(user_names):
        url = "https://www.instagram.com/" + user_name + "/"
        crawl_one_url(url, data_path, img_save_path, user_name)


if __name__ == '__main__':
    main()
