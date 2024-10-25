import base64
import time
import requests


def upload_image_by_url(image_url: str, max_retries: int = 3, delay: float = 1.0):
    CLIENT_API_KEY = "0203e9def964702a4ff81d0160670a66"
    url = f"https://api.imgbb.com/1/upload?key={CLIENT_API_KEY}"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data={"image": image_url})
            response.raise_for_status()  # 如果响应状态不是 200，将引发异常
            resp_json = response.json()
            print(f"upload_image resp_json is {resp_json}")
            return resp_json.get("data", {}).get("url")
        except Exception as e:
            if attempt == max_retries - 1:  # 如果是最后一次尝试
                raise  # 重新抛出异常
            print(f"尝试 {attempt + 1} 失败: {str(e)}. 正在重试...")
            time.sleep(delay)  # 在重试之前等待
    
    return None  # 如果所有尝试都失败，返回 None



def upload_image_by_file_path(image_file_path: str, max_retries: int = 3, delay: float = 1.0):
    CLIENT_API_KEY = "0203e9def964702a4ff81d0160670a66"
    url = f"https://api.imgbb.com/1/upload?key={CLIENT_API_KEY}"
    
    for attempt in range(max_retries):
        try:
            
            image_base64 = ""   
            # 将图片文件转换为base64
            with open(image_file_path, "rb") as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode("utf-8")
    
            response = requests.post(url, data={"image": image_base64})
            response.raise_for_status()  # 如果响应状态不是 200，将引发异常
            resp_json = response.json()
            print(f"upload_image resp_json is {resp_json}")
            return resp_json.get("data", {}).get("url")
        except Exception as e:
            if attempt == max_retries - 1:  # 如果是最后一次尝试
                raise  # 重新抛出异常
            print(f"尝试 {attempt + 1} 失败: {str(e)}. 正在重试...")
            time.sleep(delay)  # 在重试之前等待
    
    return None  # 如果所有尝试都失败，返回 None
    