"""Editorial phrase families for restaurant, beverage, and menu copy.

Rows are intentionally selected, so a cooking method is only paired with
ingredients it is used for and menu claims retain their actual meaning.
Each row contains EN, HK, CN, a search alias, and definitions in Chinese and English.
"""

DINING_FORMATS = """
Tasting Menu|品嚐餐單|品鉴菜单|degustation menu|由主厨安排多道小份菜式，按顺序呈现一季食材或料理主题。|A chef-selected sequence of small courses built around a season, ingredient or culinary theme.
Chef's Table|主廚餐桌|主厨餐桌|chef's counter|通常设在厨房旁，由主厨或团队近距离介绍料理。|Seats near the kitchen where the chef or team presents the meal directly to diners.
Counter Dining|吧枱用餐|吧台用餐|counter seats|坐在吧台用餐，常能看见备菜、调酒或出品过程。|A meal served at a counter where guests can often watch food or drinks being prepared.
Set Lunch|午市套餐|午间套餐|lunch set|午餐时段供应、按固定价格组合主菜和配菜的餐点。|A fixed-price combination of a main course and accompaniments served during lunch hours.
Early Dinner Menu|早段晚市餐單|早场晚餐菜单|early supper menu|为较早入座的客人提供一套独立晚餐菜单。|A separate dinner selection available to guests who reserve an earlier seating.
Pre-Theatre Dinner|觀劇前晚餐|观演前晚餐|pre-show dining|围绕演出开场前的时段安排节奏较快的晚餐。|A paced dinner service timed so diners can finish before a nearby performance begins.
À la Carte|單點餐單|单点菜单|a la carte|每道菜单独点选与定价，可按人数自由组合。|A menu on which dishes are ordered and priced individually.
Prix Fixe|定價套餐|固定价套餐|fixed-price menu|按统一价格供应约定道数的餐点，部分菜式可选。|A meal with a specified number of courses for a fixed price, sometimes with choices within each course.
Market Menu|街市時令餐單|时令市集菜单|daily market menu|按当天采购到的蔬果、海鲜或肉类调整菜式。|A menu that changes according to the produce, seafood or meat sourced that day.
Plant-Based Tasting Menu|植物料理品嚐餐單|植物料理品鉴菜单|plant-forward tasting|用豆类、蔬果和谷物组织多道菜式，细节需看实际配方。|A sequence of courses centred on legumes, grains, vegetables and fruit, with ingredients listed by dish.
Dim Sum Brunch|點心早午餐|广式点心早午餐|dim sum brunch service|以茶楼点心为主的早午餐，常搭配茶水与热菜。|A brunch centred on Cantonese dim sum, often served with tea and hot dishes.
Free-Flow Brunch|早午餐連無限添飲|早午餐含畅饮|bottomless brunch|早午餐附指定饮品在限定时间内续杯的权益。|Brunch with refills of specified drinks included for a stated period.
Sharing Menu|共享餐單|分享式菜单|family-style dining|菜式集中端上桌，由同桌客人分食，适合聚餐。|A selection of dishes placed at the centre of the table for guests to serve themselves.
Omakase|廚師發辦|主厨发办|chef's choice menu|客人把点菜选择交给厨师，常见于日本料理。|A Japanese dining format in which the guest leaves the choice and sequence of dishes to the chef.
Private Dining|私人宴聚|私宴定制|private dining room|为特定团体保留房间或区域，可另议菜单与服务。|A room or section reserved for a group, with menus and service arranged for the occasion.
Restaurant Buyout|餐廳包場|餐厅包场|exclusive restaurant hire|为一组宾客独家保留整间餐厅及指定用餐时段。|Exclusive use of an entire restaurant for a group during an agreed service period.
Sunday Roast|週日烤肉午餐|周日烤肉午餐|Sunday roast dinner|英式周日传统烤肉餐，通常配蔬菜、烤薯和肉汁。|A traditional British Sunday meal of roasted meat, commonly served with vegetables, potatoes and gravy.
Seasonal Specials|時令推介|当季限定菜|seasonal dishes|在食材当季期间供应，随产地和采购周期更新。|Dishes offered while particular ingredients are in season, subject to sourcing and availability.
Daily Catch|每日鮮魚|当日鲜捕|fish of the day|根据当天采购的鲜鱼决定鱼种、份量和做法。|The fresh fish available that day, with species, portion and preparation depending on the catch.
Daily Soup|是日餐湯|每日例汤|soup of the day|餐厅当天熬制并轮换供应的汤品。|The soup prepared and offered by the restaurant on a particular day.
Signature Dish|招牌菜式|招牌菜|house specialty|最能代表店家风格、通常长期供应的特色菜。|A dish that represents the restaurant's style and is usually a regular menu feature.
Small Plates|分享小碟|分享小盘菜|small plate menu|以小份上桌，方便客人同时尝试多种味道。|Dishes served in smaller portions so guests can sample or share several selections.
Dessert Trolley|甜品餐車|甜品推车|dessert cart|把多个甜点推至桌旁展示，由客人现场挑选。|A wheeled display that brings a selection of desserts to the table for guests to choose from.
Tea Pairing|佐餐配茶|茶饮配餐|tea and food pairing|按菜式的香气和口感安排不同茶叶或泡法。|A selection of teas or brewing styles chosen to complement the aromas and textures of a meal.
Wine Pairing|餐酒配搭|葡萄酒配餐|paired wines|为各道菜选择能衬托酸度、脂香或鲜味的酒款。|Wines selected for how their acidity, body and flavour complement each course.
Corkage|開瓶費|自带酒水开瓶费|corkage fee|餐厅对客人自带酒水提供开瓶和杯具服务的收费。|A restaurant charge for opening and serving wine or other drinks brought by diners.
Cakeage|切餅費|自带蛋糕服务费|cakeage fee|餐厅替自带蛋糕的客人冷藏、分切或提供餐具的收费。|A charge for storing, cutting or serving a cake that diners bring to the restaurant.
Walk-In Seating|即場輪候入座|到店排位|walk-ins welcome|未预约的客人到店按座位情况入座或排队等候。|Seating for guests without reservations, subject to table availability and any queue.
Last Seating|最後入座時間|最晚入座时间|final seating|餐厅当日接受新一桌客人就坐的最晚时间。|The latest time at which a restaurant will seat a new party on a given day.
Last Order|最後落單時間|最晚点单时间|kitchen last call|厨房或酒吧接受订单的截止时间，可能早于打烊。|The cutoff for ordering food or drinks, which may be earlier than closing time.
"""

