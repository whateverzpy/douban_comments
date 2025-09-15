# douban_comments

记录大数据导论课的作业内容。

## 项目简介

本项目基于 Scrapy 框架，用于爬取豆瓣电影的短评数据，并将其保存为 JSON 文件。适合数据分析、文本挖掘等用途。

## 目录结构

- comments.json：爬取结果示例
- douban_comments/：Scrapy 项目主目录
    - items.py：定义爬取的数据结构
    - middlewares.py：中间件配置
    - pipelines.py：数据处理管道
    - settings.py：Scrapy 配置
    - spiders/comments.py：爬虫主文件

## 安装方法

1. 克隆项目

```bash
git clone https://github.com/yourusername/douban_comments.git
cd douban_comments
```

2. 安装依赖

```bash
pip install pipenv
pipenv install
```

## 使用方法

1. 进入虚拟环境

```bash
pipenv shell
```

2. 使用自己的账号登录豆瓣，获取 cookies，将对应项填入 `.env.example` 文件，重命名为 `.env`
3. 运行爬虫

```bash
scrapy crawl comments
```

4. 爬取结果将保存在 `comments.json` 文件中。

## 注意事项

- 爬取数据请遵守豆瓣相关政策，仅供学习和研究使用。
- ~~用了几次就被封 ip 了~~

## TODO

- 我们需要更强有力的反反爬虫机制

## 代码说明

- `items.py`：定义了爬取的电影短评数据结构（如电影名、评论内容、用户等字段）。
- `middlewares.py`：配置了请求和响应的中间件，可用于处理反爬虫、请求头等。
- `pipelines.py`：实现了数据的后续处理和保存逻辑，比如将爬取结果写入 JSON 文件。
- `settings.py`：包含 Scrapy 项目的全局配置，如并发数、请求延迟、Cookies 设置等。
- `spiders/comments.py`：爬虫的主逻辑，负责先爬取电影列表，再逐个爬取每部电影的短评。
