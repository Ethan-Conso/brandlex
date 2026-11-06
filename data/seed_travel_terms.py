"""Editorial phrase families for accommodation and visitor experiences.

Rows contain EN, HK, CN, a search alias, and a distinct definition suitable for
the booking, itinerary, or property context of that phrase.
"""

ROOM_TYPES = """
Standard Room|標準客房|标准客房|standard guest room|酒店入门级常设房型，通常不含指定景观或额外空间。
Superior Room|高級客房|高级客房|superior guest room|常比标准房面积更大或配置更好，定义依酒店房型表。
Deluxe Room|豪華客房|豪华客房|deluxe guest room|酒店为特定面积、位置或设施组合使用的房型名称。
Executive Room|行政客房|行政客房|club guest room|面向行政楼层或含商务便利设施的客房，酒廊权益需另核实。
King Room|特大床客房|特大床房|king-bedded room|配置一张特大双人床的客房，实际床宽按酒店说明。
Queen Room|大床客房|大床房|queen-bedded room|配置一张大号双人床，尺寸比特大床通常更小。
Twin Room|雙床客房|双床房|twin-bedded room|房内有两张分开的床，床宽不一定相同。
Hollywood Twin|並床式雙床房|好莱坞双床房|joined twin beds|两张单人床可并列摆放成宽床布局。
Double-Double Room|兩張雙人床客房|双大床房|two double beds|房内有两张可供双人使用的床，实际入住人数以房规为准。
Triple Room|三人客房|三人间|room for three|设有三位住客的床位组合，可为三床或大床加单床。
Family Room|家庭客房|家庭房|family guest room|按家庭人数与儿童需求配置睡眠空间及设施。
Bunk-Bed Room|上下格床客房|上下铺客房|bunk room|使用上下铺提高容纳人数，儿童使用需看年龄限制。
Connecting Rooms|相連客房|连通房|interconnecting rooms|两间独立房之间有内部连通门，可不用经过走廊。
Adjoining Rooms|相鄰客房|相邻房|rooms next door|客房紧挨或接近，未必有可以互通的内门。
Accessible Room|無障礙客房|无障碍客房|wheelchair-accessible room|为有行动需求的旅客配置门宽、浴室扶手等可达性设施。
Studio Suite|開放式套房|开间套房|open-plan suite|睡眠区和起居区位于同一开放空间，通常没有隔门。
Junior Suite|小型套房|小型套房|junior guest suite|比一般客房有更多起居空间，未必拥有独立客厅。
One-Bedroom Suite|一房套房|一居室套房|separate-bedroom suite|卧室和客厅分开，通常有门可独立使用。
Family Suite|家庭套房|家庭套房|multi-room family suite|以家庭同住为目标，组合卧室与较宽敞的公共空间。
Presidential Suite|總統套房|总统套房|presidential guest suite|酒店高规格套房名称，通常设有多个独立空间。
Duplex Suite|複式套房|复式套房|split-level suite|室内由楼梯连接上下两层，活动空间与睡眠区可分隔。
Penthouse Suite|頂層套房|顶层套房|top-floor suite|设在楼宇顶层的套房，景观和露台设施视物业而定。
Harbour View Room|海港景客房|海港景房|harbor view room|客房可望见港湾或海港景色，视线范围与楼层有关。
Ocean View Room|海景客房|海景房|sea view room|客房可望见海面，未必紧贴海岸或全无遮挡。
Oceanfront Room|臨海客房|临海房|direct oceanfront room|客房位于朝海的建筑面，通常比一般海景房更直接面海。
Partial Sea View|側海景|部分海景|side sea view|从房间部分位置能看见海面，未保证全景。
City View Room|城市景觀客房|城景房|cityscape room|客房朝向城市楼宇、街景或天际线。
Garden View Room|園景客房|园景房|garden-facing room|客房的指定窗户朝向花园或绿化区域。
Pool Access Room|直通泳池客房|直通泳池房|swim-up room|从房间露台等出口可直接进入相连泳池区域。
Balcony Room|連露台客房|带阳台客房|room with balcony|客房有可使用的户外阳台，尺寸和私密性需按房型说明。
"""