MENU_DISHES = """
Charcoal-Grilled Chicken Skewers|炭燒雞串|炭烤鸡肉串|charcoal yakitori|鸡肉穿串在炭火上烤，外层会留下烤痕与烟香。|Pieces of chicken threaded on skewers and grilled over charcoal for smoky, browned edges.
Miso-Glazed Black Cod|味噌燒銀鱈魚|味噌烤银鳕鱼|miso black cod|以味噌腌制或刷酱后烤制，表层带焦甜香气。|Black cod marinated or brushed with miso and roasted until the surface develops a sweet glaze.
Pan-Seared Scallops|香煎帶子|香煎扇贝柱|seared scallops|带子在热锅中快速煎上色，内部保留柔嫩口感。|Scallops quickly browned in a hot pan while their centres remain tender.
Salt-Baked Sea Bass|鹽焗鱸魚|盐壳焗鲈鱼|sea bass baked in salt|用盐壳包裹整鱼入炉，敲壳后分切上桌。|Whole sea bass baked inside a salt crust that is cracked open before serving.
Slow-Roasted Lamb Shoulder|慢烤羊肩|低温慢烤羊肩|roast shoulder of lamb|羊肩经较长时间烘烤，肉质松软，适合分食。|Lamb shoulder roasted slowly until tender, often served in a portion for sharing.
Braised Beef Cheek|慢燉牛面頰|慢炖牛脸颊肉|braised ox cheek|牛脸颊肉炖至胶质软化，常搭配浓缩炖汁。|Beef cheek cooked slowly until its connective tissue softens, often served with reduced braising juices.
Soy-Braised Pork Belly|豉油炆五花腩|酱油焖五花肉|soy-braised belly pork|带皮五花肉在酱油调味汁中焖至软糯。|Skin-on pork belly cooked slowly in a soy-based liquid until soft and rich.
Crispy Pork Belly|脆皮燒腩仔|脆皮烧肉|crispy roast pork belly|经风干等处理后高温烤脆猪皮，与柔嫩肉层形成对比。|Pork belly roasted at high heat to crisp the skin above the tender layers of meat.
Honey-Glazed Char Siu|蜜汁叉燒|蜜汁叉烧|honey char siu|叉烧烤制中刷上蜜汁，表面带甜香与焦边。|Cantonese roast pork brushed with honey during cooking for a sweet finish and caramelised edges.
Claypot Rice|煲仔飯|煲仔饭|clay pot rice|米饭与配料在小砂锅中烹煮，锅底常有一层饭焦。|Rice and toppings cooked together in a small clay pot, often forming a crisp layer at the bottom.
Wok-Fried Beef Ho Fun|乾炒牛河|干炒牛河|beef chow fun|用猛火快炒河粉、牛肉和芽菜，成菜强调锅气。|Wide rice noodles, beef and bean sprouts tossed over high heat for the aroma of wok cooking.
Steamed Egg Custard|滑蒸水蛋|嫩蒸鸡蛋羹|Chinese steamed egg|把调稀的蛋液温和蒸熟，质地细嫩。|A smooth savoury custard made by gently steaming beaten eggs diluted with liquid.
Steamed Garoupa|清蒸石斑|清蒸石斑鱼|steamed grouper|以蒸汽快速加热石斑鱼，常配葱丝和豉油。|Grouper cooked quickly in steam and often served with scallions and soy sauce.
Typhoon Shelter Crab|避風塘炒蟹|避风塘炒蟹|typhoon-style crab|以炸蒜、辣椒等炒制蟹件，味道咸香。|Crab pieces tossed with fried garlic, chilli and seasonings in a Hong Kong style.
Salt-and-Pepper Squid|椒鹽鮮魷|椒盐鱿鱼|salt and pepper calamari|鱿鱼炸后拌入椒盐和辛香料，表面酥香。|Fried squid tossed with salt, pepper and aromatics for a crisp, seasoned coating.
Crispy Tofu|香脆豆腐|酥脆豆腐|crunchy fried tofu|豆腐经煎、烤或炸后表面酥脆，内部仍柔软。|Tofu cooked until crisp on the outside while its centre stays soft.
Chilled Drunken Chicken|冷盤醉雞|冰镇醉鸡|drunken chicken starter|熟鸡以酒香卤汁浸渍后冷食，常作前菜。|Cooked chicken steeped in an aromatic wine-based liquid and served cold, often as a starter.
Tea-Smoked Duck|茶燻鴨|茶香熏鸭|tea smoked duck|用茶叶等材料熏制鸭肉，使表层带有茶香。|Duck smoked with tea leaves and other aromatics to scent the surface.
Hong Kong Milk Tea|港式奶茶|丝袜奶茶|silk stocking milk tea|浓红茶经过滤后加淡奶调和，奶香与茶涩并重。|Strong, strained black tea mixed with evaporated milk for a rich drink with a brisk finish.
Pineapple Bun with Butter|菠蘿油|菠萝油|bolo yau|在暖菠萝包中夹入冷牛油，口感酥甜咸香。|A warm Hong Kong pineapple bun split and filled with a slice of cold butter.
Egg and Luncheon Meat Sandwich|餐蛋治|午餐肉鸡蛋三明治|luncheon meat and egg toastie|以煎蛋和午餐肉作馅，常见于港式茶餐厅。|A Hong Kong café sandwich filled with fried egg and sliced luncheon meat.
Baked Pork Chop Rice|焗豬扒飯|港式焗猪排饭|Hong Kong baked pork chop rice|煎炸猪排放在饭上，加番茄酱汁与芝士烘烤。|A Hong Kong café dish of pork chop and rice baked under tomato sauce and cheese.
Hainanese Chicken Rice|海南雞飯|海南鸡饭|Hainan chicken rice|嫩鸡配用鸡汤与油脂煮成的香饭，通常附蘸酱。|Tender chicken served with rice cooked in stock and chicken fat, usually accompanied by dipping sauces.
Crab Roe Noodles|蟹黃拌麵|蟹黄拌面|crab roe tossed noodles|用蟹黄或蟹粉调成浓酱拌面，菜单要交代实际配料。|Noodles tossed in a rich sauce made with crab roe or picked crab, depending on the recipe.
Sichuan Wontons in Chili Oil|紅油抄手|红油抄手|chili oil wontons|煮熟抄手用辣椒油和复合调味汁拌食。|Boiled Sichuan-style wontons dressed with chilli oil and a seasoned sauce.
Steamed Prawn Dumplings|鮮蝦餃|水晶虾饺|har gow|用薄透的澄粉皮包虾馅蒸熟，是粤式茶楼点心。|Cantonese dim sum with prawn filling inside thin, translucent steamed wrappers.
Steamed Pork Buns|鮮肉包|鲜肉包子|steamed pork bao|发面外皮包入猪肉馅蒸熟，馅料因店家而异。|Steamed buns made with risen dough and a savoury pork filling that varies by kitchen.
Steamed Rice Noodle Rolls|蒸腸粉|蒸肠粉|cheung fun|薄米浆蒸片卷起，常淋豉油或加入虾、牛肉等馅料。|Thin sheets of steamed rice batter rolled plain or around fillings, often served with soy sauce.
Beef Brisket Noodles|牛腩麵|牛腩面|brisket noodle soup|以炖牛腩、面条和汤底组合的主食。|Noodles served with braised beef brisket and broth.
House-Made Fish Balls|自家製魚蛋|手工鱼丸|homemade fish balls|店家自行打制成球的鱼浆制品，常加汤或咖喱酱。|Fish paste shaped and cooked in-house into balls, often served in broth or curry sauce.
Black Sesame Glutinous Rice Balls|芝麻湯圓|黑芝麻汤圆|sesame tangyuan|糯米外皮包入流质或细粒状的黑芝麻馅。|Glutinous rice dumplings with a smooth or finely ground black sesame filling.
Almond Dessert Soup|杏仁茶|杏仁甜汤|Chinese almond soup|用杏仁或南北杏等打浆熬煮的中式甜品。|A sweet Chinese soup made by blending and cooking almonds or apricot kernels, depending on the recipe.
"""

