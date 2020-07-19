# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    # 电影标题
    title = scrapy.Field()
    # 上传时间
    release_date = scrapy.Field()
    # 电影详情页
    url = scrapy.Field()
    # 电影下载链接FTP
    download_link = scrapy.Field()
    # 迅雷下载链接
    # thunder_download_link = scrapy.Field()

