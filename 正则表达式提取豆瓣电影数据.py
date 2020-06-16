import requests
import re
def get_one_page(url):
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        return response.text
    return None
def parse_one_page(html):
    pattern=re.compile('<li>.*?<em\sclass.*?>(.*?)</em>.*?title">(.*?)<.*?<p class="">.*?:(.*?)&nbsp;&nbsp;&nbsp;.*?: (.*?)<br>\s+(\d\d\d\d)(.*?)&nbsp.*?rating_num.*?>(.*?)<.*?</li>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield{'电影排名':item[0],
              '电影名称':item[1],
              '电影导演':item[2],
              '电影主演':item[3],
              '上映时间':item[4],
              '电影评分':item[5]
                }
def main(offset):
    url='https://movie.douban.com/top250?start='+str(offset)+'&filter='
    html=get_one_page(url)
    for item in parse_one_page(html):
        print(item)
if __name__=='__main__':
    for i in range(10):
        offset=i*25
        main(offset)