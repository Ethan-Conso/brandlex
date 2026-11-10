"""Editorial phrase families for accommodation and visitor experiences.

Rows contain EN, HK, CN, a search alias, and definitions in Chinese and English
for the relevant booking, itinerary, or property context.
"""

ROOM_TYPES = """
Standard Room|標準客房|标准客房|standard guest room|酒店入门级常设房型，通常不含指定景观或额外空间。|A hotel's entry-level room, typically without a specified view or extra space.
Superior Room|高級客房|高级客房|superior guest room|常比标准房面积更大或配置更好，定义依酒店房型表。|A room category often offering more space or better facilities than a standard room, depending on the hotel.
Deluxe Room|豪華客房|豪华客房|deluxe guest room|酒店为特定面积、位置或设施组合使用的房型名称。|A room category defined by a hotel for a particular combination of space, location or amenities.
Executive Room|行政客房|行政客房|club guest room|面向行政楼层或含商务便利设施的客房，酒廊权益需另核实。|A room on an executive floor or with business amenities, with any lounge access specified separately.
King Room|特大床客房|特大床房|king-bedded room|配置一张特大双人床的客房，实际床宽按酒店说明。|A guest room furnished with one king bed, whose exact width varies by hotel and market.
Queen Room|大床客房|大床房|queen-bedded room|配置一张大号双人床，尺寸比特大床通常更小。|A guest room with one queen bed, which is usually narrower than a king bed.
Twin Room|雙床客房|双床房|twin-bedded room|房内有两张分开的床，床宽不一定相同。|A guest room with two separate beds, which may differ in width.
Hollywood Twin|並床式雙床房|好莱坞双床房|joined twin beds|两张单人床可并列摆放成宽床布局。|A room with two single beds that can be placed side by side to form a wider sleeping surface.
Double-Double Room|兩張雙人床客房|双大床房|two double beds|房内有两张可供双人使用的床，实际入住人数以房规为准。|A guest room with two double beds, with occupancy subject to the property's rules.
Triple Room|三人客房|三人间|room for three|设有三位住客的床位组合，可为三床或大床加单床。|A room with sleeping space for three guests, such as three singles or a double and a single.
Family Room|家庭客房|家庭房|family guest room|按家庭人数与儿童需求配置睡眠空间及设施。|A room laid out to accommodate families, with sleeping arrangements and amenities suited to children.
Bunk-Bed Room|上下格床客房|上下铺客房|bunk room|使用上下铺提高容纳人数，儿童使用需看年龄限制。|A room with stacked beds that increases sleeping capacity, subject to safety and age limits.
Connecting Rooms|相連客房|连通房|interconnecting rooms|两间独立房之间有内部连通门，可不用经过走廊。|Two separate guest rooms linked by an internal door so guests can pass between them without entering the corridor.
Adjoining Rooms|相鄰客房|相邻房|rooms next door|客房紧挨或接近，未必有可以互通的内门。|Guest rooms next to or near one another, with no guarantee of an internal connecting door.
Accessible Room|無障礙客房|无障碍客房|wheelchair-accessible room|为有行动需求的旅客配置门宽、浴室扶手等可达性设施。|A room with features such as wider doorways or bathroom grab rails for guests with mobility needs.
Studio Suite|開放式套房|开间套房|open-plan suite|睡眠区和起居区位于同一开放空间，通常没有隔门。|A suite with its living and sleeping areas arranged in one open space.
Junior Suite|小型套房|小型套房|junior guest suite|比一般客房有更多起居空间，未必拥有独立客厅。|A room with more living space than a standard guest room, often in an open layout.
One-Bedroom Suite|一房套房|一居室套房|separate-bedroom suite|卧室和客厅分开，通常有门可独立使用。|A suite with a distinct bedroom and living room, usually separated by a door.
Family Suite|家庭套房|家庭套房|multi-room family suite|以家庭同住为目标，组合卧室与较宽敞的公共空间。|A suite with bedrooms and shared space arranged for a family travelling together.
Presidential Suite|總統套房|总统套房|presidential guest suite|酒店高规格套房名称，通常设有多个独立空间。|A high-tier hotel suite that typically includes multiple separate spaces.
Duplex Suite|複式套房|复式套房|split-level suite|室内由楼梯连接上下两层，活动空间与睡眠区可分隔。|A suite arranged over two floors linked by a private staircase.
Penthouse Suite|頂層套房|顶层套房|top-floor suite|设在楼宇顶层的套房，景观和露台设施视物业而定。|A suite on a building's top floor, with views and terrace facilities depending on the property.
Harbour View Room|海港景客房|海港景房|harbor view room|客房可望见港湾或海港景色，视线范围与楼层有关。|A room overlooking a harbour or bay, with the extent of the view depending on the location and floor.
Ocean View Room|海景客房|海景房|sea view room|客房可望见海面，未必紧贴海岸或全无遮挡。|A room from which the ocean can be seen, possibly at a distance or with obstructions.
Oceanfront Room|臨海客房|临海房|direct oceanfront room|客房位于朝海的建筑面，通常比一般海景房更直接面海。|A room on the seaward side of a property, typically facing the ocean more directly than an ocean-view room.
Partial Sea View|側海景|部分海景|side sea view|从房间部分位置能看见海面，未保证全景。|A room view in which only part of the sea is visible or can be seen from certain positions.
City View Room|城市景觀客房|城景房|cityscape room|客房朝向城市楼宇、街景或天际线。|A room facing city buildings, streets or a skyline.
Garden View Room|園景客房|园景房|garden-facing room|客房的指定窗户朝向花园或绿化区域。|A room with windows oriented toward a garden or landscaped area.
Pool Access Room|直通泳池客房|直通泳池房|swim-up room|从房间露台等出口可直接进入相连泳池区域。|A room with a door or terrace that leads directly to an adjoining swimming pool.
Balcony Room|連露台客房|带阳台客房|room with balcony|客房有可使用的户外阳台，尺寸和私密性需按房型说明。|A room with a usable outdoor balcony, with its size and privacy specified by the property.
"""

