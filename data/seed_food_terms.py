"""Editorial phrase families for restaurant, beverage, and menu copy.

Rows are intentionally selected, so a cooking method is only paired with
ingredients it is used for and menu claims retain their actual meaning.
Each row contains EN, HK, CN, a search alias, and a concept-specific definition.
"""

DINING_FORMATS = """
Tasting Menu|品嚐餐單|品鉴菜单|degustation menu|由主厨安排多道小份菜式，按顺序呈现一季食材或料理主题。
Chef's Table|主廚餐桌|主厨餐桌|chef's counter|通常设在厨房旁，由主厨或团队近距离介绍料理。
Counter Dining|吧枱用餐|吧台用餐|counter seats|坐在吧台用餐，常能看见备菜、调酒或出品过程。
Set Lunch|午市套餐|午间套餐|lunch set|午餐时段供应、按固定价格组合主菜和配菜的餐点。
Early Dinner Menu|早段晚市餐單|早场晚餐菜单|early supper menu|为较早入座的客人提供一套独立晚餐菜单。
Pre-Theatre Dinner|觀劇前晚餐|观演前晚餐|pre-show dining|围绕演出开场前的时段安排节奏较快的晚餐。
À la Carte|單點餐單|单点菜单|a la carte|每道菜单独点选与定价，可按人数自由组合。
Prix Fixe|定價套餐|固定价套餐|fixed-price menu|按统一价格供应约定道数的餐点，部分菜式可选。
Market Menu|街市時令餐單|时令市集菜单|daily market menu|按当天采购到的蔬果、海鲜或肉类调整菜式。
Plant-Based Tasting Menu|植物料理品嚐餐單|植物料理品鉴菜单|plant-forward tasting|用豆类、蔬果和谷物组织多道菜式，细节需看实际配方。
Dim Sum Brunch|點心早午餐|广式点心早午餐|dim sum brunch service|以茶楼点心为主的早午餐，常搭配茶水与热菜。
Free-Flow Brunch|早午餐連無限添飲|早午餐含畅饮|bottomless brunch|早午餐附指定饮品在限定时间内续杯的权益。
Sharing Menu|共享餐單|分享式菜单|family-style dining|菜式集中端上桌，由同桌客人分食，适合聚餐。
Omakase|廚師發辦|主厨发办|chef's choice menu|客人把点菜选择交给厨师，常见于日本料理。
Private Dining|私人宴聚|私宴定制|private dining room|为特定团体保留房间或区域，可另议菜单与服务。
Restaurant Buyout|餐廳包場|餐厅包场|exclusive restaurant hire|为一组宾客独家保留整间餐厅及指定用餐时段。
Sunday Roast|週日烤肉午餐|周日烤肉午餐|Sunday roast dinner|英式周日传统烤肉餐，通常配蔬菜、烤薯和肉汁。
Seasonal Specials|時令推介|当季限定菜|seasonal dishes|在食材当季期间供应，随产地和采购周期更新。
Daily Catch|每日鮮魚|当日鲜捕|fish of the day|根据当天采购的鲜鱼决定鱼种、份量和做法。
Daily Soup|是日餐湯|每日例汤|soup of the day|餐厅当天熬制并轮换供应的汤品。
Signature Dish|招牌菜式|招牌菜|house specialty|最能代表店家风格、通常长期供应的特色菜。
Small Plates|分享小碟|分享小盘菜|small plate menu|以小份上桌，方便客人同时尝试多种味道。
Dessert Trolley|甜品餐車|甜品推车|dessert cart|把多个甜点推至桌旁展示，由客人现场挑选。
Tea Pairing|佐餐配茶|茶饮配餐|tea and food pairing|按菜式的香气和口感安排不同茶叶或泡法。
Wine Pairing|餐酒配搭|葡萄酒配餐|paired wines|为各道菜选择能衬托酸度、脂香或鲜味的酒款。
Corkage|開瓶費|自带酒水开瓶费|corkage fee|餐厅对客人自带酒水提供开瓶和杯具服务的收费。
Cakeage|切餅費|自带蛋糕服务费|cakeage fee|餐厅替自带蛋糕的客人冷藏、分切或提供餐具的收费。
Walk-In Seating|即場輪候入座|到店排位|walk-ins welcome|未预约的客人到店按座位情况入座或排队等候。
Last Seating|最後入座時間|最晚入座时间|final seating|餐厅当日接受新一桌客人就坐的最晚时间。
Last Order|最後落單時間|最晚点单时间|kitchen last call|厨房或酒吧接受订单的截止时间，可能早于打烊。
"""