COOKING_METHODS = """
Dry-Aged|乾式熟成|干式熟成|dry aging|肉类在受控温湿度下熟成，水分蒸发后风味更集中。|Meat matured under controlled temperature and humidity to concentrate its flavour as moisture evaporates.
Wet-Aged|濕式熟成|湿式熟成|wet aging|肉类在真空包装中冷藏熟成，保留较多水分。|Meat matured under refrigeration in sealed packaging to retain moisture.
Sous Vide|慢煮|低温真空慢煮|sous-vide cooking|把食材密封后以受控水温加热至目标熟度。|A method of cooking sealed ingredients in temperature-controlled water to reach a precise doneness.
Reverse-Seared|反向煎封|反向煎烤|reverse sear|先以低温使内部接近目标温度，再高温煎香表面。|Cooked first at a low temperature, then seared at high heat to brown the surface.
Open-Fire Cooking|明火烹調|明火烹制|live fire cooking|直接运用炭、柴或火焰加热，风味随燃料和火候变化。|Cooking over flame, wood or coals, where the fuel and heat influence the flavour.
Wood-Fired|柴火烤製|柴火烤制|wood-fired cooking|以木材燃烧形成的高温炉烘烤，例如柴火炉披萨。|Cooked in an oven heated by burning wood, as with many pizzas and flatbreads.
Stone-Baked|石板焗製|石板烘烤|stone oven baked|在预热石板上烘烤以快速定型底部，常用于面包和薄饼。|Baked on a preheated stone that quickly sets the base of bread or flatbread.
Double-Boiled|隔水燉|隔水炖|double-boiling|用带盖炖盅间接受热，减少汤汁蒸发。|Cooked gently in a covered vessel heated indirectly to limit evaporation.
Cold-Smoked|冷燻|冷熏|cold smoking|在较低温度熏染风味，通常不会把食材加热至全熟。|Exposed to smoke at a low temperature to add flavour without necessarily cooking the food through.
Hot-Smoked|熱燻|热熏|hot smoking|用带热量的烟熏制，熏制与加热烹调同时进行。|Cooked and flavoured at the same time by exposure to warm smoke.
Confit|油封慢煮|油封慢煮|confit cooking|食材浸在油脂中缓慢加热，鸭腿与蒜头是常见例子。|An ingredient slowly cooked in fat, as with duck legs or garlic.
Flambé|火焰煮法|火焰料理|flambe|用适量酒液引火完成一道烹调步骤，有时在客人桌旁进行。|A technique in which alcohol is ignited briefly during cooking, sometimes at the table.
Bain-Marie|水浴加熱|水浴加热|water bath cooking|在容器外加热水使内部均匀受热，适合焗布丁或酱汁。|A hot-water bath that heats custards, sauces or other delicate preparations evenly.
Pressure-Cooked|壓力鍋烹調|高压烹煮|pressure cooking|用密闭容器提高烹调温度，缩短软化肉类或豆类所需时间。|Cooked in a sealed vessel under pressure to soften ingredients at a higher temperature in less time.
Air-Fried|氣炸|空气炸制|air fryer cooking|以强制热风让食材表面脱水上色，油量仍以实际配方为准。|Cooked with fast-circulating hot air to dry and brown the surface, with oil use depending on the recipe.
Deep-Fried|油炸|深油炸制|deep frying|食材浸入热油，使外部快速定型并形成脆壳。|Immersed in hot oil to set and crisp the exterior quickly.
Blanched|飛水|焯水|blanching|把食材短时间放入沸水，随后捞起，常用于蔬菜或去浮沫。|Briefly immersed in boiling water, often to prepare vegetables or remove impurities.
Charred|微焦炙烤|炙烤焦香|charred cooking|用高温让食材局部着色，带出焦香，常见于蔬菜或果片。|Partly blackened over high heat to bring a toasted, smoky flavour to the surface.
Gratinated|芝士焗面|焗烤上色|au gratin|以芝士、面包糠或酱汁覆盖表层烤至金黄。|Baked with a topping such as cheese, breadcrumbs or sauce until golden.
Poached|浸煮|低温水煮|poaching|在低于沸腾的水或汤中温和煮熟，常见于蛋、鱼和水果。|Gently cooked in water or stock below boiling point, as with eggs, fish or fruit.
Flash-Fried|快炸|快速过油|flash frying|以较高油温短时间炸制，让薄小食材快速上色。|Fried briefly at high heat so small or thin ingredients colour quickly.
Hand-Pulled|即拉手工製作|手工现拉|hand pulled noodles|用手反复拉伸面团成条，常用于现制面条。|Shaped by stretching dough repeatedly by hand, as in fresh noodles.
Hand-Cut|人手切製|手工切制|hand cut|用刀手工切分食材，能体现切面和厚薄。|Cut by hand to give an ingredient a particular thickness or finish.
Stone-Ground|石磨|石磨研磨|stone milled|用石磨研磨谷物、芝麻或香料，影响颗粒度和口感。|Milled between stones, a process that can affect the texture of grains, seeds and spices.
Lacto-Fermented|乳酸菌發酵|乳酸发酵|lactic fermentation|利用乳酸菌生成酸味，常用于泡菜和部分乳制品。|Fermented with lactic acid bacteria for a tangy flavour, as in pickles and some dairy products.
Small-Batch Preserves|小批製果醬|小批量熬制果酱|small batch jam|按小锅分批熬煮的果酱，便于根据原果甜度控制批次。|Fruit preserves cooked in small batches to adjust for the sweetness and character of each lot.
"""

