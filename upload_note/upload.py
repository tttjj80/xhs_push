import json
from datetime import datetime
from http import cookies
import shutil

import requests
from xhs import XhsClient

from config import config_settings
from lib_art_2_xhs.gen_xhs_note import gen_xhs_note
from utils.logging_util import logger


def beauty_print(data: dict):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def sign(uri, data=None, a1="", web_session=""):
    """
    签名函数
    :param uri:
    :param data:
    :param a1:
    :param web_session:
    :return:
    """
    # 填写自己的 flask 签名服务端口地址
    res = requests.post(config_settings.url_sign_sign,
                        json={"uri": uri, "data": data, "a1": a1, "web_session": web_session})
    signs = res.json()
    return {
        "x-s": signs["x-s"],
        "x-t": signs["x-t"]
    }


def get_a1():
    """
    获取a1
    :return:
    """
    logger.info("获取a1")
    url_a1 = config_settings.url_sign_a1
    response = requests.get(url_a1)

    if response.status_code == 200:
        return response.json()["a1"]
    logger.error(response.text)
    raise ValueError("获取a1失败")


def get_cookies():
    """
    获取cookies
    :return:
    """
    logger.info("获取cookies")
    c = cookies.SimpleCookie()
    c.load(config_settings.cookies)

    c["a1"] = get_a1()
    str_cookies = ""
    for morsel in c.values():
        str_cookies += f"{str(morsel.key)}={str(morsel.value)};"
    return str_cookies


def upload_note():
    """
    上传笔记
    :return:
    """


    xhs_title,xhs_content,xhs_topics,image_names,post_time = gen_xhs_note()

    now = datetime.now()
    cookie = get_cookies()
    logger.info("实例化客户端")
    # 参考 https://github.com/ReaJason/xhs/
    xhs_client = XhsClient(cookie, sign=sign)

    title = xhs_title
    #最长20个字
    title = title[:19]

    logger.info("准备上传笔记")

    # with open(f"{config_settings.download_dir}/{now.strftime('%Y%m%d')}/xhs_note.txt", "r", encoding='utf-8') as f:
    #     desc = f.read()
    desc = xhs_content
    # images = [
    #     f"{config_settings.download_dir}/{now.strftime('%Y%m%d')}/TrendingProjects.png",
    # # ]
    #images = ["./tmp_image/aaa.png"]
    images = image_names

    topics = None
    if xhs_topics is not None and len(xhs_topics) > 0:
        topics = []
        for topic_keyword in xhs_topics:
            try:        
                _topics = xhs_client.get_suggest_topic(topic_keyword)
                if _topics and len(_topics)>0:
                    topics.append(_topics[0])
            except Exception as e:
                logger.error(f"获取话题失败 {e}")
    # topics = [    
    #     {
    #         "id": "63d293be00000000010012d0",
    #         "name": "github宝藏项目",
    #         "link": "",
    #         "type": "topic"
    #     },
    #     {
    #         "id": "5d35dd9b000000000e0088dc",
    #         "name": "Python",
    #         "link": "",
    #         "type": "topic"
    #     },
    #     {
    #         "id": "61be006c0000000001005c3f",
    #         "name": "github",
    #         "link": "",
    #         "type": "topic"
    #     }
    # ]
    #xhs_topics 最多3个
    if topics and len(topics) > 3:
        topics = topics[:3] 
    print(f"开始计划发布小红书笔记 标题是{title} 内容是{desc} 图片是{images} 发布时间是{post_time} 话题是{topics}")
    try:
        note = xhs_client.create_image_note(title, desc, images,post_time=post_time, topics=topics)
        beauty_print(note)
    except Exception as e:
        logger.error(f"上传小红书笔记失败 {e}")
        # 这里失败的话 把图片放到/tmp_image_error/文件夹下面
        for image_name in image_names:
            shutil.move(image_name, f"./tmp_image_error/{image_name}")
        return

    
    logger.info("小红书笔记上传完毕")




def upload_note_from_history(xhs_title,xhs_content,xhs_topics,image_names,post_time):
    """
    上传笔记
    :return:
    """



    now = datetime.now()
    cookie = get_cookies()
    logger.info("实例化客户端")
    xhs_client = XhsClient(cookie, sign=sign)

    title = xhs_title
    logger.info("准备上传笔记")

    # with open(f"{config_settings.download_dir}/{now.strftime('%Y%m%d')}/xhs_note.txt", "r", encoding='utf-8') as f:
    #     desc = f.read()
    desc = xhs_content
    # images = [
    #     f"{config_settings.download_dir}/{now.strftime('%Y%m%d')}/TrendingProjects.png",
    # # ]
    #images = ["./tmp_image/aaa.png"]
    images = image_names

    topics = None
    if xhs_topics is not None and len(xhs_topics) > 0:
        topics = []
        for topic_keyword in xhs_topics:
            try:        
                _topics = xhs_client.get_suggest_topic(topic_keyword)
                if _topics and len(_topics)>0:
                    topics.append(_topics[0])
            except Exception as e:
                logger.error(f"获取话题失败 {e}")
    # topics = [    
    #     {
    #         "id": "63d293be00000000010012d0",
    #         "name": "github宝藏项目",
    #         "link": "",
    #         "type": "topic"
    #     },
    #     {
    #         "id": "5d35dd9b000000000e0088dc",
    #         "name": "Python",
    #         "link": "",
    #         "type": "topic"
    #     },
    #     {
    #         "id": "61be006c0000000001005c3f",
    #         "name": "github",
    #         "link": "",
    #         "type": "topic"
    #     }
    # ]
    #xhs_topics 最多3个
    if topics and len(topics) > 3:
        topics = topics[:3] 
    print(f"开始计划发布小红书笔记 标题是{title} 内容是{desc} 图片是{images} 发布时间是{post_time} 话题是{xhs_topics}")
    note = xhs_client.create_image_note(title, desc, images,post_time=post_time, topics=topics)
    beauty_print(note)
    logger.info("上传完毕")



def test_get_suggest_topic():
    """
    上传笔记
    :return:
    """



    now = datetime.now()
    cookie = get_cookies()
    logger.info("实例化客户端")
    xhs_client = XhsClient(cookie, sign=sign)

    title = "xhs_title"
    logger.info("准备上传笔记")

    
    topic_keyword = "你们在"
    topics = xhs_client.get_suggest_topic(topic_keyword)
    beauty_print(topics)

    logger.info("上传完毕")


if __name__ == '__main__':
    test_upload_note()