MENU_DISHES = """
Charcoal-Grilled Chicken Skewers|炭燒雞串|炭烤鸡肉串|charcoal yakitori|鸡肉穿串在炭火上烤，外层会留下烤痕与烟香。
Miso-Glazed Black Cod|味噌燒銀鱈魚|味噌烤银鳕鱼|miso black cod|以味噌腌制或刷酱后烤制，表层带焦甜香气。
Pan-Seared Scallops|香煎帶子|香煎扇贝柱|seared scallops|带子在热锅中快速煎上色，内部保留柔嫩口感。
Salt-Baked Sea Bass|鹽焗鱸魚|盐壳焗鲈鱼|sea bass baked in salt|用盐壳包裹整鱼入炉，敲壳后分切上桌。
Slow-Roasted Lamb Shoulder|慢烤羊肩|低温慢烤羊肩|roast shoulder of lamb|羊肩经较长时间烘烤，肉质松软，适合分食。
Braised Beef Cheek|慢燉牛面頰|慢炖牛脸颊肉|braised ox cheek|牛脸颊肉炖至胶质软化，常搭配浓缩炖汁。
Soy-Braised Pork Belly|豉油炆五花腩|酱油焖五花肉|soy-braised belly pork|带皮五花肉在酱油调味汁中焖至软糯。
Crispy Pork Belly|脆皮燒腩仔|脆皮烧肉|crispy roast pork belly|经风干等处理后高温烤脆猪皮，与柔嫩肉层形成对比。
Honey-Glazed Char Siu|蜜汁叉燒|蜜汁叉烧|honey char siu|叉烧烤制中刷上蜜汁，表面带甜香与焦边。
Claypot Rice|煲仔飯|煲仔饭|clay pot rice|米饭与配料在小砂锅中烹煮，锅底常有一层饭焦。
Wok-Fried Beef Ho Fun|乾炒牛河|干炒牛河|beef chow fun|用猛火快炒河粉、牛肉和芽菜，成菜强调锅气。
Steamed Egg Custard|滑蒸水蛋|嫩蒸鸡蛋羹|Chinese steamed egg|把调稀的蛋液温和蒸熟，质地细嫩。
Steamed Garoupa|清蒸石斑|清蒸石斑鱼|steamed grouper|以蒸汽快速加热石斑鱼，常配葱丝和豉油。
Typhoon Shelter Crab|避風塘炒蟹|避风塘炒蟹|typhoon-style crab|以炸蒜、辣椒等炒制蟹件，味道咸香。
Salt-and-Pepper Squid|椒鹽鮮魷|椒盐鱿鱼|salt and pepper calamari|鱿鱼炸后拌入椒盐和辛香料，表面酥香。
Crispy Tofu|香脆豆腐|酥脆豆腐|crunchy fried tofu|豆腐经煎、烤或炸后表面酥脆，内部仍柔软。
Chilled Drunken Chicken|冷盤醉雞|冰镇醉鸡|drunken chicken starter|熟鸡以酒香卤汁浸渍后冷食，常作前菜。
Tea-Smoked Duck|茶燻鴨|茶香熏鸭|tea smoked duck|用茶叶等材料熏制鸭肉，使表层带有茶香。
Hong Kong Milk Tea|港式奶茶|丝袜奶茶|silk stocking milk tea|浓红茶经过滤后加淡奶调和，奶香与茶涩并重。
Pineapple Bun with Butter|菠蘿油|菠萝油|bolo yau|在暖菠萝包中夹入冷牛油，口感酥甜咸香。
Egg and Luncheon Meat Sandwich|餐蛋治|午餐肉鸡蛋三明治|luncheon meat and egg toastie|以煎蛋和午餐肉作馅，常见于港式茶餐厅。
Baked Pork Chop Rice|焗豬扒飯|港式焗猪排饭|Hong Kong baked pork chop rice|煎炸猪排放在饭上，加番茄酱汁与芝士烘烤。
Hainanese Chicken Rice|海南雞飯|海南鸡饭|Hainan chicken rice|嫩鸡配用鸡汤与油脂煮成的香饭，通常附蘸酱。
Crab Roe Noodles|蟹黃拌麵|蟹黄拌面|crab roe tossed noodles|用蟹黄或蟹粉调成浓酱拌面，菜单要交代实际配料。
Sichuan Wontons in Chili Oil|紅油抄手|红油抄手|chili oil wontons|煮熟抄手用辣椒油和复合调味汁拌食。
Steamed Prawn Dumplings|鮮蝦餃|水晶虾饺|har gow|用薄透的澄粉皮包虾馅蒸熟，是粤式茶楼点心。
Steamed Pork Buns|鮮肉包|鲜肉包子|steamed pork bao|发面外皮包入猪肉馅蒸熟，馅料因店家而异。
Steamed Rice Noodle Rolls|蒸腸粉|蒸肠粉|cheung fun|薄米浆蒸片卷起，常淋豉油或加入虾、牛肉等馅料。
Beef Brisket Noodles|牛腩麵|牛腩面|brisket noodle soup|以炖牛腩、面条和汤底组合的主食。
House-Made Fish Balls|自家製魚蛋|手工鱼丸|homemade fish balls|店家自行打制成球的鱼浆制品，常加汤或咖喱酱。
Black Sesame Glutinous Rice Balls|芝麻湯圓|黑芝麻汤圆|sesame tangyuan|糯米外皮包入流质或细粒状的黑芝麻馅。
Almond Dessert Soup|杏仁茶|杏仁甜汤|Chinese almond soup|用杏仁或南北杏等打浆熬煮的中式甜品。
"""