BAKERY = """
Butter Croissant|牛油牛角包|黄油可颂|all-butter croissant|以牛油分层折叠面团，烘烤形成酥皮和蜂窝气孔。|A laminated pastry whose folded butter layers bake into a crisp shell and open crumb.
Pain au Chocolat|朱古力酥包|巧克力可颂卷|chocolate croissant|酥皮面团包入巧克力条烘烤，常见于法式烘焙柜。|A French laminated pastry baked around bars of chocolate.
Almond Croissant|杏仁牛角包|杏仁可颂|almond cream croissant|牛角包加杏仁奶油馅与杏仁片再烤，外脆内润。|A croissant filled with almond cream, topped with sliced almonds and baked again.
Sourdough Loaf|酸種麵包|天然酵种面包|sourdough bread|用天然酵种发酵的面包，常有轻微酸味与韧性。|Bread leavened with a natural starter, often with a mild tang and chewy crumb.
Brioche|牛油布里歐|布里欧修|French butter bread|在面团中加入较多蛋和牛油，质地绵软浓香。|A rich, soft bread made with an enriched dough containing eggs and butter.
Milk Bread|鮮奶方包|牛奶吐司|Japanese milk bread|用乳品等制作的柔软吐司，常做三文治或厚切烤吐司。|A soft loaf enriched with milk, often sliced for sandwiches or thick toast.
Focaccia|意式佛卡夏|意式佛卡夏|Italian flatbread|在面团表面按窝，淋橄榄油并配香草等烘烤。|A dimpled Italian bread baked with olive oil and often topped with herbs.
Sea Salt Butter Roll|海鹽牛油卷|海盐黄油卷|shio pan|在面团中卷入牛油并撒盐烘烤，底部常有脆层。|A roll baked with butter folded into the dough and salt on top, often with a crisp base.
Pandan Chiffon|斑蘭戚風蛋糕|斑斓戚风蛋糕|pandan sponge|带斑斓叶香的轻盈戚风蛋糕，以蛋白霜撑起蓬松口感。|An airy chiffon cake scented with pandan leaves and lifted by whipped egg whites.
Basque Cheesecake|巴斯克芝士蛋糕|巴斯克芝士蛋糕|burnt Basque cheesecake|用高温烤成深色表面，内层保持柔滑。|A cheesecake baked at high heat for a dark top and a soft, creamy centre.
Japanese Cheesecake|日式梳乎厘芝士蛋糕|日式舒芙蕾芝士蛋糕|soufflé cheesecake|加入打发蛋白的轻盈芝士蛋糕，口感接近海绵蛋糕。|A light cheesecake lifted with whipped egg whites for a sponge-like texture.
Burnt Custard Tart|焦糖吉士撻|焦糖卡仕达挞|caramelised custard tart|蛋奶馅表面烤出焦糖色，搭配酥脆塔壳。|A crisp tart shell filled with custard and baked until the top caramelises.
Portuguese Egg Tart|葡式蛋撻|葡式蛋挞|pastel de nata|酥皮包裹蛋奶馅高温烤制，表面常见焦糖斑点。|A flaky pastry cup filled with custard and baked at high heat to produce dark spots on top.
Hong Kong Egg Tart|港式蛋撻|港式蛋挞|Hong Kong custard tart|以曲奇皮或酥皮包裹细嫩蛋馅的港式点心。|A Hong Kong pastry with delicate egg custard in a shortcrust or flaky shell.
Canelé|可麗露|可露丽|canele pastry|法式小蛋糕，外皮焦糖化而内芯湿润。|A small French cake with a dark, caramelised crust and a moist centre.
Financier|法式杏仁金磚|费南雪|almond brown butter cake|以杏仁粉和焦化牛油做成的小蛋糕，常用长方模。|A small French almond cake made with browned butter, often baked in a rectangular mould.
Madeleine|貝殼蛋糕|玛德琳|shell-shaped sponge cake|贝壳形的小蛋糕，有时加入柠檬皮或其他香料。|A small shell-shaped cake sometimes flavoured with citrus zest or spices.
Palmier|蝴蝶酥|蝴蝶酥|elephant ear pastry|把撒糖酥皮折成双卷后切片烤脆。|Sugared puff pastry folded into two coils, sliced and baked until crisp.
Kouign-Amann|法式焦糖牛油酥|布列塔尼焦糖酥|Breton butter pastry|牛油酥面团叠入砂糖后烘烤，外皮形成焦糖薄层。|A Breton pastry with sugar folded into layers of butter-rich dough that caramelise as it bakes.
Mille-Feuille|法式千層酥|法式拿破仑酥|Napoleon pastry|层叠酥皮夹卡仕达等馅料，具有明显酥脆层次。|Layers of crisp puff pastry alternating with fillings such as pastry cream.
Cream Puff|吉士泡芙|奶油泡芙|choux puff|空心泡芙壳内注入吉士或鲜奶油等馅料。|A hollow choux pastry shell filled with custard, whipped cream or a similar filling.
Éclair|法式長泡芙|闪电泡芙|eclair pastry|长条形泡芙填入奶油馅，顶部常覆糖霜或巧克力。|An elongated choux pastry filled with cream and often topped with icing or chocolate.
Mochi Doughnut|麻糬冬甩|麻薯甜甜圈|mochi donut|加入糯米粉等带来软韧口感的甜甜圈。|A doughnut made with an ingredient such as glutinous rice flour to give it a chewy texture.
Chocolate Babka|朱古力辮子包|巧克力巴布卡|chocolate swirl loaf|卷入巧克力馅再拧成辫形烘烤的面包。|A sweet loaf made by rolling dough around chocolate filling and twisting the layers before baking.
Brown Butter Cookie|焦化牛油曲奇|焦化黄油曲奇|browned butter cookie|用加热至呈坚果香的牛油制作曲奇。|A cookie made with butter heated until the milk solids turn brown and smell nutty.
Salted Caramel Brownie|海鹽焦糖布朗尼|海盐焦糖布朗尼|salt caramel brownie|巧克力布朗尼搭配咸焦糖，使甜味更有层次。|A chocolate brownie with salted caramel for a sweet and salty finish.
Mango Pomelo Sago|楊枝甘露|杨枝甘露|mango sago dessert|芒果与柚子、西米组合成的港式冷甜品。|A chilled Hong Kong dessert combining mango, pomelo and sago pearls.
Double-Skin Milk|雙皮奶|双皮奶|double skin milk pudding|加热奶液并蒸成软凝乳，保留奶皮口感的顺德甜品。|A Shunde dessert made by steaming milk into a soft custard and retaining its delicate surface skin.
Ginger Milk Curd|薑汁撞奶|姜撞奶|ginger milk pudding|利用鲜姜汁中的酶使温热牛奶凝固，呈柔嫩口感。|A soft milk dessert set by the natural enzymes in fresh ginger juice.
"""

COFFEE_PROVENANCE = """
Specialty Coffee|精品咖啡|精品咖啡|speciality coffee|以原料品质、可追溯性和感官表现为卖点的咖啡。|Coffee sold for its bean quality, traceable origin and distinctive sensory attributes.
Single-Origin Coffee|單一產區咖啡|单一产地咖啡|single origin|来自单一国家、产区或庄园的咖啡，范围需具体说明。|Coffee sourced from one stated country, growing area or farm.
Single-Estate Coffee|單一莊園咖啡|单一庄园咖啡|estate coffee|原豆来自同一座庄园，可进一步标示品种或地块。|Coffee whose beans come from one estate, sometimes with the variety or plot named.
Micro-Lot Coffee|微批次咖啡|微批次咖啡豆|microlot coffee|将某批原豆单独采收或处理，通常具有较明确的来源。|A separately harvested or processed batch of coffee with a defined provenance.
House Blend|自家拼配咖啡|门店拼配咖啡|house coffee blend|店家按杯测风味将不同来源或不同烘焙度的豆搭配。|A café or roaster's own mix of coffees or roast profiles selected for a consistent flavour.
Espresso Blend|意式拼配豆|意式拼配咖啡豆|espresso beans blend|按浓缩萃取表现搭配的咖啡豆，兼顾奶咖与纯饮。|A mix of beans designed for espresso extraction, often to suit both black and milk-based drinks.
Washed Coffee|水洗咖啡|水洗处理咖啡|washed process|去除果肉并清除黏液后再干燥，常呈现清晰酸质。|Coffee dried after the fruit and mucilage are removed, often showing a clean acidity.
Natural Process Coffee|日曬咖啡|日晒处理咖啡|dry process coffee|让咖啡果实带皮干燥后再脱壳，常见较明显果香。|Coffee dried in the whole cherry before hulling, often with prominent fruit aromas.
Honey Process Coffee|蜜處理咖啡|蜜处理咖啡|pulped natural coffee|去除果皮后保留部分黏液干燥，不代表添加蜂蜜。|Coffee dried with some of its mucilage still attached after the skin is removed.
Anaerobic Fermentation Coffee|厭氧發酵咖啡|厌氧发酵咖啡豆|anaerobic coffee|让咖啡果实或去皮豆在低氧环境发酵，再进入后续处理。|Coffee fermented in a low-oxygen environment before further processing.
Carbonic Maceration Coffee|二氧化碳浸漬咖啡|二氧化碳浸渍咖啡|carbonic maceration process|在二氧化碳环境中进行整果等处理，具体方式由生产者说明。|Coffee cherries processed in a carbon dioxide-rich environment, with the exact method varying by producer.
Wet-Hulled Coffee|濕刨咖啡|湿刨处理咖啡|giling basah|咖啡豆在仍有较高含水量时脱壳，常见于印尼。|Coffee hulled while its beans retain more moisture than in conventional processing, a method common in Indonesia.
Swiss Water Decaf|瑞士水處理低因咖啡|瑞士水处理低因咖啡|Swiss Water Process|采用瑞士水处理工艺降低原豆中的咖啡因含量。|Coffee decaffeinated with the Swiss Water process, which uses water-based extraction.
Sugarcane Decaf|甘蔗法低因咖啡|甘蔗法低因咖啡|ethyl acetate decaf|使用由甘蔗等来源取得的乙酸乙酯降低咖啡因。|Coffee decaffeinated with ethyl acetate sourced from sugarcane or similar materials.
Light Roast|淺烘焙|浅烘焙|light-roasted coffee|烘焙发展程度较浅，常突出豆子原本的香气和酸质。|Coffee roasted to a lighter degree, often retaining more of the bean's original aromas and acidity.
Medium Roast|中度烘焙|中度烘焙|medium-roasted coffee|介于浅焙与深焙之间，常兼顾原豆风味与烘焙甜感。|Coffee roasted between light and dark, balancing origin flavours with sweetness developed during roasting.
Dark Roast|深烘焙|深烘焙|dark-roasted coffee|烘焙较深的豆，常出现焦糖、烟熏或苦甜味。|Coffee roasted to a deeper degree for prominent roasted, bittersweet or smoky notes.
Roast Date|烘焙日期|烘焙日期|date roasted|记录咖啡豆烘焙完成的日期，与包装和到期日期不同。|The date coffee beans finished roasting, separate from their packing or expiry date.
Resting Period|養豆期|养豆期|coffee degassing window|豆子在烘焙后排出二氧化碳的时期，影响萃取的稳定性。|The interval after roasting when beans release carbon dioxide, which can affect extraction.
Coffee Cupping|咖啡杯測|咖啡杯测|coffee tasting session|按相对一致的冲煮条件比较多款咖啡的香气、口感和余韵。|A standardised tasting method for comparing coffees' aroma, texture and finish.
Bean Subscription|咖啡豆訂閱|咖啡豆订阅|coffee subscription|定期寄送约定重量或品类的咖啡豆，可按方案换口味。|A recurring delivery of coffee beans in quantities or varieties set by a subscription plan.
Coffee Bean Sampler|咖啡豆試飲組合|咖啡豆试喝装|coffee discovery pack|把少量多款原豆组在一起，方便客人对比风味。|A set of small portions of different coffees sold for side-by-side tasting.
Freshly Ground Coffee|即磨咖啡|现磨咖啡|ground to order|在点单或出货前研磨咖啡豆，减少研磨后的香气流失。|Coffee beans ground close to serving or dispatch to limit aroma loss after grinding.
Burr Grinder|磨盤咖啡磨豆機|刀盘式磨豆机|burr coffee mill|以相对的磨盘磨碎咖啡豆，可按冲煮方式调整粗细。|A grinder that uses two opposing burrs with an adjustable gap to control the grind size.
Dial-In|調校萃取|萃取调参|espresso calibration|通过试冲调整研磨、用量或萃取时间，达到目标味道。|Trial brewing to adjust grind size, dose or extraction time until the coffee tastes as intended.
Seasonal Guest Bean|時令客席咖啡豆|当季客座豆|guest roaster coffee|店家阶段性选用其他烘焙商的豆，和常设拼配区分。|A rotating coffee from a visiting roaster that sits alongside a café's regular offerings.
"""