ROOM_FEATURES = """
Pillow Menu|枕頭選單|枕头菜单|pillow selection|旅客可按软硬、高低或材质选择睡枕。|A choice of pillows with different firmness, height or filling offered to guests.
Blackout Curtains|遮光窗簾|遮光窗帘|room-darkening drapes|能显著减少外部光线进入房间的窗帘。|Curtains designed to block most outside light from entering a room.
Sound-Insulated Windows|隔音玻璃窗|隔音窗|acoustic glazing|采用隔音结构或玻璃降低室外噪声的窗。|Windows with glass or construction that reduces noise from outside.
Floor-to-Ceiling Windows|落地玻璃窗|落地窗|full-height windows|从地板延伸至接近天花的窗，能提供较开阔视野。|Windows that extend from the floor to near the ceiling for a wider outlook.
Walk-In Wardrobe|步入式衣帽間|步入式衣帽间|walk-in closet|可进入其中整理行李、衣物的独立储物空间。|A storage space large enough for guests to enter to arrange clothes and luggage.
Kitchenette|簡易廚房|简易厨房|in-room kitchenette|包含基础备餐设备的房内小厨房，灶具配置不统一。|A small in-room kitchen with basic food preparation facilities.
Full Kitchen|設備齊全的廚房|全配厨房|fully equipped kitchen|通常配备炉具、冰箱和烹饪工具，可准备完整餐食。|A kitchen equipped for preparing full meals, usually with a stove, refrigerator and utensils.
In-Room Minibar|客房迷你吧|客房迷你吧|guestroom minibar|房内提供的饮品和零食，部分或全部可能另收费。|A selection of drinks and snacks in the room that may be billed separately.
Minibar Credit|迷你吧消費額|迷你吧消费额度|minibar allowance|可抵扣指定迷你吧项目的额度，未使用余额未必可退。|An allowance for eligible minibar purchases, with any unused balance handled under the booking terms.
Rain Shower|雨淋式花灑|雨淋式淋浴|rainfall shower|从上方大面积出水的花洒设计。|An overhead shower head that spreads water over a broad area.
Soaking Tub|浸浴浴缸|泡澡浴缸|deep soaking bathtub|有足够深度用于浸泡的浴缸，不代表具有按摩功能。|A bathtub with enough depth for a person to soak comfortably.
Separate Bath and Shower|獨立浴缸及花灑|浴缸淋浴分设|separate bathtub and shower|浴缸和淋浴区各自独立，客人可任选。|A bathroom configuration with a bathtub and shower in distinct areas.
Grab Rails|浴室扶手|无障碍扶手|grab bars|在厕所、淋浴或浴缸周边提供可抓握支撑。|Fixed bars near a toilet, bath or shower that offer a handhold for support.
Roll-In Shower|無門檻淋浴間|轮椅可进入淋浴间|wheel-in shower|无明显高差且为轮椅进入留有空间的淋浴区。|A shower with a level or near-level entrance and space to enter with a wheelchair.
Portable Cot|便攜式嬰兒床|便携婴儿床|travel crib|可依请求搬入客房的婴幼儿睡床，需按安全年龄使用。|A movable crib available for a baby or toddler on request, subject to age and safety limits.
Rollaway Bed|摺疊加床|折叠加床|roll-away bed|根据房间面积与人数限制临时增设的可移动床铺。|A movable extra bed added when room size and occupancy limits allow.
Sofa Bed|梳化床|沙发床|convertible sofa|白天作沙发、展开后作睡床的家具。|A sofa that unfolds or converts into a bed.
In-Room Safe|客房保險箱|客房保险箱|guest room safe|住客可自行锁存物品的小型保险箱。|A small lockable safe in a guest room for storing personal belongings.
Work Desk|客房書枱|客房办公桌|in-room desk|供电脑工作、书写或视频通话使用的桌面。|An in-room table or desk for computer work, writing or calls.
Universal Power Outlets|多制式插座|多国制式插座|international power sockets|支持不止一种插头规格的插座，供电规格仍须核对。|Electrical sockets that accept multiple plug types, with voltage compatibility to be checked separately.
Bedside Charging|床邊充電位|床头充电位|bedside charging ports|可在床头方便接入电源或设备充电线。|Power outlets or charging ports located within reach of the bed.
Private Plunge Pool|私人小泳池|私享泡池|private dipping pool|套房或别墅内的小型戏水池，深度与面积有限。|A small pool reserved for a suite or villa, typically intended for a quick dip.
Private Terrace|私人平台|私家露台|exclusive-use terrace|房间宾客独用的户外平台，与公共露台区分。|An outdoor platform or patio reserved for the occupants of a particular room.
Outdoor Shower|戶外花灑|户外淋浴|open-air shower|设于室外或露天空间的淋浴设施，私密性依布局。|A shower in an outdoor or open-air area, with privacy depending on its layout.
Separate Living Area|獨立起居空間|独立起居区|separate sitting area|与睡眠区域明确分隔的起居区，不一定有隔门。|A sitting area physically or visually set apart from the bed area.
Pet Bed|寵物睡床|宠物床|dog bed amenity|为入住宠物预备的垫子或小床，通常需提前申请。|A cushion or small bed provided for a guest's pet, often by request.
"""

