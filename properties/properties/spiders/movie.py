# -*- coding: utf-8 -*-
import scrapy
# 导入item类
from properties.items import MovieItem


class MovieSpider(scrapy.Spider):
    # 爬虫名
    name = 'movie'
    # 爬虫爬取的域
    allowed_domains = ['www.dy2018.com']
    # 爬取页面链接
    start_urls = ['https://www.dy2018.com/4/']

    # 解析函数
    def parse(self, response):
        # 定义一个列表存放items
        items = []
        # 取全部标题，转化为列表
        title = response.xpath('//table//b/a[2]/text()').extract()
        # 取全部上传时间，转化为列表
        release_date = response.xpath('//table//font[1]/text()').extract()
        # 取全部详情页的链接
        url = response.xpath('//table//b/a[2]/@href').extract()

        # 遍历列表，将结果存入items
        for i in range(0, len(title)):
            # 实例化一个item类，然后将结果全部存入items
            item = MovieItem()
            item['title'] = title[i]
            item['release_date'] = release_date[i]
            # 拼接URL，获取所有电影详情的URL，拼成完整的URL来访问地址
            item['url'] = 'https://www.dy2018.com' + url[i]

            items.append(item)
        # 如果parse函数没有解析完成，可以将结果存为字典春给meta变量，交给parse_download_link继续解析
        for item in items:
            yield scrapy.Request(url=item['url'], meta={'meta': item}, callback=self.parse_download_link)
        # 这个是下一页跟进，从第二页开始，因为第一页我们已经爬过了。
        next_urls = response.xpath('//select[@name="select"]/option/@value').extract()[1:]
        for next_url in next_urls: #for next_url in response.xpath('//..../@href'): for a in response.xpath('li.next a'):
            yield response.follow(next_url, callback=self.parse)

    # 这个函数进入详情页获取下载地址
    def parse_download_link(self, response):
        # 先获取parse函数解析的结果
        item = response.meta['meta']
        # 取到下载链接，实际上这里有两个
        item['download_link'] = response.xpath('//td[@style="WORD-WRAP: break-word"]//a/@href').extract()[0]
        # # 有些电影是没有下载地址的，所以要判断一下，有的才继续下一步。
        # if len(download_link) is not None:
        #     # 首先获取到FTP的地址
        #     item['download_link'] = download_link[0]
        #     # 有些是没有迅雷下载地址的，所以要判断一下，没有thunder_download_link就为空，不然会报错。
        #     if len(download_link) == 2:
        #         item['thunder_download_link'] = download_link[1]
        #     else:
        #         item['thunder_download_link'] = ''
        # # 现在我们已经拿到全部数据了，可以把item返回了。
        yield item
