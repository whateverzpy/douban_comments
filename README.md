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

2. 运行爬虫

```bash
scrapy crawl comments
```

3. 爬取结果将保存在 `comments.json` 文件中。

## 注意事项

- 爬取数据请遵守豆瓣相关政策，仅供学习和研究使用。
- ~~用了几次就被封 ip 了~~

## TODO

- 我们需要更强有力的反反爬虫机制