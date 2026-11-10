"""Editorial source for BrandLex's three-market marketing library."""

from copy import deepcopy

from data.seed_brand_copy import BRAND_TERMS, COPY_TERMS
from data.seed_commerce_growth import COMMERCE_TERMS, GROWTH_TERMS
from data.seed_core_definitions import with_english_definition


SOCIAL_CATEGORY = "社媒与种草"


def _social(identifier, en, hk, cn, aliases, platforms, meaning, bad,
            example_en, example_hk, example_cn, tip):
    return {
        "id": identifier, "term_en": en, "term_hk": hk, "term_cn": cn,
        "aliases": aliases, "category": SOCIAL_CATEGORY, "platforms": platforms,
        "meaning": meaning, "bad_example": bad, "good_example_en": example_en,
        "good_example_hk": example_hk, "good_example_cn": example_cn,
        "usage_tip": tip,
    }


SOCIAL_TERMS = [
    _social(1, "Product Seeding", "好物推介", "种草",
            ["seeding", "种草", "種草", "安利", "誠意推介"], ["IG", "FB", "小红书"],
            "让创作者或用家分享真实使用感受，令别人产生尝试或购买的兴趣；寄送试用品也是常见做法。",
            "『亲，这支精华必须种草！』——直接搬到香港品牌帖文，称呼和语气容易显得突兀。",
            "A little everyday luxury: see how Maya uses our face oil in her evening routine.",
            "今次好物推介：質地輕盈嘅面部精華油，晚間護膚多一份滋潤。",
            "最近被这瓶轻盈精华油种草了，晚间护肤加一步，干燥季也能舒服一点。",
            "内地『种草』重在激发兴趣；香港可用『好物推介』，付费合作或赠品体验需按实际情况清楚标示。"),
    _social(2, "Unboxing", "開箱實測", "开箱测评",
            ["unboxing video", "開箱", "开箱", "上手体验"], ["IG", "YouTube", "小红书"],
            "用照片或影片展示收到产品、打开包装和首次使用的过程，让观众看清实物与细节。",
            "『今天进行拆箱子的操作。』——像说明书，缺少观众想看的实际体验。",
            "Unbox our travel kit with Lena and see what fits in a carry-on.",
            "同 Lena 一齊開箱實測旅行套裝，睇吓放入手提行李有幾方便。",
            "旅行套装开箱测评：跟 Lena 看看尺寸、收纳和第一次上手的感受。",
            "香港常说『開箱／實測』，内地常说『开箱测评』；只有拆包装时别暗示已做长期效果测试。"),
    _social(3, "Viral Hit", "全城熱話", "破圈爆火",
            ["viral", "爆红", "爆紅", "破圈", "刷屏", "熱話"], ["IG", "TikTok", "小红书"],
            "一则内容或一件产品被大量分享，讨论扩散到原本关注品牌以外的人群。",
            "『这杯咖啡具有病毒性。』——把 viral 直译成病毒，会令人误解食品安全。",
            "The cloud latte everyone is sharing is back this weekend.",
            "成為全城熱話嘅雲朵拿鐵，今個週末再度登場。",
            "刷屏的云朵拿铁周末回归，来拍下属于你的第一口云朵。",
            "英文用『went viral』描述传播；港繁『熱話』与内地『破圈』都应有真实讨论支持，避免自封爆火。"),
    _social(4, "Key Opinion Consumer", "用家口碑分享者", "真实体验分享官",
            ["KOC", "key opinion consumer", "素人推荐", "素人推介", "用户口碑"],
            ["IG", "小红书", "微信"],
            "以普通消费者的亲身体验影响身边人或小圈子的人，通常比大型创作者更贴近日常购物场景。",
            "『她只有五百粉丝，所以测评一定客观。』——粉丝数量并不能证明评价独立。",
            "We invited five everyday runners to share an honest week in our new trainers.",
            "邀請五位日常跑手試穿新款跑鞋一星期，分享真實用家感受。",
            "邀请五位日常跑者担任体验分享官，记录新跑鞋一周的真实穿着感受。",
            "KOC 是团队沟通常用缩写；面对消费者写『用家分享／真实体验』更清楚，赠品和合作关系仍要说明。"),
    _social(5, "Pinned Post", "置頂帖文", "置顶笔记",
            ["pin post", "置頂", "置顶", "pinned content"], ["IG", "FB", "小红书"],
            "把重要内容固定在个人主页或动态顶部，让新访客先看到品牌介绍、活动说明或购买指南。",
            "『请阅读我们钉住的邮件。』——把 post 和 pinned 生搬硬译，找不到对应内容。",
            "New here? Start with our pinned post for shades, sizing and delivery details.",
            "第一次嚟？先睇置頂帖文，一次過了解色號、尺寸同送貨安排。",
            "第一次来主页？置顶笔记整理了色号、尺码和配送说明，先收藏再慢慢选。",
            "香港 IG／FB 常写『置頂帖文』；小红书写『置顶笔记』，要按实际平台功能调整指引。"),
    _social(6, "Aesthetic Grid", "IG 版面佈置", "主页九宫格",
            ["Instagram grid", "feed aesthetic", "九宮格", "九宫格", "版面"], ["IG", "小红书"],
            "统一主页上多张图片的色彩、构图和排列，让访客一眼认出品牌风格。",
            "『我们建立了美学网格。』——消费者很难联想到社媒主页的视觉风格。",
            "Soft greens and honest textures bring our refill collection together on the feed.",
            "柔和綠調配搭自然質感，令補充裝系列喺 IG 版面更有一致感。",
            "用柔和绿调和自然材质统一主页九宫格，让补充装系列的环保理念一眼可见。",
            "香港团队多说『IG 版面』；内地『九宫格』也可指单篇九图帖，执行前先确认是主页还是一组图。"),
    _social(7, "Check-in Spot", "打卡熱點", "出片打卡点",
            ["photo spot", "打卡", "Instagrammable", "出片"], ["IG", "小红书", "微信"],
            "适合拍照、分享位置或参与现场活动的地方，常用来带动到店和自然分享。",
            "『到我们的登记点拍照。』——把 check-in 译成登记，混淆了拍照和报到。",
            "Find the sunlit flower wall at our weekend pop-up and make it your next photo stop.",
            "週末嚟期間限定店，陽光花牆已經準備好，等你發掘新打卡熱點。",
            "周末来快闪店找这面阳光花墙，随手拍也能留下好看的打卡照。",
            "『打卡』三地中文都能理解；英文广告常写『photo spot』更直白，记得附地点与开放时间。"),
    _social(8, "Teaser", "率先預告", "新品预告",
            ["sneak peek", "预热", "預熱", "抢先看", "搶先睇"], ["IG", "FB", "微信"],
            "在正式发布前透露部分画面或线索，先让受众知道日期并期待下一步消息。",
            "『这是一个产品挑逗者。』——teaser 在发布场景是预告，不是对人的形容。",
            "A new shade is on the way. Get a first look this Friday.",
            "全新色調即將登場，今個星期五率先睇。",
            "新色即将上线，周五揭晓，先来猜猜这次的灵感。",
            "香港可用『率先預告／搶先睇』，内地可用『新品预告／预热』；预告要给出明确揭晓时间。"),
    _social(9, "Giveaway", "送禮活動", "宠粉福利",
            ["prize draw", "抽獎", "抽奖", "give away", "粉丝福利"], ["IG", "FB", "小红书"],
            "通过活动向参与者赠送奖品，吸引互动或回馈关注者；抽选、先到先得等方式需要讲清楚。",
            "『免费给每个人！』——实际只有三名中奖者，容易造成错误期待。",
            "Tell us your go-to weekend ritual for a chance to win one of three self-care sets.",
            "留言分享你嘅週末放鬆習慣，即有機會獲得三份護理套裝其中一份。",
            "宠粉福利来啦：评论分享你的周末放松方式，抽三位送出护理套装。",
            "『送禮活動』适合香港，『宠粉福利』偏内地社媒语气；两地都要写清奖品、名额、截止时间与参与条件。"),
    _social(10, "User-Generated Content", "用家分享內容", "用户原创内容",
            ["UGC", "用户晒图", "用家投稿", "customer content"], ["IG", "小红书", "Shopify"],
            "由消费者自行拍摄或撰写的照片、影片和评价，可展示产品在真实生活中的使用方式。",
            "『客户发过这张图，所以我们可以随便拿来投广告。』——公开发布不等于授权商用。",
            "Your shelf, your style. Share a photo with #MyDailyShelf; we will ask before featuring it.",
            "你嘅層架，你嘅風格。用 #MyDailyShelf 分享相片，我哋轉載前會先徵求同意。",
            "晒出你的日常收纳角，带上 #MyDailyShelf 分享原创照片，入选展示前会先征得授权。",
            "UGC 是团队用语；消费者页面可写『用家分享／用户晒图』，转发和广告使用应分别取得适当授权。"),
    _social(11, "Influencer Collaboration", "KOL 合作", "达人合作",
            ["KOL", "influencer marketing", "博主合作", "創作者合作"], ["IG", "YouTube", "小红书"],
            "关键意见领袖（KOL）是在特定领域有影响力的人。达人合作指品牌与这类创作者共同制作或发布内容。",
            "『这位博主是自然推荐，不需要提赞助。』——隐藏付费合作会损害信任。",
            "Paid partnership with Nora: three easy ways to style our linen shirt.",
            "與 Nora 合作呈獻：一件麻質恤衫，三種日常穿搭提案。",
            "与穿搭达人 Nora 合作分享：一件亚麻衬衫，搭出三种通勤风格。",
            "香港常用『KOL 合作』，内地多用『达人／博主合作』；英文『collab』也可能指联名，需写明合作形式。"),
    _social(12, "Short-Form Video", "短片內容", "短视频",
            ["Reels", "short video", "短片", "竖屏视频", "直向短片"], ["IG", "TikTok", "小红书"],
            "用较短的影片快速展示一个卖点、步骤或故事，通常适合手机竖屏观看。",
            "『把五分钟说明书全塞进十五秒。』——信息过密，观众看不清重点。",
            "One brush, one minute: watch our quick everyday brow routine.",
            "一支眉掃，一分鐘，短片示範日常自然眉形。",
            "一支眉刷，一分钟，用短视频讲清日常自然眉的画法。",
            "香港宣传常说『短片』，内地说『短视频』；写 Reels 时确认发布平台，别把功能名称当成所有短片的通称。"),
    _social(13, "Livestream Shopping", "直播購物", "直播带货",
            ["live shopping", "直播", "直播間", "直播间"], ["IG", "小红书", "微信"],
            "主持人在直播中展示产品、回答问题并引导购买，观众可以边看边了解优惠和使用方法。",
            "『进入我们的生活购物房间。』——live 在这里指直播，不是生活。",
            "Join our live demo at 7 pm and ask the stylist about fit before you shop.",
            "今晚七點直播試身，先問清楚剪裁同尺寸，再揀心水款式。",
            "今晚七点直播间见，主播现场试穿，尺码和版型问题都可以来问。",
            "香港『直播購物／直播試用』较自然，内地『直播带货』更常见；要同时写清时区和可用购买渠道。"),
    _social(14, "Save-Worthy Content", "實用收藏帖", "干货收藏帖",
            ["save for later", "收藏", "懶人包", "干货", "乾貨"], ["IG", "小红书", "微信"],
            "把步骤、清单或实用建议整理成便于保存的内容，让读者在需要时回来查阅。",
            "『一百个秘密都在这里，先收藏再说。』——内容没有兑现标题承诺，难留住读者。",
            "Save this five-step packing list for your next weekend away.",
            "週末短遊點執行李？收藏呢份五步清單，下次出發前再睇。",
            "周末短途旅行怎么打包？这份五步清单先收藏，下次出发直接照着收。",
            "内地『干货』常表示实用内容，香港面向大众可用『實用貼士／懶人包』，避免把它直译成 dry goods。"),
    _social(15, "Hashtag Challenge", "主題標籤挑戰", "话题挑战",
            ["hashtag", "话题标签", "主題標籤", "challenge"], ["IG", "TikTok", "小红书"],
            "邀请用户围绕同一主题拍摄或发帖，并使用统一标签，方便大家参与和浏览相关内容。",
            "『使用十个无关热门标签就能保证流量。』——标签要对应内容，不能保证传播效果。",
            "Show us your refill routine with #RefillTogether and inspire a friend to try it.",
            "參加 #RefillTogether 主題挑戰，分享你嘅補充裝日常。",
            "加入 #RefillTogether 话题挑战，晒出你的补充装使用日常。",
            "香港常说『hashtag／主題標籤』，小红书常说『话题』；参与动作要简单，活动标签与品牌标签分工要清楚。"),
    _social(16, "Content Calendar", "社交平台發帖排程", "内容排期",
            ["editorial calendar", "content plan", "排期表", "內容日曆"], ["IG", "FB", "小红书", "微信"],
            "按日期安排要发布的主题、素材和负责人，避免临时赶稿，也让推广节奏与活动时间配合。",
            "『周五发布周三结束的优惠。』——排期没有对齐活动有效期。",
            "Our June content calendar pairs weekly styling tips with the summer launch.",
            "六月發帖排程：每週穿搭貼士配合夏季新品，發文同上架節奏一致。",
            "六月内容排期已安排好：每周穿搭干货搭配夏季上新，避免连续硬广。",
            "香港团队常用『發帖排程』，内地常用『内容排期』；跨市场排期要同时核对当地节日、时区与货期。"),
    _social(17, "Community Engagement", "社群互動", "社群互动",
            ["community interaction", "粉丝互动", "粉絲互動", "engagement"], ["IG", "FB", "微信"],
            "通过回复、提问、讨论或用户活动与社群成员建立来回交流，而不只是不断发促销消息。",
            "『每天发二十条促销就是高互动。』——发布次数多不代表有真实交流。",
            "Which workshop should we host next? Tell us what you want to learn.",
            "下次想參加咩工作坊？留言話我哋知，一齊決定活動主題。",
            "下一场工作坊你想学什么？欢迎在群里投票，也可以提出新点子。",
            "『互动』应指真实回应；香港 FB 群组与内地微信社群的交流习惯不同，先选择符合场景的提问方式。"),
    _social(18, "Product Review", "用後評價", "真实测评",
            ["review", "用後感", "使用心得", "测评", "評價"], ["IG", "小红书", "Shopify"],
            "记录产品使用后的优点、限制和适合的人群，帮助潜在买家判断是否满足自己的需求。",
            "『所有肤质用了都立刻有效。』——忽略个体差异，也没有说明体验依据。",
            "After two weeks: how our lightweight moisturiser felt on my combination skin.",
            "連續試用兩星期，混合肌用家分享輕盈面霜嘅保濕感同使用心得。",
            "混合皮两周真实测评：这瓶轻盈面霜的肤感、保湿表现和不适合的场景。",
            "香港『用後感／用家評價』偏体验分享，内地『测评』常令人期待比较与依据，别把广告冒充独立评测。"),
    _social(19, "Behind-the-Scenes Content", "幕後花絮", "幕后花絮",
            ["BTS", "behind the scenes", "幕后", "幕後", "制作过程"], ["IG", "YouTube", "小红书"],
            "分享设计、制作、拍摄或团队工作的过程，让受众看到成品背后的人和细节。",
            "『欢迎观看场景后面的内容。』——逐字翻译，读者不知道是制作花絮。",
            "Behind the scenes: watch our ceramicists hand-finish every cup.",
            "幕後花絮：由陶藝師親手修整杯口，細看每隻杯嘅製作過程。",
            "幕后花絮来了：跟着陶艺师看一只杯子如何完成最后的手工修整。",
            "中英文都可直接写『幕后花絮／behind the scenes』；BTS 缩写在消费文案中可能指艺人组合，首次出现最好写全。"),
    _social(20, "Carousel Post", "多圖輪播帖文", "多图笔记",
            ["carousel", "多圖帖", "多图", "滑动浏览", "左右滑動"], ["IG", "FB", "小红书"],
            "在一篇帖文中放入多张可切换的图片，用连续页面讲步骤、对比或完整故事。",
            "『点击我们的旋转木马了解清洁步骤。』——carousel 在这里是多图轮播，不是游乐设施。",
            "Swipe through for three ways to care for your linen pieces.",
            "向左掃睇多圖教學，三個步驟學識打理麻質衣物。",
            "左右滑动这篇多图笔记，三个步骤学会打理亚麻衣物。",
            "香港 IG 常用『向左掃』，内地小红书常用『左右滑动』；首图交代收益，最后一图再给清晰下一步。"),
]