COFFEE_NOTES = """
Jasmine Notes|茉莉花香|茉莉花香调|jasmine aroma|像茉莉花般轻盈的香气，常以鼻后香或热闻感受。|A light floral aroma reminiscent of jasmine, perceived when smelling or sipping the coffee.
Orange Blossom Notes|橙花香|橙花香调|orange flower aroma|呈现类似橙花的甜白花香，和橙汁的味道不同。|A sweet white-flower aroma resembling orange blossom.
Bergamot Notes|佛手柑香|佛手柑香调|bergamot aroma|带柑橘皮和茶香般的气息，常令人联想到伯爵茶。|A citrus-peel aroma reminiscent of bergamot and Earl Grey tea.
Lemon Zest Notes|檸檬皮香|柠檬皮香调|lemon peel aroma|类似现刨柠檬外皮的芳香油气息，有时带微苦。|A fragrant lemon-peel character that may carry a slight bitterness.
Grapefruit Notes|西柚風味|葡萄柚风味|pink grapefruit character|像西柚般明亮，酸感后可带轻微清苦。|Bright citrus acidity reminiscent of grapefruit, sometimes followed by a gentle bitterness.
Mandarin Notes|柑橘甜香|蜜橘甜香|tangerine notes|像熟柑橘果肉的柔甜气息，通常比柠檬圆润。|A rounded, sweet citrus aroma reminiscent of ripe mandarins.
Green Apple Acidity|青蘋果般酸香|青苹果酸感|malic apple-like acidity|清脆而略尖的酸感，令人联想到青苹果。|A sharp, refreshing acidity that recalls biting into a green apple.
Pear Notes|梨香|雪梨风味|ripe pear aroma|清淡爽甜的果香，有时伴随类似梨汁的水润口感。|A light, sweet fruit aroma that can recall the juiciness of a pear.
White Peach Notes|白桃香|白桃风味|white peach aroma|类似成熟白桃的香气，可带轻柔花香。|A ripe white-peach aroma with a possible soft floral undertone.
Apricot Notes|杏桃果香|杏果风味|apricot aroma|类似鲜杏或杏脯的甜酸香气，常在温度降低后显现。|A sweet-tart aroma resembling fresh or dried apricots, sometimes clearer as coffee cools.
Blackberry Notes|黑莓果香|黑莓风味|blackberry aroma|偏深色浆果的酸甜气息，和红莓的明亮感不同。|A sweet-tart dark berry character reminiscent of blackberries.
Blueberry Notes|藍莓果香|蓝莓风味|blueberry aroma|类似熟蓝莓或蓝莓酱的果香与甜味联想。|A fruit aroma or sweetness reminiscent of ripe blueberries or blueberry jam.
Redcurrant Notes|紅醋栗酸香|红醋栗风味|red currant aroma|类似红醋栗的鲜酸小浆果香。|A bright, tart berry aroma reminiscent of redcurrants.
Dried Fig Notes|無花果乾香|无花果干风味|dried fig aroma|带果干与蜜糖般的甜香，常表现于余韵。|A dried-fruit and honey-like sweetness often noticed in the finish.
Raisin Notes|提子乾香|葡萄干风味|raisin aroma|类似葡萄干的浓缩果甜，有时伴随微酒香。|A concentrated dried-grape sweetness, sometimes with a wine-like aroma.
Pineapple Notes|菠蘿果香|菠萝风味|pineapple aroma|像菠萝果肉的热带香气，可同时带鲜酸。|A tropical fruit character reminiscent of pineapple, sometimes with a bright acidity.
Passion Fruit Notes|熱情果香|百香果风味|passionfruit notes|鲜明热带果香，常与活泼酸质一同出现。|A distinctive tropical aroma reminiscent of passion fruit, often paired with lively acidity.
Cacao Nib Notes|可可碎粒香|可可碎粒风味|cocoa nib aroma|像烘烤可可豆碎的微苦香气，通常甜感较低。|A roasted cacao aroma with mild bitterness and little perceived sweetness.
Dark Chocolate Finish|黑朱古力餘韻|黑巧克力尾韵|dark cocoa finish|吞咽后留在口中的可可香与轻微苦甜感。|A lingering cocoa aroma and bittersweet taste after swallowing.
Toasted Almond Notes|烘烤杏仁香|烘烤杏仁风味|roasted almond aroma|似烤过杏仁的坚果香，常见于烘焙甜感较明显的豆。|A roasted nut aroma reminiscent of toasted almonds.
Hazelnut Notes|榛子香|榛子风味|hazelnut aroma|类似榛子仁的圆润烘烤气息，可与可可香同时出现。|A rounded, roasted nut aroma that can accompany cocoa-like flavours.
Brown Sugar Sweetness|黑糖般甜香|红糖甜感|molasses sweetness|似未精炼糖的甘甜联想，有时带糖蜜香。|A perceived sweetness reminiscent of unrefined brown sugar or molasses.
Maple Syrup Notes|楓糖漿香|枫糖浆风味|maple sweetness|带类似枫糖的烘烤甜香，不等于实际含糖浆。|A warm, toasted sweetness reminiscent of maple syrup.
Black Tea Finish|紅茶餘韻|红茶尾韵|tea-like finish|尾段出现茶叶般香气，质地通常清爽而略涩。|A lingering black tea aroma, often with a light, slightly astringent finish.
Silky Mouthfeel|絲滑口感|丝滑质感|silky texture|液体在口腔中显得细致顺滑，少有粗糙感。|A fine, smooth texture in the mouth with little roughness.
"""

