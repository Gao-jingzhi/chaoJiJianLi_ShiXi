# 第一步 导入第三方库
# 第二步 获取目标网页
# 第三步 解析目标网页
# 第四步 下载目标网页数据


import requests
from lxml import etree
import csv
import json
import datetime
import time
import pymongo


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}


#get_video_contents
# 目的：获取视频相关信息（）
def get_video_contents(url):

    response = requests.get(url=url, headers=headers).json()
    # time.sleep(1)
    try:
        data = response['data']
        aid = data['aid']
        view = data['view']
        coin = data['coin']
        like = data['like']
        favorite = data['favorite']
        share = data['share']
        danmaku = data['danmaku']

        # print('视频编号', aid)
        # print('观看数量', view)
        # print('投币数量', coin)
        # print('收藏数量', favorite)
        # print('点赞数量', like)
        # print('分享数量', share)
        # print('弹幕数量', danmaku)

    except:
        aid = ''
        view = ''
        coin = ''
        like = ''
        favorite = ''
        share = ''
        danmaku = ''

    return aid,view,coin,like,favorite,share,danmaku

#get_up_content
# 目的：获取up主相关信息（）

#总视频数
def get_up_contents1(url):

    response = requests.get(url=url, headers=headers).json()
    # time.sleep(1)
    # video = 0
    try:
        data = response['data']
        video = data['video']

        # print('UP主编号', mid)
        # print('关注数', following)
        # print('粉丝数', follower)

    except:
        video = ''

    return video

#总粉丝数
def get_up_contents2(url):
    response = requests.get(url=url, headers=headers).json()
    # time.sleep(1)
    try:
        data = response['data']
        mid = data['mid']
        # following = data['following']
        follower = data['follower']


        # print('UP主编号', mid)
        # print('关注数', following)
        # print('粉丝数', follower)


    except:
        mid = ''
        follower = ''

    return mid, follower

#总播放量，总获赞量
#{
# "code":0,
# "message":"0",
# "ttl":1,
# "data":
#   {
# # "archive":{"view":299647},
#   "article":{"view":0},
# #  "likes":25912
#   }
# }
def get_up_contents3(url):
    response = requests.get(url=url, headers=headers).json()
    # time.sleep(1)
    try:
        data = response['data']
        likes = data['likes']
        archive = data['archive']['view']


        # print('UP主编号', mid)
        # print('关注数', following)
        # print('粉丝数', follower)


    except:
        likes = ''
        archive = ''


    return archive,likes
#播放量、点赞量



def getSource(url):

    response = requests.get(url,headers = headers)
    #修改编码格式 防止出现乱码
    response.encoding = 'UTF-8'

    #定义一个列表 目的：展示数据[{},{},{}]
    movieList =[]

    #定义一个字典 目的：保存数据
    movieDict={}

    s = etree.HTML(response.text)

    aid1 = url[-8:]
    video_information_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}'.format(aid1)
    video_infromation = get_video_contents(video_information_url)

    up_link = s.xpath('//div[@class="name"]/a[@report-id="name"]/@href')
    if up_link:
        up_link = up_link[0]
        up_mid = up_link[21:]
        # print(up_mid)

        up_link1 = 'https://api.bilibili.com/x/space/navnum?mid={}'.format(up_mid)

        up_link2 = 'https://api.bilibili.com/x/relation/stat?vmid={}'.format(up_mid)

        up_link3 = 'https://api.bilibili.com/x/space/upstat?mid={}'.format(up_mid)

        up_info1 = ''
        up_info2 =[]
        up_info3 =[]

        up_info1 = get_up_contents1(up_link1)


        up_info2 = get_up_contents2(up_link2)


        up_info3 = get_up_contents3(up_link3)

    else:
        up_link = ''
        up_mid = ''
        up_info1 = ''
        up_info2 = []
        up_info3 = []


# 1.video_url: String # 视频地址
    video_url = url
# 2.up_id: String # up 主 ID
    up_id = up_mid