ROOM_FEATURES = """
Pillow Menu|枕頭選單|枕头菜单|pillow selection|旅客可按软硬、高低或材质选择睡枕。
Blackout Curtains|遮光窗簾|遮光窗帘|room-darkening drapes|能显著减少外部光线进入房间的窗帘。
Sound-Insulated Windows|隔音玻璃窗|隔音窗|acoustic glazing|采用隔音结构或玻璃降低室外噪声的窗。
Floor-to-Ceiling Windows|落地玻璃窗|落地窗|full-height windows|从地板延伸至接近天花的窗，能提供较开阔视野。
Walk-In Wardrobe|步入式衣帽間|步入式衣帽间|walk-in closet|可进入其中整理行李、衣物的独立储物空间。
Kitchenette|簡易廚房|简易厨房|in-room kitchenette|包含基础备餐设备的房内小厨房，灶具配置不统一。
Full Kitchen|設備齊全的廚房|全配厨房|fully equipped kitchen|通常配备炉具、冰箱和烹饪工具，可准备完整餐食。
In-Room Minibar|客房迷你吧|客房迷你吧|guestroom minibar|房内提供的饮品和零食，部分或全部可能另收费。
Minibar Credit|迷你吧消費額|迷你吧消费额度|minibar allowance|可抵扣指定迷你吧项目的额度，未使用余额未必可退。
Rain Shower|雨淋式花灑|雨淋式淋浴|rainfall shower|从上方大面积出水的花洒设计。
Soaking Tub|浸浴浴缸|泡澡浴缸|deep soaking bathtub|有足够深度用于浸泡的浴缸，不代表具有按摩功能。
Separate Bath and Shower|獨立浴缸及花灑|浴缸淋浴分设|separate bathtub and shower|浴缸和淋浴区各自独立，客人可任选。
Grab Rails|浴室扶手|无障碍扶手|grab bars|在厕所、淋浴或浴缸周边提供可抓握支撑。
Roll-In Shower|無門檻淋浴間|轮椅可进入淋浴间|wheel-in shower|无明显高差且为轮椅进入留有空间的淋浴区。
Portable Cot|便攜式嬰兒床|便携婴儿床|travel crib|可依请求搬入客房的婴幼儿睡床，需按安全年龄使用。
Rollaway Bed|摺疊加床|折叠加床|roll-away bed|根据房间面积与人数限制临时增设的可移动床铺。
Sofa Bed|梳化床|沙发床|convertible sofa|白天作沙发、展开后作睡床的家具。
In-Room Safe|客房保險箱|客房保险箱|guest room safe|住客可自行锁存物品的小型保险箱。
Work Desk|客房書枱|客房办公桌|in-room desk|供电脑工作、书写或视频通话使用的桌面。
Universal Power Outlets|多制式插座|多国制式插座|international power sockets|支持不止一种插头规格的插座，供电规格仍须核对。
Bedside Charging|床邊充電位|床头充电位|bedside charging ports|可在床头方便接入电源或设备充电线。
Private Plunge Pool|私人小泳池|私享泡池|private dipping pool|套房或别墅内的小型戏水池，深度与面积有限。
Private Terrace|私人平台|私家露台|exclusive-use terrace|房间宾客独用的户外平台，与公共露台区分。
Outdoor Shower|戶外花灑|户外淋浴|open-air shower|设于室外或露天空间的淋浴设施，私密性依布局。
Separate Living Area|獨立起居空間|独立起居区|separate sitting area|与睡眠区域明确分隔的起居区，不一定有隔门。
Pet Bed|寵物睡床|宠物床|dog bed amenity|为入住宠物预备的垫子或小床，通常需提前申请。
"""

