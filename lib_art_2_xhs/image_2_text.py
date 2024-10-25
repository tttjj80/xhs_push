


import time
import requests
import json
from utils.logging_util import logger


def image_to_text(image_url):
    """
    将图片URL转换为文本描述
    
    参数:
    image_url (str): 图片的URL地址
    
    返回:
    str: 图片的文本描述
    """
    url = "https://api.coze.cn/v1/workflow/run"
    
    headers = {
        'Authorization': 'Bearer pat_oSe7G2HzDtJ7tnf82n7hXAlxVEGzqDKt3n2tDmbrnRdovdNBCniTQrRgb1yp8HIU',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'api.coze.cn',
        'Connection': 'keep-alive'
    }
    
    payload = json.dumps({
        "workflow_id": "7417891223299751970",
        "parameters": {
            "user_id": "12345",
            "user_name": "George",
            "BOT_USER_INPUT": image_url
        }
    })
    
    for i in range(3):
        try:
            # 记录耗时
            start_time = time.time()
            response = requests.post(url, headers=headers, data=payload)
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            response.raise_for_status()  # 如果请求不成功则抛出异常
            result = response.json()
            logger.info(f"请求结果: {result}")  
            
            if result['code'] == 0:
                data = json.loads(result['data'])
                if data['code'] == 0 and data['output'] and data['output'] != "":
                    logger.info(f"image_to_text 成功 耗时: {elapsed_time:.2f}秒")
                    return data['output']
            logger.info(f"image_to_text 请求未成功,正在进行第{i+1}次重试")
            
            time.sleep(5)
        except Exception as e:
            logger.error(f"image_to_text 发生错误: {e}")
            if i < 2:  # 如果不是最后一次尝试
                logger.info(f"image_to_text 正在进行第{i+1}次重试")
                time.sleep(5)
            else:
                return None
    
    return None





