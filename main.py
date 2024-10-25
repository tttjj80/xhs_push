# daily job
import json
import time
from github_trending.get_trending import trending
from lib_art_2_xhs.image_2_text import image_to_text
from lib_art_2_xhs.upload_img import upload_image_by_file_path
from summarize_projects.pic import generate_image
from summarize_projects.summarize import get_summarize_for_all
from upload_note.upload import test_get_suggest_topic, upload_note, upload_note_from_history
from utils.logging_util import logger
import schedule
import traceback


def main():
    """
    主任务
    :return:
    """
    logger.info("启动")

    upload_note()

    logger.info("结束")


if __name__ == '__main__':
    #服务启动后就开始执行第一次.
    
    main()


    # 图片理解
    # image_url = "https://i.ibb.co/LPqLpBX/959c13b3-aac4-4c25-994c-1a29ddd1f5d8.png"
    # description = image_to_text(image_url)
    # print(description)

    # image_base64
    # image_file_path = "./tmp_image/0b399dea-ab15-41c1-8e30-e63d3b8d115e.png"
    # image_url = upload_image_by_file_path(image_file_path)
    # print(image_url)



    # xhs_title="日暖阳下的法式慵懒🍁"
    # xhs_content = "静谧在我心，独自享受着这属于自己的时光。\n✨秋天的阳光透过艺术工作室的大窗户，洒下温暖的金色光芒🍁"
    # xhs_topics = ["秋日穿搭","法式优雅","生活美学"]
    # image_names = ["./tmp_image/7f1b3279-fa4d-4886-8640-7247c24aa2cf.png","./tmp_image/6699737d-f8c5-41f5-89a9-1991a34bd050.png","./tmp_image/5b0455c7-4c2b-4d52-b04f-319e4da381e0.png","./tmp_image/8c5e2a60-76c1-40ee-83d9-42e44d33ba82.png"]
    # upload_note_from_history(xhs_title,xhs_content,xhs_topics,image_names,None)


    #test_get_suggest_topic()


    #启动一个定时任务 每6小时调用一次main_function方法
    # schedule.every(6).hours.do(main)
    # while True:
    #     try:    
    #         schedule.run_pending()
    #     except Exception as e:
    #         time.sleep(1)
    #         logger.error(f"Error: {e}")
    #         traceback.print_exc()