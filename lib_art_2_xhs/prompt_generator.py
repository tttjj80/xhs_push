import random
from typing import Dict, List, Optional
import asyncio
import json
import datetime

from lib_art_2_xhs.gptnb import call_llm

class PromptGenerator:
    def __init__(self):
        
        
        # 基础场景模板
        self.scenes = scenes = [
    "高级咖啡厅工作", "海边漫步", "都市街拍", "图书馆看书", "樱花公园散步",
    "高端健身房运动", "米其林餐厅用餐", "创意办公室开会", "现代艺术展览", "奢侈品购物中心",
    "复古书店探索", "花艺工作室", "山顶日落", "游艇派对", "下午茶时光",
    "博物馆参观", "音乐厅演出", "城市天台", "温泉度假", "古典庭院",
    "高级酒吧", "瑜伽课堂", "画廊开幕", "赛马场", "私人飞机舱",
    "英式花园", "法式城堡", "意大利广场", "日式庭园", "韩式咖啡厅",
    "设计师工作室", "星级酒店大堂", "私人影院", "高尔夫球场", "豪华游轮甲板",
            "钢琴房", "红酒庄园", "古董店", "天文台", "玻璃温室",
            "城市空中花园", "私人别墅泳池", "香水工坊", "茶艺馆", "手工艺工作室",
            "观景阳台", "水疗中心", "古典音乐厅", "美术工作室", "时尚摄影棚"
        ]
        
        # 服装风格模板
        self.clothing_styles = [
    "法式优雅职业装", "轻奢休闲装", "高级运动装", "波西米亚度假风", "日系甜美风",
    "纽约街头风", "复古摩登风", "巴黎优雅风", "简约极简风", "轻熟知性风",
    "英伦学院风", "北欧简约风", "意式浪漫风", "东京街头风", "加州休闲风",
    "高级定制风", "赛车少女风", "民族风情", "古典优雅风", "现代都市风",
    "海滨度假风", "户外探险风", "芭蕾舞者风", "爵士风情", "维多利亚复古风",
    "哥特风格", "赛博朋克风", "牛仔美式风", "韩系清新风",
    "日式和服风", "中国旗袍风", "法式小香风", "意大利奢华风", "北欧极简风",
    "波普艺术风", "嬉皮士风格", "太空未来风", "复古摇滚风", "芭比粉嫩风",
    "英式贵族风", "美式校园风", "欧式宫廷风", "东方禅意风", "热带度假风",
    "山系户外风", "赛博时尚风", "舞台表演风", "都市丽人风", "艺术家风格",""
]
        
        # 场景情绪模板
        self.moods = [
    "优雅从容", "温柔似水", "活力四射", "知性优雅", "清新脱俗",
    "时尚前卫", "浪漫梦幻", "冷艳高贵", "甜美可人", "干练精英",
    "慵懒随性", "青春活泼", "神秘魅惑", "典雅端庄", "率性不羁",
    "淡雅恬静", "高冷御姐", "俏皮可爱", "独特艺术", "优雅贵气",
    "自信从容", "温婉娴淑", "帅气飒爽", "灵动俏皮", "冷静睿智",
    "温暖治愈", "明艳动人", "沉稳大气", "清冷孤傲", "浪漫唯美",
    "优雅知性", "活力阳光", "冷酷帅气", "温柔恬静", "古典优雅",
    "时尚潮流", "清新自然", "高贵典雅", "甜美温暖", "干练精明",
    "浪漫迷人", "清纯可爱", "优雅成熟", "率真活泼", "深邃神秘",
    "淡然从容", "温柔婉约", "英气逼人", "灵动优美", "知性雅致"
]
        # 季节模板
        self.seasons = [
    "初春", "春分", "暮春",
    "初夏", "盛夏", "夏末",
    "初秋", "秋分", "深秋",
    "初冬", "冬至", "寒冬",
    "春夏之交", "夏秋之交", "秋冬之交", "冬春之交",
    "梅雨季", "樱花季", "枫叶季", "雪季",
    "清明时节", "立夏", "芒种", "小满",
    "立秋", "白露", "寒露", "霜降",
    "立冬", "小雪", "大雪", "小寒", "大寒",
    "立春", "雨水", "惊蛰",
    "五月天", "仲夏夜", "金秋十月", "腊月",
    "春节", "元宵", "端午", "中秋", "重阳",
            "暑假", "寒假", "开学季", "毕业季"
        ]
        
    def get_image_quality_prompt(self) -> str:

        quality_prompt = """
        (masterpiece:1.4), (best quality:1.3), (ultra-detailed:1.2), (sharp focus:1.1), 8k uhd, high-res, photorealistic, professional photography, 
        (soft lighting:1.2), (natural skin texture:1.1), (subtle makeup:1.1), (delicate features:1.2), 
        (elegant pose:1.3), (gentle expression:1.2), (alluring gaze:1.1), 
        (fashion magazine style:1.2), (Instagram aesthetic:1.1), (Xiaohongshu composition:1.3), 
        (pure and sensual:1.4), (innocent yet alluring:1.3), (subtle sexiness:1.2), 
        (soft color palette:1.1), (dreamy atmosphere:1.2), (shallow depth of field:1.1), 
        (film grain:0.3), (high fashion:1.2), (trendy outfit:1.1), (youthful glow:1.2)
        """

        return quality_prompt

    # 返回prompt和errdesc
    def get_flux_prompt(self, scene: str, style: str, mood: str, season: str, model="gpt-4o-mini"):
        """Generate detailed prompt description using LLM API"""   
        
        system_prompt = """
You are an elite AI image generation prompt engineer for Flux AI, specializing in creating high-quality, trendy Xiaohongshu (Little Red Book) images that embody the 'pure desire' aesthetic.

Your task: Generate a detailed Flux prompt based on the given scene, clothing style, mood, and season. The prompt should result in a visually stunning image that captures Xiaohongshu style and balances innocence with allure. Emphasize seasonal elements to enhance the atmosphere and relevance of the image.

Key requirements:
1. Output a single, comma-separated string of English phrases.
2. The total character count must not exceed 500 characters.
3. Balance innocence and sensuality without being explicit.
4. Incorporate trendy Xiaohongshu elements and create a dreamy, aspirational atmosphere.
5. Provide vivid, specific details for photorealistic image generation.
6. Strongly emphasize seasonal characteristics, ensuring clothing and environment are highly relevant to the season.

Include these elements:
1. Overall scene and atmosphere (emphasizing seasonal feel)
2. Detailed environment description (including season-specific elements)
3. Clothing and accessory details (must be season-appropriate)
4. Character's pose and body language
5. Facial expression and gaze
6. Lighting and color palette (reflecting seasonal characteristics)
7. Camera angle and photography style
8. Trendy, share-worthy details (related to the season)

Use specific photography and post-processing terms to enhance image quality and style. Do not include explanations or separate sections.
"""
    
        user_prompt = f"""
        Generate a Flux AI prompt for a Xiaohongshu-style image with the following elements:

Scene: {scene}
Clothing Style: {style}
Mood: {mood}
Season: {season}

Additional requirements:
1. The prompt should result in an image that embodies the 'pure desire' aesthetic, balancing innocence and allure.
2. Incorporate trendy elements popular on Xiaohongshu, such as soft color palettes, dreamy lighting, and fashionable details.
3. Ensure the description is detailed enough to create a visually stunning and artistic image.
4. Include specific photography and post-processing terms to enhance the overall quality and style of the generated image.
5. Add elements that make the image stand out and be share-worthy on Xiaohongshu.
6. Strongly emphasize {season} seasonal characteristics, ensuring clothing, environment, and overall atmosphere are highly relevant to the season.
7. Describe at least 3 specific elements related to {season} (e.g., specific plants, weather phenomena, seasonal events).

Remember to format the prompt as a single, comma-separated string without explanations or sections.
"""
    
        return call_llm(system_prompt, user_prompt, model=model, temperature=0.9)
        

    # 
    def generate_face_prompt(self) ->str:
        face_prompt = """
        oval face,golden ratio,small V-shaped chin,graceful jawline,symmetrical face,(face width-to-height 1:1.5),soft contours,(phoenix eyes:1.3),upturned corners,double eyelids,bright clear eyes,almond-shaped,eye spacing one eye width,long lashes,hooded upper lids,dark iris,lustrous expression,(eye ratio 1:0.45),(straight bridge nose:1.2),refined tip,moderate height,subtle wings,ideal nose-to-lip ratio,bridge matching inner eye corners,natural contour,perfect projection,(curved Cupid's bow:1.3),full upper lip,fuller lower lip,pink tone,upturned corners,lip ratio 1:1.2,proportional width,(curved eyebrows:1.4),arch at outer third,tapering ends,moderate thickness,clean shape,ideal distance,(porcelain skin:1.3),rosy undertone,ethereal glow,fine pores,jade-like luster,youthful,even texture,perfect thirds division,balanced features,golden ratio (1.618:1),harmonious spacing,ideal philtrum,graceful angles,feminine softness,goddess aura,elegant demeanor,gentle expression,ethereal beauty,oriental standards,celestial features,timeless grace
        """
        return face_prompt


    def generate_daily_prompt(self, scene=None, style=None, mood=None,season=None,model="gpt-4o-mini") -> Dict[str, str]:
        """生成每日不同的prompt组合"""
        if scene is None:
            scene = random.choice(self.scenes)
        if style is None:
            style = random.choice(self.clothing_styles)
        if mood is None:
            mood = random.choice(self.moods)
        if season is None:
            season = random.choice(self.seasons)
    
        
        prompt,errdesc = self.get_flux_prompt(scene, style, mood,season,model=model)
        
        return {
            "positive_prompt": prompt,
            "metadata": {
                "scene": scene,
                "style": style,
                "mood": mood,
                "date": datetime.datetime.now().strftime("%Y-%m-%d")
            },
            "errdesc": errdesc
        }

    async def save_prompt_history(self, prompt_data: Dict[str, str], filename: str = "prompt_history.json"):
        """保存生成的prompt历史记录"""
        try:
            with open(filename, 'r') as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []
            
        history.append(prompt_data)
        
        with open(filename, 'w') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)


    def get_comprehensive_negative_prompt(self) -> str:
        """获取详细的负面提示词"""
        
        # 基础质量问题
        quality_issues = """
        (worst quality:1.4), (low quality:1.4), (normal quality:1.4), low resolution, 
        jpeg artifacts, blurry, pixelated, poor quality, grainy image, unclear details,
        compression artifacts, oversaturated, overexposed, underexposed, washed out,
        """

        # 人体解剖问题
        anatomy_issues = """
        (bad anatomy:1.3), (inaccurate limb:1.2), anatomical error, bad proportions,
        wrong anatomy, distorted body, bodypart error, improper anatomy, 
        malformed limbs, extra limbs, missing limbs, disconnected limbs,
        mutation, deformed, malformed, disfigured, gross proportions,
        extra joints, broken joints, fused joints, bent joints,
        """

        # 手部问题
        hand_issues = """
        (bad hands:1.4), (wrong hands:1.3), (malformed hands:1.3), ugly hands, 
        missing fingers, extra fingers, fused fingers, too many fingers,
        wrong finger placement, distorted fingers, broken fingers,
        extra digit, fewer digits, long fingers, short fingers,
        """

        # 面部问题
        face_issues = """
        (bad face:1.4), (ugly face:1.3), (wrong face:1.3), (deformed face:1.3),
        distorted face, ugly eyes, wrong eyes, misaligned eyes, crossed eyes,
        asymmetric eyes, uneven eyes, weird eyes, strange mouth, bad mouth,
        crooked nose, wrong nose, bad nose structure, weird mouth, bad lips,
        asymmetric face, disproportionate face, uncanny valley,
        """

        # 眼睛问题
        eye_issues = """
        (cross-eyed:1.3), (crossed eyes:1.3), (misaligned eyes:1.3),
        uneven eyes, asymmetric eyes, different sized eyes,
        lazy eye, wandering eye, cockeyed, strabismus,
        """

        # 皮肤和纹理问题
        skin_issues = """
        (bad skin:1.3), (ugly skin:1.2), (weird skin:1.2), (skin issues:1.2),
        bad_skin_quality, rough skin, uneven skin, poor skin texture,
        unrealistic skin, plastic skin, overly smooth skin,
        """

        # 衣物问题
        clothing_issues = """
        (bad clothing:1.3), (deformed clothing:1.2), (wrong clothing:1.2),
        missing clothing, unrealistic clothing, floating clothing,
        poorly drawn clothing, inconsistent clothing, weird clothing folds,
        """

        # 头发问题
        hair_issues = """
        (bad hair:1.3), (weird hair:1.2), (wrong hair:1.2), (messy hair:1.2),
        unrealistic hair, floating hair, poorly drawn hair,
        inconsistent hair, merged hair, unnatural hair flow,
        """

        # 构图问题
        composition_issues = """
        bad composition, poor composition, confusing composition,
        cluttered composition, awkward composition, unbalanced composition,
        """

        # 技术问题
        technical_issues = """
        watermark, signature, text, logo, copyright, username,
        timestamp, date stamp, label, title, caption,
        """

        # 画面元素问题
        element_issues = """
        multiple views, split image, frame within frame,
        collage, panorama, tiled image, duplicate, repeating elements,
        """

        # 渲染问题
        rendering_issues = """
        rendering artifacts, 3d rendering errors, bad shading,
        unrealistic shadows, harsh shadows, missing shadows,
        wrong perspective, bad perspective, distorted perspective,
        """

        # 光线问题
        lighting_issues = """
        bad lighting, harsh lighting, unrealistic lighting,
        inconsistent lighting, missing shadows, wrong shadows,
        unnatural shadows, multiple light sources conflict,
        """

        # AI生成特有问题
        ai_artifacts = """
        (ai artifacts:1.3), (ai generated:1.2), artwork by ai,
        artificial looking, machine learning artifacts,
        stable diffusion artifacts, midjourney style,
        """

        # 组合所有负面提示词
        comprehensive_negative = f"""
        {quality_issues}
        {anatomy_issues}
        {hand_issues}
        {face_issues}
        {eye_issues}
        {skin_issues}
        {clothing_issues}
        {hair_issues}
        {composition_issues}
        {technical_issues}
        {element_issues}
        {rendering_issues}
        {lighting_issues}
        {ai_artifacts}
        """
        
        # 删除多余空格和换行，整理格式
        return ", ".join(
            [x.strip() for x in comprehensive_negative.split(',') 
            if x.strip() and not x.isspace()]
        )       



