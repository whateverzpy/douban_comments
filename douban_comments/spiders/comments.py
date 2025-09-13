import scrapy
import os
import re
from dotenv import load_dotenv
from douban_comments.items import DoubanCommentsItem, DoubanMovieItem

load_dotenv()


class CommentsSpider(scrapy.Spider):
    name = "comments"
    allowed_domains = ["movie.douban.com"]

    def __init__(self):
        self.movie_count = 0
        self.max_movies = 130  # 设置最大爬取电影数量

    def start_requests(self):
        cookies = {
            'bid': os.getenv('DOUBAN_BID'),
            'dbcl2': os.getenv('DOUBAN_DBCL2'),
            'ck': os.getenv('DOUBAN_CK')
        }

        # 从豆瓣电影Top250开始爬取电影列表
        start_url = 'https://movie.douban.com/top250'
        yield scrapy.Request(start_url,
                             cookies=cookies,
                             callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        # 解析电影列表页面
        movies = response.css('div.item')

        for movie in movies:
            # 检查是否已达到最大电影数量
            if self.movie_count >= self.max_movies:
                self.logger.info(f"已爬取{self.max_movies}部电影，停止爬取")
                return

            movie_url = movie.css('div.hd a::attr(href)').get()
            movie_name = movie.css('div.hd a span.title::text').get()

            if movie_url and movie_name:
                # 提取电影ID
                movie_id = re.search(r'/subject/(\d+)/', movie_url).group(1)

                # 增加计数器
                self.movie_count += 1
                self.logger.info(f"开始爬取第{self.movie_count}部电影: {movie_name}")

                # 构造评论页面URL
                comments_url = f'{movie_url}comments'

                yield scrapy.Request(comments_url,
                                     callback=self.parse_comments,
                                     meta={'movie_name': movie_name, 'movie_id': movie_id})

        # 只有在未达到最大数量时才继续翻页
        if self.movie_count < self.max_movies:
            next_page = response.css('span.next a::attr(href)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse_movie_list)

    def parse_comments(self, response):
        movie_name = response.meta['movie_name']
        comments = response.css("div.comment-item")

        for c in comments:
            item = DoubanCommentsItem()
            item["movie_name"] = movie_name
            item["user"] = c.css("span.comment-info a::text").get()
            item["comment"] = c.css("span.short::text").get()

            # 处理评分
            rating_class = c.css("span[class*='allstar']::attr(class)").get()
            if rating_class:
                rating = re.search(r'allstar(\d+)', rating_class)
                item["rating"] = rating.group(1) if rating else None
            else:
                item["rating"] = None

            item["date"] = c.css("span.comment-time::attr(title)").get()
            yield item

        # 处理评论翻页
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page,
                                  callback=self.parse_comments,
                                  meta={'movie_name': movie_name})