COOKING_METHODS = """
Dry-Aged|乾式熟成|干式熟成|dry aging|肉类在受控温湿度下熟成，水分蒸发后风味更集中。
Wet-Aged|濕式熟成|湿式熟成|wet aging|肉类在真空包装中冷藏熟成，保留较多水分。
Sous Vide|慢煮|低温真空慢煮|sous-vide cooking|把食材密封后以受控水温加热至目标熟度。
Reverse-Seared|反向煎封|反向煎烤|reverse sear|先以低温使内部接近目标温度，再高温煎香表面。
Open-Fire Cooking|明火烹調|明火烹制|live fire cooking|直接运用炭、柴或火焰加热，风味随燃料和火候变化。
Wood-Fired|柴火烤製|柴火烤制|wood-fired cooking|以木材燃烧形成的高温炉烘烤，例如柴火炉披萨。
Stone-Baked|石板焗製|石板烘烤|stone oven baked|在预热石板上烘烤以快速定型底部，常用于面包和薄饼。
Double-Boiled|隔水燉|隔水炖|double-boiling|用带盖炖盅间接受热，减少汤汁蒸发。
Cold-Smoked|冷燻|冷熏|cold smoking|在较低温度熏染风味，通常不会把食材加热至全熟。
Hot-Smoked|熱燻|热熏|hot smoking|用带热量的烟熏制，熏制与加热烹调同时进行。
Confit|油封慢煮|油封慢煮|confit cooking|食材浸在油脂中缓慢加热，鸭腿与蒜头是常见例子。
Flambé|火焰煮法|火焰料理|flambe|用适量酒液引火完成一道烹调步骤，有时在客人桌旁进行。
Bain-Marie|水浴加熱|水浴加热|water bath cooking|在容器外加热水使内部均匀受热，适合焗布丁或酱汁。
Pressure-Cooked|壓力鍋烹調|高压烹煮|pressure cooking|用密闭容器提高烹调温度，缩短软化肉类或豆类所需时间。
Air-Fried|氣炸|空气炸制|air fryer cooking|以强制热风让食材表面脱水上色，油量仍以实际配方为准。
Deep-Fried|油炸|深油炸制|deep frying|食材浸入热油，使外部快速定型并形成脆壳。
Blanched|飛水|焯水|blanching|把食材短时间放入沸水，随后捞起，常用于蔬菜或去浮沫。
Charred|微焦炙烤|炙烤焦香|charred cooking|用高温让食材局部着色，带出焦香，常见于蔬菜或果片。
Gratinated|芝士焗面|焗烤上色|au gratin|以芝士、面包糠或酱汁覆盖表层烤至金黄。
Poached|浸煮|低温水煮|poaching|在低于沸腾的水或汤中温和煮熟，常见于蛋、鱼和水果。
Flash-Fried|快炸|快速过油|flash frying|以较高油温短时间炸制，让薄小食材快速上色。
Hand-Pulled|即拉手工製作|手工现拉|hand pulled noodles|用手反复拉伸面团成条，常用于现制面条。
Hand-Cut|人手切製|手工切制|hand cut|用刀手工切分食材，能体现切面和厚薄。
Stone-Ground|石磨|石磨研磨|stone milled|用石磨研磨谷物、芝麻或香料，影响颗粒度和口感。
Lacto-Fermented|乳酸菌發酵|乳酸发酵|lactic fermentation|利用乳酸菌生成酸味，常用于泡菜和部分乳制品。
Small-Batch Preserves|小批製果醬|小批量熬制果酱|small batch jam|按小锅分批熬煮的果酱，便于根据原果甜度控制批次。
"""

