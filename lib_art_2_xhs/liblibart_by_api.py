import base64
import datetime
from hashlib import sha1
import hmac
import time
import uuid
import requests
import json

# 使用页面生成图片
# curl --location 'https://openapi.liblibai.cloud/api/generate/webui/text2img/ultra?AccessKey=qG3h1v7b8ICXkQ63WjFzEw&Signature=zvBZ0xK7remn7mhQJza7aX5adrY&Timestamp=1729345402581&SignatureNonce=e20d676f-1ac4-47e4-b752-4087b6ee0fc8' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: acw_tc=6425a8a5-9567-4f24-96f6-4266e08a758e01ec456bf6347297933616237606bcf6' \
# --data '{
#     "templateUuid": "5d7e67009b344550bc1aa6ccbfa1d7f4",
#     "generateParams": {
        
#         "prompt": "oval face,golden ratio,small V-shaped chin,graceful jawline,symmetrical face,(face width-to-height 1:1.5),soft contours,(phoenix eyes:1.3),upturned corners,double eyelids,bright clear eyes,almond-shaped,eye spacing one eye width,long lashes,hooded upper lids,dark iris,lustrous expression,(eye ratio 1:0.45),(straight bridge nose:1.2),refined tip,moderate height,subtle wings,ideal nose-to-lip ratio,bridge matching inner eye corners,natural contour,perfect projection,(curved Cupid'\''s bow:1.3),full upper lip,fuller lower lip,pink tone,upturned corners,lip ratio 1:1.2,proportional width,(curved eyebrows:1.4),arch at outer third,tapering ends,moderate thickness,clean shape,ideal distance,(porcelain skin:1.3),rosy undertone,ethereal glow,fine pores,jade-like luster,youthful,even texture,perfect thirds division,balanced features,golden ratio (1.618:1),harmonious spacing,ideal philtrum,graceful angles,feminine softness,goddess aura,elegant demeanor,gentle expression,ethereal beauty,oriental standards,celestial features,timeless grace,Luxurious private villa poolside, minimalist chic swimwear, warm and healing mood, serene atmosphere, lush greenery surrounding pool, gentle ripples on water surface, sleek modern sun loungers, soft white towels, character reclining gracefully on lounger, legs slightly bent, one arm resting behind head, subtle arch in back, delicate necklace glinting in sunlight, soft, inviting gaze, slight smile, sun-kissed skin glowing, gentle breeze tousling hair (masterpiece:1.4), (best quality:1.3), (ultra-detailed:1.2), 8k uhd, photorealistic, (soft lighting:1.2), (natural skin:1.1), (subtle makeup:1.1), (elegant pose:1.3), (alluring gaze:1.1), (Xiaohongshu style:1.3), (fashion magazine:1.2), (pure and sensual:1.4), (innocent yet alluring:1.3), (dreamy atmosphere:1.2), (shallow depth of field:1.1), (high fashion:1.2), (youthful glow:1.2)",
#         "aspectRatio":"square",
#         "steps": 37, 
#         "width": 768, 
#         "height": 1024, 
#         "imgCount": 1,    
#         "seed": -1, 
#         "restoreFaces": 0
#     }
# }'
# 将上面的curl 转换为python代码 只保留prompt入参
def generate_image_by_oapi(prompt,steps=37,width=768,height=1024):
    timestamp,signature_nonce,sign = make_sign("/api/generate/webui/text2img/ultra")
    url = 'https://openapi.liblibai.cloud/api/generate/webui/text2img/ultra'
    
    #贵林秘钥 来自 https://www.liblib.art/apis  liblib提供的openapi 但是我简单的结论是 感觉效果一般 然后价格也比在线的贵 一般不要用 
    params = {
        'AccessKey': 'qG3h1v7b8ICXkQ63WjFzEw',
        'Signature': sign,
        'Timestamp': timestamp,
        'SignatureNonce': signature_nonce
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=6425a8a5-9567-4f24-96f6-4266e08a758e01ec456bf6347297933616237606bcf6'
    }
    
    data = {
        "templateUuid": "5d7e67009b344550bc1aa6ccbfa1d7f4",
        "generateParams": {
            "prompt": prompt,
            "aspectRatio": "square",
            "steps": steps,
            "width": width,
            "height": height,
            "imgCount": 1,
            "seed": -1,
            "restoreFaces": 0
        }
    }
    
    response = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    print(f"generate_image_by_oapi done resp is {response.json()}")
    return response.json()