# 3.up_username: String # up 主用户名
    up_username = s.xpath('//div[@class="name"]/a/text()')
    if up_username:
        up_username = up_username[0]
    else:
        up_username = ''
# 4.video_url: # 视频链接
    video_url = url
# 5.video_name: String # 视频名称
#     video_name = s.xpath('//div[@id="viewbox_report"]/h1/span[@class="tit"]/text()')
    video_name = s.xpath('//div[@id="viewbox_report"]/h1/span/text()')
    if video_name:
        video_name = video_name[0]
    else:
        video_name = ''

    # up_id_link = s.xpath('//div[@class="name"]/a/@href')[0]
# 6.video_published_at: Datetime # 发布时间
    video_published_at = s.xpath('//div[@id="viewbox_report"]/div[@class="video-data"]/span/text()')

    if video_published_at:
        video_published_at = video_published_at[0]
    else:
        video_published_at = ''

# 7.video_playback_num: Integer # 视频播放量
    if video_infromation:
        video_playback_num = video_infromation[1]

# 8.video_barrage_num: Integer # 弹幕量
        video_barrage_num = video_infromation[6]
# 9.video_like_num: Integer # 点赞量
        video_like_num = video_infromation[3]
# 10.video_coin_num: Integer # 投币量
        video_coin_num = video_infromation[2]
# 11.video_favorite_num: Integer # 收藏量
        video_favorite_num = video_infromation[4]
# 12.video_forward_num: Integer # 转发量
        video_forward_num = video_infromation[5]
    else:
        # 7.video_playback_num: Integer # 视频播放量
        video_playback_num = ''

        # 8.video_barrage_num: Integer # 弹幕量
        video_barrage_num = ''
        # 9.video_like_num: Integer # 点赞量
        video_like_num = ''
        # 10.video_coin_num: Integer # 投币量
        video_coin_num = ''
        # 11.video_favorite_num: Integer # 收藏量
        video_favorite_num = ''
        # 12.video_forward_num: Integer # 转发量
        video_forward_num = ''

# 13.video_tag # 视频标签
    video_tag = s.xpath('//div[@id="v_tag"]/ul[@class="tag-area clearfix"]/li[@class="tag"]/a/text()')
# 14.video_length # 视频时长
    video_length = 0
# 15.created_at: Datetime # 爬取时间
    created_at = 0
# 16.up_video_num: Integer # Up 主总视频数
    up_video_num = up_info1
    if up_info1 :

        up_video_num = up_info1
    else:
        up_video_num = ''

# 17.up_follow_num: Integer # Up 主总粉丝数
    if up_info2:

        up_follow_num = up_info2[1]
    else:
        up_follow_num = ''
# 18.up_like_num:Integer # Up 主总获赞数
    if up_info3:

        up_like_num = up_info3[1]
    else:
        up_like_num = ''
# 19.up_video_playback_num:Integer # Up 主总播放数
    if up_info3:

        up_video_playback_num = up_info3[0]
    else:
        up_video_playback_num = ''



#保存到字典当中

# 1.video_url: String # 视频地址
    movieDict['video_url'] = video_url
# 2.up_id: String # up 主 ID
    movieDict['up_id'] = up_id
# 3.up_username: String # up 主用户名
    movieDict['up_username'] = up_username
# 4.video_url: # 视频链接
    movieDict['video_url'] = video_url
# 5.video_name: String # 视频名称
    movieDict['video_name'] = video_name

    # up_id_link = s.xpath('//div[@class="name"]/a/@href')[0]
    # up_username = s.xpath('//div[@class="name"]/a/text()')[0]
# 6.video_published_at: Datetime # 发布时间
    movieDict['video_published_at'] = video_published_at
# 7.video_playback_num: Integer # 视频播放量
    movieDict['video_playback_num'] = video_playback_num

# 8.video_barrage_num: Integer # 弹幕量
    movieDict['video_barrage_num'] = video_barrage_num
