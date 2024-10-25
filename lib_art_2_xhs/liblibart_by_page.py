import time
import requests
import json

# 使用页面生成图片
#curl 'https://www.liblib.art/gateway/sd-api/generate/image' \
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
#   --data-raw $'{"checkpointId":2295774,"generateType":21,"frontCustomerReq":{"frontId":"8921d0c9-bda1-4af6-95bc-efa111b8f747","windowId":"","tabType":"txt2img","conAndSegAndGen":"gen"},"text2img":{"prompt":"oval face shape,golden ratio proportions,small V-shaped chin,graceful jawline,symmetrical face structure,(face width-to-height ratio 1:1.5),soft facial contours,(phoenix eyes:1.3),upturned outer corners,double eyelids with moderate crease,bright clear eyes,slightly almond-shaped,eye spacing exactly one eye width apart,long natural lashes,slightly hooded upper eyelids,dark rich iris color,lustrous eye expression,(eye ratio width-to-height 1:0.45),(straight bridge nose:1.2),refined nose tip,moderate nose height,subtle nose wings,ideal nose-to-lip ratio,nose bridge height matching inner eye corners,natural nose contour,perfect nose projection,(curved Cupid\'s bow:1.3),full upper lip with defined peaks,slightly fuller lower lip,natural pink tone,mouth corners slightly upturned,lip ratio upper-to-lower 1:1.2,moderate lip width proportional to nose width,(curved delicate eyebrows:1.4),natural arch position at outer third,tapering ends,moderate thickness,clean defined shape,ideal distance from eyes,soft brown color,(porcelain smooth skin:1.3),natural rosy undertone,ethereal glow,translucent complexion,fine pores,jade-like luster,youthful moisture,even skin texture,perfect thirds face division,balanced facial features,golden ratio facial proportions (1.618:1),harmonious feature spacing,ideal philtrum length,graceful facial angles,feminine softness,goddess aura,elegant demeanor,gentle expression,ethereal beauty,oriental beauty standards,celestial features,timeless grace,(professional black business attire:1.3),high-end tailored black blazer,slim fit design,elegant black pencil skirt knee length,silk blouse,sophisticated office look,high quality fabric texture,natural pose,professional photography,fashion magazine style,soft studio lighting,minimalist background,vintage luxury style,gentle feminine demeanor,business elite,executive level,urban fashion,quiet elegance,graceful posture,confident aura,delicate silver jewelry,designer watch,simple pearl,","negativePrompt":"(worst quality, low quality:1.4),bad anatomy,bad hands,text,error,missing fingers,extra digit,fewer digits,cropped,jpeg artifacts,signature,watermark,username,blurry,bad feet,poorly drawn face,distorted face,mutation,deformed face,extra limbs,extra face,extra breasts,(cross-eyed),disfigured,gross proportions,malformed limbs,missing arms,missing legs,extra arms,extra legs,mutated hands,fused fingers,too many fingers,long neck,","extraNetwork":"","samplingMethod":1,"samplingStep":20,"width":1024,"height":1024,"imgCount":1,"cfgScale":3.5,"seed":-1,"seedExtra":0,"clipSkip":2,"randnSource":0,"restoreFaces":0,"hiResFix":0,"tiling":0},"additionalNetwork":[{"modelId":2608725,"type":0,"weight":0.8,"modelName":"Flux_小红书真实风格丨日常照片丨极致逼真","modelVersionName":"V1","url":"https://liblibai-online.liblib.cloud/img/1ce9c67df11178bb289ce47624e4824e/dd95a9d8a54271c8b745b6435d169593ba706e19d136e35e2f2053ae3a5268a1.png?x-oss-process=image%2Fresize%2Cm_lfit%2Cw_40%2Ch_40"}],"taskQueuePriority":1}'

# 将上面的curl 转换为python代码 只保留prompt和negativePrompt作为入参

