"""Editorial forms for the learning feed and generated glossary records."""

from functools import lru_cache
import re
from unicodedata import normalize

from core.chinese_converter import convert_script


# Keep market and product qualifiers intact. Previous labels become search aliases.
_SHORT_HEADWORDS = {
    "社媒与种草": {
        "Audience Question Prompt": "Question Prompt",
        "Community Guidelines Post": "Community Rules Post",
        "Content Performance Recap": "Performance Recap",
        "Link Tracking Tag": "Tracking Tag",
        "Side-by-Side Comparison": "Side-by-Side Test",
    },
    "电商与转化": {
        "Fixed-Amount Discount": "Flat Discount",
        "Free Delivery Threshold": "Free Delivery Minimum",
        "Percentage Discount": "Percent Off",
        "Returning Customer": "Repeat Buyer",
    },
    "投放与增长": {
        "Add-to-Cart Rate": "ATC Rate",
        "Cost per Order": "CPO",
        "Non-Branded Search": "Nonbrand Search",
    },
    "公关与线下": {
        "Arrival Instructions": "Arrival Info",
        "Guest Thank-You Note": "Thank-You Note",
        "Product Launch Event": "Product Launch",
        "Trade Show Run of Show": "Trade Show Run Sheet",
    },
    "文案与修辞": {
        "Accessibility Microcopy": "Accessible Copy",
        "Appointment Reminder Email": "Appointment Reminder",
        "App Store Listing": "App Listing",
        "Delivery Update Email": "Delivery Update",
        "Event Registration Page": "Event Sign-Up",
        "Feedback Request Email": "Feedback Email",
        "Frequently Asked Questions": "FAQ",
        "Gift Guide Page": "Gift Guide",
        "Hero Headline": "Hero Title",
        "Image Alt Description": "Alt Description",
        "Image Alt Text": "Alt Text",
        "Loyalty Statement Email": "Points Statement",
        "Order Confirmation Email": "Order Confirmation",
        "Pickup Reminder Email": "Pickup Reminder",
        "Plain-Text Version": "Plain Text",
        "Primary Button Copy": "Primary Button",
        "Price Drop Alert Email": "Price Drop Alert",
        "Product Comparison Page": "Product Comparison",
        "Product Detail Page": "Product Page",
        "Product Waitlist Page": "Product Waitlist",
        "Restock Alert Email": "Restock Email",
        "Service Overview Page": "Service Overview",
        "Store Locator Page": "Store Locator",
        "Subject Line": "Subject",
        "Subscription Renewal Email": "Renewal Email",
        "Trial Ending Email": "Trial Expiry Email",
    },
    "美妆与个护": {"Eau de Parfum": "EDP"},
    "数码与科技": {
        "Blood-Oxygen-Tracking": "Blood Oxygen",
        "High-Refresh-Rate": "High Refresh",
        "Skin-Temperature-Tracking": "Skin Temperature",
        "Electronic Image Stabilisation Smartphone Camera": "Phone Camera with EIS",
        "Electronic Image Stabilisation Action Camera": "Action Camera with EIS",
        "Electronic Image Stabilisation Mirrorless Camera": "Mirrorless Camera with EIS",
    },
    "金融与支付": {
        "Foreign Currency Markup": "FX Markup",
        "Refund to Original Payment Method": "Original Payment Refund",
    },
    "合规与风控": {
        "Before-and-After": "Before/After",
        "Conditions of Use": "Use Conditions",
        "Participation Cap": "Entry Cap",
        "Recycled Material Claim Verification Standard": "Recycled Material Claim Standard",
    },
}


def _headword(category, name):
    for previous, replacement in _SHORT_HEADWORDS.get(category, {}).items():
        name = re.sub(rf"(?<![A-Za-z]){re.escape(previous)}(?![A-Za-z])", replacement, name)
    return name


def _key(value):
    return normalize("NFKC", value).casefold()


def _sentence_name(name):
    # Preserve acronyms and common proper names in food and device labels.
    proper = {"Hong", "Kong", "Sichuan", "Asscher", "Bluetooth", "Matter", "Wi", "Fi", "Cantonese",
              "Swiss", "Riesling", "Chardonnay", "Hainanese", "Taiwanese", "Macau", "Fujian"}
    return re.sub(r"[A-Za-zÀ-ÖØ-öø-ÿ]+",
                  lambda match: match[0] if match[0].isupper() or match[0] in proper else match[0].lower(),
                  name)