STAY_PLANS = """
Staycation|宅度假|城市度假|local hotel staycation|在居住地附近订酒店短住，享用餐饮或休闲设施。
Bed and Breakfast Rate|客房連早餐房價|含早房价|B&B rate|住宿价格内包含指定客人的早餐。
Room-Only Rate|淨房價|仅住宿房价|accommodation only rate|仅含客房，不含餐饮与其他增值服务。
Half Board|半膳住宿|半餐住宿|half-board package|房价内含早餐及另一餐，餐型按住宿方案说明。
Full Board|全膳住宿|全餐住宿|full-board package|住宿附早餐、午餐、晚餐，不一定含饮料。
All-Inclusive Stay|全包式住宿|一价全包度假|all-inclusive package|房价组合住宿及指定餐饮、饮品和活动，范围须列明。
Direct Booking Rate|官網直訂房價|官网直订价|book direct rate|通过酒店自营渠道购买的房价，可能另附直订礼遇。
Advance Purchase Rate|提早預訂房價|提前预订房价|advance booking rate|需在入住日前一定时间下单的优惠价，条款可能更严格。
Flexible Rate|彈性房價|灵活房价|flexible booking rate|允许按条款免费修改或取消的房价，逾期仍可能收费。
Non-Refundable Rate|不可退款房價|不可退款房价|prepaid non-refundable rate|付款后原则上不能退款的房价，实际修改规则依订单。
Members' Rate|會員專享房價|会员专享价|member hotel rate|面向登录会员的特定房价，并非所有房型均参加。
Long-Stay Offer|長住優惠|长住特惠|extended-stay deal|满足连续入住晚数条件后适用的住宿优惠。
Midweek Stay Offer|平日住宿優惠|工作日入住优惠|weekday accommodation offer|适用于指定周间入住日期的住宿推广。
Weekend Getaway Package|週末短住套票|周末微度假套餐|weekend escape package|为周末短住组合客房及一项或多项体验。
Family Stay Package|親子住宿套票|亲子度假套餐|family getaway package|把家庭房、儿童活动或儿童餐等权益组合销售。
Romantic Getaway|雙人浪漫住宿|双人浪漫度假|couples escape|面向两人短住的体验组合，可能含双人餐或布置。
Anniversary Stay|週年紀念住宿套票|纪念日住宿套餐|anniversary hotel package|为周年纪念设计的住宿，可加订花束、餐饮或其他安排。
Spa Retreat Package|水療住宿套票|水疗度假套餐|spa stay package|把住宿和指定水疗护理组合，通常需另预约时间。
Dine-and-Stay Package|住宿連餐飲套票|住宿餐饮套餐|stay and dine package|住宿附指定正餐、餐券或餐饮消费额的组合。
Michelin-Starred Dining Stay|米芝蓮星級餐飲住宿套票|米其林星级餐饮住宿套餐|Michelin dining stay|住宿和在指定获星餐厅用餐的权益组合，须核实奖项年份及具体餐厅。
Afternoon Tea Stay|住宿連下午茶套票|住宿下午茶套餐|afternoon tea hotel package|住店方案含指定人数的下午茶，餐期与入住日可能不同。
Theme Park Hotel Package|酒店連主題樂園套票|乐园门票加酒店套餐|park and hotel package|把酒店和指定乐园门票一起销售，入园可能需预约。
Rail and Hotel Package|火車連酒店套票|火车票加酒店套餐|train and stay package|为同一行程组合车票与酒店，退改规则可能分别适用。
Flight and Hotel Package|機票連酒店套票|机票加酒店套餐|flight plus hotel|同时预订机票与住宿的旅行产品。
Ski and Stay Package|滑雪住宿套票|滑雪加住宿套餐|ski hotel package|把住宿与雪票、租具或课程等项目组合。
Golf and Stay Package|高爾夫住宿套票|高尔夫住宿套餐|golf hotel break|住宿和指定球场的开球时段等高尔夫权益组合。
Resort Credit|度假村消費額|度假村消费金|resort spending credit|用于抵扣度假村内符合条件的餐饮、护理或活动的金额。
Hotel Gift Voucher|酒店禮券|酒店礼品券|hotel gift certificate|可赠予他人按规则兑换房晚、消费金额或服务的凭证。
"""

BOOKING_POLICIES = """
Best Available Rate|當日最優惠公開房價|最优可订公开房价|BAR rate|酒店在指定渠道和条件下公开销售的标准动态房价。
Rate Parity|房價一致安排|渠道同价|hotel price parity|在约定的可比条件下让各渠道房价保持一致。
Booking Deposit|預訂訂金|预订定金|reservation deposit|为保留预订需预先缴付的款项，抵扣或退还按条款。
Security Deposit|入住按金|入住押金|hotel damage deposit|用于担保额外消费或损坏费用的款项，通常离店结算后退回。
Card Preauthorization|信用卡預先授權|信用卡预授权|card pre-authorisation hold|在卡片额度内暂时预留金额，并不等于已最终扣款。
Incidental Charges|住宿雜項收費|住宿杂项费用|incidental fees|除房价之外产生的餐饮、停车或其他住客消费。
Resort Fee|度假村設施費|度假村设施费|destination amenity fee|某些物业单列的每日费用，覆盖范围需按酒店披露。
Tourism Tax|旅遊住宿稅|旅游住宿税|city accommodation tax|某些目的地按房晚、房价或人头收取的住宿相关税费。
Cancellation Window|免費取消時限|免费取消截止时间|free cancellation deadline|预订可免费取消的最晚日期和当地时间。
Cancellation Fee|取消預訂費用|取消预订手续费|hotel cancellation penalty|在特定日期之后取消预订时收取的费用。
No-Show Fee|逾時未入住收費|未到店费用|hotel no show charge|客人未按期入住且未按要求取消时产生的费用。
Modification Policy|更改預訂條款|订单改期规则|booking amendment terms|规定可改日期、房型或人数的时限、差价和费用。
Minimum Stay|最少入住晚數|最少连住晚数|minimum length of stay|指定房价或日期要求旅客连续预订的最低晚数。
Maximum Occupancy|最高入住人數|房型限住人数|max guests per room|房间可接待的最大人数，成人与儿童的限制可能不同。
Extra Guest Charge|額外住客收費|加人费用|additional occupant fee|超过房价包含的基础入住人数时收取的费用。
Child Stay Policy|小童入住條款|儿童入住政策|children accommodation policy|规定儿童的年龄范围、床位、餐费与额外收费。
Pet Policy|寵物入住條款|宠物入住须知|pet accommodation policy|说明可携宠物种类、体重限制、费用及活动范围。
Blackout Dates|不適用日期|不可用日期|excluded stay dates|优惠、兑换或房券不能使用的指定日期。
Subject to Room Availability|視乎客房供應情況|以实际房态为准|room availability applies|表示升级、加床或指定房型需视当时供应情况安排。
Guaranteed Reservation|保證留房預訂|担保预订|guaranteed booking|按卡片担保或预付安排保留房间，迟到或未到店仍受条款约束。
Waitlisted Booking|候補預訂|候补预约|reservation waitlist|当前没有确认供应，名额释放后才可能获确认。
Check-In Cutoff|最遲登記入住時間|最晚办理入住时间|latest check-in time|仍可正常登记入住的最晚时段，迟抵需提前沟通。
Check-Out Time|退房時間|最晚退房时间|departure time hotel|住客按原房价应交还客房的截止时间。
Early Departure Fee|提早退房費用|提前离店费|early checkout charge|客人提前结束住宿时按预订条件可能收取的费用。
Booking Confirmation|預訂確認書|预订确认单|reservation confirmation|列出房型、日期、价格和预订识别信息的确认文件。
"""

