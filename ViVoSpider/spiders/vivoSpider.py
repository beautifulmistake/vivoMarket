import json
from urllib import parse

import redis
import scrapy
from scrapy_redis.spiders import RedisSpider

from ViVoSpider.items import VivospiderItem

"""
ViVo手机应用应用商城数据采集
使用夜神模拟器模拟安卓系统
使用Fiddler抓取请求包
"""

default_value = "null"  # 设置全局的变量，默认值设定
# 定义自己的爬虫
class ViVoRedisSpider(RedisSpider):
    name = "ViVoSpider"     # 为爬虫命名
    redis_key = "ViVoSpider:start_urls"     # 启动爬虫的命令
    def __init__(self):
        """
        初始化方法，初始url,数据库的连接
        """
        # 与获取的关键字构造出请求，动态的修改关键字和ajax加载的页号
        self.base_url = 'https://search.appstore.vivo.com.cn/port/packages/?app_version=1527&key={0}&page_index={1}'
        # 获取与数据库的连接
        self.conn = redis.Redis(host='127.0.0.1',port=6379,db=5, password='pengfeiQDS')
    def start_requests(self):
        """
        获取数据库中的关键字构造出初始请求
        :return: Request
        """
        keyword_total = self.conn.dbsize()  # 获取数据库的关键字总数
        # 遍历获取每一个关键字
        # 测试时使用代码
        for index in range(420001,540001):
        #for index in range(keyword_total):
            keyword = self.conn.get(str(index)).decode('utf-8')     # 获取关键字
            # 构造初始请求
            target_url = self.base_url.format(parse.quote(keyword),str(1))
            print("查看获取的url：",target_url)
            # 将初始请求加入请求队列
            yield scrapy.Request(url=target_url, callback=self.get_page, meta={'keyword': keyword})
    def get_page(self,response):
        """
        获取响应，解析json,从中获取目标数据
        value的值决定是否有匹配的结果，如果没有将关键字写入无匹配结果的文件中
        maxPage的值为页号，即代表的动态加载总次数
        pageNo的值代表当前的页号

        totalCount的值代表搜索总数，也可做为判断是否有搜索结果的依据
        :param response:
        :return:
        """
        # 判断状态码
        if response.status == 200:
            # 获取当前关键字
            keyword = response.meta['keyword']
            # print("查看当前获取的响应==============================：", response.text)
            json_result = json.loads(response.text)
            print("查看转换后的数据：", json_result)
            # 最大页号,用于判断是否发起爹日次请求
            maxPage = json_result.get('maxPage')
            print("查看获取的最大页号：", maxPage)
            # 当前页号
            pageNo = json_result.get('pageNo')
            print("查看当前页号：", pageNo)
            # 搜索总数量，用于判断是否有搜索结果
            totalCount = json_result.get('totalCount')
            print("查看获取的搜索总件数：", totalCount)
            # 判断是否有搜索的结果
            if totalCount:
                app_list = json_result['value']  # 获取为当前页所有App的列表,而每一项又是字典的数据
                for app in app_list:
                    # 创建item对象
                    item = VivospiderItem()
                    # APP名称
                    title_zh = app.get('title_zh')
                    # APP功能描述
                    remark = app.get('remark')
                    # APP更换时间
                    patchs = app.get('patchs')
                    # APP开发者
                    developer = app.get('developer')
                    # APP下载量
                    download_count = app.get('download_count')
                    # APP图片地址
                    icon_url = app.get('icon_url')
                    # APP详情页链接，有 com.search.kdy
                    # APP种类，暂无，有一个应用属性，暂时未找到采集入口
                    # APP大小,需要换算成M
                    size = app.get('size')
                    # APP版本号,需要拼接v
                    version_name = app.get('version_name')
                    # APP评分
                    score = app.get('score')
                    # APP评论数
                    commentCount = app.get('commentCount')
                    # 判断值是否为空，为空赋默认值
                    item['keyword'] = keyword.strip()
                    item['title_zh'] = title_zh if title_zh else default_value  # APP名称
                    item['remark'] = "".join((remark.split())) if remark else default_value  # APP描述
                    item['patchs'] = patchs if patchs else default_value    # APP上线时间
                    item['developer'] = developer if developer else default_value   # APP开发者
                    item['download_count'] = download_count if download_count else default_value    # APP下载量
                    item['icon_url'] = icon_url if icon_url else default_value  # APP图片
                    item['detail_page'] = default_value  # APP详情页链接，为手机app,故未采集
                    item['category'] = default_value    # APP种类
                    item['size'] = '%.2f' % (size / 1024) + "M" if size else default_value  # APP大小
                    item['version_name'] = version_name if version_name else default_value  # APP版本号
                    item['score'] = score if score else default_value   # APP 评分
                    item['commentCount'] = commentCount if commentCount else default_value  # APP评论数
                    yield item
            else:
                # 将关键字写入无匹配结果的文件之中
                with open('./无匹配结果.txt', 'a+', encoding='utf-8') as f:
                    f.write(keyword)
            # 判断总页数,如果大于1,代表还有下一页的请求
            if maxPage > 1 and pageNo < maxPage:
                    yield scrapy.Request(url=self.base_url.format(parse.quote(keyword), str(pageNo+1)), callback=self.get_page, meta={'keyword': keyword})