if __name__ == "__main__":

    promptGenerator = PromptGenerator()
    
    daily_prompt = promptGenerator.generate_daily_prompt(model="gpt-4o")
    # 打印positive_prompt长度
    print(len(daily_prompt["positive_prompt"]))
    print(json.dumps(daily_prompt, indent=4, ensure_ascii=False))
    # s ="oval face shape,golden ratio proportions,small V-shaped chin,graceful jawline,symmetrical face structure,(face width-to-height ratio 1:1.5),soft facial contours,(phoenix eyes:1.3),upturned outer corners,double eyelids with moderate crease,bright clear eyes,slightly almond-shaped,eye spacing exactly one eye width apart,long natural lashes,slightly hooded upper eyelids,dark rich iris color,lustrous eye expression,(eye ratio width-to-height 1:0.45),(straight bridge nose:1.2),refined nose tip,moderate nose height,subtle nose wings,ideal nose-to-lip ratio,nose bridge height matching inner eye corners,natural nose contour,perfect nose projection,(curved Cupid's bow:1.3),full upper lip with defined peaks,slightly fuller lower lip,natural pink tone,mouth corners slightly upturned,lip ratio upper-to-lower 1:1.2,moderate lip width proportional to nose width,(curved delicate eyebrows:1.4),natural arch position at outer third,tapering ends,moderate thickness,clean defined shape,ideal distance from eyes,soft brown color,(porcelain smooth skin:1.3),natural rosy undertone,ethereal glow,translucent complexion,fine pores,jade-like luster,youthful moisture,even skin texture,perfect thirds face division,balanced facial features,golden ratio facial proportions (1.618:1),harmonious feature spacing,ideal philtrum length,graceful facial angles,feminine softness,goddess aura,elegant demeanor,gentle expression,ethereal beauty,oriental beauty standards,celestial features,timeless grace,"
    # s ="oval face,golden ratio,small V-shaped chin,graceful jawline,symmetrical face,(face width-to-height 1:1.5),soft contours,(phoenix eyes:1.3),upturned corners,double eyelids,bright clear eyes,almond-shaped,eye spacing one eye width,long lashes,hooded upper lids,dark iris,lustrous expression,(eye ratio 1:0.45),(straight bridge nose:1.2),refined tip,moderate height,subtle wings,ideal nose-to-lip ratio,bridge matching inner eye corners,natural contour,perfect projection,(curved Cupid's bow:1.3),full upper lip,fuller lower lip,pink tone,upturned corners,lip ratio 1:1.2,proportional width,(curved eyebrows:1.4),arch at outer third,tapering ends,moderate thickness,clean shape,ideal distance,(porcelain skin:1.3),rosy undertone,ethereal glow,fine pores,jade-like luster,youthful,even texture,perfect thirds division,balanced features,golden ratio (1.618:1),harmonious spacing,ideal philtrum,graceful angles,feminine softness,goddess aura,elegant demeanor,gentle expression,ethereal beauty,oriental standards,celestial features,timeless grace"
    # print(len(s))
