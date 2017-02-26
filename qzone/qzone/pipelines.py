# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class PhotoPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        """ 添加存储路径 """
        for i, image_url in enumerate(item['image_urls']):
            qq, tid = item['owner'], item['tid']
            path = '/{qq}/{tid}_{i}.jpg'.format(qq=qq, tid=tid, i=i + 1)
            yield scrapy.Request(image_url, meta={'path': path})

    def file_path(self, request, response=None, info=None):
        path = super(PhotoPipeline, self).file_path(request, response, info)
        return request.meta.get('path') or path