GUEST_SERVICES = """
Executive Lounge Access|行政酒廊禮遇|行政酒廊权益|club lounge access|符合条件的住客可进入行政酒廊并使用指定时段的服务。
Club Lounge Breakfast|行政酒廊早餐|行政酒廊早餐|executive lounge breakfast|在行政酒廊指定时段供应给合资格住客的早餐。
Evening Canapés|黃昏佐酒小食|晚间佐酒小食|evening hors d'oeuvres|傍晚在酒廊配合饮品供应的少量咸点。
Afternoon Refreshments|午後茶點|午后茶歇|lounge afternoon snacks|下午供应的轻食和饮料，份量与品种依酒店说明。
Welcome Drink|迎賓飲品|欢迎饮品|arrival drink|客人抵达或到指定场所时获赠的饮料。
Welcome Amenity|迎賓小禮|欢迎礼遇|welcome gift amenity|酒店在客房为特定住客预备的小食、饮品或礼品。
Turndown Service|晚間開床服務|夜床服务|evening turndown|晚间整理床铺与客房，方便客人就寝。
In-Room Dining|客房送餐|客房送餐服务|room service dining|住客从菜单订餐后由酒店送到房间。
Express Check-In|特快登記入住|快速入住|fast-track check-in|通过已填资料、独立柜台等方式减少办理入住所需时间。
Mobile Check-In|手機登記入住|手机自助入住|online hotel check-in|在手机上提前提交入住资料，取钥匙仍可能需核验身份。
Digital Room Key|手機房卡|手机电子房卡|mobile key|在支持的手机或应用上启用可开客房门的电子钥匙。
Express Check-Out|特快退房|快速退房|express departure|按规定确认账单并快速退房，无需完整柜台流程。
Early Check-In|提早入住|提前入住|early room access|在标准时间之前交付客房，需看空房或付费条件。
Late Check-Out|延遲退房|延时退房|extended checkout|允许晚于常规时间交还客房，是否收费需说明。
Room Upgrade|客房升級|房型升级|complimentary room upgrade|从已订房型换到较高类别，可能需付差价或受房态限制。
Luggage Storage|行李寄存|行李寄存|left luggage service|酒店代为临时保管行李，常在入住前或离店后使用。
Bell Service|行李員服務|礼宾行李服务|porter service|由行李员协助把行李运送到客房、门口或车辆。
Concierge Service|禮賓服務|礼宾服务|guest concierge|酒店协助预订餐厅、安排交通或提供当地行程建议。
Butler Service|管家服務|私人管家服务|personal butler|由专人协调套房住客的入住、餐饮或行程需求。
Valet Parking|代客泊車|代客泊车|valet service|工作人员接收车辆、代为停放并在客人离开时取回。
Laundry Service|洗衣服務|客房洗衣服务|hotel garment cleaning|代为清洗、烘干或熨烫住客衣物，时限和收费按件说明。
Pressing Service|熨衣服務|熨烫服务|garment pressing|为住客熨烫衣物去皱，未必包含洗涤。
Shoe Shine Service|擦鞋服務|擦鞋服务|shoe polishing|为住客清洁或抛光可护理的鞋面。
Kids' Club|兒童天地|儿童俱乐部|resort kids club|酒店内为儿童提供游戏或带领活动的场地。
Babysitting Service|幼兒看顧服務|儿童看护服务|hotel childminding|经预订由工作人员照看儿童的服务，年龄和收费需明确。
Poolside Cabana|池畔私人涼亭|泳池边私享凉亭|pool cabana|泳池边可预订的遮阳休憩空间，有时配餐饮消费额。
"""