CAFE_DRINKS = """
Ristretto|短萃濃縮|短萃意式浓缩|short shot|同样用量以较少水量萃出，杯中液体更少。|An espresso-style shot made with less water for a smaller yield from a similar dose of coffee.
Lungo|長萃濃縮|长萃意式浓缩|long shot espresso|用更多水通过咖啡粉来延长萃取，与事后加水不同。|An espresso-style shot drawn with more water passing through the grounds for a larger yield.
Espresso Macchiato|意式濃縮瑪奇朵|意式浓缩玛奇朵|caffè macchiato|在浓缩上点少量奶泡，保留明显的咖啡味。|Espresso marked with a small amount of milk foam.
Cortado|西班牙小奶啡|科尔塔多|espresso cortado|在浓缩中加入近似等量的温奶以减轻锋利口感。|Espresso mixed with roughly the same amount of warm milk to soften its intensity.
Piccolo Latte|小杯拿鐵|皮卡洛拿铁|piccolo coffee|杯量较小的奶咖，常以短萃浓缩搭配蒸奶。|A small milk coffee often made with a ristretto shot and steamed milk.
Flat White|馥芮白|澳白|flatwhite|奶泡较薄、奶质细滑的奶咖，具体杯量各店不同。|An espresso-based milk coffee with fine-textured steamed milk and a thin layer of foam.
Dirty Coffee|冰奶熱濃縮|Dirty 脏咖啡|dirty latte|把热浓缩直接倒在冷奶上，形成冷暖与色泽分层。|Hot espresso poured directly over cold milk to create layers and a temperature contrast.
Espresso Tonic|湯力濃縮咖啡|汤力气泡咖啡|espresso and tonic|浓缩咖啡与汤力水组合成的冰饮，常带苦甜气泡。|A chilled drink combining espresso with tonic water for a bittersweet sparkle.
Cold Brew|冷泡咖啡|冷萃咖啡|cold-brewed coffee|用冷水浸泡研磨后的咖啡豆较长时间再过滤。|Coffee made by steeping grounds in cold water for an extended period before filtering.
Nitro Cold Brew|氮氣冷泡咖啡|氮气冷萃|nitro coffee|在冷泡咖啡中注入氮气，倒出后有绵密泡沫。|Cold brew infused with nitrogen to create a fine, creamy head when poured.
Japanese Iced Coffee|日式急冷手沖|日式冰手冲|flash brew coffee|用热水萃取咖啡并直接滴在冰块上迅速降温。|Coffee brewed hot directly over ice for rapid chilling.
Pour-Over Coffee|手沖咖啡|手冲咖啡|filter pour over|用水壶分次把热水注入滤杯，让咖啡慢慢滤下。|Coffee brewed by pouring hot water over grounds in a filter by hand.
French Press Coffee|法式濾壓咖啡|法压壶咖啡|cafetiere coffee|咖啡粉浸泡后用金属滤网下压分离，常保留油脂。|Coffee steeped in water and separated by pressing down a metal filter.
Moka Pot Coffee|摩卡壺咖啡|摩卡壶咖啡|stovetop moka|用炉火加热下壶水，借压力把水推过咖啡粉。|Coffee brewed in a stovetop pot that uses pressure to push hot water through the grounds.
Batch Brew|批次滴濾咖啡|批量滴滤咖啡|batch filter coffee|使用滴滤机一次煮多杯，适合持续稳定出杯。|Drip coffee brewed several servings at a time on an automatic brewer.
Vietnamese Iced Coffee|越式滴漏凍咖啡|越南滴漏冰咖啡|ca phe sua da|用越式滤器冲泡浓咖啡，再配炼奶和冰块饮用。|Strong coffee brewed with a Vietnamese filter and served over ice, often with condensed milk.
Affogato|濃縮咖啡配雪糕|阿芙佳朵|espresso over gelato|把浓缩浇在冰淇淋或意式冰淇淋上，冷热同吃。|Espresso poured over gelato or ice cream and served immediately.
Oat Milk Latte|燕麥奶拿鐵|燕麦拿铁|oat latte|用燕麦饮代替牛奶的拿铁，口感受品牌配方影响。|An espresso latte made with an oat-based drink instead of dairy milk.
Brown Sugar Latte|黑糖拿鐵|红糖拿铁|molasses latte|以黑糖或红糖糖浆调甜的奶咖，有独特糖蜜香。|An espresso and milk drink sweetened with brown sugar syrup for a molasses-like note.
Orange Espresso|鮮橙濃縮咖啡|橙香浓缩咖啡|orange espresso drink|把鲜橙汁或橙风味基底与意式浓缩组合。|A drink combining espresso with orange juice or an orange-flavoured base.
Matcha Latte|抹茶鮮奶|抹茶拿铁|matcha milk latte|以打散的抹茶粉与牛奶或植物饮调和。|A drink of whisked matcha powder and dairy or plant-based milk.
Hojicha Latte|焙茶鮮奶|焙茶拿铁|roasted green tea latte|烘焙过的绿茶粉与奶调成，茶香偏坚果或木质。|A milk drink made with roasted green tea, often with nutty or woody aromas.
Genmaicha|玄米茶|玄米茶|roasted rice green tea|将炒玄米与绿茶拼配，米香与清鲜茶味并存。|A Japanese blend of green tea and roasted brown rice.
Cold Brew Oolong|冷泡烏龍茶|冷泡乌龙|cold-steeped oolong|以冷水慢慢泡出乌龙茶香，适合直接冷饮。|Oolong tea steeped in cold water to extract its aroma gradually.
Hong Kong Lemon Tea|港式檸檬茶|港式冻柠茶|Hong Kong iced lemon tea|以浓红茶配柠檬片，可按冷热与糖量分别出品。|A Hong Kong drink of strong black tea and sliced lemon, served hot or iced.
Yuenyeung|港式鴛鴦|港式鸳鸯奶茶|coffee milk tea|把咖啡与港式奶茶混合，兼具茶涩与咖啡烘焙香。|A Hong Kong café drink blending coffee with milk tea.
Cheese Foam Tea|芝士奶蓋茶|芝士奶盖茶|cheese tea|在茶汤上覆带咸味的打发奶盖。|Tea topped with whipped dairy foam with a lightly salty flavour.
Sparkling Yuzu Tea|柚子梳打茶|柚子气泡茶|yuzu tea soda|茶汤加入柚子汁或柚子酱，再以气泡水调开。|Tea mixed with yuzu juice or preserve and topped up with sparkling water.
Hand-Shaken Fruit Tea|手搖鮮果茶|手打鲜果茶|shaken fruit tea|将果肉、茶汤与冰块现场摇匀，保持水果香气。|A drink made by shaking fruit, tea and ice together just before serving.
"""

