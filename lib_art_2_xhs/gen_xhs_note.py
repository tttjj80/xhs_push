
#调用liblibart_by_page.py 生成图片 保存到本地 然后调用LLM接口生成笔记
import datetime
import random
import shutil
import uuid

import requests
from lib_art_2_xhs.gen_xhs_text import generate_xhs_text
from lib_art_2_xhs.image_2_text import image_to_text
from lib_art_2_xhs.liblibart_by_api import generate_image_and_get_result_by_oapi
from lib_art_2_xhs.liblibart_by_page import generate_image_and_get_result
from lib_art_2_xhs.prompt_generator import PromptGenerator
from lib_art_2_xhs.upload_img import upload_image_by_file_path


def gen_xhs_note():

    #1.生成Prompt
    promptGenerator = PromptGenerator()
    
    # return {
    #         "positive_prompt": prompt,
    #         "metadata": {
    #             "scene": scene,
    #             "style": style,
    #             "mood": mood,
    #             "date": datetime.datetime.now().strftime("%Y-%m-%d")
    #         },
    #         "errdesc": errdesc
    #     }
    season="初秋"
    daily_prompt = promptGenerator.generate_daily_prompt(scene=None, style=None, mood=None,season=season, model="gpt-4o")

    if daily_prompt['errdesc'] is not None:
        print(f"gen_xhs_note error,generate_daily_prompt error : {daily_prompt['errdesc']}")
        return
    prompt = daily_prompt['positive_prompt']
    print(f"生成的prompt长度是: {len(prompt)} ，prompt是: {prompt} ")
    negative_prompt = promptGenerator.get_comprehensive_negative_prompt()

    #最终的prompt 由人脸描述 和 其他描述组成
    full_positive_prompt = promptGenerator.generate_face_prompt() + "," + prompt+","+promptGenerator.get_image_quality_prompt()
    
    #2.生成图片

    #2.1.调用liblibart_by_page.py 生成图片
    # 调用三次
    image_urls = []
    for i in range(6):  
        try: 
            image_url = generate_image_and_get_result(full_positive_prompt, negative_prompt)
            if image_url is not None:
                image_urls.append(image_url)
        except Exception as e:
            print(f"gen_xhs_note error,generate_image_and_get_result error : {e}")
            continue

    # 调用liblibart_by_api.py生成图片
    # 调用三次   不使用这个 有点垃圾
    # for i in range(3):
    #     try:
    #         image_url = generate_image_and_get_result_by_oapi(full_positive_prompt)
    #         if image_url is not None:
    #             image_urls.append(image_url)
    #     except Exception as e:
    #         print(f"gen_xhs_note error,generate_image_and_get_result_by_oapi error : {e}")
    #         continue

    # 如果image_urls为空 则报错
    if len(image_urls) == 0:
        print(f"gen_xhs_note error,no image_url")
        return

    #post_time
    #当前之间往后面0-6小时时间随机一个时间   
    post_time = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(0, 6*60*60))
    # yyyy-mm-dd hh:mm:ss
    post_time = post_time.strftime("%Y-%m-%d %H:%M:%S") 


    #3.生成小红书文案
    # 调用generate_xhs_text.py 生成小红书文案
    # 3.1 获取图片描述
    image_desc = get_image_desc_by_url(image_urls[0])
    xhs_content_json = generate_xhs_text(image_desc,season=season,model="gpt-4o-mini")
    #{"title":"", "content":""} 
    xhs_title = xhs_content_json["title"]
    xhs_content = xhs_content_json["content"]
    xhs_topics = xhs_content_json.get("topics",[]) 
    # 去除#
    xhs_topics = [topic.replace("#", "") for topic in xhs_topics]
   
    
    # 图片保存在/tmp_image/文件夹下面 随机生成图片名称
    image_names = []
    for image_url in image_urls:
        image_name = str(uuid.uuid4()) + ".png"
        image_path =f"./tmp_image/{image_name}"
        image_names.append(image_path)
        #下载图片
        # 根据image_url 下载图片
        download_image(image_url, image_path)

       


    return xhs_title,xhs_content,xhs_topics,image_names,post_time    

        


# 获取图片描述
def get_image_desc_by_file_path(image_file_path):
    
    image_url = upload_image_by_file_path(image_file_path)

    description = image_to_text(image_url)

    return description

def get_image_desc_by_url(image_url):
    description = image_to_text(image_url)
    return description  


def download_image(image_url, image_name):
    # 根据image_url 下载图片
    response = requests.get(image_url)
    with open(image_name, "wb") as f:
        f.write(response.content)   




if __name__ == '__main__':
    image_name = str(uuid.uuid4()) + ".png"
    image_path =f"./tmp_image/{image_name}"
    image_url = "https://liblibai-tmp-image.liblib.cloud/img/fcd0c9a99fdd421391033b3228d597bd/dbfe235f68ad1acbdf1d65421cb956dbb014bf2e085a3676056995204a4066cb.png"
    download_image(image_url, image_path)
    print(f"下载图片成功,图片名称：{image_name}")