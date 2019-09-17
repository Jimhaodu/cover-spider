# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from multiprocessing.dummy import Pool as ThreadPool
import urllib3
import bs4
import os
import time
##
def save_img(url, file_path):
            # file_path = url.split('/')[-1]

            res1 = urllib3.PoolManager().request('get', url,        
                                                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",}).data
            with open(file_path, 'wb') as f:
                f.write(res1)
            print('Get：' + file_path)
            time.sleep(2)

def get_pageUrl(first_url):
    print('star download!')
    http=urllib3.PoolManager(headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        })
    urls=[]
    
    for url in first_url:
        pageData = http.request('get',url)     
        soup = bs4.BeautifulSoup(pageData.data,'lxml')
        count_pages=len(soup.findAll('option'))
        for x in range(1,count_pages+1):
            urls.append(url[:-1]+str(x))
    return urls 
first_url=["http://www.dudu-sex.biz/m/category.php?tid=hospital&page=1"
           ,"http://www.dudu-sex.biz/m/category.php?tid=av&page=1"
           ,"http://www.dudu-sex.biz/m/category.php?tid=csubtitle&page=1"
           ,"http://www.dudu-sex.biz/m/category.php?tid=nomask&page=1"
           ,]
urls = get_pageUrl(first_url)

http=urllib3.PoolManager( headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        })
print(str(len(urls))+"Pages To DownLoad!")    


def spyder(url):
    # for url in urls:
    movies=[]
    print('downloading '+url+'\n In Thread')
    pageData = http.request('get',url)
    soup = bs4.BeautifulSoup(pageData.data,'lxml')
    dl = soup.select('#data_list  li')

    for dd in dl:
        detial_List = []
        detial_List.append( dd.select('img')[0].attrs['data-src'])
       # dd.xpath('//img/@data-src').extract_first() 图片的链接
        detial_List.append( dd.select('.sTit')[0].getText())
       # dd.xpath("//span[@class='sTit']//text()").extract_first()# 影片名称mnt/e/I
        detial_List.append( dd.select('.sBottom')[0].getText())
       # dd.xpath("//div/a/span[@class='sBottom']/text()").extract_first('None')# 影片号码  ''.join(stat.split(': ')[1].split(' '))
        detial_List.append( 'http://www.dudu-sex.biz/m/'+ dd.select('div a')[0].attrs['href'])
        # dd.xpath('//div/a/@href').extract_first()# 具体地址
        # 提取图片链接
        detial_List.append(url)
        movies.append(detial_List)

    for movie in movies:
        ncutUrl = movie[0].split('cover.jpg')[0]+'ncut.jpg'
        coverUrl = movie[0]
       # <img src="https://d46.online/a_image.php?locate=/secure/aMovie/hospital/2013020501/cover.jpg" onerror="nofind(this)">
       #dir_path = '%s/%s/%s' % ('e:/project', 'AVspider',movie[-1].split('=')[-2].split('&')[0])  # 存储路径
        dir_path = '%s/%s/%s' % ('/mnt/e/I', 'AVspider',coverUrl.split('/')[-3])  # 存储路径
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                os.makedirs(dir_path + '/cover')
                os.makedirs(dir_path + '/movie')

            file_name = coverUrl.split('/')[-2] + '-' + movie[1] + '-' + movie[2] + '-'
            cover_file_path = '%s/%s%s' % (dir_path + '/cover', file_name,coverUrl.split('/')[-1])
            ncut_file_path = '%s/%s%s' % (dir_path + '/cover', file_name, ncutUrl.split('/')[-1])

            if not os.path.exists(cover_file_path):
                save_img(coverUrl, cover_file_path)
            else:
                print(cover_file_path + ' 已存在！')
            if not os.path.exists(ncut_file_path):
                save_img(ncutUrl, ncut_file_path)
            else:
                print(cover_file_path + ' 已存在！')
        except IOError:
            print("Error: 没有找到文件或读取文件失败")
        except IndexError:
            print("Error: IndexError 边界出错")
    time.sleep(0.5)

pool = ThreadPool(7) #3核电脑
pool.map(spyder, urls)#多线程工作
pool.close()
pool.join()