# Full-frame edits are scoped to their originating subject. These match known
# seed recipes and retain conditions such as eligible devices and timed offers.
_COPY_FRAMES = {
    "公关与线下": (
        ("Keep your pass ready at the entrance to {x}. It admits one guest to the main hall.",
         "Show your pass for {x} at the main hall. One guest per pass."),
        ("出席今次{x}請預備入場證，每張只供一位來賓進入主場。", "入主場時出示{x}入場證，每張限一位。"),
        ("参加本次{x}请提前准备入场凭证，每张限一人进入主会场。", "进主会场请出示{x}入场凭证，每张限一人。"),
    ),
    "美妆与个护": (
        ("Smooth the {x} over freshly cleansed skin, then follow with moisturiser.",
         "After cleansing, layer the {x} under moisturiser."),
        ("Finish your routine with the {x}, applying a little more where skin feels dry.",
         "Finish with the {x}, adding a little extra to dry areas."),
        ("Try the {x} on the back of your hand to get a feel for how it spreads.",
         "Swatch the {x} on your hand to feel how it blends."),
        ("外出前均勻搽上{x}，並按說明補搽。", "出門前搽勻{x}，按說明補搽。"),
        ("出门前均匀涂抹{x}，补涂时间以说明为准。", "出门前涂匀{x}，按说明补涂。"),
    ),
    "时尚与奢品": (
        ("Layer the {x} over a tee and check how the shoulders sit when you move.",
         "Layer the {x} over a tee and try moving your shoulders."),
        ("Pack a book and a water bottle in the {x}, after checking its inner dimensions.",
         "Check the {x} dimensions for your book and water bottle."),
        ("Position the {x} at hip level if the strap allows, and see how it sits as you walk.",
         "If the strap adjusts, try the {x} at hip height."),
        ("用{x}襯短袖上衣，活動手臂時留意肩位。", "短袖外面襯件{x}，試吓抬手嘅肩位。"),
        ("{x}叠穿短袖，抬手试试肩部活动量。", "短袖外搭{x}，试试肩部余量。"),
        ("袋帶可調的話，將{x}調至髖位，行幾步感受貼身程度。", "袋帶可調嘅話，將{x}調到髖位試行幾步。"),
        ("肩带可调的话，把{x}调到胯部附近，走两步试试贴合感。", "肩带可调的话，把{x}调到胯部试走几步。"),
    ),
    "数码与科技": (
        ("Use the sizing kit for the {x} before ordering, then pair it with the app.",
         "Use the sizing kit before ordering, then pair your {x} with the app."),
        ("訂購前用{x}嘅量度套裝確認尺寸，到手後再配對應用程式。",
         "先用量度套裝揀啱尺寸，{x}到手再配對應用程式。"),
        ("先用{x}的量圈工具确认尺码，到手再连接应用。", "先用量圈工具选好尺码，{x}到手后再连接应用。"),
        ("Try the {x} with a familiar track and check how the headband sits.",
         "Play a familiar track on the {x} and check the fit."),
        ("Wear the {x} for a short walk and see how they sit as you move.",
         "Take a short walk in the {x} to check the fit."),
        ("Type a short paragraph on the {x} to check the layout and feel.",
         "Type a few lines on the {x} to try the layout and feel."),
        ("Try the {x} on a short outing and review the footage before changing settings.",
         "Take the {x} out for a test clip and review it before adjusting settings."),
        ("用熟悉曲目試聽{x}，同時感受頭帶貼合度。", "用{x}播首熟悉嘅歌，試吓頭帶貼唔貼。"),
        ("用熟悉的歌试听{x}，顺便感受头梁贴合度。", "用{x}放首熟悉的歌，试试头梁贴合度。"),
    ),
    "餐饮与酒水": (
        ("{x} | On this week's menu. Ask the team what goes well with this dish.",
         "Try our {x} this week."),
        ("{x} | In the pastry case today. Ask when the next batch comes out.",
         "In the pastry case today: {x}."),
        ("{x} | Explore the menu and book a table for this weekend.",
         "Explore our {x} and book a table this weekend."),
        ("{x} | Ask the barista about this week's beans and try a cup at the brew bar.",
         "Ask the barista about {x} at the brew bar."),
        ("{x} | Ask our sommelier what to look for and which dish to pair it with.",
         "Ask our sommelier about {x}."),
        ("On the drinks board: {x}. Ask the barista how we make it.", "On the drinks board today: {x}."),
        ("Take a moment between sips and look for {x} as the coffee cools.",
         "Look for {x} as your coffee cools."),
        ("本週餐單有{x}，想配其他菜式，不妨問問店員。", "本週餐單有{x}。"),
        ("这周菜单上有{x}，还没决定怎么搭配的话，可以问问店员。", "这周菜单上有{x}，来尝一口。"),
        ("今日餅櫃有{x}，想試新鮮出爐嘅可以問吓下一爐幾點。", "今日餅櫃有{x}，歡迎嚟試。"),
        ("今天烘焙柜有{x}，想趁热吃可以问问下一炉几点出炉。", "今天烘焙柜有{x}，欢迎来尝尝。"),
        ("飲品餐牌有{x}，想知點沖，可以問吓咖啡師。", "今日飲品餐牌有{x}。"),
        ("饮品单上有{x}，感兴趣的话，可以请咖啡师讲讲做法。", "今天饮品单上有{x}。"),
    ),
    "文旅与酒店": (
        ("{x} | Check the room photos, bed layout and guest capacity before booking.",
         "See {x} photos, bed layouts and guest capacity before booking."),
        ("{x} | See what is included and how to get here before you book.",
         "See what the {x} offers and how to get there before you book."),
        ("{x} | Ask reception about availability, hours and any charges.",
         "Ask reception about {x} hours, fees and availability."),
        ("{x} | Confirm the departure details before you set off.",
         "Find your {x} departure time and meeting point."),
        ("{x} | Check the venue and times before planning your visit.",
         "Find the venue and times for {x}."),
        ("{x} | Review the terms for your dates and room rate before you confirm.",
         "Review the {x} for your dates and room rate."),
        ("{x} | Review the entry times and eligibility before you buy.",
         "Check times and eligibility for {x} before buying."),
        ("想用{x}？可向酒店前台查詢服務時間同收費。", "向酒店前台查詢{x}時間同收費。"),
        ("想使用{x}，可以先问酒店前台开放时间、预约方式和费用。", "向酒店前台咨询{x}的时间、预约和费用。"),
        ("出發前請確認{x}詳情，包括集合地點及出發時間。", "出發前睇清{x}嘅集合時間同地點。"),
        ("出发前建议核对{x}的时间和地点，以免耽误行程。", "出发前看好{x}的集合时间和地点。"),
    ),
}


