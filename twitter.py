
#1.从twitter获取观看大于10W的 点赞大于1K的推文 2.判断是否是说工具类的 AI类的信息




import time
import requests


#在不同时间段测试发布内容，找到最佳发布时间
# 发布的文章不要说是自己 而是说有人 

#抓取提及AI 工具类的推文
def get_ai_tools_tweets():
    key_worlds = ["AI","AI工具","AI工具类","AI工具类推荐","AI工具类分享","AI工具类推荐","AI工具类分享"]


def get_all_mentions_tweets(query,max_count=20,queryType='Latest'):
    all_tweets = []
    cursor = None
    
    while True:
        try:
            response = get_latest_tweets(query, cursor=cursor,queryType=queryType)
            
            # 解析返回的数据
            data = response.get('data', {}).get('search_by_raw_query', {}).get('search_timeline', {}).get('timeline', {})
            instructions = data.get('instructions', [])
            
            entries = []
            cursor = None
            # 查找 TimelineAddEntries 指令

            # instructions 中没有一个instruction的__typename是TimelineAddEntries,那么说明没有数据了
            has_TimelineAddEntries_in_instructions = False
            for instruction in instructions:
                if instruction.get('__typename') == 'TimelineAddEntries':
                    entries = instruction.get('entries', [])
                    
                    # 提取推文数据
                    for entry in entries:
                        if entry.get('content', {}).get('__typename') == 'TimelineTimelineItem':
                            has_TimelineAddEntries_in_instructions = True
                            tweet_data = entry.get('content', {}).get('content', {}).get('tweet_results', {}).get('result', {})
                            if tweet_data:
                                if tweet_data.get('__typename')=='TweetWithVisibilityResults':
                                    tweet_data = tweet_data.get('tweet',None)
                                    if tweet_data:
                                        # 手动添加这个字段 保持一致 防止后面处理的时候有问题
                                        tweet_data['__typename'] = 'Tweet'  
                                        all_tweets.append(tweet_data)
                                elif tweet_data.get('__typename')=='Tweet':
                                    all_tweets.append(tweet_data)
                                else:
                                    # TODO 这里需要打印出来 看看是什么类型 
                                    print(f"unknown type: {tweet_data.get('__typename')}")

                        #下一页的key ,当第一页查询的时候Cursor在这里..  
                        if entry.get('content', {}).get('__typename') == 'TimelineTimelineCursor':
                            if entry.get('content', {}).get('cursor_type') == 'Bottom':
                                cursor = entry.get('content', {}).get('value',None)              

                #不是第一页的话 分页在这里                
                if instruction.get('__typename') == 'TimelineReplaceEntry':
                    if instruction.get('entry',{}).get('content',{}).get('cursor_type','') == 'Bottom':
                        cursor = instruction.get('entry',{}).get('content',{}).get('value','')

            
            # 检查是否有下一页
            print("begin check next page")
            
            
            if not has_TimelineAddEntries_in_instructions:
                print("last page. there isn't data.")
                break

            
            # 如果没有下一页，退出循环.这个方法应该到不了 光标永远有值
            if not cursor or len(cursor) ==0 :
                break
            
            if len(all_tweets)>=max_count:
                print("reach the max count.")
                break

            # 添加延迟以避免超过 API 限制
            time.sleep(0.5)
        
        except Exception as e:
            print(f"Error occurred: {e}")
            break
    
    return all_tweets

# 获取最新的20条数据
def get_latest_tweets(query,cursor=None,queryType='Latest'):    
    url = "https://twitter283.p.rapidapi.com/Search"

    if cursor:
        querystring = {"q":f"{query}","type":f"{queryType}","count":20,"cursor":f"{cursor}"}
    else:
        querystring = {"q":f"{query}","type":f"{queryType}","count":20}

    headers = {
        "x-rapidapi-host": "twitter283.p.rapidapi.com",
        "x-rapidapi-key": "7721d9c00fmsh4b30137fffdb1cfp129cb1jsne1de6b3c88cb"
    }

    MAX_RETRIES = 3
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            break   
        except Exception as e:
            logger.error(f"Error occurred: {e},will try again {attempt+1} of {MAX_RETRIES}")
            time.sleep(1)
            #如果最后一次还失败 打印日志
            if attempt == MAX_RETRIES - 1:
                logger.error(f"Error occurred: {e},调用rapidApi接口 最后一次还失败")

    print(response.text)
    return response.json() 
