# -*- coding: utf-8 -*-
import json

import scrapy
import getpass

from qzone.items import PhotoItem
from qzone import api


class PhotoSpider(scrapy.Spider):
    name = "photo"
    allowed_domains = ["qzone.qq.com"]

    def __init__(self, *args, **kwargs):
        if not kwargs.get('qq'):
            self.qq = raw_input('Your QQ Number: ')
        self.passwd = getpass.getpass('Your QQ Password: ')
        if not kwargs.get('target'):
            self.target = raw_input('Target QQ Number: ')
        super(PhotoSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = api.url_msglist()
        yield scrapy.Request(url, self.parse_msglist, meta={'pos': 0})

    def parse_msglist(self, response):
        """ 解析说说列表 """
        data = json.loads(response.body)
        msglist = data.get('msglist', None)
        if msglist is None:
            self.logger.info('没有更多说说了')
            return

        # 请求下一页列表
        pos = response.meta['pos'] + api.MaxPageSize
        url = api.url_msglist(pos)
        yield scrapy.Request(url, self.parse_msglist, meta={'pos': pos})

        # 请求图片列表
        for msg in msglist:
            try:  # 非转发 and 有图片
                assert not 'rt_certified' in msg
                tid, pic_id = msg['tid'], msg['pic'][0]['pic_id']
            except (AssertionError, KeyError, TypeError, IndexError):
                continue
            url = api.url_photolist(tid, pic_id)
            # 2017.2.26 - 这里的Cookies会因为response而丢失，因而需要主动赋值
            #             暂时没有找到比较优雅的解决方案
            yield scrapy.Request(url, self.parse_photolist,
                                 meta={'tid': tid}, cookies=self.qz_cookies)

    def parse_photolist(self, response):
        """ 解析说说图片列表 """
        data = json.loads(response.body)
        if 'data' in data and data['data'].get('photos'):
            tid = response.meta['tid']
            urls = [p['url'] for p in data['data']['photos']]
            yield PhotoItem(owner=self.target, tid=tid, image_urls=urls)
        else:
            err_msg = data.get('message', data)
            self.logger.warning('解析说说图片列表失败: {}'.format(err_msg))
