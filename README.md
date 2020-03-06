## Introduction
This repo includes two useful tools to crawl instagram posts by usernames or by hashtags. It uses selenium to open a browser and animate the human's action (e.g., click, scroll, and etc.), thus can crawl the Instagram without requiring the official API.

## Requirements
python2.7
argparse   
selenium  
json  
urllib  
hashlib  
requests  
reverse\_geocoder

## Usage
1. Crawl by usernames:  
python crawl\_by\_user.py [-h] [-u USER_LIST] [-d DATA\_PATH] [-i IMAGE_PATH]  
or just try it with default arguments: python crawl\_by\_user.py  
You can save the usernames in the ./users.txt file, each line of which is a username of Instagram. The default download directory is ./data/userss (save metadata such as number of likes, comments, texts, etc.) ./data/userss\_images (save all the images).  
2. Crawl by hashtags:  
python crawl\_by\_hashtag.py [-h] [-t TAG] [-d DATA\_PATH] [-i IMAGE_PATH]  
or just try it with default arguments: python crawl\_by\_hashtag.py  
You can save the hashtags in the ./hashtags.txt file, each line of which is a hashtag in Instagram. The default download directory is ./data/hashtags (save metadata such as number of likes, comments, texts, etc.) ./data/hastags\_images (save all the images)  