TRANSIT = """
Airport Transfer|機場接送|机场接送|hotel airport transfer|机场与酒店等指定地点之间的预订接送服务。
Arrival Transfer|接機服務|接机服务|airport arrival pick-up|从机场抵达区接旅客前往酒店或其他目的地。
Departure Transfer|送機服務|送机服务|airport drop-off|在离境前按约定时间把旅客从住宿地点送至机场。
Round-Trip Transfer|來回接送|往返接送|return shuttle transfer|一次预订包含去程和回程两段接送。
Private Transfer|專車接送|专车接送|exclusive car transfer|为该订单独立安排车辆，不与其他乘客拼乘。
Shared Transfer|共乘接送|拼车接送|shared shuttle|多个订单旅客共乘，可能途经其他酒店。
Complimentary Shuttle|免費穿梭巴士|免费接驳巴士|free shuttle bus|不用额外购票、在指定站点与时间行驶的接驳车。
Scheduled Shuttle|定時穿梭巴士|定点班车|timetabled shuttle|按固定班次发车，不按客人选择时间单独出车。
Station Pick-Up|車站接送|接站服务|railway station pick-up|司机在约定车站出口接旅客前往住宿地。
Hotel Courtesy Car|酒店禮賓專車|酒店礼宾用车|hotel house car|酒店安排的住客短程用车，服务范围与费用按物业。
Meet and Greet|舉牌迎接|举牌接待|airport meet-and-assist|接待人员在约定位置辨认并引导旅客与司机会合。
Accessible Transfer|無障礙接送|无障碍接驳|wheelchair-friendly transfer|为轮椅等需求提供适配的车辆和上下车条件。
Car Seat Request|預約兒童安全座椅|预约儿童安全座椅|child seat on request|接送时提前安排与儿童年龄体重匹配的安全座椅。
Luggage Allowance|行李限額|行李额度|baggage allowance|行程或车票允许携带的行李件数、重量或尺寸。
Carry-On Baggage|手提行李|随身行李|cabin baggage|可由旅客随身带入客舱并按要求存放的行李。
Checked Baggage|寄艙行李|托运行李|hold baggage|交由承运人放在行李舱运输的行李。
Priority Boarding|優先登機|优先登机|early boarding access|符合条件的旅客可在部分普通旅客之前登机。
Airport Fast Track|機場快速通道|机场快速通道|fast-track airport service|使用机场指定的优先流程，覆盖安检或证件查验需说明。
Airport Lounge Pass|機場貴賓室通行證|机场贵宾厅使用券|airport lounge entry|在符合条件的航站楼和时段进入指定机场贵宾室。
Early-Bird Airfare|早鳥機票|早鸟机票|advance airfare deal|提前购票才能获得的机票价格，库存和出行日期受限制。
Open-Jaw Itinerary|開口程機票|开口程机票|open jaw flight itinerary|去程到达城市与回程出发城市不同等非闭环机票组合。
Stopover Package|中途停留套票|中转停留套餐|stopover hotel deal|航程中在中转城市停留较长时间并组合住宿或观光。
Rail Pass|鐵路周遊券|铁路通票|train travel pass|在有效期和适用线路内搭乘指定列车的通票。
Ferry Crossing|渡輪航程|轮渡航程|ferry trip|以渡轮连接水域两边或岛屿，按码头与班次安排。
Water Taxi|水上的士|水上出租船|water cab|在指定码头之间接载乘客的小型水上交通服务。
Self-Drive Itinerary|自駕遊路線|自驾路线|road trip itinerary|以自行驾驶连接多个目的地，并安排停靠、停车或住宿。
Bike Rental|單車租借|自行车租赁|bicycle hire|按时段或里程租用自行车，可另配头盔与路线图。
"""

