# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VivospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    # 关键字
    keyword = scrapy.Field()
    # APP名称
    title_zh = scrapy.Field()
    # APP功能描述
    remark = scrapy.Field()
    # APP更新时间
    patchs = scrapy.Field()
    # APP开发者
    developer = scrapy.Field()
    # APP下载量
    download_count = scrapy.Field()
    # APP图片地址
    icon_url = scrapy.Field()
    # APP详情页链接
    detail_page = scrapy.Field()
    # APP种类
    category = scrapy.Field()
    # APP大小,需要换算成M
    size = scrapy.Field()
    # APP版本号,需要拼接v
    version_name = scrapy.Field()
    # APP评分
    score = scrapy.Field()
    # APP评论数
    commentCount = scrapy.Field()