# 9.video_like_num: Integer # 点赞量
    movieDict['video_like_num'] = video_like_num
# 10.video_coin_num: Integer # 投币量
    movieDict['video_coin_num'] = video_coin_num
# 11.video_favorite_num: Integer # 收藏量
    movieDict['video_favorite_num'] = video_favorite_num
# 12.video_forward_num: Integer # 转发量
    movieDict['video_forward_num'] = video_forward_num
# 13.video_tag # 视频标签
    movieDict['video_tag'] = video_tag
# 14.video_length # 视频时长
    movieDict['video_length'] = video_length
# 15.created_at: Datetime # 爬取时间
    movieDict['created_at'] = created_at
# 16.up_video_num: Integer # Up 主总视频数
    movieDict['up_video_num'] = up_video_num
# 17.up_follow_num: Integer # Up 主总粉丝数
    movieDict['up_follow_num'] = up_follow_num
# 18.up_like_num:Integer # Up 主总获赞数
    movieDict['up_like_num'] = up_like_num
# 19.up_video_playback_num:Integer # Up 主总播放数
    movieDict['up_video_playback_num'] = up_video_playback_num

    movieList.append(movieDict)

    return movieList


# 第四步 下载目标网页数据
# 1.video_url: String # 视频地址
# 2.up_id: String # up 主 ID
# 3.up_username: String # up 主用户名
# 4.video_url: # 视频链接
# 5.video_name: String # 视频名称
# 6.video_published_at: Datetime # 发布时间
# 7.video_playback_num: Integer # 视频播放量
# 8.video_barrage_num: Integer # 弹幕量
# 9.video_like_num: Integer # 点赞量
# 10.video_coin_num: Integer # 投币量
# 11.video_favorite_num: Integer # 收藏量
# 12.video_forward_num: Integer # 转发量
# 13.video_tag # 视频标签
# 14.video_length # 视频时长
# 15.created_at: Datetime # 爬取时间
# 16.up_video_num: Integer # Up 主总视频数
# 17.up_follow_num: Integer # Up 主总粉丝数
# 18.video_length # Up 主总获赞数
# 19.created_at: Datetime # Up 主总播放数


###将数据写入mongo数据库
# def write_to_mongo(movieList):
#     # 连接数据库
#     client = pymongo.MongoClient('localhost',27017)
#     bili_db = client['bili_db']
#     bili_table = bili_db['bili_table']
#     for each in movieList:
#         bili_table.insert_one(each)

def writeData(movieList):
    with open('BiLiBili.csv','w',encoding='UTF-8-sig',newline='')as ft:
        writer = csv.DictWriter(ft,fieldnames=['video_url','up_id','up_username','video_url','video_name',
                                              'video_published_at','video_playback_num',
                                              'video_barrage_num','video_like_num','video_coin_num','video_favorite_num',
                                              'video_forward_num','video_tag','video_length' ,
                                              'created_at','up_video_num','up_follow_num','up_like_num','up_video_playback_num'])
        writer.writeheader() #写入表头

        #传入的这个参数 是一个列表，每个元素代表每行数据
        for each in movieList:
            writer.writerow(each)




if __name__ =='__main__':
    while True:
        now = datetime.datetime.now()
        # print(now.hour, now.minute)
        if now.hour == 1 and now.minute == 0:
            movieList=[]
            i = 1
            with open("bili.txt") as file:
                for biliUrl in file:
                    biliUrl = biliUrl.strip('\n')
                    movieList += getSource(biliUrl)
                    print(str(i) + '-200')
                    i += 1
                # print(movieList[:10])
                writeData(movieList)
                print('excel打印完毕')
                time.sleep(30)
        # 每隔60秒检测一次
        time.sleep(60)
###安装并配置mongo数据库后可以将数据存储到mongo数据库
        # write_to_mongo(movieList)
        # print('mongo数据库存储完毕')

    # //movieList += getEveryItem(source)