SAMPLE_DRAFTS = [
    {
        "id": "beauty-hk",
        "title": "美妆好物帖：调整为香港 Instagram 语气",
        "target_market": "hk",
        "text": "亲们，今天给宝宝们种草这支爆款保湿精华！质地清爽不粘，通勤前用也很舒服。\n"
                "上周被朋友安利后终于拔草了，性价比高，学生党也能入。\n"
                "新品早鸟福利限时上线，满299包邮，还能领券。点击链接购买，评论区聊聊你的换季护肤烦恼吧！",
    },
    {
        "id": "launch-en",
        "title": "无线耳机新品发布：改掉生硬英文直译",
        "target_market": "en",
        "text": "Good news! Our new wireless earbuds are heavy launched today. Bring you a new experience "
                "with comfortable fit and clear calls on the morning commute. The compact case slips into "
                "your pocket. High cost performance makes it the first choice of urban people. "
                "Welcome to buy. Please pay attention to our official account for more surprises.",
    },
    {
        "id": "giftbox-hk",
        "title": "节日限量礼盒：补上清晰的购买引导",
        "target_market": "hk",
        "text": "以香氣，留住相聚的片刻。冬日限量珍藏版禮盒，精選雪松香氛蠟燭與手工陶瓷托盤，"
                "附送燙金心意卡，由你寫下節日祝福。\n"
                "Seasonal gifting, thoughtfully wrapped. A candle, a keepsake tray, and a note from you.\n"
                "禮盒售價 HK$680，11 月 20 日起於中環專門店及網店同步發售。",
    },
    {
        "id": "cafe-cn",
        "title": "咖啡店快闪邀请：调整为内地社媒表达",
        "target_market": "cn",
        "text": "週末一齊歎杯啡！我們的期間限定店將登陸上海安福路，聯乘本地陶藝工作室，"
                "帶來柚子冷萃與手作咖啡杯。\n"
                "現場設有打卡熱點，首五十位到店客人買滿即送限定明信片。早鳥禮遇預訂現已開放，"
                "有興趣可以了解一下。活動時間：週六至週日 11:00–18:00。",
    },
]


def build_seed_terms():
    """Return fresh records so editing a term never changes the defaults."""
    return [with_english_definition(term) for term in deepcopy(
        SOCIAL_TERMS + COMMERCE_TERMS + GROWTH_TERMS + BRAND_TERMS + COPY_TERMS
    )]


def build_sample_drafts():
    """Return four editable examples covering all three target markets."""
    return deepcopy(SAMPLE_DRAFTS)