BAKERY = """
Butter Croissant|牛油牛角包|黄油可颂|all-butter croissant|以牛油分层折叠面团，烘烤形成酥皮和蜂窝气孔。
Pain au Chocolat|朱古力酥包|巧克力可颂卷|chocolate croissant|酥皮面团包入巧克力条烘烤，常见于法式烘焙柜。
Almond Croissant|杏仁牛角包|杏仁可颂|almond cream croissant|牛角包加杏仁奶油馅与杏仁片再烤，外脆内润。
Sourdough Loaf|酸種麵包|天然酵种面包|sourdough bread|用天然酵种发酵的面包，常有轻微酸味与韧性。
Brioche|牛油布里歐|布里欧修|French butter bread|在面团中加入较多蛋和牛油，质地绵软浓香。
Milk Bread|鮮奶方包|牛奶吐司|Japanese milk bread|用乳品等制作的柔软吐司，常做三文治或厚切烤吐司。
Focaccia|意式佛卡夏|意式佛卡夏|Italian flatbread|在面团表面按窝，淋橄榄油并配香草等烘烤。
Sea Salt Butter Roll|海鹽牛油卷|海盐黄油卷|shio pan|在面团中卷入牛油并撒盐烘烤，底部常有脆层。
Pandan Chiffon|斑蘭戚風蛋糕|斑斓戚风蛋糕|pandan sponge|带斑斓叶香的轻盈戚风蛋糕，以蛋白霜撑起蓬松口感。
Basque Cheesecake|巴斯克芝士蛋糕|巴斯克芝士蛋糕|burnt Basque cheesecake|用高温烤成深色表面，内层保持柔滑。
Japanese Cheesecake|日式梳乎厘芝士蛋糕|日式舒芙蕾芝士蛋糕|soufflé cheesecake|加入打发蛋白的轻盈芝士蛋糕，口感接近海绵蛋糕。
Burnt Custard Tart|焦糖吉士撻|焦糖卡仕达挞|caramelised custard tart|蛋奶馅表面烤出焦糖色，搭配酥脆塔壳。
Portuguese Egg Tart|葡式蛋撻|葡式蛋挞|pastel de nata|酥皮包裹蛋奶馅高温烤制，表面常见焦糖斑点。
Hong Kong Egg Tart|港式蛋撻|港式蛋挞|Hong Kong custard tart|以曲奇皮或酥皮包裹细嫩蛋馅的港式点心。
Canelé|可麗露|可露丽|canele pastry|法式小蛋糕，外皮焦糖化而内芯湿润。
Financier|法式杏仁金磚|费南雪|almond brown butter cake|以杏仁粉和焦化牛油做成的小蛋糕，常用长方模。
Madeleine|貝殼蛋糕|玛德琳|shell-shaped sponge cake|贝壳形的小蛋糕，有时加入柠檬皮或其他香料。
Palmier|蝴蝶酥|蝴蝶酥|elephant ear pastry|把撒糖酥皮折成双卷后切片烤脆。
Kouign-Amann|法式焦糖牛油酥|布列塔尼焦糖酥|Breton butter pastry|牛油酥面团叠入砂糖后烘烤，外皮形成焦糖薄层。
Mille-Feuille|法式千層酥|法式拿破仑酥|Napoleon pastry|层叠酥皮夹卡仕达等馅料，具有明显酥脆层次。
Cream Puff|吉士泡芙|奶油泡芙|choux puff|空心泡芙壳内注入吉士或鲜奶油等馅料。
Éclair|法式長泡芙|闪电泡芙|eclair pastry|长条形泡芙填入奶油馅，顶部常覆糖霜或巧克力。
Mochi Doughnut|麻糬冬甩|麻薯甜甜圈|mochi donut|加入糯米粉等带来软韧口感的甜甜圈。
Chocolate Babka|朱古力辮子包|巧克力巴布卡|chocolate swirl loaf|卷入巧克力馅再拧成辫形烘烤的面包。
Brown Butter Cookie|焦化牛油曲奇|焦化黄油曲奇|browned butter cookie|用加热至呈坚果香的牛油制作曲奇。
Salted Caramel Brownie|海鹽焦糖布朗尼|海盐焦糖布朗尼|salt caramel brownie|巧克力布朗尼搭配咸焦糖，使甜味更有层次。
Mango Pomelo Sago|楊枝甘露|杨枝甘露|mango sago dessert|芒果与柚子、西米组合成的港式冷甜品。
Double-Skin Milk|雙皮奶|双皮奶|double skin milk pudding|加热奶液并蒸成软凝乳，保留奶皮口感的顺德甜品。
Ginger Milk Curd|薑汁撞奶|姜撞奶|ginger milk pudding|利用鲜姜汁中的酶使温热牛奶凝固，呈柔嫩口感。
"""

COFFEE_PROVENANCE = """
Specialty Coffee|精品咖啡|精品咖啡|speciality coffee|以原料品质、可追溯性和感官表现为卖点的咖啡。
Single-Origin Coffee|單一產區咖啡|单一产地咖啡|single origin|来自单一国家、产区或庄园的咖啡，范围需具体说明。
Single-Estate Coffee|單一莊園咖啡|单一庄园咖啡|estate coffee|原豆来自同一座庄园，可进一步标示品种或地块。
Micro-Lot Coffee|微批次咖啡|微批次咖啡豆|microlot coffee|将某批原豆单独采收或处理，通常具有较明确的来源。
House Blend|自家拼配咖啡|门店拼配咖啡|house coffee blend|店家按杯测风味将不同来源或不同烘焙度的豆搭配。
Espresso Blend|意式拼配豆|意式拼配咖啡豆|espresso beans blend|按浓缩萃取表现搭配的咖啡豆，兼顾奶咖与纯饮。
Washed Coffee|水洗咖啡|水洗处理咖啡|washed process|去除果肉并清除黏液后再干燥，常呈现清晰酸质。
Natural Process Coffee|日曬咖啡|日晒处理咖啡|dry process coffee|让咖啡果实带皮干燥后再脱壳，常见较明显果香。
Honey Process Coffee|蜜處理咖啡|蜜处理咖啡|pulped natural coffee|去除果皮后保留部分黏液干燥，不代表添加蜂蜜。
Anaerobic Fermentation Coffee|厭氧發酵咖啡|厌氧发酵咖啡豆|anaerobic coffee|让咖啡果实或去皮豆在低氧环境发酵，再进入后续处理。
Carbonic Maceration Coffee|二氧化碳浸漬咖啡|二氧化碳浸渍咖啡|carbonic maceration process|在二氧化碳环境中进行整果等处理，具体方式由生产者说明。
Wet-Hulled Coffee|濕刨咖啡|湿刨处理咖啡|giling basah|咖啡豆在仍有较高含水量时脱壳，常见于印尼。
Swiss Water Decaf|瑞士水處理低因咖啡|瑞士水处理低因咖啡|Swiss Water Process|采用瑞士水处理工艺降低原豆中的咖啡因含量。
Sugarcane Decaf|甘蔗法低因咖啡|甘蔗法低因咖啡|ethyl acetate decaf|使用由甘蔗等来源取得的乙酸乙酯降低咖啡因。
Light Roast|淺烘焙|浅烘焙|light-roasted coffee|烘焙发展程度较浅，常突出豆子原本的香气和酸质。
Medium Roast|中度烘焙|中度烘焙|medium-roasted coffee|介于浅焙与深焙之间，常兼顾原豆风味与烘焙甜感。
Dark Roast|深烘焙|深烘焙|dark-roasted coffee|烘焙较深的豆，常出现焦糖、烟熏或苦甜味。
Roast Date|烘焙日期|烘焙日期|date roasted|记录咖啡豆烘焙完成的日期，与包装和到期日期不同。
Resting Period|養豆期|养豆期|coffee degassing window|豆子在烘焙后排出二氧化碳的时期，影响萃取的稳定性。
Coffee Cupping|咖啡杯測|咖啡杯测|coffee tasting session|按相对一致的冲煮条件比较多款咖啡的香气、口感和余韵。
Bean Subscription|咖啡豆訂閱|咖啡豆订阅|coffee subscription|定期寄送约定重量或品类的咖啡豆，可按方案换口味。
Coffee Bean Sampler|咖啡豆試飲組合|咖啡豆试喝装|coffee discovery pack|把少量多款原豆组在一起，方便客人对比风味。
Freshly Ground Coffee|即磨咖啡|现磨咖啡|ground to order|在点单或出货前研磨咖啡豆，减少研磨后的香气流失。
Burr Grinder|磨盤咖啡磨豆機|刀盘式磨豆机|burr coffee mill|以相对的磨盘磨碎咖啡豆，可按冲煮方式调整粗细。
Dial-In|調校萃取|萃取调参|espresso calibration|通过试冲调整研磨、用量或萃取时间，达到目标味道。
Seasonal Guest Bean|時令客席咖啡豆|当季客座豆|guest roaster coffee|店家阶段性选用其他烘焙商的豆，和常设拼配区分。
"""