# curl 'https://www.liblib.art/gateway/sd-api/generate/progress/msg/v3/86818133' \
#   -H 'accept: application/json, text/plain, */*' \
#   -H 'accept-language: zh-CN,zh;q=0.9' \
#   -H 'content-type: application/json' \
#   -H 'cookie: webid=1729317419639vlhxgoin; Hm_lvt_2f4541bcbee365f31b21f65f00e8ae8b=1729317421; HMACCOUNT=2AD1654D052541F3; AGL_USER_ID=f3321e8e-5478-40bc-90a3-337085629dd1; _ga=GA1.1.1975539900.1729317422; _bl_uid=O3m242Rmfetq4ay610yC4wRleth4; usertoken=578eb380d1b94e8fbb7a5df92527be10; Hm_lpvt_2f4541bcbee365f31b21f65f00e8ae8b=1729413914; acw_tc=0bd17c4a17294148004528275eda117c0c8f7268fe07d2f8ea84cec04b6f87; _ga_24MVZ5C982=GS1.1.1729409401.6.1.1729414853.60.0.0' \
#   -H 'origin: https://www.liblib.art' \
#   -H 'priority: u=1, i' \
#   -H 'referer: https://www.liblib.art/v4/editor' \
#   -H 'sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'token: 578eb380d1b94e8fbb7a5df92527be10' \
#   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36' \
#   --data-raw '{"flag":0}'


# 成功
# "percentCompleted": 100,
#         "timeTaken": 1,
#         "estTimeLeft": 1,
#         "images": [
#             {
#                 "id": 209712786,
#                 "previewPath": "https://liblibai-tmp-image.liblib.cloud/sd-images/251501797eb499be0407a28eaa92392e22233203adc09792ae82abddc3937c58.png",
#                 "storagePath": "sd-images/251501797eb499be0407a28eaa92392e22233203adc09792ae82abddc3937c58.png",
#                 "illegal": null,
#                 "isNfsw": null,
#                 "imageInfo": "oval face shape,golden ratio proportions,small V-shaped chin,graceful jawline,symmetrical face structure,(face width-to-height ratio 1:1.5),soft facial contours,(phoenix eyes:1.3),upturned outer corners,double eyelids with moderate crease,bright clear eyes,slightly almond-shaped,eye spacing exactly one eye width apart,long natural lashes,slightly hooded upper eyelids,dark rich iris color,lustrous eye expression,(eye ratio width-to-height 1:0.45),(straight bridge nose:1.2),refined nose tip,moderate nose height,subtle nose wings,ideal nose-to-lip ratio,nose bridge height matching inner eye corners,natural nose contour,perfect nose projection,(curved Cupid's bow:1.3),full upper lip with defined peaks,slightly fuller lower lip,natural pink tone,mouth corners slightly upturned,lip ratio upper-to-lower 1:1.2,moderate lip width proportional to nose width,(curved delicate eyebrows:1.4),natural arch position at outer third,tapering ends,moderate thickness,clean defined shape,ideal distance from eyes,soft brown color,(porcelain smooth skin:1.3),natural rosy undertone,ethereal glow,translucent complexion,fine pores,jade-**** luster,youthful moisture,even skin texture,perfect thirds face division,balanced facial features,golden ratio facial proportions (1.618:1),harmonious feature spacing,ideal philtrum length,graceful facial angles,feminine softness,goddess aura,elegant demeanor,gentle expression,ethereal beauty,oriental beauty standards,celestial features,timeless grace,(professional black business attire:1.3),high-end tailored black blazer,slim fit design,elegant black pencil skirt knee length,silk blouse,sophisticated office look,high quality fabric texture,natural pose,professional photography,fashion magazine style,soft studio lighting,minimalist background,vintage luxury style,gentle feminine demeanor,business elite,executive level,urban fashion,quiet elegance,graceful posture,confident aura,delicate silver jewelry,designer watch,simple pearl,\nNegative prompt:  ,nsfw\nSteps: 20, Sampler: Euler, CFG scale: 3.5, Seed: 3114216152, Size: 1024x1024, Model hash: 8cba4f1ef4, Model: F.1基础算法模型-哩布在线可运行_F.1-dev-fp8.safetensors, Denoising strength: 0, RNG: CPU, Lora 1: Flux_小红书真实风格丨日常照片丨极致逼真, Lora Hash 1: 158a4fa05a, Lora Weight 1: 0.8, vae_name: automatic",
#                 "script": null,
#                 "isScript": null,
#                 "openposeJson": null,
#                 "nodeId": null
#             }
#         ],