# 贵林秘钥 上面那个curl是在https://www.liblib.art/modelinfo/d9675e37370e493ab8bf52046827a2b0?from=search&versionUuid=7852ee527ca34d8b940d0749a75e4b67 
# 点在线生图后 抓取的http请求 
def generate_image(prompt, negative_prompt):
    url = 'https://www.liblib.art/gateway/sd-api/generate/image'
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.liblib.art',
        'referer': 'https://www.liblib.art/v4/editor',
        'token': '578eb380d1b94e8fbb7a5df92527be10',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    
    data = {
        "checkpointId": 2295774,
        "generateType": 21,
        "frontCustomerReq": {
            "frontId": "8921d0c9-bda1-4af6-95bc-efa111b8f747",
            "windowId": "",
            "tabType": "txt2img",
            "conAndSegAndGen": "gen"
        },
        "text2img": {
            "prompt": prompt,
            "negativePrompt": negative_prompt,
            "samplingMethod": 1,
            "samplingStep": 20,
            "width": 1024,
            "height": 1024,
            "imgCount": 1,
            "cfgScale": 3.5,
            "seed": -1,
            "seedExtra": 0,
            "clipSkip": 2,
            "randnSource": 0,
            "restoreFaces": 0,
            "hiResFix": 0,
            "tiling": 0
        },
        "additionalNetwork": [
            {
                "modelId": 2608725,
                "type": 0,
                "weight": 0.8,
                "modelName": "Flux_小红书真实风格丨日常照片丨极致逼真",
                "modelVersionName": "V1",
                "url": "https://liblibai-online.liblib.cloud/img/1ce9c67df11178bb289ce47624e4824e/dd95a9d8a54271c8b745b6435d169593ba706e19d136e35e2f2053ae3a5268a1.png?x-oss-process=image%2Fresize%2Cm_lfit%2Cw_40%2Ch_40"
            }
        ],
        "taskQueuePriority": 1
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
    # 返回值 {"code":0,"data":86818133,"msg":""} 
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
def check_progress(task_id):
    url = f'https://www.liblib.art/gateway/sd-api/generate/progress/msg/v3/{task_id}'
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.liblib.art',
        'referer': 'https://www.liblib.art/v4/editor',
        'token': '578eb380d1b94e8fbb7a5df92527be10',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    
    data = {
        "flag": 0
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
    return response.json()


# "images": [
#             {
#                 "id": 209795179,
#                 "previewPath": "https://liblibai-tmp-image.liblib.cloud/sd-images/cd226a901a0ce7406252c7f84ead4c35052baa9407bcd704b82b18686fc58343.png",
#                 "storagePath": "sd-images/cd226a901a0ce7406252c7f84ead4c35052baa9407bcd704b82b18686fc58343.png",
#                 "illegal": null,
#                 "isNfsw": null,
#                 "imageInfo": "oval face,golden ratio,small V-shaped chin,graceful jawline,symmetrical face,(face width-to-height 1:1.5),soft contours,(phoenix eyes:1.3),upturned corners,double eyelids,bright clear eyes,almond-shaped,eye spacing one eye width,long lashes,hooded upper lids,dark iris,lustrous expression,(eye ratio 1:0.45),(straight bridge nose:1.2),refined tip,moderate height,subtle wings,ideal nose-to-lip ratio,bridge matching inner eye corners,natural contour,perfect projection,(curved Cupid's bow:1.3),full upper lip,fuller lower lip,pink tone,upturned corners,lip ratio 1:1.2,proportional width,(curved eyebrows:1.4),arch at outer third,tapering ends,moderate thickness,clean shape,ideal distance,(porcelain skin:1.3),rosy undertone,ethereal glow,fine pores,jade-**** luster,youthful,even texture,perfect thirds division,balanced features,golden ratio (1.618:1),harmonious spacing,ideal philtrum,graceful angles,feminine softness,goddess aura,elegant demeanor,gentle expression,ethereal beauty,oriental standards,celestial features,timeless grace,Luxurious private villa poolside,minimalist chic swimwear,warm and healing mood,serene atmosphere,lush greenery surrounding pool,gentle ripples on water surface,sleek modern sun loungers,soft white towels,character reclining gracefully on lounger,legs slightly bent,one arm resting behind head,subtle arch in back,delicate necklace glinting in sunlight,soft,inviting gaze,slight smile,sun-kissed skin glowing,gentle breeze tousling hair (masterpiece:1.4),(best quality:1.3),(ultra-detailed:1.2),8k uhd,photorealistic,(soft lighting:1.2),(natural skin:1.1),(subtle makeup:1.1),(elegant pose:1.3),(alluring gaze:1.1),(Xiaohongshu style:1.3),(fashion magazine:1.2),(pure and sensual:1.4),(innocent yet alluring:1.3),(dreamy atmosphere:1.2),(shallow depth of field:1.1),(high fashion:1.2),(youthful glow:1.2),\nNegative prompt: (worst quality:1.4),(low quality:1.4),(normal quality:1.4),low resolution,jpeg artifacts,blurry,pixelated,poor quality,grainy image,unclear details,compression artifacts,oversaturated,overexposed,underexposed,washed out,(bad anatomy:1.3),(inaccurate limb:1.2),anatomical error,bad proportions,wrong anatomy,distorted body,bodypart error,improper anatomy,malformed limbs,extra limbs,missing limbs,disconnected limbs,mutation,deformed,malformed,disfigured,gross proportions,extra joints,broken joints,fused joints,bent joints,(bad hands:1.4),(wrong hands:1.3),(malformed hands:1.3),ugly hands,missing fingers,extra fingers,fused fingers,too many fingers,wrong finger placement,distorted fingers,broken fingers,extra digit,fewer digits,long fingers,short fingers,(bad face:1.4),(ugly face:1.3),(wrong face:1.3),(deformed face:1.3),distorted face,ugly eyes,wrong eyes,misaligned eyes,crossed eyes,asymmetric eyes,uneven eyes,weird eyes,strange mouth,bad mouth,crooked nose,wrong nose,bad nose structure,weird mouth,bad lips,asymmetric face,disproportionate face,uncanny valley,(cross-eyed:1.3),(crossed eyes:1.3),(misaligned eyes:1.3),uneven eyes,asymmetric eyes,different sized eyes,lazy eye,wandering eye,cockeyed,strabismus,(bad skin:1.3),(ugly skin:1.2),(weird skin:1.2),(skin issues:1.2),bad_skin_quality,rough skin,uneven skin,poor skin texture,unrealistic skin,plastic skin,overly smooth skin,(bad clothing:1.3),(deformed clothing:1.2),(wrong clothing:1.2),missing clothing,unrealistic clothing,floating clothing,poorly drawn clothing,inconsistent clothing,weird clothing folds,(bad hair:1.3),(weird hair:1.2),(wrong hair:1.2),(messy hair:1.2),unrealistic hair,floating hair,poorly drawn hair,inconsistent hair,merged hair,unnatural hair flow,bad composition,poor composition,confusing composition,cluttered composition,awkward composition,unbalanced composition,watermark,sign,,nsfw\nSteps: 37, Sampler: Euler, CFG scale: 3.5, Seed: 2214838464, Size: 768x1024, Model hash: 8cba4f1ef4, Model: F.1基础算法模型-哩布在线可运行_F.1-dev-fp8.safetensors, Denoising strength: 0, RNG: CPU, Lora 1: Flux_小红书真实风格丨日常照片丨极致逼真, Lora Hash 1: 158a4fa05a, Lora Weight 1: 0.8, vae_name: automatic",
#                 "script": null,
#                 "isScript": null,
#                 "openposeJson": null,
#                 "nodeId": null
#             }
#         ],
# 直接返回url
def generate_image_and_get_result(prompt, negative_prompt):
    task_obj = generate_image(prompt, negative_prompt)
    task_id = task_obj["data"]
    code = task_obj["code"]
    if code != 0:
        print(f"generate_image_and_get_result error,resp is :   {task_obj}")
        return None
    # 轮询检查进度 每3S检查一次 ，最多等待5分钟
    # 打印总共的耗时
    start_time = time.time()
    for i in range(100):
        print(f"check_progress {task_id} {i} 次")
        result = check_progress(task_id)
        if result['code']!=0:
            print(f"check_progress {task_id} error,resp is :   {result}")
            return None 
        if result.get("data",{}).get("percentCompleted",0) == 100:
            images = result["data"]["images"]   
            # 打印总共的耗时
            end_time = time.time()
            total_time = end_time - start_time
            print(f"generate_image_and_get_result done .总共的耗时: {total_time}秒")
            return images[0]["previewPath"]
        time.sleep(3)
    print(f"generate_image_and_get_result timeout")
    return None




if __name__ == '__main__':
    prompt = """
    oval face,golden ratio,small V-shaped chin,graceful jawline,symmetrical face,(face width-to-height 1:1.5),soft contours,(phoenix eyes:1.3),upturned corners,double eyelids,bright clear eyes,almond-shaped,eye spacing one eye width,long lashes,hooded upper lids,dark iris,lustrous expression,(eye ratio 1:0.45),(straight bridge nose:1.2),refined tip,moderate height,subtle wings,ideal nose-to-lip ratio,bridge matching inner eye corners,natural contour,perfect projection,(curved Cupid's bow:1.3),full upper lip,fuller lower lip,pink tone,upturned corners,lip ratio 1:1.2,proportional width,(curved eyebrows:1.4),arch at outer third,tapering ends,moderate thickness,clean shape,ideal distance,(porcelain skin:1.3),rosy undertone,ethereal glow,fine pores,jade-like luster,youthful,even texture,perfect thirds division,balanced features,golden ratio (1.618:1),harmonious spacing,ideal philtrum,graceful angles,feminine softness,goddess aura,elegant demeanor,gentle expression,ethereal beauty,oriental standards,celestial features,timeless grace,Luxurious private villa poolside,minimalist chic swimwear,warm and healing mood,serene atmosphere,lush greenery surrounding pool,gentle ripples on water surface,sleek modern sun loungers,soft white towels,character reclining gracefully on lounger,legs slightly bent,one arm resting behind head,subtle arch in back,delicate necklace glinting in sunlight,soft,inviting gaze,slight smile,sun-kissed skin glowing,gentle breeze tousling hair (masterpiece:1.4),(best quality:1.3),(ultra-detailed:1.2),8k uhd,photorealistic,(soft lighting:1.2),(natural skin:1.1),(subtle makeup:1.1),(elegant pose:1.3),(alluring gaze:1.1),(Xiaohongshu style:1.3),(fashion magazine:1.2),(pure and sensual:1.4),(innocent yet alluring:1.3),(dreamy atmosphere:1.2),(shallow depth of field:1.1),(high fashion:1.2),(youthful glow:1.2),
    """
    negative_prompt = """
    (worst quality:1.4),(low quality:1.4),(normal quality:1.4),low resolution,jpeg artifacts,blurry,pixelated,poor quality,grainy image,unclear details,compression artifacts,oversaturated,overexposed,underexposed,washed out,(bad anatomy:1.3),(inaccurate limb:1.2),anatomical error,bad proportions,wrong anatomy,distorted body,bodypart error,improper anatomy,malformed limbs,extra limbs,missing limbs,disconnected limbs,mutation,deformed,malformed,disfigured,gross proportions,extra joints,broken joints,fused joints,bent joints,(bad hands:1.4),(wrong hands:1.3),(malformed hands:1.3),ugly hands,missing fingers,extra fingers,fused fingers,too many fingers,wrong finger placement,distorted fingers,broken fingers,extra digit,fewer digits,long fingers,short fingers,(bad face:1.4),(ugly face:1.3),(wrong face:1.3),(deformed face:1.3),distorted face,ugly eyes,wrong eyes,misaligned eyes,crossed eyes,asymmetric eyes,uneven eyes,weird eyes,strange mouth,bad mouth,crooked nose,wrong nose,bad nose structure,weird mouth,bad lips,asymmetric face,disproportionate face,uncanny valley,(cross-eyed:1.3),(crossed eyes:1.3),(misaligned eyes:1.3),uneven eyes,asymmetric eyes,different sized eyes,lazy eye,wandering eye,cockeyed,strabismus,(bad skin:1.3),(ugly skin:1.2),(weird skin:1.2),(skin issues:1.2),bad_skin_quality,rough skin,uneven skin,poor skin texture,unrealistic skin,plastic skin,overly smooth skin,(bad clothing:1.3),(deformed clothing:1.2),(wrong clothing:1.2),missing clothing,unrealistic clothing,floating clothing,poorly drawn clothing,inconsistent clothing,weird clothing folds,(bad hair:1.3),(weird hair:1.2),(wrong hair:1.2),(messy hair:1.2),unrealistic hair,floating hair,poorly drawn hair,inconsistent hair,merged hair,unnatural hair flow,bad composition,poor composition,confusing composition,cluttered composition,awkward composition,unbalanced composition,watermark,sign,
    """

    url = generate_image_and_get_result(prompt, negative_prompt)
    print(url)
 
# print(check_progress('86884480'))