COFFEE_NOTES = """
Jasmine Notes|茉莉花香|茉莉花香调|jasmine aroma|像茉莉花般轻盈的香气，常以鼻后香或热闻感受。
Orange Blossom Notes|橙花香|橙花香调|orange flower aroma|呈现类似橙花的甜白花香，和橙汁的味道不同。
Bergamot Notes|佛手柑香|佛手柑香调|bergamot aroma|带柑橘皮和茶香般的气息，常令人联想到伯爵茶。
Lemon Zest Notes|檸檬皮香|柠檬皮香调|lemon peel aroma|类似现刨柠檬外皮的芳香油气息，有时带微苦。
Grapefruit Notes|西柚風味|葡萄柚风味|pink grapefruit character|像西柚般明亮，酸感后可带轻微清苦。
Mandarin Notes|柑橘甜香|蜜橘甜香|tangerine notes|像熟柑橘果肉的柔甜气息，通常比柠檬圆润。
Green Apple Acidity|青蘋果般酸香|青苹果酸感|malic apple-like acidity|清脆而略尖的酸感，令人联想到青苹果。
Pear Notes|梨香|雪梨风味|ripe pear aroma|清淡爽甜的果香，有时伴随类似梨汁的水润口感。
White Peach Notes|白桃香|白桃风味|white peach aroma|类似成熟白桃的香气，可带轻柔花香。
Apricot Notes|杏桃果香|杏果风味|apricot aroma|类似鲜杏或杏脯的甜酸香气，常在温度降低后显现。
Blackberry Notes|黑莓果香|黑莓风味|blackberry aroma|偏深色浆果的酸甜气息，和红莓的明亮感不同。
Blueberry Notes|藍莓果香|蓝莓风味|blueberry aroma|类似熟蓝莓或蓝莓酱的果香与甜味联想。
Redcurrant Notes|紅醋栗酸香|红醋栗风味|red currant aroma|类似红醋栗的鲜酸小浆果香。
Dried Fig Notes|無花果乾香|无花果干风味|dried fig aroma|带果干与蜜糖般的甜香，常表现于余韵。
Raisin Notes|提子乾香|葡萄干风味|raisin aroma|类似葡萄干的浓缩果甜，有时伴随微酒香。
Pineapple Notes|菠蘿果香|菠萝风味|pineapple aroma|像菠萝果肉的热带香气，可同时带鲜酸。
Passion Fruit Notes|熱情果香|百香果风味|passionfruit notes|鲜明热带果香，常与活泼酸质一同出现。
Cacao Nib Notes|可可碎粒香|可可碎粒风味|cocoa nib aroma|像烘烤可可豆碎的微苦香气，通常甜感较低。
Dark Chocolate Finish|黑朱古力餘韻|黑巧克力尾韵|dark cocoa finish|吞咽后留在口中的可可香与轻微苦甜感。
Toasted Almond Notes|烘烤杏仁香|烘烤杏仁风味|roasted almond aroma|似烤过杏仁的坚果香，常见于烘焙甜感较明显的豆。
Hazelnut Notes|榛子香|榛子风味|hazelnut aroma|类似榛子仁的圆润烘烤气息，可与可可香同时出现。
Brown Sugar Sweetness|黑糖般甜香|红糖甜感|molasses sweetness|似未精炼糖的甘甜联想，有时带糖蜜香。
Maple Syrup Notes|楓糖漿香|枫糖浆风味|maple sweetness|带类似枫糖的烘烤甜香，不等于实际含糖浆。
Black Tea Finish|紅茶餘韻|红茶尾韵|tea-like finish|尾段出现茶叶般香气，质地通常清爽而略涩。
Silky Mouthfeel|絲滑口感|丝滑质感|silky texture|液体在口腔中显得细致顺滑，少有粗糙感。
"""

