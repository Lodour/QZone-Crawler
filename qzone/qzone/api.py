# coding=utf-8
""" QZone API """
import urllib
from time import time
from random import randint

import qqlib
from qqlib import qzone

MaxPageSize = 40


def login(qq, passwd, logger=None):
    """ 登录QQ空间 返回Cookies及API相关参数
    Args:
        qq: 登录的QQ号
        passwd: QQ密码
        logger: 用于输出日志，不指定则无输出

    Returns:
        cookies: dict - 登陆后的Cookies
        g_tk: int - API要用到的参数

    Raises:
        qqlib.NeedVerifyCode: 需要验证码
    """
    qzObj = qzone.QZone(qq, passwd)

    try:
        qzObj.login()
    except qqlib.NeedVerifyCode:
        logger and logger.warning('登录失败，重试中...')
        return login(qq, passwd, logger)

    logger and logger.info('登录成功: %s' % qzObj.nick)
    cookies = qzObj.session.cookies.get_dict()
    g_tk = qzObj.g_tk()
    return cookies, g_tk


def add_arguments(url, qq, target, g_tk):
    """ 对url进行参数补充
    注意: 每次都补充所有可能的参数 多余的参数被自动忽略
    注意: scrapy.Request会将url编码，需要解码后再格式化

    Args:
        url: 待补充参数的url
        qq: 登录QQ号
        target: 目标QQ号
        g_tk: 登录后获得的参数

    Returns:
        added: 是否补充了新的参数
        url: 补充了参数的url
    """
    params = {
        'qq': qq,
        'g_tk': g_tk,
        'target': target
    }
    new_url = urllib.unquote(url).format(**params)
    return url != new_url, new_url


def parse_json(text):
    """ 从返回数据中提取出json部分(如果有)
    Args:
        text: 待处理的数据

    Returns:
        text: 处理后的数据
    """
    return text.lstrip('_Callback(').rstrip(');')


def url_msglist(pos=0, num=MaxPageSize):
    """ 获取说说列表的API地址
    Args:
        pos: 获取从最近第几条开始的说说，默认为0
        num: 获取说说条数，默认为40
             2017.2.23 - 测试显示num大于40时，仅返回10条

    Returns:
        url: 添加了基本参数的url
    """
    u = ('https://h5.qzone.qq.com/proxy/domain/taotao.qq.com'
         '/cgi-bin/emotion_cgi_msglist_v6?uin={target}&ftype'
         '=0&sort=0&pos={pos}&num={num}&replynum=100&g_tk={g_tk}'
         '&callback=&code_version=1&format=jsonp&need_privat'
         'e_comment=1')
    return u.format(pos=pos, num=num, target='{target}', g_tk='{g_tk}')


def url_photolist(tid, pid):
    """ 获取说说图片列表的API地址
    Args:
        tid: 说说的topic_id
        pid: 说说内任一图片的id

    Returns:
        url: 添加了基本参数的url   
    """
    u = ('https://h5.qzone.qq.com/proxy/domain/plist.photo.qq.com'
         '/fcgi-bin/cgi_floatview_photo_list_v2?g_tk={g_tk}&callb'
         'ack=&t={rand}&topicId={target}_{tid}_1&picKey={pid}&sho'
         'otTime=&cmtOrder=1&fupdate=1&plat=qzone&source=qzone&cm'
         'tNum=10&likeNum=5&inCharset=utf-8&outCharset=utf-8&call'
         'backFun=&offset=0&number=40&uin={qq}&appid=311&isFirst='
         '1&hostUin={target}&need_private_comment=1&_={timestamp}')
    return u.format(g_tk='{g_tk}', target='{target}',
                    tid=tid, pid=pid, qq='{qq}',
                    rand=randint(10**9, 10**10 - 1),
                    timestamp=int(round(time() * 1000)))