def _compile_frames(frames):
    return tuple((re.compile(re.escape(before).replace(r"\{x\}", r"(?P<title>.+)")), after)
                 for before, after in frames)


_EDITORS = {category: _compile_frames(frames) for category, frames in _COPY_FRAMES.items()}
_RING_FIRST_PHRASE = re.compile(r"blood-oxygen-tracking|skin-temperature-tracking", flags=re.I)
_RING_TERMS = {"Blood-Oxygen-Tracking Smart Ring", "Skin-Temperature-Tracking Smart Ring"}


def _edit_example(example, market, category):
    for pattern, replacement in _EDITORS.get(category, ()):
        match = pattern.fullmatch(example)
        if match:
            title = match["title"]
            if market == "en":
                title = _sentence_name(title)
            return replacement.format(x=title)
    if market == "en" and category in {"餐饮与酒水", "文旅与酒店"}:
        return example.replace(" | ", " — ", 1)
    return example


def _examples(term, canonical):
    edited = {}
    for market in ("en", "hk", "cn"):
        field = f"good_example_{market}"
        example = _edit_example(term[field], market, term["category"])
        if market == "en" and term["term_en"] in _RING_TERMS and canonical != term["term_en"]:
            example = _RING_FIRST_PHRASE.sub(_sentence_name(canonical.removesuffix(" Smart Ring")), example)
        edited[field] = example
    return edited


