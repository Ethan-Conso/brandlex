"""Build the dining and hospitality seed terms from curated phrase families."""

from dataclasses import dataclass

from data import seed_food_terms as food
from data import seed_travel_terms as travel
from data.seed_food_travel_examples import FEATURED_COPY


@dataclass(frozen=True)
class CopyContext:
    """Channel-specific examples and editorial guardrails for related terms."""

    platforms: tuple[str, ...]
    english: str
    hong_kong: str
    mainland: str
    bad: str
    tip: str


def _entries(category, source, context):
    for line in source.strip().splitlines():
        en, hk, cn, alias, meaning = line.split("|")
        names = {"en": en, "hk": hk, "cn": cn}
        defaults = (context.english, context.hong_kong, context.mainland, context.bad, context.tip)
        example_en, example_hk, example_cn, bad, tip = (
            value.format(**names) for value in FEATURED_COPY.get(en, defaults)
        )
        yield {
            "term_en": en,
            "term_hk": hk,
            "term_cn": cn,
            "aliases": [alias],
            "category": category,
            "platforms": list(context.platforms),
            "meaning": meaning,
            "bad_example": bad,
            "good_example_en": example_en,
            "good_example_hk": example_hk,
            "good_example_cn": example_cn,
            "usage_tip": tip,
        }


def _split_rows(source, count):
    rows = source.strip().splitlines()
    return "\n".join(rows[:count]), "\n".join(rows[count:])