OUTDOORS = """
Guided Hike|行山導賞團|徒步向导团|guided trekking walk|由熟悉路线的人员领队，并介绍沿途地貌或生态。
Self-Guided Walk|自助步行遊|自助步行游|independent walking route|旅客按地图、路标或语音资料自行完成的步行行程。
Coastal Trail|海岸步道|滨海步道|coastal walking path|沿海岸连接景点的步行路线，开放状况受天气影响。
Country Park Walk|郊野公園健行|郊野公园徒步|country park hike|在郊野公园指定路线进行的步行体验。
Sunrise Hike|日出行山團|日出徒步团|sunrise trek|配合日出时刻出发，到指定观景处的早晨徒步。
Night Hike|夜行導賞|夜间徒步|evening guided hike|在天黑后行走的路线，照明、同伴和难度需提前说明。
Scenic Lookout|景觀瞭望點|观景台|scenic viewpoint|可眺望山海或城市的指定观景点。
Clifftop Walk|崖頂步道|悬崖步道|cliff-top walking route|沿高处崖边布设的路线，风险与护栏情况需说明。
Mangrove Kayaking|紅樹林獨木舟|红树林皮划艇|mangrove paddle|乘小艇在红树林水域观察湿地，通常依潮汐安排。
Sea Kayaking|海上獨木舟|海上皮划艇|coastal kayaking|在海湾或沿岸水域划行，受浪高与风向影响。
Stand-Up Paddleboarding|直立板體驗|桨板体验|SUP experience|站在浮板上用长桨划行的水上运动。
Snorkelling Trip|浮潛之旅|浮潜体验|snorkeling tour|借面镜与呼吸管在水面观察水下生物。
Introductory Dive|初階潛水體驗|体验潜水|discover scuba dive|在专业人员指导下进行的入门潜水活动。
Reef-Safe Snorkel Briefing|珊瑚保育浮潛簡介|浮潜珊瑚保护说明|reef etiquette briefing|下水前说明如何避免踩踏、触碰或损伤珊瑚。
Dolphin-Watching Tour|海豚觀賞團|观豚船游|dolphin watching cruise|乘船寻找并远距离观察海豚，不能保证遇见。
Birdwatching Tour|觀鳥導賞團|观鸟向导团|birding tour|在合适季节与地点观察鸟类，通常用望远镜辅助。
Wetland Boardwalk|濕地木棧道|湿地栈道|marsh boardwalk|架设在湿地上、供游客不踩入栖息地的步行道。
Stargazing Experience|觀星體驗|星空观测体验|night sky tour|在较暗地点观赏星空，受云量、月相与灯光影响。
Glamping|豪華露營|精致露营|glamorous camping|提供已搭帐篷、寝具等便利的露营住宿。
Campsite Pitch|營位|露营营位|tent pitch|供一组旅客搭设帐篷或停放指定露营设施的位置。
Forest Bathing|森林浴|森林疗愈漫步|shinrin-yoku|在林地放慢步速、观察感官体验的活动，不作治疗承诺。
Trail Running Route|越野跑路線|越野跑路线|trail run course|适合在非铺装路面跑步的路线，需说明爬升和补给。
Cycling Greenway|單車綠道|骑行绿道|cycle greenway|供自行车与步行等使用的绿色通道，分流方式依地区。
Rock-Climbing Taster|攀石體驗課|攀岩体验课|intro rock climbing|在指导与保护装备下体验基础攀岩动作的课程。
Picnic Site|野餐地點|野餐区|picnic ground|可铺垫或使用桌椅用餐的指定户外地点。
Seasonal Blossom Walk|時令賞花路線|当季赏花路线|blossom trail|按花季安排的步行路线，花期受天气和养护影响。
"""

