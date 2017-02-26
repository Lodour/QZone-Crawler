# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from qzone import api


class QzoneSpiderMiddleware(object):
    """ 处理QQ空间登录相关问题 """

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_start_requests(self, start_requests, spider):
        """ 将获取的cookies合并到request上 """
        for r in start_requests:
            yield r.replace(cookies=spider.qz_cookies)

    def spider_opened(self, spider):
        """ 爬虫启动时 登录并获取cookies与相关参数 """
        spider.logger.info('Spider opened: %s' % spider.name)
        spider.logger.info('尝试登录 {qq}'.format(qq=spider.qq))
        cookies, g_tk = api.login(spider.qq, spider.passwd, spider.logger)
        setattr(spider, 'qz_cookies', cookies)
        setattr(spider, 'g_tk', g_tk)


class QzoneEntryMiddleware(object):
    """ 处理QQ空间 补充接口参数/提取json数据 的问题 """

    # 待添加的参数
    fields = ('qq', 'target', 'g_tk')

    def process_request(self, request, spider):
        """ 为访问的url添加完整的参数 """
        kwargs = {k: getattr(spider, k) for k in self.fields}
        added, url = api.add_arguments(request.url, **kwargs)
        return added and request.replace(url=url) or None

    def process_response(self, request, response, spider):
        """ 从获得的返回数据中 提取出json部分(如果有) """
        text = response.body
        return response.replace(body=api.parse_json(text))