_MEAL_TYPES, _DINING_TERMS = _split_rows(food.DINING_FORMATS, 25)
FOOD_FAMILIES = (
    (_MEAL_TYPES, CopyContext(
        ("OpenRice", "大众点评", "IG"),
        "{en} | Explore the menu and book a table for this weekend.",
        "今個週末想約朋友食飯？先睇{hk}詳情，再揀心水時段。",
        "周末约饭可以先看看{cn}的供应时段，再选位预约。",
        "『{cn}全年随到随有，内容不变。』——实际菜式和供应时段会轮换。",
        "香港餐牌常用『餐單／午市』；内地常用『菜单／午间』。写{en}时注明供应日期及是否需预约。",
    )),
    (_DINING_TERMS, CopyContext(
        ("OpenRice", "大众点评", "微信"),
        "{en} | Check our dining policies before visiting.",
        "到店前可先查看{hk}及用餐安排，有疑問歡迎致電。",
        "到店前可以先确认{cn}和用餐规则，有问题欢迎电话咨询。",
        "『{cn}现场再说，页面无须提示。』——隐去会影响到店决定的条款。",
        "香港可在餐單旁标『{hk}』；内地团购详情写『{cn}』。如涉及费用或截止时段，直接列出数额或当地时间。",
    )),
    (food.MENU_DISHES, CopyContext(
        ("OpenRice", "大众点评", "小红书"),
        "{en} | On this week's menu. Ask the team what goes well with this dish.",
        "本週餐單有{hk}，想配其他菜式，不妨問問店員。",
        "这周菜单上有{cn}，还没决定怎么搭配的话，可以问问店员。",
        "『{cn}，招牌秘方，原料一律保密。』——应能说明主要食材与过敏原。",
        "英文餐牌可用『{en}』保留菜式特点。港陆菜名尽量写主要食材及做法，别用一个『秘制』代替。",
    )),
    (food.COOKING_METHODS, CopyContext(
        ("OpenRice", "大众点评", "官网"),
        "From our kitchen: look for {en} on the menu and ask about the preparation.",
        "睇餐單見到『{hk}』？歡迎向店員查詢食材同煮法。",
        "菜单上标注了「{cn}」，想了解做法和配料，可以直接问店员。",
        "『采用{cn}，保证人人都喜欢。』——工艺不代表所有人的口味。",
        "『{hk}／{cn}』用来交代真实工序。食材产地、烹调时间、营养信息应另外列明。",
    )),
    (food.BAKERY, CopyContext(
        ("IG", "小红书", "外卖平台"),
        "{en} | In the pastry case today. Ask when the next batch comes out.",
        "今日餅櫃有{hk}，想試新鮮出爐嘅可以問吓下一爐幾點。",
        "今天烘焙柜有{cn}，想趁热吃可以问问下一炉几点出炉。",
        "『{cn}口感有层次，所以完全不含乳制品。』——质地与配料无关。",
        "香港常说『牛油、朱古力、吉士』，内地常说『黄油、巧克力、卡仕达』。有过敏提示时附上实际配料。",
    )),
    (food.COFFEE_PROVENANCE, CopyContext(
        ("官网", "IG", "小红书"),
        "{en} | Ask the barista about this week's beans and try a cup at the brew bar.",
        "想了解『{hk}』？今個星期到手沖吧，試飲再同咖啡師傾吓。",
        "想了解「{cn}」？这周来手冲吧喝一杯，顺便和咖啡师聊聊选豆。",
        "『{cn}，只凭名字就能保证杯杯同味。』——批次与萃取都会改变表现。",
        "豆卡可并列『{hk}／{cn}』和实际产地、处理法、烘焙日。别把产地、拼配与处理法混写。",
    )),
    (food.COFFEE_NOTES, CopyContext(
        ("IG", "小红书", "官网"),
        "Take a moment between sips and look for {en} as the coffee cools.",
        "咖啡放涼少少再飲，{hk}會更容易察覺。",
        "让咖啡稍微凉一会儿再喝，更容易感受到{cn}。",
        "『尝到{cn}，说明咖啡豆里加了同名配料。』——风味描述不等于配料表。",
        "用『{hk}／{cn}』描述实测的香气或口感，区分风味联想、人工调味和实际添加原料。",
    )),
    (food.CAFE_DRINKS, CopyContext(
        ("IG", "小红书", "大众点评"),
        "On the drinks board: {en}. Ask the barista how we make it.",
        "飲品餐牌有{hk}，想知點沖，可以問吓咖啡師。",
        "饮品单上有{cn}，感兴趣的话，可以请咖啡师讲讲做法。",
        "『{cn}，随意替换基底和做法，口味完全一样。』——饮品名称应对应实际做法。",
        "对外可以并列『{en}』与本地中文名。冷热、杯量、奶种及咖啡因信息按门店实际出品标注。",
    )),
    (food.WINE_TASTING, CopyContext(
        ("OpenRice", "官网", "微信"),
        "{en} | Ask our sommelier what to look for and which dish to pair it with.",
        "想了解{hk}？請侍酒師講講風格，再揀道菜一齊試。",
        "对{cn}感兴趣？可以请侍酒师介绍风格，再搭一道菜尝尝。",
        "『{cn}，任何年份、产地喝起来都一样。』——酒款表现取决于原料和工艺。",
        "香港可说『試飲／配搭』，内地常说『品鉴／配餐』。酒款页面注明产区、酒精度及试饮份量。",
    )),
    (food.COCKTAILS, CopyContext(
        ("IG", "OpenRice", "小红书"),
        "Curious about {en}? Ask the bartender what's in the glass.",
        "對{hk}有興趣？可以問調酒師用咗咩材料、味道偏甜定偏乾。",
        "想试试{cn}？可以先问调酒师配方和甜度，再决定点哪一款。",
        "『{cn}，喝起来清爽就等于不含酒精。』——口感不能替代酒精度信息。",
        "香港酒牌常写『雞尾酒／特飲』，内地常写『特调』。区分有酒精、低度和无酒精，勿靠甜度判断。",
    )),
    (food.BEER_SAKE, CopyContext(
        ("IG", "OpenRice", "小红书"),
        "Try {en} alongside a small plate. Ask the team about the style and serving size.",
        "想小酌，可以揀{hk}配份小食；杯量同酒精度可向店員查詢。",
        "想小酌可以点{cn}搭一份小食，杯量和酒精度可以先问店员。",
        "『{cn}入口轻盈，酒精度一定很低。』——请按标签或店家信息核对。",
        "酒牌可并列『{en}』和本地名；生啤是出品方式，清酒等级是酿造分类，都不能直接换算为酒精度。",
    )),
)