CULTURAL_EXPERIENCES = """
Heritage Walk|歷史文化導賞|历史文化漫步|heritage walking tour|用步行连接历史建筑、街区与文化故事的导览。
Old Town Walking Tour|舊城漫遊導賞|古城步行导览|historic quarter walking tour|沿老街、街巷和老店观察聚落变迁的步行路线。
Architecture Tour|建築導賞|建筑导览|architectural tour|带领游客认识建筑风格、材料与设计背景。
Street Art Tour|街頭藝術導賞|街头艺术导览|mural walking tour|沿街欣赏壁画和公共艺术，并了解创作语境。
Market Food Tour|街市美食導賞|菜市场美食导览|market tasting tour|在当地市场了解食材并试吃指定摊位小食。
Food Heritage Tour|飲食文化導賞|饮食文化探访|culinary heritage walk|通过老店、工艺与招牌菜理解当地饮食传统。
Museum Highlights Tour|博物館精華導賞|博物馆重点展品导览|museum highlights walk|在有限时间内讲解馆内有代表性的藏品。
Curator-Led Tour|策展人導賞|策展人导览|curator's tour|由策展人讲解展品选择、展览主题与布展思路。
After-Hours Museum Visit|閉館後專場參觀|闭馆后专场参观|private after-hours viewing|在常规开放结束后为特定宾客开放的场次。
Permanent Collection|常設館藏|常设馆藏|permanent exhibition holdings|机构长期保存或展示的藏品，部分展件仍会轮换。
Temporary Exhibition|期間展覽|临时展览|limited-run exhibition|只在指定日期区间开放的展览。
Travelling Exhibition|巡迴展覽|巡回展览|touring exhibition|在多个城市或场馆按不同日期轮换展出的展览。
Open Studio|開放工作室|工作室开放日|artist studio visit|创作者在指定时段接待访客观看工作过程与作品。
Artist Talk|藝術家分享會|艺术家分享会|artist conversation|由创作者现场交流作品和方法的活动。
Audio Guide|語音導賞|语音导览|audio tour guide|通过设备或手机按展点播放讲解内容。
Multilingual Guided Tour|多語言導賞團|多语种导览团|multilingual tour|提供多种语言的导览场次，预约时需选择语言。
Hands-On Craft Workshop|手作體驗班|手工体验课|craft-making workshop|在导师协助下亲手制作指定手工成品。
Pottery Wheel Workshop|陶藝拉坯班|陶艺拉坯体验|wheel throwing class|使用陶轮给泥坯塑形的课程，烧制与取件另按安排。
Tea Ceremony Experience|茶道體驗|茶道体验|tea ceremony session|跟随主持人体验备器、泡茶、奉茶等过程。
Calligraphy Workshop|書法體驗班|书法体验课|brush calligraphy class|由导师指导基本笔法并书写作品。
Indigo Dyeing Workshop|藍染體驗班|蓝染体验课|indigo textile class|用靛蓝染料和绑扎等技法制成布艺图案。
Lantern-Making Workshop|紮燈籠體驗|灯笼制作体验|lantern craft class|组装骨架和纸面制作灯笼，材料与年龄限制依课程。
Neighbourhood Walk|社區漫遊|街区漫步|neighborhood tour|在居民生活街区以步行了解店铺、建筑与社区故事。
Night Market Tour|夜市導賞|夜市探访|guided night market walk|在夜市开放时段由导游带领探访摊位和饮食。
Photography Walk|攝影散步團|摄影采风|photo walk tour|跟随摄影向导寻找不同取景角度和光线的步行活动。
Community-Led Tour|社區主導導賞|社区居民带领的导览|local-led community tour|由社区参与设计和讲解，体现本地居民的经验与视角。
"""

TICKETING = """
Timed Entry|分時段入場|分时段入场|timed admission|入场票仅可在所选时间窗口使用，避免同时到场拥挤。
Open-Date Ticket|不指定日期門票|不定日门票|open dated admission|购票时未固定参观日期，仍有使用期限或预约规则。
Same-Day Ticket|即日門票|当日票|same day admission|当天购买并用于当天入场的门票。
Advance Ticket|預售門票|预售门票|advance admission ticket|在正式开场或使用日前提前出售的门票。
Admission Pass|入場證|入场通行证|admission ticket|在指定范围和有效时段内允许进入的凭证。
Attraction Pass|景點通行證|景区通票|multi-attraction pass|一张凭证可兑换多个景点或项目的入场资格。
Combination Ticket|聯票|联票|combo admission|把两个或更多参观项目合并成一张票。
Family Admission|家庭門票|家庭套票|family entrance ticket|按指定成人与儿童组合出售的家庭入场票。
Concession Ticket|特惠門票|优待票|reduced admission|向符合年龄、学生或其他资格者提供的低价门票。
Student Admission|學生門票|学生票|student rate ticket|面向持有效学生证明的访客的门票。
Senior Admission|長者門票|老年人优惠票|senior rate ticket|按规定年龄或证件资格适用的优惠门票。
Resident Admission|本地居民門票|本地居民优惠票|local resident ticket|向可证明在指定地区居住的访客提供的票种。
Annual Pass|全年通行證|年卡|annual membership pass|在规定年度或自激活日起一年内多次入场。
Season Pass|季度通行證|季卡|season admission pass|在指定活动季或开放季内反复入场。
Re-Entry|離場後再入場|二次入园|same day re-entry|在规则允许时离场后再次进入，可能需盖章或保留票券。
Skip-the-Line Entry|免排隊入場|快速入场|priority entrance lane|通过指定入口缩短验票队列时间，安检等流程仍适用。
Reserved Seating|劃位入座|对号入座|assigned seats|门票绑定具体座位，而非按到达先后选座。
General Admission|不設劃位門票|无指定座席门票|unreserved admission|可进入指定区域但不保证具体座位。
Mobile Ticket|手機電子門票|手机电子票|digital entry ticket|用手机展示可扫描凭证入场，无需纸本。
Ticket Redemption|換領門票|兑换门票|voucher redemption|按规则使用电子凭证、兑换码或实体券换取入场票。
Gate Price|現場票價|现场票价|walk-up ticket price|在入口票务处购买门票时适用的价格。
Booking Fee|訂票手續費|票务手续费|ticket handling fee|票务平台或售票处在票价以外收取的服务费用。
Accessibility Companion Ticket|無障礙同行者門票|无障碍陪同票|essential companion admission|符合条件的访客可为必要陪同人员申请的票。
Weather Contingency|惡劣天氣安排|恶劣天气应急安排|weather backup plan|活动因天气无法照常举行时采用的改期、替代方案或退款规则。
Sold-Out Session|額滿場次|已售罄场次|fully booked session|预订名额已达上限、目前无法再买票的指定场次。
"""