CAFE_DRINKS = """
Ristretto|短萃濃縮|短萃意式浓缩|short shot|同样用量以较少水量萃出，杯中液体更少。
Lungo|長萃濃縮|长萃意式浓缩|long shot espresso|用更多水通过咖啡粉来延长萃取，与事后加水不同。
Espresso Macchiato|意式濃縮瑪奇朵|意式浓缩玛奇朵|caffè macchiato|在浓缩上点少量奶泡，保留明显的咖啡味。
Cortado|西班牙小奶啡|科尔塔多|espresso cortado|在浓缩中加入近似等量的温奶以减轻锋利口感。
Piccolo Latte|小杯拿鐵|皮卡洛拿铁|piccolo coffee|杯量较小的奶咖，常以短萃浓缩搭配蒸奶。
Flat White|馥芮白|澳白|flatwhite|奶泡较薄、奶质细滑的奶咖，具体杯量各店不同。
Dirty Coffee|冰奶熱濃縮|Dirty 脏咖啡|dirty latte|把热浓缩直接倒在冷奶上，形成冷暖与色泽分层。
Espresso Tonic|湯力濃縮咖啡|汤力气泡咖啡|espresso and tonic|浓缩咖啡与汤力水组合成的冰饮，常带苦甜气泡。
Cold Brew|冷泡咖啡|冷萃咖啡|cold-brewed coffee|用冷水浸泡研磨后的咖啡豆较长时间再过滤。
Nitro Cold Brew|氮氣冷泡咖啡|氮气冷萃|nitro coffee|在冷泡咖啡中注入氮气，倒出后有绵密泡沫。
Japanese Iced Coffee|日式急冷手沖|日式冰手冲|flash brew coffee|用热水萃取咖啡并直接滴在冰块上迅速降温。
Pour-Over Coffee|手沖咖啡|手冲咖啡|filter pour over|用水壶分次把热水注入滤杯，让咖啡慢慢滤下。
French Press Coffee|法式濾壓咖啡|法压壶咖啡|cafetiere coffee|咖啡粉浸泡后用金属滤网下压分离，常保留油脂。
Moka Pot Coffee|摩卡壺咖啡|摩卡壶咖啡|stovetop moka|用炉火加热下壶水，借压力把水推过咖啡粉。
Batch Brew|批次滴濾咖啡|批量滴滤咖啡|batch filter coffee|使用滴滤机一次煮多杯，适合持续稳定出杯。
Vietnamese Iced Coffee|越式滴漏凍咖啡|越南滴漏冰咖啡|ca phe sua da|用越式滤器冲泡浓咖啡，再配炼奶和冰块饮用。
Affogato|濃縮咖啡配雪糕|阿芙佳朵|espresso over gelato|把浓缩浇在冰淇淋或意式冰淇淋上，冷热同吃。
Oat Milk Latte|燕麥奶拿鐵|燕麦拿铁|oat latte|用燕麦饮代替牛奶的拿铁，口感受品牌配方影响。
Brown Sugar Latte|黑糖拿鐵|红糖拿铁|molasses latte|以黑糖或红糖糖浆调甜的奶咖，有独特糖蜜香。
Orange Espresso|鮮橙濃縮咖啡|橙香浓缩咖啡|orange espresso drink|把鲜橙汁或橙风味基底与意式浓缩组合。
Matcha Latte|抹茶鮮奶|抹茶拿铁|matcha milk latte|以打散的抹茶粉与牛奶或植物饮调和。
Hojicha Latte|焙茶鮮奶|焙茶拿铁|roasted green tea latte|烘焙过的绿茶粉与奶调成，茶香偏坚果或木质。
Genmaicha|玄米茶|玄米茶|roasted rice green tea|将炒玄米与绿茶拼配，米香与清鲜茶味并存。
Cold Brew Oolong|冷泡烏龍茶|冷泡乌龙|cold-steeped oolong|以冷水慢慢泡出乌龙茶香，适合直接冷饮。
Hong Kong Lemon Tea|港式檸檬茶|港式冻柠茶|Hong Kong iced lemon tea|以浓红茶配柠檬片，可按冷热与糖量分别出品。
Yuenyeung|港式鴛鴦|港式鸳鸯奶茶|coffee milk tea|把咖啡与港式奶茶混合，兼具茶涩与咖啡烘焙香。
Cheese Foam Tea|芝士奶蓋茶|芝士奶盖茶|cheese tea|在茶汤上覆带咸味的打发奶盖。
Sparkling Yuzu Tea|柚子梳打茶|柚子气泡茶|yuzu tea soda|茶汤加入柚子汁或柚子酱，再以气泡水调开。
Hand-Shaken Fruit Tea|手搖鮮果茶|手打鲜果茶|shaken fruit tea|将果肉、茶汤与冰块现场摇匀，保持水果香气。
"""

