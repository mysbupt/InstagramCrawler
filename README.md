## Introduction
This repo includes two useful tools to crawl instagram posts by usernames or by hashtags. It uses selenium to open a browser and simulate the human's action (e.g., click, scroll, and etc.), thus can crawl the Instagram without requiring the official API.

### Requirements
python2.7
argparse   
selenium  
json  
urllib  
hashlib  
requests  
reverse\_geocoder

### Usage
1. Crawl by usernames:  
python crawl\_by\_user.py [-h] [-u USER_LIST] [-d DATA\_PATH] [-i IMAGE_PATH]  
or just try it with default arguments: python crawl\_by\_user.py  
You can save the usernames in the ./users.txt file, each line of which is a username of Instagram. The default download directory is ./data/userss (save metadata such as number of likes, comments, texts, etc.) ./data/userss\_images (save all the images).  
2. Crawl by hashtags:  
python crawl\_by\_hashtag.py [-h] [-t TAG] [-d DATA\_PATH] [-i IMAGE_PATH]  
or just try it with default arguments: python crawl\_by\_hashtag.py  
You can save the hashtags in the ./hashtags.txt file, each line of which is a hashtag in Instagram. The default download directory is ./data/hashtags (save metadata such as number of likes, comments, texts, etc.) ./data/hastags\_images (save all the images)  

### Citation
This repo is first contributed along with the paper ["Who, Where, and What to Wear? Extracting Fashion Knowledge from Social Media"](https://dl.acm.org/doi/pdf/10.1145/3343031.3350889), so if you use the code of this repo, kindly cite it as:
```
@inproceedings{ma2019and,
  title={Who, Where, and What to Wear? Extracting Fashion Knowledge from Social Media},
  author={Ma, Yunshan and Yang, Xun and Liao, Lizi and Cao, Yixin and Chua, Tat-Seng},
  booktitle={Proceedings of the 27th ACM International Conference on Multimedia},
  pages={257--265},
  year={2019}
}
```

### Acknowledgement
This project is supported by the National Research Foundation, Prime Minister's Office, Singapore under its IRC@Singapore Funding Initiative.

<img src="https://github.com/mysbupt/InstagramCrawler/blob/master/next.png" width = "297" height = "100" alt="next" align=center />