PROPERTY_TYPES = """
Boutique Hotel|精品酒店|精品酒店|design boutique hotel|房量通常较小、突出设计或个性化体验的酒店。
Design Hotel|設計酒店|设计酒店|design-led hotel|以建筑、室内设计或艺术策展作为主要识别点的酒店。
Heritage Hotel|歷史建築酒店|历史建筑酒店|heritage property|由具有历史背景的建筑改建或延续经营的酒店。
Business Hotel|商務酒店|商务酒店|corporate hotel|提供办公便利与会议配套、主要面向商旅客人的酒店。
Airport Hotel|機場酒店|机场酒店|airport accommodation|靠近机场或航站楼，为抵达与离境旅客提供住宿。
Transit Hotel|轉機酒店|中转酒店|layover hotel|为转机或过境的旅客提供短住，有些设在安检区域内。
Extended-Stay Hotel|長住酒店|长住酒店|long stay hotel|针对连续多晚住宿配置厨房、洗衣等便利的酒店。
Serviced Apartment|服務式住宅|服务式公寓|aparthotel apartment|有住宅布局并提供一定酒店式清洁或接待服务的住宿。
Beach Resort|海濱度假村|滨海度假酒店|beachfront resort|靠近海滩、结合住宿与海边休闲设施的度假物业。
Island Resort|離島度假村|海岛度假村|island retreat|位于岛屿上的度假住宿，交通可能需船只接驳。
Mountain Lodge|山間旅舍|山间小屋酒店|mountain retreat lodge|设于山区的住宿，常为徒步或避暑客人提供休憩。
Ski-In Ski-Out Hotel|滑雪直出直入酒店|滑进滑出酒店|slope-side ski hotel|客人可按路线和雪况从酒店附近滑入或滑出雪道。
Spa Resort|水療度假村|水疗度假酒店|wellness spa resort|以水疗护理与康养设施为主要度假体验的物业。
Hot Spring Resort|溫泉度假村|温泉度假酒店|hot springs resort|以温泉浸浴等设施作为主要服务的度假住宿。
Eco Lodge|生態旅舍|生态度假屋|eco-lodge|强调自然环境与运营影响管理的住宿，认证需单独核对。
Vineyard Stay|葡萄園住宿|葡萄酒庄住宿|winery stay|在葡萄园或酒庄经营范围内入住的体验。
Farm Stay|農莊住宿|农场民宿|farm accommodation|设在经营中的农场或农庄内的短期住宿。
Ryokan|日式旅館|日式传统旅馆|Japanese ryokan inn|有日式传统接待与房间布置的旅馆，餐食和浴场依店。
Capsule Hotel|膠囊酒店|胶囊旅馆|pod hotel|以相对独立的小型睡眠舱作住宿单位。
Youth Hostel|青年旅舍|青年旅舍|youth guest hostel|通常设共享寝室和公共空间，床位可分开预订。
Guesthouse|民宿旅館|家庭旅馆|guest house|小型住宿经营，服务和房间配置常因店而异。
Private Villa|獨立度假別墅|独栋度假别墅|exclusive-use villa|可由同一组旅客独用、通常有独立起居设施的房屋。
Overwater Villa|水上別墅|水上别墅|overwater bungalow|建于水面上方的独立度假客房，水深和通行方式需说明。
Adult-Only Resort|只限成人入住度假村|仅限成人度假村|adults-only resort|只接待符合最低年龄要求的旅客的度假物业。
Pet-Friendly Hotel|寵物友善酒店|宠物友好酒店|dog-friendly accommodation|在规定种类、数量与区域内允许携带宠物的酒店。
Convention Hotel|會展酒店|会展酒店|conference hotel|配备会议、宴会和住宿设施，可承接大型活动。
Conference Day Package|全日會議套票|全天会议套餐|day delegate rate|按日或人数组合场地、茶歇、餐食与设备的会议方案。
Residential Meeting Package|住宿連會議套票|会议住宿套餐|overnight conference package|把参会者住宿、会议设施与餐饮统一组合报价。
"""