STAY_PLANS = """
Staycation|宅度假|城市度假|local hotel staycation|在居住地附近订酒店短住，享用餐饮或休闲设施。|A short holiday near home, often at a hotel with dining or leisure facilities.
Bed and Breakfast Rate|客房連早餐房價|含早房价|B&B rate|住宿价格内包含指定客人的早餐。|A room rate that includes breakfast for the guests named in the offer.
Room-Only Rate|淨房價|仅住宿房价|accommodation only rate|仅含客房，不含餐饮与其他增值服务。|A rate covering the room without meals or other add-ons.
Half Board|半膳住宿|半餐住宿|half-board package|房价内含早餐及另一餐，餐型按住宿方案说明。|A rate that includes accommodation, breakfast and one other meal.
Full Board|全膳住宿|全餐住宿|full-board package|住宿附早餐、午餐、晚餐，不一定含饮料。|A rate that includes accommodation and all three daily meals, with drinks depending on the terms.
All-Inclusive Stay|全包式住宿|一价全包度假|all-inclusive package|房价组合住宿及指定餐饮、饮品和活动，范围须列明。|A stay sold with specified meals, drinks and activities included in the rate.
Direct Booking Rate|官網直訂房價|官网直订价|book direct rate|通过酒店自营渠道购买的房价，可能另附直订礼遇。|A rate available through the hotel's own sales channels, sometimes with additional benefits.
Advance Purchase Rate|提早預訂房價|提前预订房价|advance booking rate|需在入住日前一定时间下单的优惠价，条款可能更严格。|A rate available when guests book a specified time ahead of their arrival, often with stricter terms.
Flexible Rate|彈性房價|灵活房价|flexible booking rate|允许按条款免费修改或取消的房价，逾期仍可能收费。|A rate that permits changes or cancellation within stated conditions, with possible fees after the deadline.
Non-Refundable Rate|不可退款房價|不可退款房价|prepaid non-refundable rate|付款后原则上不能退款的房价，实际修改规则依订单。|A prepaid rate that generally cannot be refunded, with any changes governed by the booking terms.
Members' Rate|會員專享房價|会员专享价|member hotel rate|面向登录会员的特定房价，并非所有房型均参加。|A room rate reserved for eligible signed-in members on participating bookings.
Long-Stay Offer|長住優惠|长住特惠|extended-stay deal|满足连续入住晚数条件后适用的住宿优惠。|A discounted rate or benefit triggered by booking the required number of consecutive nights.
Midweek Stay Offer|平日住宿優惠|工作日入住优惠|weekday accommodation offer|适用于指定周间入住日期的住宿推广。|A hotel promotion for stays on specified days of the week, usually outside the weekend.
Weekend Getaway Package|週末短住套票|周末微度假套餐|weekend escape package|为周末短住组合客房及一项或多项体验。|A package bundling a short weekend stay with one or more activities or benefits.
Family Stay Package|親子住宿套票|亲子度假套餐|family getaway package|把家庭房、儿童活动或儿童餐等权益组合销售。|A package that bundles accommodation with family benefits such as children's meals or activities.
Romantic Getaway|雙人浪漫住宿|双人浪漫度假|couples escape|面向两人短住的体验组合，可能含双人餐或布置。|A short stay designed for two guests, sometimes including a meal or room arrangement for a couple.
Anniversary Stay|週年紀念住宿套票|纪念日住宿套餐|anniversary hotel package|为周年纪念设计的住宿，可加订花束、餐饮或其他安排。|A stay designed for an anniversary, with optional dining, flowers or other arrangements.
Spa Retreat Package|水療住宿套票|水疗度假套餐|spa stay package|把住宿和指定水疗护理组合，通常需另预约时间。|Accommodation bundled with specified spa treatments, often requiring a separate appointment.
Dine-and-Stay Package|住宿連餐飲套票|住宿餐饮套餐|stay and dine package|住宿附指定正餐、餐券或餐饮消费额的组合。|A stay that includes a meal, a dining voucher or credit for specified outlets.
Michelin-Starred Dining Stay|米芝蓮星級餐飲住宿套票|米其林星级餐饮住宿套餐|Michelin dining stay|住宿和在指定获星餐厅用餐的权益组合，须核实奖项年份及具体餐厅。|Accommodation paired with a meal at a specified Michelin-starred restaurant.
Afternoon Tea Stay|住宿連下午茶套票|住宿下午茶套餐|afternoon tea hotel package|住店方案含指定人数的下午茶，餐期与入住日可能不同。|A stay that includes afternoon tea for a stated number of guests, subject to separate service times.
Theme Park Hotel Package|酒店連主題樂園套票|乐园门票加酒店套餐|park and hotel package|把酒店和指定乐园门票一起销售，入园可能需预约。|Accommodation and admission to a specified theme park sold together, sometimes with an entry reservation requirement.
Rail and Hotel Package|火車連酒店套票|火车票加酒店套餐|train and stay package|为同一行程组合车票与酒店，退改规则可能分别适用。|Rail tickets and accommodation bundled for one trip, with change rules that may differ by component.
Flight and Hotel Package|機票連酒店套票|机票加酒店套餐|flight plus hotel|同时预订机票与住宿的旅行产品。|A travel bundle combining flights and accommodation in one purchase.
Ski and Stay Package|滑雪住宿套票|滑雪加住宿套餐|ski hotel package|把住宿与雪票、租具或课程等项目组合。|Accommodation bundled with a ski benefit such as lift passes, equipment rental or lessons.
Golf and Stay Package|高爾夫住宿套票|高尔夫住宿套餐|golf hotel break|住宿和指定球场的开球时段等高尔夫权益组合。|Accommodation bundled with golfing benefits such as tee times at a specified course.
Resort Credit|度假村消費額|度假村消费金|resort spending credit|用于抵扣度假村内符合条件的餐饮、护理或活动的金额。|An allowance guests can spend on eligible dining, treatments or activities at a resort.
Hotel Gift Voucher|酒店禮券|酒店礼品券|hotel gift certificate|可赠予他人按规则兑换房晚、消费金额或服务的凭证。|A giftable certificate redeemable for a hotel stay, spending allowance or service under stated terms.
"""

BOOKING_POLICIES = """
Best Available Rate|當日最優惠公開房價|最优可订公开房价|BAR rate|酒店在指定渠道和条件下公开销售的标准动态房价。|A hotel's publicly offered dynamic base room rate for a specified channel and set of conditions.
Rate Parity|房價一致安排|渠道同价|hotel price parity|在约定的可比条件下让各渠道房价保持一致。|The practice or agreement of keeping comparable room rates consistent across booking channels.
Booking Deposit|預訂訂金|预订定金|reservation deposit|为保留预订需预先缴付的款项，抵扣或退还按条款。|An upfront payment that holds a reservation, with refund or credit terms set by the booking.
Security Deposit|入住按金|入住押金|hotel damage deposit|用于担保额外消费或损坏费用的款项，通常离店结算后退回。|A refundable amount held to cover possible damage or incidental charges and settled after the stay.
Card Preauthorization|信用卡預先授權|信用卡预授权|card pre-authorisation hold|在卡片额度内暂时预留金额，并不等于已最终扣款。|A temporary hold on a payment card's available funds or credit before any final charge is taken.
Incidental Charges|住宿雜項收費|住宿杂项费用|incidental fees|除房价之外产生的餐饮、停车或其他住客消费。|Additional guest charges for items such as dining or parking beyond the room rate.
Resort Fee|度假村設施費|度假村设施费|destination amenity fee|某些物业单列的每日费用，覆盖范围需按酒店披露。|A separately disclosed property charge, often per day, that covers a stated set of amenities or services.
Tourism Tax|旅遊住宿稅|旅游住宿税|city accommodation tax|某些目的地按房晚、房价或人头收取的住宿相关税费。|A destination levy on accommodation that may be charged per room, night or guest or based on the rate.
Cancellation Window|免費取消時限|免费取消截止时间|free cancellation deadline|预订可免费取消的最晚日期和当地时间。|The deadline, in local time, for cancelling a booking without a penalty.
Cancellation Fee|取消預訂費用|取消预订手续费|hotel cancellation penalty|在特定日期之后取消预订时收取的费用。|A charge applied when a booking is cancelled after its stated deadline or under specified conditions.
No-Show Fee|逾時未入住收費|未到店费用|hotel no show charge|客人未按期入住且未按要求取消时产生的费用。|A charge for failing to arrive or cancel a reservation according to its terms.
Modification Policy|更改預訂條款|订单改期规则|booking amendment terms|规定可改日期、房型或人数的时限、差价和费用。|The rules for changing a booking's dates, room category or guest count, including deadlines and fees.
Minimum Stay|最少入住晚數|最少连住晚数|minimum length of stay|指定房价或日期要求旅客连续预订的最低晚数。|The fewest consecutive nights a guest must book for a specified rate or dates.
Maximum Occupancy|最高入住人數|房型限住人数|max guests per room|房间可接待的最大人数，成人与儿童的限制可能不同。|The maximum number of guests permitted in a room, with separate rules possible for adults and children.
Extra Guest Charge|額外住客收費|加人费用|additional occupant fee|超过房价包含的基础入住人数时收取的费用。|An additional fee for a guest beyond the occupancy included in the base rate.
Child Stay Policy|小童入住條款|儿童入住政策|children accommodation policy|规定儿童的年龄范围、床位、餐费与额外收费。|The terms for children's stays, including eligible ages, sleeping arrangements, meals and any fees.
Pet Policy|寵物入住條款|宠物入住须知|pet accommodation policy|说明可携宠物种类、体重限制、费用及活动范围。|The rules for bringing pets, including accepted animals, size limits, fees and permitted areas.
Blackout Dates|不適用日期|不可用日期|excluded stay dates|优惠、兑换或房券不能使用的指定日期。|Specified dates when a promotion, points redemption or voucher cannot be used.
Subject to Room Availability|視乎客房供應情況|以实际房态为准|room availability applies|表示升级、加床或指定房型需视当时供应情况安排。|A booking condition indicating a room type, upgrade or extra bed is only offered if inventory permits.
Guaranteed Reservation|保證留房預訂|担保预订|guaranteed booking|按卡片担保或预付安排保留房间，迟到或未到店仍受条款约束。|A booking held with a card guarantee or prepayment, subject to late arrival and no-show terms.
Waitlisted Booking|候補預訂|候补预约|reservation waitlist|当前没有确认供应，名额释放后才可能获确认。|A request placed in a queue that remains unconfirmed until inventory becomes available.
Check-In Cutoff|最遲登記入住時間|最晚办理入住时间|latest check-in time|仍可正常登记入住的最晚时段，迟抵需提前沟通。|The latest time guests can check in normally, with late arrivals often requiring advance notice.
Check-Out Time|退房時間|最晚退房时间|departure time hotel|住客按原房价应交还客房的截止时间。|The local deadline for vacating a guest room under the booked rate.
Early Departure Fee|提早退房費用|提前离店费|early checkout charge|客人提前结束住宿时按预订条件可能收取的费用。|A potential charge for shortening a stay after booking or checking in.
Booking Confirmation|預訂確認書|预订确认单|reservation confirmation|列出房型、日期、价格和预订识别信息的确认文件。|A record confirming a reservation, typically with dates, room type, price and a booking reference.
"""

