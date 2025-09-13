# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanCommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user = scrapy.Field()  # 用户名
    comment = scrapy.Field()  # 评论内容
    rating = scrapy.Field()  # 评分
    date = scrapy.Field()  # 评论日期