#     s ="Designer's studio, modern and chic, ballet dancer-inspired fashion, wearing a flowing, delicate tulle skirt paired with a form-fitting, elegant top, pastel colors, soft and graceful. She stands poised en pointe, one arm raised gracefully above her head, conveying a sense of movement and elegance. Warm, diffused lighting creates a soft, inviting glow, highlighting her silhouette. The camera angle is slightly from below, capturing her full figure and the artistic atmosphere, aligning with Xiaohongshu's aesthetic, blending purity with allure."
    s ="""

Luxurious private villa poolside, minimalist chic swimwear, warm and healing mood, serene atmosphere, lush greenery surrounding pool, gentle ripples on water surface, sleek modern sun loungers, soft white towels, character reclining gracefully on lounger, legs slightly bent, one arm resting behind head, subtle arch in back, delicate necklace glinting in sunlight, soft, inviting gaze, slight smile, sun-kissed skin glowing, gentle breeze tousling hair, golden hour lighting, warm sun rays casting soft shadows, pastel blue and blush pink color palette, close-up angle capturing elegance, dreamy bokeh effect, light lens flare, high-definition clarity, cinematic depth of field, soft-focus technique, glossy magazine style, trendy Xiaohongshu aesthetics, aspirational lifestyle, artful composition, fashionable yet understated, ethereal and captivating, perfect for sharing, photorealistic detail, post-processed for vibrancy and warmth, subtle vignette for emphasis, harmonious blend of elements, visually stunning and share-worthy."""
    print(len(s))