GUEST_SERVICES = """
Executive Lounge Access|行政酒廊禮遇|行政酒廊权益|club lounge access|符合条件的住客可进入行政酒廊并使用指定时段的服务。|The right for eligible guests to enter an executive lounge and use its specified services during opening hours.
Club Lounge Breakfast|行政酒廊早餐|行政酒廊早餐|executive lounge breakfast|在行政酒廊指定时段供应给合资格住客的早餐。|Breakfast offered to eligible guests in a hotel club lounge during set hours.
Evening Canapés|黃昏佐酒小食|晚间佐酒小食|evening hors d'oeuvres|傍晚在酒廊配合饮品供应的少量咸点。|Small savoury bites served in the evening, often alongside lounge drinks.
Afternoon Refreshments|午後茶點|午后茶歇|lounge afternoon snacks|下午供应的轻食和饮料，份量与品种依酒店说明。|Light food and drinks served in the afternoon, with the selection and portions set by the property.
Welcome Drink|迎賓飲品|欢迎饮品|arrival drink|客人抵达或到指定场所时获赠的饮料。|A complimentary drink offered on arrival or at a designated venue.
Welcome Amenity|迎賓小禮|欢迎礼遇|welcome gift amenity|酒店在客房为特定住客预备的小食、饮品或礼品。|A snack, drink or gift placed in the room for eligible or selected arriving guests.
Turndown Service|晚間開床服務|夜床服务|evening turndown|晚间整理床铺与客房，方便客人就寝。|An evening housekeeping visit to prepare the room and bed for sleep.
In-Room Dining|客房送餐|客房送餐服务|room service dining|住客从菜单订餐后由酒店送到房间。|Hotel meals and drinks ordered from a menu and delivered to a guest room.
Express Check-In|特快登記入住|快速入住|fast-track check-in|通过已填资料、独立柜台等方式减少办理入住所需时间。|A shortened arrival process using advance details, a dedicated desk or another streamlined arrangement.
Mobile Check-In|手機登記入住|手机自助入住|online hotel check-in|在手机上提前提交入住资料，取钥匙仍可能需核验身份。|Submitting check-in details by phone before arrival, with possible identity checks when collecting a key.
Digital Room Key|手機房卡|手机电子房卡|mobile key|在支持的手机或应用上启用可开客房门的电子钥匙。|An electronic key delivered to a compatible phone or app for opening the room door.
Express Check-Out|特快退房|快速退房|express departure|按规定确认账单并快速退房，无需完整柜台流程。|A faster departure process that lets guests settle their bill without completing the usual front-desk routine.
Early Check-In|提早入住|提前入住|early room access|在标准时间之前交付客房，需看空房或付费条件。|Access to a guest room before the standard check-in time, subject to availability or a charge.
Late Check-Out|延遲退房|延时退房|extended checkout|允许晚于常规时间交还客房，是否收费需说明。|Permission to keep a room beyond the standard departure time, subject to any fee or availability limit.
Room Upgrade|客房升級|房型升级|complimentary room upgrade|从已订房型换到较高类别，可能需付差价或受房态限制。|Moving a guest to a higher room category, which may depend on availability or an additional payment.
Luggage Storage|行李寄存|行李寄存|left luggage service|酒店代为临时保管行李，常在入住前或离店后使用。|Temporary storage of guest bags, often before check-in or after check-out.
Bell Service|行李員服務|礼宾行李服务|porter service|由行李员协助把行李运送到客房、门口或车辆。|Staff assistance transporting luggage between the hotel entrance, vehicles and guest rooms.
Concierge Service|禮賓服務|礼宾服务|guest concierge|酒店协助预订餐厅、安排交通或提供当地行程建议。|Hotel assistance with restaurant bookings, transport and local recommendations.
Butler Service|管家服務|私人管家服务|personal butler|由专人协调套房住客的入住、餐饮或行程需求。|Dedicated assistance coordinating a suite guest's arrival, dining and plans.
Valet Parking|代客泊車|代客泊车|valet service|工作人员接收车辆、代为停放并在客人离开时取回。|A service in which staff park a guest's vehicle and retrieve it on request.
Laundry Service|洗衣服務|客房洗衣服务|hotel garment cleaning|代为清洗、烘干或熨烫住客衣物，时限和收费按件说明。|A service for washing, drying or ironing guest clothes with stated item rates and turnaround times.
Pressing Service|熨衣服務|熨烫服务|garment pressing|为住客熨烫衣物去皱，未必包含洗涤。|A service for removing wrinkles from garments, which may be offered separately from washing.
Shoe Shine Service|擦鞋服務|擦鞋服务|shoe polishing|为住客清洁或抛光可护理的鞋面。|Cleaning or polishing eligible footwear for hotel guests.
Kids' Club|兒童天地|儿童俱乐部|resort kids club|酒店内为儿童提供游戏或带领活动的场地。|A dedicated hotel space offering supervised games or activities for children.
Babysitting Service|幼兒看顧服務|儿童看护服务|hotel childminding|经预订由工作人员照看儿童的服务，年龄和收费需明确。|A booked childcare service with stated age requirements and fees.
Poolside Cabana|池畔私人涼亭|泳池边私享凉亭|pool cabana|泳池边可预订的遮阳休憩空间，有时配餐饮消费额。|A shaded area beside a pool available to reserve, sometimes with a food and beverage allowance.
"""