WINE_TASTING = """
Wine Flight|葡萄酒試飲組合|葡萄酒品鉴组|wine tasting flight|按主题把几款酒分成小杯呈现，便于对比。
By-the-Glass Wine|單杯葡萄酒|杯卖葡萄酒|wine by the glass|以单杯定价供应，客人不必购买整瓶。
Cellar Selection|酒窖珍藏|酒窖精选|cellar list|餐厅从储藏酒款中挑出的特定酒单。
House Wine|餐廳精選餐酒|店选餐酒|house pour|餐厅挑选为日常供应的餐酒，常可按杯点。
Sommelier's Choice|侍酒師推介|侍酒师推荐|sommelier pick|由侍酒师根据当季菜单或客人喜好推荐的酒款。
Old-Vine Wine|老藤葡萄酒|老藤葡萄酒|old vine wine|用较老葡萄藤结出的果实酿成，树龄描述需有依据。
Single-Vineyard Wine|單一葡萄園佳釀|单一葡萄园葡萄酒|single vineyard bottling|葡萄原料来自一个标明的园区，与单一产区不同。
Vintage Release|指定年份新發行|指定年份新上市|vintage launch|推出标明葡萄采收年份的酒款，年份不是装瓶日。
Late-Harvest Wine|晚收葡萄酒|晚采葡萄酒|late harvest bottling|延后采收使葡萄糖分或香气累积，酒款风格依做法而异。
Ice Wine|冰酒|冰葡萄酒|eiswein|用按产区要求自然结冰采收的葡萄压榨酿造。
Fortified Wine|加烈葡萄酒|加强型葡萄酒|fortified style|酿造过程中添加蒸馏酒，提高酒精度并形成特定风格。
Orange Wine|橙酒|橙葡萄酒|skin contact wine|白葡萄带皮浸渍酿造而成，不表示加入橙汁。
Pet-Nat|自然氣泡酒|自然起泡酒|pétillant naturel|发酵尚未结束时装瓶以保留气泡的酒款。
Traditional-Method Sparkling|傳統法氣泡酒|传统法起泡酒|traditional method sparkling wine|通常以瓶中二次发酵产生气泡，工艺不等于香槟产地。
Brut Nature|零添糖極乾氣泡酒|天然极干型起泡酒|zero dosage sparkling|依相关标签标准使用的极低残糖类别，不额外补糖。
Blanc de Blancs|白中白氣泡酒|白中白起泡酒|white grapes sparkling wine|用白葡萄酿成的白色气泡酒，常见品种为霞多丽。
Rosé|粉紅葡萄酒|桃红葡萄酒|rose wine|颜色呈粉红的葡萄酒，可能通过短时浸皮等方式制成。
Dry Riesling|乾型雷司令|干型雷司令|trocken riesling|以雷司令酿成的干型白葡萄酒，常带清晰酸度。
Unoaked Chardonnay|無橡木桶霞多麗|未过橡木桶霞多丽|unoaked chardonnay wine|用不带橡木影响的容器发酵或陈放的霞多丽。
Full-Bodied Red|酒體厚實的紅酒|饱满酒体红葡萄酒|full body red|喝起来较有重量与厚度的红葡萄酒。
Light-Bodied White|輕盈白葡萄酒|轻酒体白葡萄酒|light body white|入口较轻、适合搭配细致口味菜式的白葡萄酒。
Fine Tannins|細緻單寧|细腻单宁|fine-grained tannins|涩感颗粒细、结构均匀的感官形容。
Crisp Acidity|爽脆酸度|清爽酸度|bright acidity|让味道显得清新、有唾液感的酸质表现。
Mineral Finish|礦物感餘韻|矿物感尾韵|mineral character|以石头、白垩等联想描述余味，不代表检测到矿物质。
Lees Aging|酒泥陳釀|酒泥陈酿|sur lie aging|让酒液在发酵后的酵母沉淀上陈放，可能增加质感。
Barrel Aging|橡木桶陳釀|橡木桶陈酿|oak maturation|让酒在木桶中陈放，香气受到木材、桶龄和时长影响。
Decanting|醒酒|醒酒处理|wine aeration|把酒倒入另一容器，按酒款情况帮助分离沉淀或接触空气。
"""