TRAVEL_FAMILIES = (
    (travel.ROOM_TYPES, CopyContext(
        ("酒店官网", "Booking.com", "携程"),
        "{en} | Check the room photos, bed layout and guest capacity before booking.",
        "考慮訂{hk}？可以先睇相、床型同可入住人數。",
        "想订{cn}？先看一下房型图、床位安排和入住人数限制。",
        "『{cn}的房间大小、景观、床位全部一样。』——实际配置要看这间酒店。",
        "香港可写『{hk}』，内地写『{cn}』。房型页同时写明可住人数、床宽、景观范围，避免只写等级名。",
    )),
    (travel.ROOM_FEATURES, CopyContext(
        ("酒店官网", "Booking.com", "携程"),
        "Need {en} for your stay? Check that your chosen room includes it before booking.",
        "想用{hk}？落訂前睇清楚所選房型有冇提供。",
        "需要{cn}的话，下单前可以先确认所选房型是否提供。",
        "『见到{cn}的照片，就代表每间房都提供。』——设施可能只在指定房型。",
        "房型比较页可标『{hk}／{cn}』，区分标准配置、需申请项目和额外付费项目。",
    )),
    (travel.STAY_PLANS, CopyContext(
        ("酒店官网", "携程", "微信"),
        "Explore {en} and check the dates and inclusions before you reserve.",
        "想訂{hk}？先睇可入住日期、適用房型同包含嘅禮遇。",
        "想订{cn}，可以先看可用日期、适用房型和包含哪些权益。",
        "『订了{cn}，酒店内所有项目都免费。』——套餐只涵盖明确列出的权益。",
        "香港促销常写『房價／套票／禮遇』，内地常写『房价／套餐／权益』。把房晚、适用人数和预约条件列出来。",
    )),
    (travel.BOOKING_POLICIES, CopyContext(
        ("酒店官网", "Booking.com", "携程"),
        "{en} | Review the terms for your dates and room rate before you confirm.",
        "確認訂房前，請睇清楚{hk}，條款會按入住日子同房價而定。",
        "确认预订前请查看{cn}，具体安排以所选日期和订单条款为准。",
        "『{cn}不影响预订，付款后再看。』——关键条款应在付款前可见。",
        "把『{hk}／{cn}』放在价格及付款按钮附近；日期和时间使用酒店所在地的时区。",
    )),
    (travel.GUEST_SERVICES, CopyContext(
        ("酒店官网", "微信", "EDM"),
        "{en} | Ask reception about availability, hours and any charges.",
        "想用{hk}？可向酒店前台查詢服務時間同收費。",
        "想使用{cn}，可以先问酒店前台开放时间、预约方式和费用。",
        "『所有住客都可随时免费使用{cn}。』——权益可能限房型、时段或人数。",
        "香港品牌页常称『禮遇』，内地常称『权益』。明确服务对象、是否免费、预约方式和每日适用时段。",
    )),
    (travel.TRANSIT, CopyContext(
        ("酒店官网", "携程", "WhatsApp"),
        "{en} | Confirm the departure details before you set off.",
        "出發前請確認{hk}詳情，包括集合地點及出發時間。",
        "出发前建议核对{cn}的时间和地点，以免耽误行程。",
        "『{cn}只要到了就能办，行程细节不用提前核对。』——可能受班次、航站楼或预订条件限制。",
        "香港常写『接送／穿梭巴士』，内地常写『接送／接驳巴士』。交通页用当地时间并标清车辆、站点或航站楼。",
    )),
    (travel.OUTDOORS, CopyContext(
        ("目的地官网", "小红书", "IG"),
        "{en} | Check the conditions and what to bring before heading out.",
        "計劃參加{hk}？出發前睇吓天氣、路線同裝備提示。",
        "准备体验{cn}？出发前先看看天气、路线和装备建议。",
        "『{cn}风雨无阻，谁都能直接参加。』——天气、装备和身体要求需提前披露。",
        "香港常写『行山／導賞』，内地常写『徒步／导览』。写明难度、集合点与恶劣天气安排，野生动物不保证出现。",
    )),
    (travel.CULTURAL_EXPERIENCES, CopyContext(
        ("场馆官网", "微信", "小红书"),
        "{en} | Check the venue and times before planning your visit.",
        "想睇{hk}？出發前先睇場地同開放時間，有場次就揀定時段。",
        "想体验{cn}，可以提前确认地点、开放时间和是否需要预约。",
        "『{cn}每天开放，也不用预约。』——实际开放时间和参与方式应核实。",
        "香港场馆常用『導賞／體驗班』，内地常用『导览／体验课』。附活动语言、地点和所需预约条件。",
    )),
    (travel.TICKETING, CopyContext(
        ("场馆官网", "携程", "微信"),
        "{en} | Review the entry times and eligibility before you buy.",
        "購買前請睇清{hk}嘅入場時段同適用條件。",
        "购票前请先查看{cn}的入场时段和使用条件。",
        "『买了{cn}，任何一天、任何人都能用。』——可能限制日期、对象或入场次数。",
        "香港常写『門票／換領』，内地常写『门票／兑换』。在付款前注明有效期、凭证和退改条件。",
    )),
    (travel.PROPERTY_TYPES, CopyContext(
        ("酒店官网", "Booking.com", "携程"),
        "{en} | See what is included and how to get here before you book.",
        "預訂{hk}前，不妨睇吓住宿配套、位置同前往方法。",
        "预订{cn}前，可以看看具体配套、位置和到达方式。",
        "『{cn}的名称写在这儿，就能保证所有配套都有。』——住宿类型不等于设施清单。",
        "介绍『{hk}／{cn}』时，以实地设施及服务范围为准。品牌定位不能替代房型、交通或无障碍信息。",
    )),
)


def build_food_travel_terms():
    """Yield stable editorial records for both verticals in source order."""
    for category, families in (
        ("餐饮与酒水", FOOD_FAMILIES), ("文旅与酒店", TRAVEL_FAMILIES)
    ):
        for source, context in families:
            yield from _entries(category, source, context)