TRANSIT = """
Airport Transfer|機場接送|机场接送|hotel airport transfer|机场与酒店等指定地点之间的预订接送服务。|A prearranged ride between an airport and a specified destination such as a hotel.
Arrival Transfer|接機服務|接机服务|airport arrival pick-up|从机场抵达区接旅客前往酒店或其他目的地。|A pickup from the airport arrivals area for travel to a hotel or other destination.
Departure Transfer|送機服務|送机服务|airport drop-off|在离境前按约定时间把旅客从住宿地点送至机场。|A prearranged ride from accommodation to the airport in time for a departing flight.
Round-Trip Transfer|來回接送|往返接送|return shuttle transfer|一次预订包含去程和回程两段接送。|A transfer booking that includes both the outward and return rides.
Private Transfer|專車接送|专车接送|exclusive car transfer|为该订单独立安排车辆，不与其他乘客拼乘。|A transfer with a vehicle reserved for one booking party.
Shared Transfer|共乘接送|拼车接送|shared shuttle|多个订单旅客共乘，可能途经其他酒店。|A transfer carrying passengers from several bookings, often with multiple pickup or drop-off stops.
Complimentary Shuttle|免費穿梭巴士|免费接驳巴士|free shuttle bus|不用额外购票、在指定站点与时间行驶的接驳车。|A shuttle ride included at no extra charge, operating at specified times and stops.
Scheduled Shuttle|定時穿梭巴士|定点班车|timetabled shuttle|按固定班次发车，不按客人选择时间单独出车。|A shuttle that leaves at fixed times on a published timetable.
Station Pick-Up|車站接送|接站服务|railway station pick-up|司机在约定车站出口接旅客前往住宿地。|A ride that meets a traveller at a specified station exit and continues to their accommodation.
Hotel Courtesy Car|酒店禮賓專車|酒店礼宾用车|hotel house car|酒店安排的住客短程用车，服务范围与费用按物业。|A hotel-arranged short-distance car service for guests, subject to its service area and fees.
Meet and Greet|舉牌迎接|举牌接待|airport meet-and-assist|接待人员在约定位置辨认并引导旅客与司机会合。|A service in which a representative meets travellers at an agreed point and directs them to their driver.
Accessible Transfer|無障礙接送|无障碍接驳|wheelchair-friendly transfer|为轮椅等需求提供适配的车辆和上下车条件。|A transfer with a vehicle and boarding arrangements suited to mobility needs such as wheelchair access.
Car Seat Request|預約兒童安全座椅|预约儿童安全座椅|child seat on request|接送时提前安排与儿童年龄体重匹配的安全座椅。|An advance request for a vehicle child seat suited to the child's age and weight.
Luggage Allowance|行李限額|行李额度|baggage allowance|行程或车票允许携带的行李件数、重量或尺寸。|The number, weight or dimensions of bags a fare or transfer permits.
Carry-On Baggage|手提行李|随身行李|cabin baggage|可由旅客随身带入客舱并按要求存放的行李。|Baggage passengers can bring into the cabin and stow in line with carrier rules.
Checked Baggage|寄艙行李|托运行李|hold baggage|交由承运人放在行李舱运输的行李。|Baggage handed to the carrier for transport in a luggage hold.
Priority Boarding|優先登機|优先登机|early boarding access|符合条件的旅客可在部分普通旅客之前登机。|An arrangement allowing eligible passengers to board before some other travellers.
Airport Fast Track|機場快速通道|机场快速通道|fast-track airport service|使用机场指定的优先流程，覆盖安检或证件查验需说明。|A designated expedited airport process covering specified checks such as security or immigration.
Airport Lounge Pass|機場貴賓室通行證|机场贵宾厅使用券|airport lounge entry|在符合条件的航站楼和时段进入指定机场贵宾室。|Access to a specified airport lounge at eligible terminals and times.
Early-Bird Airfare|早鳥機票|早鸟机票|advance airfare deal|提前购票才能获得的机票价格，库存和出行日期受限制。|An airfare available for bookings made far enough in advance, subject to seats and travel dates.
Open-Jaw Itinerary|開口程機票|开口程机票|open jaw flight itinerary|去程到达城市与回程出发城市不同等非闭环机票组合。|An itinerary where the return departs from a different city or ends in a different city from the original departure.
Stopover Package|中途停留套票|中转停留套餐|stopover hotel deal|航程中在中转城市停留较长时间并组合住宿或观光。|A trip package that adds a longer stay in a connecting city, often with accommodation or sightseeing.
Rail Pass|鐵路周遊券|铁路通票|train travel pass|在有效期和适用线路内搭乘指定列车的通票。|A pass covering designated rail journeys within stated routes and validity periods.
Ferry Crossing|渡輪航程|轮渡航程|ferry trip|以渡轮连接水域两边或岛屿，按码头与班次安排。|A scheduled boat crossing between shores or islands, departing from specified terminals.
Water Taxi|水上的士|水上出租船|water cab|在指定码头之间接载乘客的小型水上交通服务。|A small passenger vessel offering rides between specified piers.
Self-Drive Itinerary|自駕遊路線|自驾路线|road trip itinerary|以自行驾驶连接多个目的地，并安排停靠、停车或住宿。|A travel plan linking destinations by car with suggested stops, parking or overnight stays.
Bike Rental|單車租借|自行车租赁|bicycle hire|按时段或里程租用自行车，可另配头盔与路线图。|Temporary use of a bicycle for a set period or distance, sometimes with a helmet or route map.
"""

