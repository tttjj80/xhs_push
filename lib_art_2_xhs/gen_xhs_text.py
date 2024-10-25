

# 根据图片的提示 调用LLM生成小红书文案



import json
import re
from lib_art_2_xhs.gptnb import call_llm
from utils.logging_util import logger



# 返回json数据 {"title":"", "content":""}   
def generate_xhs_text(image_desc,season,model="gpt-4o") -> str:
    system_prompt = """
    """


    user_prompt = f"""
【人设】
你现在是一位深谙小红书平台调性的内容创作专家。

【背景】
你的小红书账号的人设是一个你年轻美丽的搞笑女并且有点色色的坏坏的感觉，很会勾人心魄。

【任务】
这你的任务是根据我给你的照片的描述，创作一篇具有小红书特色的笔记,包含标题、内容、话题。 

【必须要遵守的核心原则】：
1. 语气风格：避免使用\"来分享\"、\"给大家介绍\"等营销感强的表达。用随性自然的口吻，像在跟闺蜜炫耀新发现，适量使用\"啦\"、\"呢\"、\"叭\"等俏皮语气词，营造\"不经意间拍出了绝美效果\"的感觉。
2. 内容结构（严格控制在4段以内）：
    第1段：吸引开场（2-3句），以轻松活泼的语气制造惊喜感，避免说教式开场。
    第2段：重点描述（3-4句），重点介绍搭配/场景的亮点，加入实用小贴士。
    第3段：场景营造（2-3句），描述当下的氛围和感受，可加入拍摄小技巧。
    第4段：互动引导（0-2句），简短有趣的互动话题，避免过于复杂的问题。或者也可以没有，最重要不要啰嗦复杂。
3. 标题格式：主标题（核心吸引点，5-8字）| 副标题（调皮俏皮，8-12字）+ 2个emoji，确保标题简短有力，避免过度堆砌形容词。
4. emoji使用：每段最多使用2个emoji，在关键词后适当添加，避免连续使用相同emoji。
5. 标签使用：控制在6-8个，包含2-3个热门标签，包含2-3个细分标签，包含2个差异化标签。
6. 可以参考下当前的时节是{season}，可以适当添加一些季节性的元素。
请记住：内容要像是随手记录的生活瞬间，不要像精心准备的分享，重点在于制造\"我也想要\"的共鸣感，保持简洁，避免过度描述，重点突出实用性建议和小技巧。

图片描述：
{image_desc}

格式要求：
- 使用 "\\n" 来表示段落之间的换行
- JSON 必须正确格式化且有效
- 所有文本必须使用中文
- 始终保持第一人称视角，但是尽量不要使用我这个字眼，只评价客观事实
- 话题应该是一个没有 # 符号的字符串数组
格式要求：
{{
    "title": "Chinese title string", # 标题 ，需要吸引人 长度不能超过15个字 
    "content": "First-person Chinese content string with multiple paragraphs, emojis and interaction design", # 内容 ，需要包含多个段落，每个段落包含多个emoji和互动设计
    "topics": ["hashtag1", "hashtag2", "hashtag3", ...] # 话题 ，需要包含2-3个热门话题，2-3个细分话题，2个差异化话题。字符串数组类型，每一元素中不要带#。
}}

Let's think step by step.

"""
    # 调用LLM生成小红书文案
    # 重试三次
    max_retries = 3
    retry_count = 0
    while retry_count <= max_retries:
        try:    
            logger.info(f"generate_xhs_text by llm begin,system_prompt is {system_prompt},user_prompt is {user_prompt}") 
            llm_resp,err_desc =  call_llm(system_prompt, user_prompt,model=model,temperature=0.7)
            logger.info(f"generate_xhs_text by llm done,llm_resp is {llm_resp},err_desc is {err_desc}") 
            if err_desc is not None:
                print(f"generate_xhs_text error: {err_desc}")
                retry_count += 1
                continue 
            llm_resp = clean_llm_text(llm_resp)
            llm_resp = llm_resp.replace("```json\n","").replace("```","") 
            json_data = json.loads(llm_resp)
            return json_data
        except Exception as e:
            print(f"generate_xhs_text error: {e},will retry,{retry_count}/{max_retries} ")
            retry_count += 1
    return None


def clean_llm_text(text):
    # 移除控制字符,但保留换行符和空格
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    
    # 处理转义字符
    #text = text.replace('\\', '\\\\').replace('"', '\\"')
    
    return text

if __name__ == '__main__':
    image_prompt="""
    picture of one lady,IMG_2222.HEIC,reversal film photography,xhs,LTFGR,LLL,1girl black hair bottle box chair computer desk indoors leaning forward long hair mirror realistic shirt short shorts shorts signature sitting socks solo white shirt window,
"""

    llm_resp = '```json\n{\n    "title": "在清晨的茶香中沉醉",\n    "content": "此刻是凌晨的宁静时分，微微的月光透过窗帘洒在茶桌上，心中满是柔和的思绪。🌙\\n\\n今天，我选择了一套维多利亚风格的复古服饰，搭配精致的珍珠项链和薄纱手套，感觉仿佛置身于梦幻的茶会中。☕️✨\\n\\n在这优雅的茶室里，暖黄的灯光洒落，四周环绕着郁郁葱葱的植物，整个环境如同一幅精致的画卷。每一口茶都仿佛能品味到生活的细腻与温暖。🌿💖\\n\\n此刻的我，温柔而自信，微微侧目，嘴角挂着淡淡的微笑，仿佛在与这个世界分享我的小秘密。🎀\\n\\n想问问大家，夜深人静时，你们最喜欢做些什么呢？是品茶、写日记，还是沉浸在书本的世界里？🤔💭\\n\\n期待听到你们的故事！",\n    "topics": [\n        "生活方式",\n        "茶文化",\n        "复古风格",\n        "时尚搭配",\n        "女性魅力",\n        "心灵成长",\n        "优雅生活",\n        "夜深思考",\n        "时尚灵感",\n        "心情分享",\n        "温暖瞬间",\n        "美好日常"\n    ]\n}\n```'
    print(f"llm_resp is: {llm_resp}")
    llm_resp = clean_llm_text(llm_resp)

    print(f"llm_resp is: {llm_resp}")
    llm_resp = llm_resp.replace("```json\n","").replace("```","") 
    json_data = json.loads(llm_resp)
    print(json_data["title"])
    print(json_data["content"])
    print(json_data["topics"])
    #print(generate_xhs_text(image_prompt,model="gpt-4o-mini"))
    print(clean_llm_text("""
    picture of one lady,IMG_2222.HEIC,reversal film photography,xhs,LTFGR,LLL,1girl black hair bottle box chair computer desk indoors leaning forward long hair mirror realistic shirt short shorts shorts signature sitting socks solo white shirt window,
    """))