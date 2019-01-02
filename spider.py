import requests
import os
import sys
from bs4 import BeautifulSoup as bs
#Cover: <meta data-vue-meta="true" property="og:image" content=".jpg">
#Content of video: <script>
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

def init_soup(url):
    
    kv = {'user-agent':user_agent}
    try:
        r = requests.get(url,headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        soup = bs(html,'html.parser')
        #print(soup.prettify())
    except:
        print('failed to crawl:'+str(r.status_code))
    return soup

def download_image(soup):
    image_url = ''
    image_tag = soup.find_all(property="og:image")
    image_url = image_tag[0]['content']
    image_path = './image'
    full_path = image_path + '/'+image_url.split('/')[-1]
    try:
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        if not os.path.exists(full_path):
            rimage = requests.get(image_url)
            rimage.raise_for_status()
            with open(full_path,'wb') as fimage:
                fimage.write(rimage.content)
                fimage.close()
        else:
            print('file already exist')
    except:
        print('failed to download..:'+str(rimage.status_code))
def download_video(soup, url):
    script = soup.find_all('script')[2].string
    video_url = ''
    text_list = script.split('"')
    for text in text_list:
        if 'http://' in text:
            video_url = text
    print(video_url)
    host = video_url.split('/')[2]
    print(host)
    kv = {
        'user-agent': user_agent,
        'accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'en-US,en;q=0.9',
          'Host': host,
          'Origin': 'https://www.bilibili.com',
          'Referer': url
    }
    video_path = './video'
    full_path = video_path + '/'+video_url.split('/')[-1].split('?e')[0]
    print(full_path)
    try:
        if not os.path.exists(video_path):
            os.mkdir(video_path)
        if not os.path.exists(full_path):
            r = requests.get(video_url,headers = kv,verify = False, stream = True)
            r.raise_for_status()
            print(r.request.headers)
            with open(full_path,'wb') as f:
                f.write(r.content)
                f.close()
        else:
            print('file already exist')
    except:
        print('failed to download..:'+str(r.status_code))
url = sys.argv[1]
#url = "https://www.bilibili.com/video/av10227994?from=search&seid=7268245292007641644"
soup = init_soup(url)
download_video(soup,url)
#download_image(soup)