哔哩哔哩视频相关信息定时爬取程序

程序运行环境
（1）python 3.6.3
（2）系统：win7
（3）IDE：pycharm
（4）安装并配置好mongo数据库


设计思路：
第一步 导入第三方库
第二步 获取目标网页和js的api接口
第三步 解析目标网页得到相关数据
第四步 下载数据到excel和mongo数据库中


操作流程：
通过运行start.bat，运行bilibili.py,程序每天凌晨1:00自动更新数据，存入excel和mongo数据库中。爬取链接信息见BiLiBili.csv文件。


ps：想要每天定时启动，最好是把程序放在linux服务器上运行，毕竟linux可以不用关机，即定时任务一直存活。