OUTDOORS = """
Guided Hike|行山導賞團|徒步向导团|guided trekking walk|由熟悉路线的人员领队，并介绍沿途地貌或生态。|A hike led by someone familiar with the route who may explain the landscape or ecology along the way.
Self-Guided Walk|自助步行遊|自助步行游|independent walking route|旅客按地图、路标或语音资料自行完成的步行行程。|A walk visitors complete independently using directions, signs or audio instructions.
Coastal Trail|海岸步道|滨海步道|coastal walking path|沿海岸连接景点的步行路线，开放状况受天气影响。|A walking route along the coast, where weather may affect access.
Country Park Walk|郊野公園健行|郊野公园徒步|country park hike|在郊野公园指定路线进行的步行体验。|A walking experience along designated routes in a country park.
Sunrise Hike|日出行山團|日出徒步团|sunrise trek|配合日出时刻出发，到指定观景处的早晨徒步。|An early hike timed to reach a viewpoint around sunrise.
Night Hike|夜行導賞|夜间徒步|evening guided hike|在天黑后行走的路线，照明、同伴和难度需提前说明。|A hike after dark for which lighting, route difficulty and group arrangements should be clear.
Scenic Lookout|景觀瞭望點|观景台|scenic viewpoint|可眺望山海或城市的指定观景点。|A designated viewpoint overlooking features such as the coast, mountains or a city.
Clifftop Walk|崖頂步道|悬崖步道|cliff-top walking route|沿高处崖边布设的路线，风险与护栏情况需说明。|A walking route along a cliff edge, with safety features and risks depending on the site.
Mangrove Kayaking|紅樹林獨木舟|红树林皮划艇|mangrove paddle|乘小艇在红树林水域观察湿地，通常依潮汐安排。|Kayaking through mangrove waters to see wetland habitats, often timed around the tide.
Sea Kayaking|海上獨木舟|海上皮划艇|coastal kayaking|在海湾或沿岸水域划行，受浪高与风向影响。|Kayaking in bays or coastal water, subject to wind and wave conditions.
Stand-Up Paddleboarding|直立板體驗|桨板体验|SUP experience|站在浮板上用长桨划行的水上运动。|A water sport in which a participant stands on a floating board and moves with a long paddle.
Snorkelling Trip|浮潛之旅|浮潜体验|snorkeling tour|借面镜与呼吸管在水面观察水下生物。|An outing to see underwater life while floating at the surface with a mask and snorkel.
Introductory Dive|初階潛水體驗|体验潜水|discover scuba dive|在专业人员指导下进行的入门潜水活动。|A beginner scuba experience conducted under a qualified instructor's supervision.
Reef-Safe Snorkel Briefing|珊瑚保育浮潛簡介|浮潜珊瑚保护说明|reef etiquette briefing|下水前说明如何避免踩踏、触碰或损伤珊瑚。|Instructions given before snorkelling on how to avoid touching, stepping on or damaging coral.
Dolphin-Watching Tour|海豚觀賞團|观豚船游|dolphin watching cruise|乘船寻找并远距离观察海豚，不能保证遇见。|A boat trip to look for and observe dolphins at a distance, with sightings dependent on wildlife and conditions.
Birdwatching Tour|觀鳥導賞團|观鸟向导团|birding tour|在合适季节与地点观察鸟类，通常用望远镜辅助。|A trip to look for birds in a suitable season and habitat, often with binoculars.
Wetland Boardwalk|濕地木棧道|湿地栈道|marsh boardwalk|架设在湿地上、供游客不踩入栖息地的步行道。|A raised path allowing visitors to cross a wetland without walking directly in its habitat.
Stargazing Experience|觀星體驗|星空观测体验|night sky tour|在较暗地点观赏星空，受云量、月相与灯光影响。|A session for observing the night sky from a dark location, subject to cloud cover, moon phase and local lights.
Glamping|豪華露營|精致露营|glamorous camping|提供已搭帐篷、寝具等便利的露营住宿。|Camping accommodation with comforts such as an already erected tent and bedding.
Campsite Pitch|營位|露营营位|tent pitch|供一组旅客搭设帐篷或停放指定露营设施的位置。|A designated space for a party to set up a tent or park permitted camping equipment.
Forest Bathing|森林浴|森林疗愈漫步|shinrin-yoku|在林地放慢步速、观察感官体验的活动，不作治疗承诺。|A slow, sensory experience in woodland focused on observing the surroundings.
Trail Running Route|越野跑路線|越野跑路线|trail run course|适合在非铺装路面跑步的路线，需说明爬升和补给。|An unpaved running route, typically described with details about elevation and supplies.
Cycling Greenway|單車綠道|骑行绿道|cycle greenway|供自行车与步行等使用的绿色通道，分流方式依地区。|A landscaped route for cycling and often walking, with local rules determining how users share it.
Rock-Climbing Taster|攀石體驗課|攀岩体验课|intro rock climbing|在指导与保护装备下体验基础攀岩动作的课程。|A beginner rock-climbing session with instruction and protective equipment.
Picnic Site|野餐地點|野餐区|picnic ground|可铺垫或使用桌椅用餐的指定户外地点。|A designated outdoor spot for eating with a picnic blanket or provided table.
Seasonal Blossom Walk|時令賞花路線|当季赏花路线|blossom trail|按花季安排的步行路线，花期受天气和养护影响。|A walking route timed for a flowering season, with blooms subject to weather and site conditions.
"""