def polish_generated_terms(terms, reserved=()):
    """Make independent, ordered seed records without changing their identities."""
    originals = tuple(terms)
    names = {_key(term["term_en"]) for term in originals}
    names.update(_key(term["term_en"]) for term in reserved)
    polished = []
    for term in originals:
        previous = term["term_en"]
        candidate = _headword(term["category"], previous)
        canonical = candidate if _key(candidate) not in names else previous
        names.add(_key(canonical))
        aliases = term["aliases"] if canonical == previous else [*term["aliases"], previous]
        polished.append({
            **term, "term_en": canonical, "aliases": list(dict.fromkeys(aliases)),
            "platforms": list(term["platforms"]), **_examples(term, canonical),
        })
    return polished


# In order of editorial specificity. Only use a pair if both actual market
# headwords (or both localized examples) contain the selected expressions.
_REGIONAL_PAIRS = (
    ("合作關係標示", "商业合作标注"), ("連結追蹤標記", "链接追踪参数"),
    ("每宗訂單", "单笔订单"), ("電郵主旨", "邮件主题行"),
    ("遊戲手掣", "游戏手柄"), ("手提電腦", "笔记本"),
    ("記者會", "新闻发布会"), ("專題座談", "圆桌讨论"), ("報到處", "签到台"),
    ("店內限定", "门店专享"), ("推廣專頁", "落地页"), ("通用字", "非品牌词"),
    ("工作階段", "会话数"), ("加入購物車", "加购"), ("定額扣減", "固定金额立减"),
    ("兌換時段", "核销有效期"), ("最低消費額", "起用门槛"), ("同時使用", "叠加"),
    ("免運費", "包邮"), ("禮遇", "福利"), ("皇牌產品", "爆款单品"),
    ("好物推介", "种草"), ("封面畫面", "封面帧"), ("創作者", "达人"),
    ("替代文字", "替代文本"), ("按鈕文字", "按钮文案"), ("介面短句", "界面提示语"),
    ("純文字", "纯文本"), ("開首句", "开场句"), ("新登記會員", "新用户"),
    ("以用家好處為先", "利益点"), ("用家好處", "用户收益"), ("網上預約", "在线预约"),
    ("訂閱計劃", "订阅方案"), ("應用程式", "应用"), ("用家", "用户"),
    ("產品示範", "产品演示"), ("操作教學", "实用教程"), ("並列實測", "同屏对比"),
    ("初用感受", "初体验"), ("用後再評", "追更测评"), ("實錄短片", "日常实录"),
    ("包裝過程", "打包"), ("保養指南", "养护指南"), ("選購指南", "选购攻略"),
    ("清單帖", "清单笔记"), ("回覆留言", "评论回复"), ("留言提問", "评论区提问"),
    ("補充畫面", "辅助镜头"), ("影片分鏡", "视频分镜脚本"), ("循環剪接", "循环剪辑"),
    ("直接入題", "开门见山"), ("影片旁白", "视频配音"), ("系列內容", "系列内容专栏"),
    ("素材再編", "内容二创"), ("待審留言", "评论待审"), ("成效回顧", "效果复盘"),
    ("用家分享", "用户故事"), ("舊客回購", "老客复购"), ("分級滿額", "阶梯满减"),
    ("額外積分", "加赠积分"), ("購物贈品", "下单赠品"), ("套裝定價", "组合价"),
    ("不適用貨品", "不参加活动商品"), ("使用次數上限", "限用次数"),
    ("上市前", "首发前"), ("舊客回流", "老客召回"), ("禮物清單", "礼品心愿单"),
    ("訂戶專享", "订阅用户专享"),
    ("網店專享", "线上专享"), ("門市專享", "门店专享"), ("指定貨品", "指定商品"),
    ("成交比率", "购买转化率"), ("造訪收入", "访问收入"), ("成效歸因", "归因"),
    ("購物廣告", "商品广告"), ("影片廣告", "视频广告"), ("增量成效", "增量提升"),
    ("Podcast 廣告", "播客广告"), ("KOL 合作", "达人合作"), ("新訪客", "新增访客"),
    ("付費社交推廣", "社媒付费投放"), ("自然社交流量", "社媒自然流量"),
    ("品牌字搜尋", "品牌词搜索"), ("聯盟導流", "联盟推广流量"), ("搜尋", "搜索"),
    ("電子通訊", "电子简报"), ("短訊推廣", "短信营销"),
    ("推薦計劃", "推荐奖励计划"), ("二維碼推廣", "二维码营销"),
    ("入場證", "入场凭证"), ("出席限期", "确认截止"), ("開幕", "开业"),
    ("品牌展演", "品牌展示"), ("流程表", "执行流程表"), ("傳媒", "媒体"),
    ("商貿展覽", "行业展会"), ("致謝短箋", "感谢信"),
    ("電影放映會", "影片放映活动"), ("無障礙安排", "无障碍服务"),
    ("眉題", "眉题文案"), ("專題網站", "专题站"), ("條件註釋", "条件说明"),
    ("活動登記", "活动报名"), ("產品比較", "产品对比"), ("送禮指南", "礼品选购"),
    ("實證短句", "证据短句"),
    ("門市搜尋", "门店查询"),
    ("裝置端", "端侧"), ("更新頻率", "刷新率"), ("追蹤", "监测"),
    ("摺疊式屏幕", "折叠屏"), ("防震", "防抖"), ("消噪", "降噪"),
    ("快速充電", "快充"), ("韌體", "固件"), ("無反", "微单"),
    ("多點連接", "多设备连接"), ("抗水", "防水溅"), ("通話耳機", "通话耳麦"),
    ("語音助理", "语音助手"), ("等化器", "均衡器"), ("低光拍攝", "暗光拍摄"),
    ("縮時攝影", "延时摄影"), ("防風雨密封", "防滴防尘密封"), ("輕便相機", "便携相机"),
    ("適合游泳", "支持游泳佩戴"), ("常亮顯示", "息屏显示"), ("手錶", "手表"),
    ("螢幕", "屏幕"), ("智能手掣", "智能手柄"), ("感應器", "传感器"),
    ("座枱燈", "台灯"), ("無線更新", "OTA 升级"), ("鏡頭", "摄像头"),
    ("回程連線", "无线回程"), ("滑鼠", "鼠标"), ("解像度", "分辨率"), ("影片", "视频"),
    ("插牆充電器", "墙插充电器"), ("車用充電器", "车载充电器"), ("流動充電器", "充电宝"),
    ("電力傳輸", "快充协议"), ("雙插口", "双口"), ("配對", "连接"),
    ("啫喱", "凝胶"), ("胭脂", "腮红"), ("潤手霜", "护手霜"), ("爽膚水", "化妆水"),
    ("保濕霜", "保湿面霜"), ("洗頭水", "洗发水"), ("磨砂", "磨砂膏"),
    ("不含香料", "无添加香精"), ("淡香精", "浓香水"), ("妝前底霜", "妆前乳"),
    ("深層清潔", "净澈型"), ("潔淨麝香", "皂感麝香"),
    ("油脂平衡", "水油平衡"), ("不含香料", "不添加香精"), ("不含矽靈", "无硅配方"),
    ("維他命 C", "维 C"), ("精華油", "护肤油"), ("晚安面膜", "睡眠面膜"),
    ("霧感", "哑光"), ("定妝粉", "定妆散粉"), ("逐層加深", "叠涂加深"),
    ("妝感", "妆效"), ("持色唇彩", "染色唇釉"),
    ("霧面", "哑光"), ("精華", "精华液"), ("斜孭袋", "斜挎包"),
    ("跣水", "防泼水"), ("托特袋", "托特包"), ("恤衫", "衬衫"),
    ("方闊剪裁", "箱型剪裁"), ("加大廓形", "宽大廓形"), ("手提書包款", "手提邮差包"),
    ("錶盤", "表盘"), ("夾層", "填充"), ("戶外外套", "户外夹克"), ("大褸", "大衣"),
    ("連身裙", "连衣裙"), ("半截裙", "半身裙"), ("剪裁", "版型"),
    ("自動上鏈", "自动机械"), ("計時腕錶", "计时码表"), ("太陽能", "光动能"),
    ("水晶鏡面", "水晶表镜"), ("派克外套", "派克大衣"), ("背心", "马甲"),
    ("餐單", "菜单"), ("米芝蓮", "米其林"), ("朱古力", "巧克力"),
    ("牛油", "黄油"), ("試飲", "品鉴"), ("配搭", "配餐"),
    ("氣泡酒", "起泡酒"), ("無橡木桶", "未过橡木桶"), ("西岸", "西海岸"),
    ("酒體厚實", "饱满酒体"),
    ("梳乎厘", "舒芙蕾"), ("佳釀", "葡萄酒"),
    ("期間限定", "快闪"), ("套票", "套餐"), ("導賞", "导览"),
    ("留位", "预约"), ("自取", "自提"), ("巡迴展", "路演"),
    ("客房供應", "房态"), ("最優惠", "最优可订"), ("珊瑚保育", "珊瑚保护"),
    ("只限成人入住", "仅限成人"),
    ("登記入住", "办理入住"), ("貴賓室", "贵宾厅"),
    ("回贈", "返现"), ("增值", "充值"), ("戶口", "账户"),
    ("提款", "支取"), ("簽賬", "消费"), ("入賬", "到账"),
    ("現金提取", "现金领取"), ("到賬", "到账"), ("電子錢包", "钱包"),
    ("每日限額", "单日限额"), ("卡對卡", "卡间"), ("即時轉賬", "实时转账"),
    ("取消時段", "撤销时间"), ("外幣兌換", "外币兑换"), ("月結單", "账单"),
    ("預設日期轉賬", "预约转账"), ("簽賬提示", "交易提醒"), ("暫時鎖卡", "临时锁卡"),
    ("網上卡類", "线上银行卡"), ("實體店卡類", "线下银行卡"), ("結算貨幣", "结算币种"),
    ("流動收款機", "移动收银终端"), ("對賬", "对账"),
    ("工作天", "工作日"), ("到期指示", "到期安排"), ("批量發款", "批量付款"),
    ("扣賬卡", "借记卡"), ("公司卡", "企业卡"), ("退款時間", "退款时效"),
    ("銀行扣賬", "银行代扣"), ("私人貸款", "个人贷款"), ("開辦手續費", "贷款办理费"),
    ("還款時間表", "还款计划表"), ("到賬時間", "到账时效"),
    ("核證", "验证"), ("促銷", "营销"), ("拒收", "退订"), ("聲稱", "宣称"),
    ("客戶滿意度", "用户满意度"), ("統計期間", "统计周期"), ("涵蓋範圍", "适用范围"),
    ("表現佐證", "效果依据"), ("護髮產品", "洗护产品"), ("家居清潔劑", "家用清洁剂"),
    ("安全警告", "安全警示"), ("個人資料", "个人信息"),
    ("送禮優惠", "赠礼活动"), ("推薦有賞", "邀请奖励"), ("參加資格", "参加条件"),
    ("優惠日期", "活动期限"), ("不適用項目", "活动排除项"), ("參加上限", "参与上限"),
    ("計算方法", "评估口径"), ("資料來源", "来源"), ("市場佔有率", "市场份额"),
    ("最高級聲稱", "最高级表述"), ("有實證支持", "有证据支持"), ("環保聲稱", "环境声明"),
    ("膳食補充品", "膳食补充剂"),
    ("重要條款", "关键条款"), ("每宗", "单笔"), ("電郵", "邮件"),
    ("IG", "Instagram"),
)


def _comparison(hk, cn):
    text = f"港用「{hk}」，内地用「{cn}」。"
    if len(text) <= 22:
        return text
    text = f"港「{hk}」／内地「{cn}」"
    return text if len(text) <= 22 else ""


def _known_pair(hk, cn):
    for left, right in _REGIONAL_PAIRS:
        if left in hk and right in cn and _simplified(left) != _simplified(right):
            if text := _comparison(left, right):
                return text
    return ""


@lru_cache(maxsize=8192)
def _simplified(text):
    return convert_script(text, "cn")


def learning_tip(term):
    """Project a compact contrast without shortening the stored drawer note."""
    hk, cn = (" ".join(term.get(f"term_{market}", "").split()) for market in ("hk", "cn"))
    pair = _known_pair(hk, cn)
    if pair:
        return pair
    if hk and hk == cn:
        return "两地写法相同。"
    if hk and cn and _simplified(hk).casefold() == _simplified(cn).casefold():
        return "港繁内简，用词相同。"
    if hk and cn:
        pair = _comparison(hk, cn)
        if pair:
            return pair
    return _known_pair(term.get("good_example_hk", ""), term.get("good_example_cn", "")) or "两地常用说法，见上方对照。"