COCKTAILS = """
Signature Cocktail|招牌雞尾酒|招牌特调|house cocktail|由酒吧固定供应、能代表调酒风格的一款饮品。
Seasonal Cocktail|時令雞尾酒|当季特调|seasonal mixed drink|按当季水果、茶或香料设计的阶段性酒款。
Zero-Proof Cocktail|無酒精特調|无酒精鸡尾酒|mocktail|用无酒精配料做出鸡尾酒的风味层次和仪式感。
Low-ABV Cocktail|低酒精雞尾酒|低度鸡尾酒|low alcohol cocktail|成品酒精度比常规调酒低，但不等于无酒精。
Clarified Cocktail|澄清雞尾酒|澄清特调|clarified drink|通过过滤或其他工艺除去悬浮物，使酒液更清亮。
Milk Punch|奶洗賓治|奶洗潘趣|clarified milk punch|酸性基酒使牛奶凝结后过滤，形成清澈且柔滑的调酒。
Fat-Washed Spirit|油洗烈酒|脂洗基酒|fat washing|用牛油、芝麻油等脂肪给烈酒带入香气，再去除脂肪。
Barrel-Aged Cocktail|桶陳雞尾酒|桶陈鸡尾酒|barrel matured cocktail|将预调酒液放入桶中陈放，让各基酒和木香融合。
Smoked Cocktail|煙燻雞尾酒|烟熏鸡尾酒|smoke-infused cocktail|用烟熏木材、香料或容器为酒液带来烟香。
Tea-Infused Cocktail|茶香雞尾酒|茶酒特调|tea cocktail|以茶浸泡基酒或直接调入茶液，保留对应茶香。
Highball|高球雞尾酒|高球酒|whisky soda highball|基酒加较多气泡饮料装入高杯，通常使用充足冰块。
Whiskey Sour|威士忌酸酒|威士忌酸|whisky sour|以威士忌、柠檬和甜味成分调和，有时加入蛋白。
Old Fashioned|古典雞尾酒|古典鸡尾酒|old-fashioned whiskey cocktail|以威士忌、糖与苦精搅拌调成，常加橙皮。
Negroni|尼格羅尼|尼格罗尼|classic negroni|经典版本用金酒、红味美思和苦味开胃酒调和。
Boulevardier|林蔭大道雞尾酒|花花公子鸡尾酒|bourbon negroni|以威士忌取代经典尼格罗尼中的金酒，味道更温厚。
Espresso Martini|濃縮咖啡馬天尼|浓缩咖啡马天尼|coffee martini|用咖啡、伏特加与咖啡利口酒等摇制。
Gin and Tonic|氈酒湯力|金汤力|G&T|用金酒和汤力水调制，常以柑橘作点缀。
Champagne Cocktail|香檳雞尾酒|经典香槟鸡尾酒|classic champagne cocktail|以香槟冲入浸过苦精的方糖，常以柠檬皮点缀。
Paloma|西柚龍舌蘭特調|帕洛玛|grapefruit tequila cocktail|以龙舌兰和西柚风味气泡饮料为主要搭配。
Margarita|瑪格麗特雞尾酒|玛格丽特鸡尾酒|tequila margarita|经典配方以龙舌兰、橙味利口酒和青柠调制。
Dark and Stormy|黑冧酒薑啤特調|黑暗风暴鸡尾酒|dark rum ginger beer|用深色朗姆酒配姜汁啤酒，通常加青柠。
Sherry Cobbler|雪莉果香特調|雪莉考布勒|sherry fruit cobbler|雪莉酒、糖与水果配碎冰的经典鸡尾酒。
Aperitif|餐前開胃酒|餐前开胃酒|pre-dinner drink|通常在进餐前少量饮用，风格可干爽或带苦味。
Digestif|餐後酒|餐后消化酒|after-dinner drink|在餐后供应的酒类习惯名称，不表示有保健作用。
Spirit Flight|烈酒試飲組合|烈酒品鉴组|spirits tasting flight|将数款少量烈酒组成试饮组，便于比较桶型或产地。
"""

BEER_SAKE = """
Craft Lager|手工拉格啤酒|精酿拉格|craft lager beer|偏清爽的精酿啤酒，通常采用低温发酵和熟成。
Pilsner|皮爾森啤酒|皮尔森啤酒|pils beer|拉格啤酒的一种，常有清澈酒体和利落苦味。
Hazy IPA|混濁印度淡愛爾|浑浊 IPA|New England IPA|呈雾状的印度淡色艾尔，常突出果汁般酒花香。
West Coast IPA|美式西岸 IPA|西海岸 IPA|WCIPA|常见风格突出松针、柑橘和清晰的酒花苦度。
Dry-Hopped Pale Ale|乾投酒花淡愛爾|干投淡色艾尔|dry hopped ale|发酵阶段或之后加入酒花，主要为了强化香气。
Wheat Beer|小麥啤酒|小麦啤酒|weissbier|配方中使用较多小麦，风格可能带香蕉或香料气息。
Oatmeal Stout|燕麥世濤|燕麦世涛|oat stout|使用燕麦增加酒体顺滑感的深色啤酒。
Imperial Stout|帝國世濤|帝国世涛|imperial dark ale|风味浓厚的深色啤酒风格，酒精度通常较高。
Kettle Sour|煮鍋酸啤|壶酸啤酒|kettle soured beer|在煮沸锅中先使麦汁酸化，再进入常规酿造流程。
Fruit Gose|水果古斯酸啤|水果古斯|fruit gose beer|在带轻微咸味的酸啤基底上加入水果风味。
Draft Beer|生啤|扎啤|draught beer|从桶经酒头打出的啤酒，和瓶装、罐装区分。
Beer Flight|手工啤酒試飲組合|精酿啤酒品鉴组|beer sampler|由几款小杯啤酒组成的试饮组合，常按风格排列。
Junmai|純米清酒|纯米清酒|junmai sake|以米、米曲和水酿成的清酒类型，未添加酿造酒精。
Junmai Ginjo|純米吟釀|纯米吟酿|junmai ginjo sake|符合纯米与吟酿类别要求的清酒，常带鲜明香气。
Junmai Daiginjo|純米大吟釀|纯米大吟酿|junmai daiginjo sake|使用精米比例较低的原料并以吟酿方法酿造的纯米清酒。
Nama Sake|生酒|未杀菌生清酒|namazake|未经巴氏杀菌处理的清酒，通常需要冷藏。
Nigori Sake|濁酒|浊清酒|cloudy sake|保留部分米粒和米浆，呈乳白或浑浊外观。
Sake Flight|日本清酒試飲組合|清酒品鉴组|sake sampler|将不同精米、酿造工艺或产地的清酒分成小杯比较。
"""