WINE_TASTING = """
Wine Flight|葡萄酒試飲組合|葡萄酒品鉴组|wine tasting flight|按主题把几款酒分成小杯呈现，便于对比。|A set of small wine pours presented together for comparison.
By-the-Glass Wine|單杯葡萄酒|杯卖葡萄酒|wine by the glass|以单杯定价供应，客人不必购买整瓶。|Wine sold as an individual serving without requiring a full bottle purchase.
Cellar Selection|酒窖珍藏|酒窖精选|cellar list|餐厅从储藏酒款中挑出的特定酒单。|A selection drawn from a restaurant or merchant's stored wines.
House Wine|餐廳精選餐酒|店选餐酒|house pour|餐厅挑选为日常供应的餐酒，常可按杯点。|A wine chosen by the venue for regular service, often available by the glass.
Sommelier's Choice|侍酒師推介|侍酒师推荐|sommelier pick|由侍酒师根据当季菜单或客人喜好推荐的酒款。|A wine recommended by the sommelier for the menu or a guest's preferences.
Old-Vine Wine|老藤葡萄酒|老藤葡萄酒|old vine wine|用较老葡萄藤结出的果实酿成，树龄描述需有依据。|Wine from older grapevines, with the age claim dependent on the producer's evidence.
Single-Vineyard Wine|單一葡萄園佳釀|单一葡萄园葡萄酒|single vineyard bottling|葡萄原料来自一个标明的园区，与单一产区不同。|Wine made from grapes sourced from one named vineyard.
Vintage Release|指定年份新發行|指定年份新上市|vintage launch|推出标明葡萄采收年份的酒款，年份不是装瓶日。|A release of wine identified by its grape harvest year.
Late-Harvest Wine|晚收葡萄酒|晚采葡萄酒|late harvest bottling|延后采收使葡萄糖分或香气累积，酒款风格依做法而异。|Wine made with grapes left longer on the vine to develop sugar or aroma before harvest.
Ice Wine|冰酒|冰葡萄酒|eiswein|用按产区要求自然结冰采收的葡萄压榨酿造。|Wine pressed from grapes harvested naturally frozen, subject to local production rules.
Fortified Wine|加烈葡萄酒|加强型葡萄酒|fortified style|酿造过程中添加蒸馏酒，提高酒精度并形成特定风格。|Wine to which a distilled spirit is added during production, altering its strength and style.
Orange Wine|橙酒|橙葡萄酒|skin contact wine|白葡萄带皮浸渍酿造而成，不表示加入橙汁。|Wine made from white grapes fermented or macerated with their skins, giving colour and texture.
Pet-Nat|自然氣泡酒|自然起泡酒|pétillant naturel|发酵尚未结束时装瓶以保留气泡的酒款。|A sparkling wine bottled before its first fermentation ends so that carbon dioxide is retained.
Traditional-Method Sparkling|傳統法氣泡酒|传统法起泡酒|traditional method sparkling wine|通常以瓶中二次发酵产生气泡，工艺不等于香槟产地。|Sparkling wine produced by a second fermentation in the bottle.
Brut Nature|零添糖極乾氣泡酒|天然极干型起泡酒|zero dosage sparkling|依相关标签标准使用的极低残糖类别，不额外补糖。|A sparkling wine label for very low residual sugar with no sugar added at dosage, under applicable rules.
Blanc de Blancs|白中白氣泡酒|白中白起泡酒|white grapes sparkling wine|用白葡萄酿成的白色气泡酒，常见品种为霞多丽。|A white sparkling wine made from white grapes, commonly Chardonnay.
Rosé|粉紅葡萄酒|桃红葡萄酒|rose wine|颜色呈粉红的葡萄酒，可能通过短时浸皮等方式制成。|A pink wine often made by allowing red grapes only brief contact with their skins.
Dry Riesling|乾型雷司令|干型雷司令|trocken riesling|以雷司令酿成的干型白葡萄酒，常带清晰酸度。|A dry white wine made from Riesling grapes, often with pronounced acidity.
Unoaked Chardonnay|無橡木桶霞多麗|未过橡木桶霞多丽|unoaked chardonnay wine|用不带橡木影响的容器发酵或陈放的霞多丽。|Chardonnay fermented or matured without an influence from oak.
Full-Bodied Red|酒體厚實的紅酒|饱满酒体红葡萄酒|full body red|喝起来较有重量与厚度的红葡萄酒。|A red wine that feels substantial and weighty on the palate.
Light-Bodied White|輕盈白葡萄酒|轻酒体白葡萄酒|light body white|入口较轻、适合搭配细致口味菜式的白葡萄酒。|A white wine with a lighter texture and weight, often suited to delicate dishes.
Fine Tannins|細緻單寧|细腻单宁|fine-grained tannins|涩感颗粒细、结构均匀的感官形容。|Tannins that give wine a finely textured, even astringency.
Crisp Acidity|爽脆酸度|清爽酸度|bright acidity|让味道显得清新、有唾液感的酸质表现。|A fresh, lively acidity that creates a mouthwatering sensation.
Mineral Finish|礦物感餘韻|矿物感尾韵|mineral character|以石头、白垩等联想描述余味，不代表检测到矿物质。|A finish that evokes stone or chalk, used as a tasting impression.
Lees Aging|酒泥陳釀|酒泥陈酿|sur lie aging|让酒液在发酵后的酵母沉淀上陈放，可能增加质感。|Maturation on the yeast sediment left after fermentation, which can change the wine's texture.
Barrel Aging|橡木桶陳釀|橡木桶陈酿|oak maturation|让酒在木桶中陈放，香气受到木材、桶龄和时长影响。|Maturing wine in wooden barrels, with flavour influenced by the wood, barrel age and time.
Decanting|醒酒|醒酒处理|wine aeration|把酒倒入另一容器，按酒款情况帮助分离沉淀或接触空气。|Pouring wine into a separate vessel to leave sediment behind or expose it to air.
"""

