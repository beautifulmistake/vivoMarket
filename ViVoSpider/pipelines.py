# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ViVoSpider.utils import get_db
mongo_db = get_db()



class VivospiderPipeline(object):
    def open_spider(self,spider):
        """
        在当前目录下创建文件，记录采集的数据
        :param spider:
        :return:
        """
        self.file = open('./ViVo应用商城数据.txt', 'a+', encoding='utf-8')
    def process_item(self, item, spider):
        # 关键字
        keyword = item['keyword']
        print("查看关键字=============================：", keyword)
        # APP名称
        title_zh = item['title_zh']
        print("查看APP名称============================：", title_zh)
        # APP 描述
        app_desc = item['remark']
        print("查看APP描述============================：", app_desc)
        # APP更新时间
        patchs = item['patchs']
        print("查看APP更新时间========================：", patchs)
        # APP开发者
        developer = item['developer']
        print("查看APP开发者==========================：", developer)
        # APP下载量
        download_count = item['download_count']
        print("查看APP下载量==========================：", type(download_count))
        # APP图片地址
        icon_url = item['icon_url']
        print("查看APP图片地址========================：", icon_url)
        # APP详情页谅解，无
        detail_page = item['detail_page']
        print("查看APP详情页==========================：", detail_page)
        category = item['category']
        print("查看APP种类============================：", category)
        # APP大小,需要换算成M
        size = item['size']
        print("查看APP大小============================：", type(size))
        # APP版本号,需要拼接v
        version_name = item['version_name']
        print("查看APP版本号==========================：", version_name)
        # APP评分
        score = item['score']
        print("查看APP评分============================：", type(score))
        # APP评论数
        commentCount = item['commentCount']
        print("查看APP评论数==========================：", commentCount)
        # 将目标字段做拼接
        result_content = ""
        result_content = result_content.join(
            keyword + "ÿ" + title_zh + "ÿ" + app_desc + "ÿ" + patchs + "ÿ" + developer + "ÿ" + str(download_count) + "ÿ"
            + icon_url + "ÿ" + detail_page + "ÿ" + category + "ÿ" + str(size) + "ÿ" + version_name + "ÿ" +
            str(score) + "ÿ" + str(commentCount) + "ÿ" + "\n"
        )
        # 将采集的数据写入文件
        self.file.write(result_content)
        self.file.flush()
        return item
    def close_spider(self,spider):
        """
        将采集的数据写入文件完成后，关闭文件
        :param spider:
        :return:
        """
        # 关闭文件
        self.file.close()


# 以下代码是存储到 mongodb时需要的代码
class ResultMongoPipeline(object):
    """抓取结果导入 mongo"""

    def __init__(self, settings):
        self.collections_name = settings.get('RESULT_COLLECTIONS_NAME')

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_item(self, item, spider):
        mongo_db[self.collections_name].insert(item)
        return item

