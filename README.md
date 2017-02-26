# QZone Crawler ![python](https://img.shields.io/badge/python-2.7-ff69b4.svg)
基于Scrapy的QQ空间照片/相册爬虫。

## Dependence
* `python 2.7`
* `scrapy==1.3.2`
* `qqlib==1.0.0`

## Usage
1. `git clone git@github.com:Lodour/QZone-Crawler.git`

2. `cd QZone-Crawler`

3. `virtualenv env --python=python2.7`

4. `source ./env/bin/activate`

5. `pip install scrapy==1.3.2 qqlib==1.0.0`

6. `cd qzone`

7. `scrapy crawl photo -a qq=<Your QQ> -a passwd=<Your Password> -a target=<Target QQ>`

8. 图片保存在`QZone-Crawler/qzone/downloads`文件夹内

## Hint
* API可能会失效，一般而言最近一次Commit的时候是有效的

* 项目仍在编写中，目前仅完成了爬取原创说说中的照片

* 如果非原创的说说图片也需要爬取

请将`QZone-Crawler/qzone/qzone/spiders/photo.py`中的`assert not 'rt_certified' in msg`注释掉

* 没有对`virtualenv`的配置进行测试，如有问题请自行解决

* 及时清空终端命令历史

## License
[MIT License](https://github.com/Lodour/QZone-Crawler/blob/master/LICENSE)

## Todo
- [ ] 相册爬虫
- [ ] 空间API应该放在单独的包里，以便于管理和更新
- [ ] 密码不应该在参数中明文输入
- [ ] 优化对Cookies的处理，应该自动保持而不被取消

## Update
### 2017-2-26
Initial commit