COCKTAILS = """
Signature Cocktail|招牌雞尾酒|招牌特调|house cocktail|由酒吧固定供应、能代表调酒风格的一款饮品。|A regular cocktail chosen to represent a bar's style.
Seasonal Cocktail|時令雞尾酒|当季特调|seasonal mixed drink|按当季水果、茶或香料设计的阶段性酒款。|A temporary cocktail built around ingredients associated with the season.
Zero-Proof Cocktail|無酒精特調|无酒精鸡尾酒|mocktail|用无酒精配料做出鸡尾酒的风味层次和仪式感。|A mixed drink made with alcohol-free ingredients and served in the style of a cocktail.
Low-ABV Cocktail|低酒精雞尾酒|低度鸡尾酒|low alcohol cocktail|成品酒精度比常规调酒低，但不等于无酒精。|A cocktail with a lower alcohol by volume than typical mixed drinks, which can still contain alcohol.
Clarified Cocktail|澄清雞尾酒|澄清特调|clarified drink|通过过滤或其他工艺除去悬浮物，使酒液更清亮。|A cocktail filtered or otherwise processed to remove suspended particles for a clearer appearance.
Milk Punch|奶洗賓治|奶洗潘趣|clarified milk punch|酸性基酒使牛奶凝结后过滤，形成清澈且柔滑的调酒。|A punch clarified by curdling milk with an acidic mixture and then filtering out the solids.
Fat-Washed Spirit|油洗烈酒|脂洗基酒|fat washing|用牛油、芝麻油等脂肪给烈酒带入香气，再去除脂肪。|A spirit infused with flavour from a fat such as butter or sesame oil before that fat is removed.
Barrel-Aged Cocktail|桶陳雞尾酒|桶陈鸡尾酒|barrel matured cocktail|将预调酒液放入桶中陈放，让各基酒和木香融合。|A premixed cocktail rested in a wooden barrel so its components take on and integrate wood flavours.
Smoked Cocktail|煙燻雞尾酒|烟熏鸡尾酒|smoke-infused cocktail|用烟熏木材、香料或容器为酒液带来烟香。|A cocktail given a smoky aroma with wood smoke, aromatics or a smoked serving vessel.
Tea-Infused Cocktail|茶香雞尾酒|茶酒特调|tea cocktail|以茶浸泡基酒或直接调入茶液，保留对应茶香。|A cocktail flavoured by infusing tea into the base spirit or mixing in brewed tea.
Highball|高球雞尾酒|高球酒|whisky soda highball|基酒加较多气泡饮料装入高杯，通常使用充足冰块。|A spirit and a generous measure of carbonated mixer served over ice in a tall glass.
Whiskey Sour|威士忌酸酒|威士忌酸|whisky sour|以威士忌、柠檬和甜味成分调和，有时加入蛋白。|Whiskey, lemon juice and a sweetener, sometimes shaken with egg white.
Old Fashioned|古典雞尾酒|古典鸡尾酒|old-fashioned whiskey cocktail|以威士忌、糖与苦精搅拌调成，常加橙皮。|A stirred mix of whiskey, sugar and bitters, often finished with orange peel.
Negroni|尼格羅尼|尼格罗尼|classic negroni|经典版本用金酒、红味美思和苦味开胃酒调和。|A classic combination of gin, sweet vermouth and a bitter aperitif.
Boulevardier|林蔭大道雞尾酒|花花公子鸡尾酒|bourbon negroni|以威士忌取代经典尼格罗尼中的金酒，味道更温厚。|A cocktail with whiskey, sweet vermouth and a bitter aperitif, related to the Negroni.
Espresso Martini|濃縮咖啡馬天尼|浓缩咖啡马天尼|coffee martini|用咖啡、伏特加与咖啡利口酒等摇制。|A shaken drink commonly made with espresso, vodka and coffee liqueur.
Gin and Tonic|氈酒湯力|金汤力|G&T|用金酒和汤力水调制，常以柑橘作点缀。|Gin mixed with tonic water and often garnished with citrus.
Champagne Cocktail|香檳雞尾酒|经典香槟鸡尾酒|classic champagne cocktail|以香槟冲入浸过苦精的方糖，常以柠檬皮点缀。|Champagne poured over a sugar cube soaked in bitters, often finished with lemon peel.
Paloma|西柚龍舌蘭特調|帕洛玛|grapefruit tequila cocktail|以龙舌兰和西柚风味气泡饮料为主要搭配。|A tequila cocktail usually lengthened with a sparkling grapefruit mixer.
Margarita|瑪格麗特雞尾酒|玛格丽特鸡尾酒|tequila margarita|经典配方以龙舌兰、橙味利口酒和青柠调制。|A classic mix of tequila, orange liqueur and lime juice.
Dark and Stormy|黑冧酒薑啤特調|黑暗风暴鸡尾酒|dark rum ginger beer|用深色朗姆酒配姜汁啤酒，通常加青柠。|Dark rum mixed with ginger beer, commonly served with lime.
Sherry Cobbler|雪莉果香特調|雪莉考布勒|sherry fruit cobbler|雪莉酒、糖与水果配碎冰的经典鸡尾酒。|A classic drink of sherry, sugar and fruit over crushed ice.
Aperitif|餐前開胃酒|餐前开胃酒|pre-dinner drink|通常在进餐前少量饮用，风格可干爽或带苦味。|A drink served before a meal, often dry or bitter in style.
Digestif|餐後酒|餐后消化酒|after-dinner drink|在餐后供应的酒类习惯名称，不表示有保健作用。|A drink traditionally served after a meal, such as brandy or an herbal liqueur.
Spirit Flight|烈酒試飲組合|烈酒品鉴组|spirits tasting flight|将数款少量烈酒组成试饮组，便于比较桶型或产地。|A set of small pours of different spirits for comparing origin, ageing or style.
"""

BEER_SAKE = """
Craft Lager|手工拉格啤酒|精酿拉格|craft lager beer|偏清爽的精酿啤酒，通常采用低温发酵和熟成。|A craft beer fermented and conditioned in the lager style, usually with a clean, refreshing profile.
Pilsner|皮爾森啤酒|皮尔森啤酒|pils beer|拉格啤酒的一种，常有清澈酒体和利落苦味。|A clear lager style often characterised by a brisk hop bitterness.
Hazy IPA|混濁印度淡愛爾|浑浊 IPA|New England IPA|呈雾状的印度淡色艾尔，常突出果汁般酒花香。|An India pale ale with a cloudy appearance and often a juicy hop aroma.
West Coast IPA|美式西岸 IPA|西海岸 IPA|WCIPA|常见风格突出松针、柑橘和清晰的酒花苦度。|An India pale ale style known for distinct bitterness and pine or citrus hop character.
Dry-Hopped Pale Ale|乾投酒花淡愛爾|干投淡色艾尔|dry hopped ale|发酵阶段或之后加入酒花，主要为了强化香气。|Pale ale with hops added during or after fermentation to increase aroma.
Wheat Beer|小麥啤酒|小麦啤酒|weissbier|配方中使用较多小麦，风格可能带香蕉或香料气息。|Beer brewed with a substantial proportion of wheat, sometimes with banana or spice notes.
Oatmeal Stout|燕麥世濤|燕麦世涛|oat stout|使用燕麦增加酒体顺滑感的深色啤酒。|A dark beer brewed with oats to give the body a smooth texture.
Imperial Stout|帝國世濤|帝国世涛|imperial dark ale|风味浓厚的深色啤酒风格，酒精度通常较高。|A rich, intensely flavoured dark beer style that is typically higher in alcohol.
Kettle Sour|煮鍋酸啤|壶酸啤酒|kettle soured beer|在煮沸锅中先使麦汁酸化，再进入常规酿造流程。|A beer soured in the brewing kettle before boiling and fermentation continue.
Fruit Gose|水果古斯酸啤|水果古斯|fruit gose beer|在带轻微咸味的酸啤基底上加入水果风味。|A tart, lightly salty wheat beer with added fruit flavour.
Draft Beer|生啤|扎啤|draught beer|从桶经酒头打出的啤酒，和瓶装、罐装区分。|Beer dispensed from a keg through a tap.
Beer Flight|手工啤酒試飲組合|精酿啤酒品鉴组|beer sampler|由几款小杯啤酒组成的试饮组合，常按风格排列。|A tasting set of small beer pours, often arranged to compare different styles.
Junmai|純米清酒|纯米清酒|junmai sake|以米、米曲和水酿成的清酒类型，未添加酿造酒精。|Sake brewed with rice, koji and water without added brewing alcohol.
Junmai Ginjo|純米吟釀|纯米吟酿|junmai ginjo sake|符合纯米与吟酿类别要求的清酒，常带鲜明香气。|Aromatic sake made to both junmai and ginjo requirements.
Junmai Daiginjo|純米大吟釀|纯米大吟酿|junmai daiginjo sake|使用精米比例较低的原料并以吟酿方法酿造的纯米清酒。|Junmai sake brewed using daiginjo methods and more highly polished rice.
Nama Sake|生酒|未杀菌生清酒|namazake|未经巴氏杀菌处理的清酒，通常需要冷藏。|Unpasteurised sake that generally requires cold storage.
Nigori Sake|濁酒|浊清酒|cloudy sake|保留部分米粒和米浆，呈乳白或浑浊外观。|Cloudy sake that retains some rice particles after coarse filtration.
Sake Flight|日本清酒試飲組合|清酒品鉴组|sake sampler|将不同精米、酿造工艺或产地的清酒分成小杯比较。|A tasting set of small sake pours chosen to compare rice polishing, brewing styles or origins.
"""
