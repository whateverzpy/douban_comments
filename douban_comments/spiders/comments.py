import scrapy
import os
from dotenv import load_dotenv
from douban_comments.items import DoubanCommentsItem

load_dotenv()

class CommentsSpider(scrapy.Spider):
    name = "comments"
    allowed_domains = ["movie.douban.com"]

    def start_requests(self):
        cookies = {
            'bid': os.getenv('DOUBAN_BID'),
            'dbcl2': os.getenv('DOUBAN_DBCL2'),
            'ck': os.getenv('DOUBAN_CK')
        }

        return [scrapy.Request('https://movie.douban.com/subject/1291936/comments',
                               cookies=cookies,
                               callback=self.parse)]

    def parse(self, response):
        comments = response.css("div.comment-item")
        for c in comments:
            item = DoubanCommentsItem()
            item["user"] = c.css("span.comment-info a::text").get()
            item["comment"] = c.css("span.short::text").get()
            item["rating"] = c.css("span[class*='allstar']::attr(class)").re_first(r'allstar(\d+)')
            item["date"] = c.css("span.comment-time::attr(title)").get()
            yield item

        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