CULTURAL_EXPERIENCES = """
Heritage Walk|歷史文化導賞|历史文化漫步|heritage walking tour|用步行连接历史建筑、街区与文化故事的导览。|A walking route connecting historic buildings, neighbourhoods and stories.
Old Town Walking Tour|舊城漫遊導賞|古城步行导览|historic quarter walking tour|沿老街、街巷和老店观察聚落变迁的步行路线。|A guided walk through older streets and businesses that explains how a district developed.
Architecture Tour|建築導賞|建筑导览|architectural tour|带领游客认识建筑风格、材料与设计背景。|A visit focused on buildings' design, materials, style and historical background.
Street Art Tour|街頭藝術導賞|街头艺术导览|mural walking tour|沿街欣赏壁画和公共艺术，并了解创作语境。|A route past murals and public artworks that explains their context.
Market Food Tour|街市美食導賞|菜市场美食导览|market tasting tour|在当地市场了解食材并试吃指定摊位小食。|A guided market visit that introduces local ingredients and includes samples from specified stalls.
Food Heritage Tour|飲食文化導賞|饮食文化探访|culinary heritage walk|通过老店、工艺与招牌菜理解当地饮食传统。|A tour of long-established shops, techniques and dishes that explains a place's culinary traditions.
Museum Highlights Tour|博物館精華導賞|博物馆重点展品导览|museum highlights walk|在有限时间内讲解馆内有代表性的藏品。|A short guided visit focusing on representative objects in a museum collection.
Curator-Led Tour|策展人導賞|策展人导览|curator's tour|由策展人讲解展品选择、展览主题与布展思路。|A tour where the curator explains the exhibition theme, selected works and display choices.
After-Hours Museum Visit|閉館後專場參觀|闭馆后专场参观|private after-hours viewing|在常规开放结束后为特定宾客开放的场次。|A visit scheduled outside normal museum opening hours for eligible guests.
Permanent Collection|常設館藏|常设馆藏|permanent exhibition holdings|机构长期保存或展示的藏品，部分展件仍会轮换。|Works a museum or gallery holds long term, even if the objects on display change.
Temporary Exhibition|期間展覽|临时展览|limited-run exhibition|只在指定日期区间开放的展览。|An exhibition open only for a stated date range.
Travelling Exhibition|巡迴展覽|巡回展览|touring exhibition|在多个城市或场馆按不同日期轮换展出的展览。|An exhibition shown at different venues or cities on a rotating schedule.
Open Studio|開放工作室|工作室开放日|artist studio visit|创作者在指定时段接待访客观看工作过程与作品。|A scheduled visit to a creator's workspace to see works and methods firsthand.
Artist Talk|藝術家分享會|艺术家分享会|artist conversation|由创作者现场交流作品和方法的活动。|A live talk where an artist discusses their work or creative process.
Audio Guide|語音導賞|语音导览|audio tour guide|通过设备或手机按展点播放讲解内容。|Recorded commentary delivered on a device or phone at points along a visit.
Multilingual Guided Tour|多語言導賞團|多语种导览团|multilingual tour|提供多种语言的导览场次，预约时需选择语言。|Guided tours offered in a choice of languages, with the language usually selected at booking.
Hands-On Craft Workshop|手作體驗班|手工体验课|craft-making workshop|在导师协助下亲手制作指定手工成品。|An instructor-led session in which participants make a craft item themselves.
Pottery Wheel Workshop|陶藝拉坯班|陶艺拉坯体验|wheel throwing class|使用陶轮给泥坯塑形的课程，烧制与取件另按安排。|A class using a pottery wheel to shape clay, with separate arrangements for firing and collection.
Tea Ceremony Experience|茶道體驗|茶道体验|tea ceremony session|跟随主持人体验备器、泡茶、奉茶等过程。|A hosted activity introducing the preparation, brewing and serving steps of a tea ceremony.
Calligraphy Workshop|書法體驗班|书法体验课|brush calligraphy class|由导师指导基本笔法并书写作品。|An instructor-led class in basic brush techniques and creating a calligraphy piece.
Indigo Dyeing Workshop|藍染體驗班|蓝染体验课|indigo textile class|用靛蓝染料和绑扎等技法制成布艺图案。|A class in making fabric patterns with indigo dye and techniques such as tying the cloth.
Lantern-Making Workshop|紮燈籠體驗|灯笼制作体验|lantern craft class|组装骨架和纸面制作灯笼，材料与年龄限制依课程。|A class in making a lantern by assembling its frame and covering it, with materials and age limits set by the organiser.
Neighbourhood Walk|社區漫遊|街区漫步|neighborhood tour|在居民生活街区以步行了解店铺、建筑与社区故事。|A walk through a residential area focusing on local shops, architecture and stories.
Night Market Tour|夜市導賞|夜市探访|guided night market walk|在夜市开放时段由导游带领探访摊位和饮食。|A guided visit to stalls and food vendors during a night market's operating hours.
Photography Walk|攝影散步團|摄影采风|photo walk tour|跟随摄影向导寻找不同取景角度和光线的步行活动。|A walk led by a photographer to explore viewpoints, light and framing.
Community-Led Tour|社區主導導賞|社区居民带领的导览|local-led community tour|由社区参与设计和讲解，体现本地居民的经验与视角。|A tour shaped and delivered by community participants who share local perspectives and experience.
"""

TICKETING = """
Timed Entry|分時段入場|分时段入场|timed admission|入场票仅可在所选时间窗口使用，避免同时到场拥挤。|An admission ticket valid only during the chosen arrival window.
Open-Date Ticket|不指定日期門票|不定日门票|open dated admission|购票时未固定参观日期，仍有使用期限或预约规则。|A ticket purchased without selecting a visit date, subject to its expiry and any reservation rules.
Same-Day Ticket|即日門票|当日票|same day admission|当天购买并用于当天入场的门票。|A ticket purchased for admission on the same day.
Advance Ticket|預售門票|预售门票|advance admission ticket|在正式开场或使用日前提前出售的门票。|A ticket sold before an event starts or its admission date arrives.
Admission Pass|入場證|入场通行证|admission ticket|在指定范围和有效时段内允许进入的凭证。|A credential granting access to a venue or event within specified dates and areas.
Attraction Pass|景點通行證|景区通票|multi-attraction pass|一张凭证可兑换多个景点或项目的入场资格。|A pass that can be used to gain entry to several included attractions or activities.
Combination Ticket|聯票|联票|combo admission|把两个或更多参观项目合并成一张票。|A single ticket that covers two or more visits, experiences or attractions.
Family Admission|家庭門票|家庭套票|family entrance ticket|按指定成人与儿童组合出售的家庭入场票。|An admission ticket covering a stated combination of adults and children.
Concession Ticket|特惠門票|优待票|reduced admission|向符合年龄、学生或其他资格者提供的低价门票。|A reduced-price ticket for visitors meeting eligibility requirements such as age or student status.
Student Admission|學生門票|学生票|student rate ticket|面向持有效学生证明的访客的门票。|A ticket for visitors who can show valid evidence of student status.
Senior Admission|長者門票|老年人优惠票|senior rate ticket|按规定年龄或证件资格适用的优惠门票。|A discounted admission category for visitors meeting a stated age or identification requirement.
Resident Admission|本地居民門票|本地居民优惠票|local resident ticket|向可证明在指定地区居住的访客提供的票种。|An admission category for visitors who can prove they live in a specified area.
Annual Pass|全年通行證|年卡|annual membership pass|在规定年度或自激活日起一年内多次入场。|A pass for repeated entry during a named year or one year after activation.
Season Pass|季度通行證|季卡|season admission pass|在指定活动季或开放季内反复入场。|A pass for repeated visits during a specified event season or opening period.
Re-Entry|離場後再入場|二次入园|same day re-entry|在规则允许时离场后再次进入，可能需盖章或保留票券。|Permission to return after leaving a venue, sometimes by showing a ticket or stamp.
Skip-the-Line Entry|免排隊入場|快速入场|priority entrance lane|通过指定入口缩短验票队列时间，安检等流程仍适用。|Access through a separate ticket queue or entrance, with applicable checks such as security still in place.
Reserved Seating|劃位入座|对号入座|assigned seats|门票绑定具体座位，而非按到达先后选座。|A ticket that assigns the holder a specific seat in advance.
General Admission|不設劃位門票|无指定座席门票|unreserved admission|可进入指定区域但不保证具体座位。|An admission ticket granting entry to a specified area without guaranteeing an assigned seat.
Mobile Ticket|手機電子門票|手机电子票|digital entry ticket|用手机展示可扫描凭证入场，无需纸本。|An admission credential displayed on a phone and usually scanned at entry.
Ticket Redemption|換領門票|兑换门票|voucher redemption|按规则使用电子凭证、兑换码或实体券换取入场票。|Exchanging a voucher or code for a valid admission ticket under the stated rules.
Gate Price|現場票價|现场票价|walk-up ticket price|在入口票务处购买门票时适用的价格。|The admission price charged when tickets are bought at the venue's gate or ticket office.
Booking Fee|訂票手續費|票务手续费|ticket handling fee|票务平台或售票处在票价以外收取的服务费用。|A service charge added by a booking platform or ticket office.
Accessibility Companion Ticket|無障礙同行者門票|无障碍陪同票|essential companion admission|符合条件的访客可为必要陪同人员申请的票。|A ticket available for a necessary companion accompanying an eligible visitor with accessibility needs.
Weather Contingency|惡劣天氣安排|恶劣天气应急安排|weather backup plan|活动因天气无法照常举行时采用的改期、替代方案或退款规则。|A plan for rescheduling, providing an alternative or issuing refunds if weather disrupts an event.
Sold-Out Session|額滿場次|已售罄场次|fully booked session|预订名额已达上限、目前无法再买票的指定场次。|A particular session for which all bookable places have been taken.
"""

