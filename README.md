## Introduction
This repo includes two useful tools to crawl instagram posts by usernames or by hashtags. It uses selenium to open a browser and animate the human's action (e.g., click, scroll, and etc.), thus can crawl the Instagram without requiring the official API.

## Requirements
python2.7
packages: argparse, selenium, json, urllib, hashlib, requests, reverse\_geocoder

## Usage
1. Crawl by usernames:
crawl_by_user.py [-h] [-u USER_LIST] [-d DATA_PATH] [-i IMAGE_PATH]
You can save the usernames in the ./users.txt file, each line of which is a username of Instagram
2. Crawl by hashtags:
crawl_by_hashtag.py [-h] [-t TAG] [-d DATA_PATH] [-i IMAGE_PATH]
You can save the hashtags in the ./hashtags.txt file, each line of which is a hashtag in Instagram