def check_generation_status_by_oapi(generate_uuid):
    timestamp,signature_nonce,sign = make_sign("/api/generate/webui/status")
    url = 'https://openapi.liblibai.cloud/api/generate/webui/status'
    
    
    params = {
        'AccessKey': 'qG3h1v7b8ICXkQ63WjFzEw',
        'Signature': sign,
        'Timestamp': timestamp,
        'SignatureNonce': signature_nonce
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "generateUuid": generate_uuid
    }
    
    response = requests.post(url, params=params, headers=headers, json=data)
    print(f"check_generation_status_by_oapi done resp is {response.json()}")
    return response.json()

# 使用示例
# result = check_progress('86818133')
# print(json.dumps(result,indent=4))    


def generate_image_and_get_result_by_oapi(prompt,steps=37,width=768,height=1024):
    result = generate_image_by_oapi(prompt,steps=steps,width=width,height=height)
    generate_uuid = result['data']['generateUuid']
    # 3秒重试一次 最多重试100次 
    for i in range(100):
        print(f"try get the result for {i} times")
        result = check_generation_status_by_oapi(generate_uuid)
        if result['data']['generateStatus'] == 5:
            return result['data']['images'][0]['imageUrl']   
        time.sleep(3)

    print(f"generate_image_and_get_result_by_oapi timeout")
    return None 


# uri 
def make_sign(uri):
    """
    生成签名
    """

    # API访问密钥
    # 哩布AI 的API访问密钥  
    secret_key = 'JdZGhe9mE84s19zgRXNIf0Mz62c5bsbx'

    # 请求API接口的uri地址
    # 当前毫秒时间戳
    timestamp = str(int(time.time() * 1000))
    # 随机字符串
    signature_nonce= str(uuid.uuid4()).replace('-','')
    # 拼接请求数据
    content = '&'.join((uri, timestamp, signature_nonce))
    
    # 生成签名
    digest = hmac.new(secret_key.encode(), content.encode(), sha1).digest()
    # 移除为了补全base64位数而填充的尾部等号
    sign = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
    return timestamp,signature_nonce,sign


# timestamp,signature_nonce,sign = make_sign("/api/generate/webui/status")
# print(timestamp,signature_nonce,sign)

# /api/generate/webui/text2img/ultra
# timestamp,signature_nonce,sign = make_sign("/api/generate/webui/text2img/ultra")
# print(timestamp,signature_nonce,sign)







if __name__ == '__main__':
    prompt = """
XS,
masterpiece:1.2),best quality,high resolution,unity 8k wallpaper,(illustration:1),perfect lighting,extremely detailed CG,finely detail,large breasts,sexy,extremely detailed,soft lighting and shadow,soft yet striking lighting,film grain:1.2,(skin pores:1.2),(detailed skin texture:1),((solo:1.5)),Detailed face,(see-through:1.1),misty,Low Key:1.1,depth of field,(big breast:1.3),
A young woman with dark hair and a Sexy top,sitting on what appears to be an armchair or sofa in her home.,
"""
    result = generate_image_and_get_result_by_oapi(prompt)
    print(result)


# result = check_generation_status_by_oapi('d1f18428b2d746faa9c4f2e3597bb9d5')
# print(json.dumps(result,indent=4))

# 使用示例
# prompt = "Your prompt here"
# negative_prompt = "Your negative prompt here"
# result = generate_image(prompt, negative_prompt)
# print(result)