PROPERTY_TYPES = """
Boutique Hotel|精品酒店|精品酒店|design boutique hotel|房量通常较小、突出设计或个性化体验的酒店。|A typically small hotel with a distinctive design or personalised guest experience.
Design Hotel|設計酒店|设计酒店|design-led hotel|以建筑、室内设计或艺术策展作为主要识别点的酒店。|A hotel distinguished by its architecture, interiors or curated art.
Heritage Hotel|歷史建築酒店|历史建筑酒店|heritage property|由具有历史背景的建筑改建或延续经营的酒店。|A hotel housed in or adapted from a building with historical significance.
Business Hotel|商務酒店|商务酒店|corporate hotel|提供办公便利与会议配套、主要面向商旅客人的酒店。|A hotel oriented toward work trips with facilities such as workspaces and meeting rooms.
Airport Hotel|機場酒店|机场酒店|airport accommodation|靠近机场或航站楼，为抵达与离境旅客提供住宿。|A hotel near an airport or terminal, convenient for arriving or departing travellers.
Transit Hotel|轉機酒店|中转酒店|layover hotel|为转机或过境的旅客提供短住，有些设在安检区域内。|Accommodation for travellers making a connection or stopover, sometimes located beyond airport security.
Extended-Stay Hotel|長住酒店|长住酒店|long stay hotel|针对连续多晚住宿配置厨房、洗衣等便利的酒店。|A hotel designed for longer visits, often with cooking and laundry facilities.
Serviced Apartment|服務式住宅|服务式公寓|aparthotel apartment|有住宅布局并提供一定酒店式清洁或接待服务的住宿。|Apartment-style accommodation with some hotel services, such as housekeeping or reception.
Beach Resort|海濱度假村|滨海度假酒店|beachfront resort|靠近海滩、结合住宿与海边休闲设施的度假物业。|A resort near a beach that combines lodging with coastal recreation facilities.
Island Resort|離島度假村|海岛度假村|island retreat|位于岛屿上的度假住宿，交通可能需船只接驳。|A resort on an island, where transfers may require a boat.
Mountain Lodge|山間旅舍|山间小屋酒店|mountain retreat lodge|设于山区的住宿，常为徒步或避暑客人提供休憩。|Accommodation in a mountain area, often serving walkers and visitors seeking cooler conditions.
Ski-In Ski-Out Hotel|滑雪直出直入酒店|滑进滑出酒店|slope-side ski hotel|客人可按路线和雪况从酒店附近滑入或滑出雪道。|A hotel with access to ski routes from the property or nearby, depending on conditions and route layout.
Spa Resort|水療度假村|水疗度假酒店|wellness spa resort|以水疗护理与康养设施为主要度假体验的物业。|A resort centred on spa treatments and wellness facilities.
Hot Spring Resort|溫泉度假村|温泉度假酒店|hot springs resort|以温泉浸浴等设施作为主要服务的度假住宿。|A resort with bathing facilities fed by hot springs as a central offering.
Eco Lodge|生態旅舍|生态度假屋|eco-lodge|强调自然环境与运营影响管理的住宿，认证需单独核对。|Lodging focused on its natural setting and limiting operational impacts, with any certification disclosed separately.
Vineyard Stay|葡萄園住宿|葡萄酒庄住宿|winery stay|在葡萄园或酒庄经营范围内入住的体验。|Accommodation on or associated with a vineyard or winery.
Farm Stay|農莊住宿|农场民宿|farm accommodation|设在经营中的农场或农庄内的短期住宿。|A short stay at a working farm or agricultural property.
Ryokan|日式旅館|日式传统旅馆|Japanese ryokan inn|有日式传统接待与房间布置的旅馆，餐食和浴场依店。|A traditional Japanese inn, with meals and bathing facilities varying by property.
Capsule Hotel|膠囊酒店|胶囊旅馆|pod hotel|以相对独立的小型睡眠舱作住宿单位。|Lodging in individual compact sleeping pods.
Youth Hostel|青年旅舍|青年旅舍|youth guest hostel|通常设共享寝室和公共空间，床位可分开预订。|Budget accommodation often offering separately bookable beds in shared rooms and communal spaces.
Guesthouse|民宿旅館|家庭旅馆|guest house|小型住宿经营，服务和房间配置常因店而异。|A small accommodation property with services and room layouts that vary by operator.
Private Villa|獨立度假別墅|独栋度假别墅|exclusive-use villa|可由同一组旅客独用、通常有独立起居设施的房屋。|A standalone house reserved for one party, generally with its own living facilities.
Overwater Villa|水上別墅|水上别墅|overwater bungalow|建于水面上方的独立度假客房，水深和通行方式需说明。|A separate resort room built over water, with access and water conditions specified by the property.
Adult-Only Resort|只限成人入住度假村|仅限成人度假村|adults-only resort|只接待符合最低年龄要求的旅客的度假物业。|A resort that admits only guests meeting its stated minimum age.
Pet-Friendly Hotel|寵物友善酒店|宠物友好酒店|dog-friendly accommodation|在规定种类、数量与区域内允许携带宠物的酒店。|A hotel that accepts pets under rules covering species, numbers and permitted areas.
Convention Hotel|會展酒店|会展酒店|conference hotel|配备会议、宴会和住宿设施，可承接大型活动。|A hotel with meeting, banquet and accommodation facilities for large events.
Conference Day Package|全日會議套票|全天会议套餐|day delegate rate|按日或人数组合场地、茶歇、餐食与设备的会议方案。|A day-rate meeting bundle that includes a venue, refreshments, meals and equipment as specified.
Residential Meeting Package|住宿連會議套票|会议住宿套餐|overnight conference package|把参会者住宿、会议设施与餐饮统一组合报价。|A meeting booking that bundles overnight accommodation, meeting facilities and catering.
"""
