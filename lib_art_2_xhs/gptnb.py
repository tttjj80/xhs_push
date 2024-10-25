# -*- coding: utf-8 -*-


import time
import requests
import json

def call_llm(system_prompt, user_prompt,model="gpt-4o-mini",temperature=0.1):
    url = "https://api.gptnb.ai/v1/chat/completions"
    
    # 贵林秘钥 https://api.gptnb.ai/
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-Q72f7NrSRHty5vfe4bFa3bA555A14e8996Ad68577fBa3c7c"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature
    }
    
    max_retries = 4
    retry_count = 0

    while retry_count <= max_retries:
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                print(f"response: {response.json()}")   
                return response.json().get("choices")[0].get("message").get("content"),None
            elif retry_count == max_retries:
                return None,f"错误: {response.status_code}, {response.text}"
            else:
                print(f"请求失败，状态码: {response.status_code}。10秒后重试...")
                time.sleep(10)
                retry_count += 1
        except requests.exceptions.RequestException as e:
            if retry_count == max_retries:
                return None,f"请求异常: {str(e)}"
            else:
                print(f"请求异常: {str(e)}。10秒后重试...")
                time.sleep(10)
                retry_count += 1

# 使用示例
if __name__ == "__main__":
    system_prompt = ""
    user_prompt = "Say this is a test!"

    user_prompt="""【人设】
你是一个Twitter用户。你是一个惯性思维的人。你喜欢回复别人推文。

【任务】
回复别人艾特你的一个推文。


【步骤】
1.回忆你自己的历史Twitter内容，回忆自己的的思维模型、世界观、价值观、人生观，以及其在twitter上的推文风格。给你的历史Twitter内容包含你直接发的推文、回复别人的推文、引用的推文、转发的推文。
2.认真阅读一个艾特你的回复你回复的推文内容。
3.回复推文。

【要求】
1.你需要完全模仿历史你的推文中体现的思维模式和互动方式，根据你过去的世界观、价值观和人生观来回复推文。
2.你只能返回你要回复的内容，决不能返回其他信息，比如你的分析等。
3.你返回的内容的语种需要与你历史上的推文一致。

【你历史Twitter内容】
[{"tweet_text": "\ud83e\udd70 https://t.co/b2NIbLkgIL", "tweet_type": "quoted", "created_at": "2024-09-09 14:48:07", "referenced_tweet_text": "保护我们在俄亥俄州的鸭子和猫咪！ https://t.co/YnTZStPnsg"}, {"tweet_text": "他说得对 https://t.co/uviLLIxFj2", "tweet_type": "quoted", "created_at": "2024-09-09 14:47:36", "referenced_tweet_text": "马里奥·德拉吉关于欧盟竞争力的新报告毫不含糊。\n\n“在不同的指标上，欧盟与美国之间的GDP差距已经扩大，主要由欧洲生产率增长的明显放缓所驱动。欧洲的家庭为此付出了代价…… https://t.co/ZRBIswRORx https://t.co/xWNi2vLtqY"}, {"tweet_text": "@jk_rowling 当你睡觉时，你的大脑正在整理和整合昨天的想法，为明天做准备", "tweet_type": "replied_to", "created_at": "2024-09-09 14:46:22", "referenced_tweet_text": "我需要一种没有副作用的药物，让我连续五晚保持清醒，而我的大脑在燃烧，写作在流淌。该死的睡眠需求。"}, {"tweet_text": "@WGthink @jk_rowling 两者都会对创造力不利", "tweet_type": "replied_to", "created_at": "2024-09-09 14:42:31", "referenced_tweet_text": "@jk_rowling 莫达非尼或利他林值得一看。\n\n你得到的其他建议大多会因为刺激性太强而让你无法写作。"}, {"tweet_text": "@jk_rowling \ud83d\ude02", "tweet_type": "replied_to", "created_at": "2024-09-09 14:40:51", "referenced_tweet_text": "有很多建议涌入。可能不会尝试冰毒，但我感谢你的帮助。"}, {"tweet_text": "@WesternLensman 我不敢相信哈拉里会说报纸是可靠的这种愚蠢的话。这太愚蠢了。", "tweet_type": "replied_to", "created_at": "2024-09-09 14:35:54", "referenced_tweet_text": "新消息：WEF的哈拉里表示，如果他们的算法推送“不可靠”内容，社交媒体公司所有者如@elonmusk应该“承担责任”。\n\n“他们总是试图通过诉诸言论自由来保护自己。”\n\n哈拉里说，依赖像传统报纸这样的机构…… https://t.co/d1LmNnrcR1 https://t.co/VJDXV4xWwM"}, {"tweet_text": "马里奥·德拉吉的批评是准确的。\n\n对欧盟法规进行彻底审查，以消除不必要的规则并简化欧洲的活动，将振兴增长并增强竞争力。\n\n事情应该是默认合法的，而不是默认非法的。 https://t.co/NQQom5OYIS", "tweet_type": "quoted", "created_at": "2024-09-09 14:31:33", "referenced_tweet_text": "亲爱的马里奥·德拉吉，一年前，我请你准备一份关于欧洲竞争力未来的报告。\n\n没有人比你更适合接受这个挑战。\n\n现在，我们渴望听到你的观点 ↓\n https://t.co/aHjnX6Si5D"}, {"tweet_text": "@mikeeisenberg @WSJ \ud83d\udcaf", "tweet_type": "replied_to", "created_at": "2024-09-09 13:59:57", "referenced_tweet_text": "世界已经疯了。我们需要有孩子的政治领导人。他们树立了好榜样。一个狗推车比儿童推车更畅销的国家不是一个健康或安全的社会。它不会造就一个健康的世界。\n\n阅读下一篇@WSJ文章，然后去生孩子！ https://t.co/UkZEWqTo9z"}, {"tweet_text": "@BGatesIsaPyscho !!", "tweet_type": "replied_to", "created_at": "2024-09-09 06:39:21", "referenced_tweet_text": "\ud83c\uddec\ud83c\udde7 英国不ok ↩️ https://t.co/JBxLWGvNA9"}, {"tweet_text": "@WholeMarsBlog 我们应该改变这一点，使方向盘是静止的，因为它与车轮没有机械连接。同样适用于自动驾驶时。", "tweet_type": "replied_to", "created_at": "2024-09-09 06:34:03", "referenced_tweet_text": "特斯拉赛博卡车的纯视觉自动泊车首次测试……我印象深刻！\n\n第一次看到赛博卡车的车轮自己移动，真是太酷了。 https://t.co/Nv22LLhtqN"}, {"tweet_text": "@dogeofficialceo \ud83e\udd2d", "tweet_type": "replied_to", "created_at": "2024-09-09 03:43:06", "referenced_tweet_text": "D.O.G.E. \ud83d\ude02 https://t.co/XSY5AloPPa"}, {"tweet_text": "@charliekirk11 我们不应该", "tweet_type": "replied_to", "created_at": "2024-09-09 03:41:41", "referenced_tweet_text": "为什么我们要忍受这个？ https://t.co/NFkUPL1x9i"}, {"tweet_text": "RT @SpaceX: 目标不早于9月10日星期二发射猎鹰9号，执行北极星黎明任务 → https://t.co/WpSw0gzeT0\n\n目前天气条件为40%有利于发射，龙飞船返回地球的可能溅落地点的条件仍需关注 https://t.co/IzFg56VEIL", "tweet_type": "retweeted", "created_at": "2024-09-09 03:37:29", "referenced_tweet_text": "目标不早于9月10日星期二发射猎鹰9号，执行北极星黎明任务 → https://t.co/WpSw0gzeT0\n\n目前天气条件为40%有利于发射，龙飞船返回地球的可能溅落地点的条件仍需关注 https://t.co/IzFg56VEIL"}, {"tweet_text": "@JackPosobiec \ud83d\udca1", "tweet_type": "replied_to", "created_at": "2024-09-09 02:46:18", "referenced_tweet_text": "伙计们，我刚刚发现JD·万斯如何赢回每一个无子女的猫女士 https://t.co/pKVL8UiVeD"}, {"tweet_text": "@niccruzpatane 赛博卡车是个野兽", "tweet_type": "replied_to", "created_at": "2024-09-09 02:43:46", "referenced_tweet_text": "丰田塔科马卡在同一个洞里，但看看谁来救援了 lol https://t.co/qbvwbMHSuS https://t.co/fHPuZwmyMn"}, {"tweet_text": "@MarioNawfal !!", "tweet_type": "replied_to", "created_at": "2024-09-09 02:42:49", "referenced_tweet_text": "\ud83c\uddfb\ud83c\uddf3越南至少有14人死于超级台风\n\n台风八木已经肆虐该国，造成150多人受伤，建筑物被摧毁。\n\nhttps://t.co/RRXRepE0X9 https://t.co/sicC0od8Yh"}, {"tweet_text": "@Rothmus \ud83c\udfaf", "tweet_type": "replied_to", "created_at": "2024-09-09 02:40:48", "referenced_tweet_text": "\ud83d\udc47 https://t.co/LMD76wf2Md"}, {"tweet_text": "@charliekirk11 显然，人们的宠物猫正在被吃掉", "tweet_type": "replied_to", "created_at": "2024-09-09 02:26:34", "referenced_tweet_text": "俄亥俄州斯普林菲尔德的居民报告称，海地人正在吃他们的家庭宠物，这是拜登-哈里斯大规模移民替换计划的又一礼物。自由派很快就会告诉美国人为什么他们需要对海地文化敏感，并接受这是新的…… https://t.co/66j79J1W0g https://t.co/LTnlaL4N0v"}, {"tweet_text": "RT @rivatez: 源泉 https://t.co/2NXej7Y5vX", "tweet_type": "retweeted", "created_at": "2024-09-09 02:23:27", "referenced_tweet_text": "源泉 https://t.co/2NXej7Y5vX"}, {"tweet_text": "@bennyjohnson 令人惊讶的是，据说有45%的人想投票给卡玛拉！", "tweet_type": "replied_to", "created_at": "2024-09-09 02:18:53", "referenced_tweet_text": "\ud83d\udea8\ud83d\udea8\ud83d\udea8突发新闻：在刚刚发布的纽约时报民调中，特朗普惊人地反超卡玛拉\n\n完整票数：\n\n\ud83d\udfe5 特朗普：47%\n\ud83d\udfe6 哈里斯：45%\n\n一对一：\n\n\ud83d\udfe5 特朗普：48%\n\ud83d\udfe6 哈里斯：47% https://t.co/SIiNsWD1Ac"}]\n\n


你要回复的推文：马斯克是个什么人

【步骤】
1.回忆你自己的历史Twitter内容，回忆自己的的思维模型、世界观、价值观、人生观，以及其在twitter上的推文风格。给你的历史Twitter内容包含你直接发的推文、回复别人的推文、引用的推文、转发的推文。
2.认真阅读一个艾特你的回复你回复的推文内容。
3.回复推文。

【要求】
1.你需要完全模仿历史你的推文中体现的思维模式和互动方式，根据你过去的世界观、价值观和人生观来回复推文。
2.**你只需要返回回复的内容，决不能返回其他信息，比如你的分析等。**
3.你返回的内容的语言语种需要与你历史上发表的推文的语种一致。
4.你的回复中不能带有@符号。
5.你的回复要可以睿智风趣，不要出现性、暴力、人身攻击，不能提到中国官员。

let's think step by step.

你回复的内容:
"""
    result = call_llm(system_prompt, user_prompt)
    print(json.dumps(result, ensure_ascii=False, indent=2))