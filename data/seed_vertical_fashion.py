"""Apparel, leather goods, jewellery, and watch expressions."""

from data.seed_vertical_matrix import editorial_terms, matrix_terms


CATEGORY = "时尚与奢品"
APPAREL = ("IG", "小红书", "Shopify")
LUXURY = ("IG", "微信", "专柜")

ANCHORS = """
Capsule Collection|膠囊系列|胶囊系列|capsule wardrobe collection;小型限定系列|以同一主题推出少量易搭配的单品。规模小不一定代表限量。|「这组衣服用胶囊装。」——capsule 指小规模而有主题的搭配。|Four pieces, one palette: explore our spring capsule collection.|同一色調，四件單品，探索春日膠囊系列。|同一组色调，四件单品就能搭出春日胶囊系列。|内地也写「胶囊衣橱」，英文 capsule wardrobe 指个人衣橱组合时别译成品牌系列。
Haute Couture|高級訂製服|高级定制时装|couture fashion;高訂;高定|按客户需求制作的高级时装概念，haute couture 在法国有正式行业身份含义。|「任意量身修改都可以称 haute couture。」——普通修改不等同高级订制。|Explore the hand-finished details from our couture atelier.|近看高級訂製工坊製作嘅手工細節。|走进高定工坊，近距离看手工收边。|没有正式资质时，英文可用 made-to-measure 或 custom-made 描述实际服务。
Ready-to-Wear|高級成衣|成衣系列|prêt-à-porter;RTW fashion;成衣|按固定尺码制作、无需单独量身的系列。是否属于奢华定位要看品牌定位。|「已经穿过的衣服。」——ready-to-wear 并非二手。|The ready-to-wear line is available in our standard size range.|成衣系列備有標準尺碼，可即場試身。|成衣系列按常规尺码发售，欢迎到店试穿。|香港品牌常用「高級成衣」，一般商品页可只写「成衣」。
Made-to-Measure|量身訂製|量体定制|MTM tailoring;量身訂造;量体裁衣|以基础纸样为起点，按客户尺寸调整制成衣服。|「有尺寸调整就一定是全手工 bespoke。」——服务范围不一定相同。|Book a fitting to adjust our house block to your measurements.|預約試身，按你嘅尺寸調整本店基本紙樣。|预约量体，在品牌基础版型上做尺寸调整。|说明可调位置和交付期。别把量体定制和完全从零制版混用。
Bespoke Tailoring|全訂製裁縫|全定制裁缝服务|bespoke suit;人手訂造;独立制版|围绕客户体型与偏好独立制版，常包括多次试穿调整。|「把袖子改短就是全订制。」——局部修改并非独立制版。|Your bespoke jacket starts with an individual pattern and a first fitting.|由獨立打版到首次試身，開始製作專屬訂製外套。|先量体并独立制版，再安排第一次试穿。|香港口语可写「度身訂造」。宣传时写清试身次数与可选工艺。
Bias Cut|斜紋裁剪|斜裁|bias-cut fabric;斜布裁剪;斜丝缕剪裁|斜向布纹裁剪，让织物贴合和垂坠方式不同于直裁。|「斜裁就是裙边剪歪。」——裁剪角度针对织物经纬方向。|Cut on the bias, the satin follows the line of the body as you move.|緞面採斜紋裁剪，走動時自然貼合身形。|缎面用斜裁，走动时能看到布料自然垂坠。|用实拍说明垂坠感。bias 不译成「偏见」。
French Seam|法式包縫|法式来去缝|enclosed seam;法式縫邊;来去缝|将毛边收在接缝内部的缝法，常见于较薄的面料。|「有法式包缝就是法国制造。」——工艺名与产地无关。|Enclosed French seams keep the inside of the blouse neat.|恤衫採法式包縫，內側收口一樣整齊。|衬衫内侧做法式来去缝，毛边收得干净。|最好展示服装反面细节，避免用工艺名称暗示原产地。
Hand-Rolled Hem|人手捲邊|手工卷边|hand-rolled edge;手工捲邊;手卷边|以手工把面料边缘卷细并缝住，常见于丝巾。|「任何卷边都是手工卷边。」——应核实实际工序。|Turn the scarf over to see its fine hand-rolled edges.|翻轉絲巾，細看幼細嘅人手捲邊。|翻到丝巾背面，可以看到细细的手工卷边。|香港可用「人手」强调手作。示范细节时勿把机器工序描述成手工。
Saddle Stitch|雙針馬鞍縫|双针马鞍缝|saddle stitching;手縫馬鞍線;马鞍手缝|用双针交替穿过同一排孔缝合皮件的工艺，常见于皮具。|「有马鞍缝的袋子不会磨损。」——工艺不能保证使用寿命。|Look closely at the saddle stitching along the handle tabs.|近看手柄接駁位嘅雙針馬鞍縫。|手提连接处做双针马鞍缝，细节可以近看。|英文可补充 two-needle hand stitch，区分真实手缝与机器仿效果。
Edge Painting|皮邊油封|皮革边油工艺|leather edge paint;油邊工藝;皮边油|在皮革切边涂抹处理材料以封边并调整外观。|「染了边油就等于整块用同一色皮。」——边缘颜色可以另配。|The edge paint is matched to the leather for a clean profile.|皮邊油封與皮革同色，輪廓更俐落。|边油做同色，侧面收口更利落。|可用近镜展示平整度，别把边油当作皮革种类。
Numbered Edition|獨立編號版本|独立编号限量版|individually numbered piece;限量編號;独立编号|单件标出序号的版本，是否限量应有总数或发行规则可核对。|「印了编号，所以每件都是世界唯一款式。」——编号区别单件，不一定区别款式。|Each piece carries its own number, recorded on the accompanying card.|每件作品均有獨立編號，隨附證卡亦有記錄。|每件作品有独立编号，并记录在随附卡片上。|写清编号、版本数量和范围，不能以编号替代限量依据。
Private Viewing Appointment|私人鑑賞預約|私人鉴赏预约|appointment-only preview;預約鑑賞;专属鉴赏预约|在约定时段由专人介绍作品并安排看货或试戴。|「预订鉴赏即确保买到所有稀有款。」——预约服务与库存不同。|Reserve a private appointment to view the collection at your own pace.|預約私人鑑賞，按你嘅節奏細看系列作品。|预约私人鉴赏，由顾问陪你慢慢看这一季的作品。|注明预约地点、时长及是否收费。别承诺未确认库存。
Automatic Movement|自動上鏈機芯|自动上链机芯|self-winding movement;自動機芯;自动机械机芯|佩戴活动带动摆陀给发条储能的机械机芯。|「自动机芯取电于电池，所以不用上链。」——机械自动上链并非电池供电。|The automatic movement winds through the motion of your wrist.|手腕活動帶動自動上鏈機芯，為發條儲存動力。|日常佩戴时，手腕运动可带动自动机芯上链。|香港常用「自動上鏈」，内地可用「自动机械」。闲置时是否要手动上链按指引。
Power Reserve|動力儲備|动力储存|watch running autonomy;動儲;动储|机械表在上满链后、不继续上链时可运行的时长。|「动力储备等于电池寿命。」——适用的驱动形式不同。|Check the stated power reserve before putting the watch aside for the weekend.|週末除低腕錶前，可先了解其標示動力儲備。|周末不戴表前，可以先看表款标注的动力储存。|「动力储存」不说明误差表现，应分别列出时长与走时标准。
Screw-Down Crown|旋入式錶冠|旋入式表冠|screw-in winding crown;鎖入式錶冠;锁把表冠|可旋紧在表壳接口处的表冠结构，操作后通常需按说明锁回。|「有旋入式表冠就能无限深潜水。」——防水须看整表标示。|After setting the time, screw the crown back down as instructed.|調好時間後，按指引將旋入式錶冠扭緊。|调完时间，按说明把旋入式表冠锁回。|香港用「錶冠」，内地用「表冠」。防水深度按实际规格描述。
Removable Bag Strap|可拆式袋帶|可拆卸包带|detachable handbag strap;可拆肩帶;可拆肩带|可以从手袋扣件拆下的背带，便于改变携带方式。|「可拆包带就一定可调长度。」——两项功能须分别确认。|Unclip the strap to carry the bag by its top handle.|解開可拆式袋帶，就可以用手柄提住手袋。|拆下包带，就能用手柄手提。|在详情页分别列明可拆、可调与是否随袋附带。
Jewellery Hallmark|珠寶成色印記|贵金属纯度印记|precious metal hallmark;成色標記;成色印记|用来标示贵金属成色等信息的印记，具体体系依市场而异。|「有印记就可以不看任何检测资料。」——印记不能代替完整核验。|Ask to see the hallmark and the accompanying metal specification before purchase.|選購前可查看成色印記及隨附金屬規格。|购买前可看贵金属纯度印记，并对照产品标注。|跨区页面用实际印记与成色描述，不将普通品牌标记写成官方认证。
"""

FABRICS = """
Linen|亞麻|亚麻|Flax Linen|亚麻纤维织物常呈自然纹理，是否为纯亚麻要看标签。|「{}绝对不起皱。」——天然亚麻可有自然折痕。|港繁「亞麻」，内地「亚麻」，亚麻混纺须说明比例。|shirt dress skirt trousers
Silk|真絲|真丝|Natural Silk|由丝纤维制成，表面质感取决于织法和整理。|「{}看起来亮，就是纯真丝。」——光泽不是纤维证明。|成分以水洗标为准，注意 satin 不是 silk。|shirt dress skirt trousers
Cotton Poplin|棉府綢|棉府绸|Poplin Cotton|细密的平纹棉织物，常用于需要挺括感的款式。|「{}里的府绸就是丝绸。」——府绸是织物类型。|分别写出棉纤维成分与府绸织法。|shirt dress skirt trousers
Silk Crepe|真絲縐布|真丝绉|Silk Crêpe|以丝和绉纹质感作为面料特点，通常有较柔和的垂坠。|「{}有轻微皱纹就表示损坏。」——绉纹可能是设计质感。|香港「縐」与内地「绉」是对应写法，保养按洗标。|shirt dress skirt trousers
Cupro|銅氨纖維|铜氨纤维|Cuprammonium Rayon|纤维素再生纤维的一种，常用于有柔滑和垂感的款式。|「{}是铜丝织的衣服。」——名称不表示铜质金属面料。|不要把 cupro 直接写成真丝。成分核对供应商标签。|shirt dress skirt trousers
Lyocell|萊賽爾纖維|莱赛尔纤维|Lyocell Cellulose|常用于需要柔滑触感和垂坠感的纤维素面料。|「{}一定是某品牌天丝。」——通用纤维名称和商标不同。|没有品牌原料依据时，写通用名称莱赛尔纤维。|shirt dress skirt trousers
Cotton Twill|斜紋棉|棉斜纹|Twill Cotton|表面常可见斜向纹理，手感和重量因织物而异。|「{}的斜纹表示布织歪了。」——斜纹是正常织法。|用近镜展示纹路，不能单从 twill 判断纤维。|shirt dress skirt trousers
Satin|緞面|缎面|Sateen Finish Fabric|常用于强调较平滑、带光泽的表面；缎面不能单独证明纤维来源。|「{}有缎光就是丝绸。」——缎面也可以由其他纤维制作。|港繁「緞面」、内地「缎面」，单独标注纤维含量。|shirt dress skirt trousers
Chambray|青年布|青年布|Chambray Cotton|多见于带浅深色纱对比的平纹织物，与牛仔斜纹不同。|「{}就是任何浅色牛仔布。」——应按织法和实际成分区分。|可写「類牛仔外觀」补充触感，别把它直接当 denim。|shirt dress skirt trousers
Denim|牛仔布|牛仔面料|Denim Cloth|常见牛仔织物，厚薄、洗水效果和弹性依面料而变。|「{}一律都是厚重不弹。」——纤维和织物结构可以不同。|商品页补充水洗或弹性，别将所有牛仔布归为纯棉。|shirt dress skirt trousers
"""
FABRIC_FORMS = """
shirt|{} Shirt|{}恤衫|{}衬衫|按面料比较日常衬衫的触感和垂坠|Tuck the {} into tailored trousers or leave it loose over a tee.|將{}攝入西褲，或者打開鈕扣當薄外套著。|{}可以塞进西裤，也可以敞开叠穿在短袖外面。|香港常写「恤衫」，内地写「衬衫」。
dress|{} Dress|{}連身裙|{}连衣裙|按材质选择连身款式|Style the {} with flat sandals by day and a small shoulder bag after dark.|日間用平底涼鞋襯{}，晚上換上小手袋即可。|白天用平底凉鞋搭{}，晚上换一只小肩包。|保养和是否有里布应按成衣实际标注。
skirt|{} Skirt|{}半截裙|{}半身裙|根据面料特点选择下装|Pair the {} with a neat knit to let the fabric take the focus.|{}配簡約針織上衣，突出裙身布料質感。|{}配简洁针织上衣，把重点留给裙身质感。|不要由面料名称推断裙长。
trousers|{} Trousers|{}長褲|{}长裤|按面料选长裤搭配与季节|Try the {} with a light shirt, and check the inseam for your preferred length.|以輕薄恤衫襯{}，可睇內側褲長揀啱長度。|用轻薄衬衫搭{}，选长度时对照内侧裤长。|英式 trousers、美式 pants，跨境页以目标市场用词为准。
"""

CUTS = """
Boxy|方闊剪裁|箱型剪裁|Box Cut|衣身偏方且通常较少收腰，视觉重点在直线轮廓。|「{}代表任何人都适合同一个尺码。」——轮廓不等于尺寸。|香港可写「方闊」，内地常用「箱型／方盒版型」。|blazer jacket coat vest
Cropped|短身|短款|Cropped Cut|下摆比标准版型短，适合展示上衣比例。|「{}会自动把腰线升高。」——搭配只能改变视觉。|商品图配实际衣长，别只凭模特图判断。|blazer jacket trench vest
Longline|長身|加长款|Long-Line Cut|下摆较长，常用于强调纵向线条或叠穿效果。|「{}保证显高。」——效果取决于身高和搭配。|给出模特身高与实际衣长，避免强承诺。|blazer jacket coat vest
Belted|束腰帶|系腰带|Tie-Waist|设有可系紧或松开的腰带，视觉轮廓可按穿法变化。|「{}系腰带能永久瘦腰。」——穿搭效果并非身体改变。|注明腰带是否可拆与是否随货附送。|blazer jacket coat trench
Collarless|無領|无领|No-Collar|领口没有传统外翻领片，适合展示颈部与内搭。|「{}完全没有领口。」——无领指没有领片。|可附正面和侧面领口照片。|blazer jacket coat vest
Double-Breasted|雙排鈕|双排扣|Double-Row Button|前门襟有两排纽扣，视觉与扣合结构相对突出。|「{}前面每粒钮扣都必须扣上。」——部分纽扣仅作装饰。|港繁「雙排鈕」，内地「双排扣」，展示实际扣法。|blazer jacket coat trench
Single-Breasted|單排鈕|单排扣|Single-Row Button|衣身前幅以一排纽扣扣合，外观通常较简洁。|「{}只能有一颗钮扣。」——单排不限制颗数。|销售页可区分钮扣排数与钮扣数量。|blazer jacket coat trench
Relaxed-Fit|寬鬆剪裁|宽松版型|Easy Fit|衣身留有活动余量，通常不要求按实际尺寸买大。|「{}尺码越大，版型就越标准。」——松量由设计决定。|提供衣身实量，不把「宽松」写成一个具体尺码。|blazer jacket coat trench
Oversized|加大廓形|宽大廓形|Oversize Silhouette|刻意放大肩线或衣身，和日常版型不同。|「{}就是买大一码。」——加大廓形可能还改变肩线和袖长。|可用肩位和衣长说明 oversize 效果。|blazer jacket coat trench
Cocoon|繭形|茧型|Cocoon Silhouette|轮廓中段较饱满、下摆稍收，外形呈包围感。|「{}里面装有蚕茧。」——术语只描述外轮廓。|用侧面照展示中段和下摆对比。|jacket coat vest trench
"""
CUT_FORMS = """
blazer|{} Blazer|{}西裝外套|{}西装外套|按剪裁选择西装外套|Wear the {} open over a fine knit or button it for a sharper line.|{}可以敞開襯薄針織，也可扣鈕著出俐落線條。|{}敞开叠穿薄针织，扣上则更利落。|区分外套廓形和套装整体尺码。
jacket|{} Jacket|{}外套|{}夹克|按轮廓选择外搭|Layer the {} over a tee and check how the shoulders sit when you move.|用{}襯短袖上衣，活動手臂時留意肩位。|{}叠穿短袖，抬手试试肩部活动量。|试穿照可附手臂活动效果。
coat|{} Coat|{}大褸|{}大衣|按剪裁挑选外层大衣|Try the {} over your usual winter layers to check the fit.|用平日嘅冬季內搭試著{}，睇清楚活動空間。|把平时的冬装内搭穿上，再试{}的余量。|香港常用「大褸」，内地「大衣」。
trench|{} Trench Coat|{}風褸|{}风衣|选择日常风衣廓形|Throw on the {} for the commute; leave it open when you want a softer drape.|通勤加件{}，想輪廓自然啲可以敞開著。|通勤外搭{}，敞开穿更显自然垂感。|trench 是款式名称，防水性按实际材料说明。
vest|{} Tailored Vest|{}西裝背心|{}西装马甲|按剪裁选择无袖西装搭配|Wear the {} over a shirt, or pair it with trousers in the same cloth.|{}可以襯恤衫，亦可以配同布料長褲。|{}可以叠穿衬衫，也可以配同面料长裤。|「馬甲／马甲」在服装页指无袖背心，别与外套混写。
"""

BAG_FEATURES = """
Grained-Leather|粒面皮革|粒面皮革|Pebbled Grain Leather|表面呈可见颗粒纹理，可能来自天然纹理或压制加工。|「{}有纹理就一定未经任何加工。」——纹理来源需核实。|区分粒面效果与全粒面等级。|tote shoulder cross satchel
Suede|麂皮絨|绒面皮革|Suede Leather|表面带细绒的皮革外观，材质来源要查标签。|「{}一定由麂皮制作。」——名称常指绒面质感，动物来源需另查。|人造绒面必须与真皮区分。|tote shoulder cross satchel
Canvas|帆布|帆布|Canvas Cloth|用较结实的织物制成包身，纤维与耐磨程度依产品而异。|「{}必定可以机洗。」——内衬和皮饰也影响洗护。|配合成品清洁指引，不单凭帆布判断是否可洗。|tote shoulder cross satchel
Quilted|絎縫|绗缝|Quilt Stitch|利用线迹固定多层材料，常形成方格或菱格的立体纹理。|「{}每条线都由工匠手缝。」——纹理不能证明工艺。|商品图可展示纹样，手工声明要另有依据。|tote shoulder cross satchel
Woven-Leather|編織皮革|编织皮革|Interwoven Leather|以皮条相互交织形成表面结构和纹理。|「{}看见编织就是手工。」——编织可能由多种工序完成。|说明是编织结构还是压出类似纹理。|tote shoulder cross satchel
Zip-Top|拉鏈開口|拉链开口|Zipped Top|包口以拉链闭合，用来减少内容物外露。|「{}拉链闭合后绝对防盗。」——普通开合结构不保证安全。|展示拉链长度和是否完全覆盖包口。|tote shoulder cross satchel
Flap-Closure|翻蓋|翻盖|Flap Top|包口以翻盖覆盖，可能另有磁扣或插扣固定。|「{}有翻盖就会自动锁紧。」——实际扣件需核实。|注明磁吸、锁扣或单纯翻盖。|tote shoulder cross satchel
Structured|挺身|挺括定型|Structured Shape|包体有相对稳定的轮廓，空置时也较容易保持造型。|「{}永远不变形。」——使用和储存仍影响皮件。|用空袋侧面图展示结构，而非承诺不变形。|tote shoulder cross satchel
Soft-Sided|軟身|软包身|Soft Construction|袋身柔软，有自然下垂或随内容物变化的外观。|「{}就是不耐用的包。」——软硬度不代表耐用性。|香港「軟身」，内地可写「软包身／松弛包型」。|tote shoulder cross satchel
Lightweight|輕身|轻量|Light Carry|强调空包相对轻，实际背负重量还取决于装载量。|「{}装满之后和空袋一样轻。」——重量随内容增加。|可列空包净重和测量范围。|tote shoulder cross satchel
"""
BAG_FORMS = """
tote|{} Tote|{}托特袋|{}托特包|按袋身特点选择大开口手袋|Pack a book and a water bottle in the {}, after checking its inner dimensions.|{}可先睇內部尺寸，再放書同水樽。|先核对{}内部尺寸，再装书和水杯。|香港「托特袋」，内地「托特包」。
shoulder|{} Shoulder Bag|{}肩袋|{}单肩包|比较单肩携带的包身和开合|Try the {} over your usual outerwear to check the strap drop.|試吓將{}孭喺平日外套上，感受帶垂長度。|用平时的外套试背{}，确认肩带垂长。|肩带垂长和肩带总长不是同一尺寸。
cross|{} Crossbody Bag|{}斜孭袋|{}斜挎包|挑选斜挎款的材料和结构|Position the {} at hip level if the strap allows, and see how it sits as you walk.|袋帶可調的話，將{}調至髖位，行幾步感受貼身程度。|肩带可调的话，把{}调到胯部附近，走两步试试贴合感。|「斜孭／斜挎」指佩戴方式，不代表全部有可调肩带。
satchel|{} Satchel|{}手提書包款|{}手提邮差包|选择有手柄的包型及开合结构|Carry the {} by its handle, and check the product page for strap options.|手提{}時可用袋柄，袋帶配置以商品頁為準。|{}可以手提，是否配肩带看商品页。|satchel 可指不同书包轮廓，实物图比硬译更清楚。
"""

SETTINGS = """
Bezel-Set|包鑲|包镶|Bezel Setting|金属边围住宝石腰部的一种镶法，外缘较平整。|「{}绝不会松石。」——任何镶嵌都应保养检查。|可用侧视图说明包边是否围满一圈。|ring stud pendant
Prong-Set|爪鑲|爪镶|Claw Setting|小金属爪固定宝石，通常能看到较多宝石边缘。|「{}每一爪都是额外钻石。」——爪本身是镶座金属。|注明爪数时以实物为准，日常佩戴避免勾挂。|ring stud pendant
Halo|環鑲|光环镶|Halo Setting|小颗宝石围绕主石排列，强调视觉层次。|「{}的外圈都算进主石重量。」——主石重与总宝石重不同。|详情页将主石和配石重量分列。|ring stud pendant
Pavé|密釘鑲|密钉镶|Pave Setting|细小宝石密排在金属表面，形成连续闪亮的效果。|「{}等于整块大钻石。」——小颗宝石密镶不等于整颗石头。|香港可写「密釘鑲嵌」，内地常用「密钉镶」。|ring hoop pendant
Solitaire|單石|单石|Single-Stone Setting|设计以一颗主石为中心，具体镶法可以不同。|「{}必定使用爪镶。」——单石属于款式，不限定固定方式。|可同时标注单石款式与真实镶法。|ring stud pendant
Cluster|群鑲|群镶|Cluster Setting|数颗宝石聚为一个视觉主体，不必有单独主石。|「{}的一簇小石可以写成一颗大石。」——会误导重量与结构。|分别列颗数、大小或总重，不夸大单石规格。|ring stud pendant
Flush-Set|平鑲|埋镶|Flush Setting|宝石嵌入金属表面，外观接近齐平。|「{}宝石浮在金属上。」——齐平是这种镶法的要点。|在近照展示表面高度，别用包镶一词代替。|ring stud pendant
Channel-Set|槽鑲|槽镶|Channel Setting|宝石排列在两侧金属形成的沟槽内。|「{}每颗都用独立四爪固定。」——槽镶结构与爪镶有别。|香港可见「坑鑲」，内地常用「槽镶」。|ring hoop pendant
Shared-Prong|共爪鑲|共爪镶|Shared Claw Setting|相邻宝石共享金属爪，可减少边缘金属的视觉遮挡。|「{}的共爪表示宝石被融为一体。」——只是共用固定结构。|可在侧面特写说明共享部位。|ring hoop pendant
Invisible-Set|隱形鑲嵌|隐密式镶嵌|Invisible Setting|常把宝石紧密排列并遮住正面所见的金属固定结构。|「{}完全不需要任何镶座。」——固定结构只是较不显眼。|应核实是实际隐密镶法，还是普通密排视觉。|ring stud pendant
"""
SETTING_FORMS = """
ring|{} Ring|{}戒指|{}戒指|按宝石排列和镶嵌方式挑选戒指|See the {} from the side to understand how the stones sit above the band.|由側面睇{}，可以睇清寶石同指環嘅高度。|侧面看看{}，就能看清宝石与戒圈的高度。|商品页同时给出指围和日常保养建议。
stud|{} Stud Earrings|{}耳釘|{}耳钉|选择贴耳佩戴的镶石样式|Try the {} to see how the stones sit against the ear.|試戴{}，留意寶石同耳垂嘅貼合程度。|试戴{}，看看宝石贴在耳垂上的效果。|清楚标注单只或一对。
hoop|{} Hoop Earrings|{}圈形耳環|{}圈形耳环|按镶嵌设计选择环形耳饰|Turn the {} in the light to see the placement of the stones.|轉動{}對住光線，就可睇清排石位置。|把{}在光下转一转，能看清宝石排列。|补充内径和开合类型。
pendant|{} Pendant|{}吊墜|{}吊坠|按镶座与宝石排列选择颈饰|Look at the back of the {} as well as the front before choosing a chain.|揀頸鏈前，先睇清{}嘅正面同背面。|选链条前先看看{}的正面和背面。|要明确是否含链与吊环尺寸。
"""

DIAMOND_CUTS = """
Round Brilliant|圓形明亮式|圆形明亮式|Round Brilliant-Cut|圆形轮廓与明亮式刻面排列结合，强调光线反射。|「{}只要是圆的就一定是明亮式。」——轮廓与刻面需一起确认。|可列报告所记切工名称，避免混用圆形与明亮式。|ring stud pendant
Emerald-Cut|祖母綠形切割|祖母绿形切割|Emerald Cut|多见切角长方轮廓和阶梯状刻面。|「{}用的就是祖母绿宝石。」——祖母绿形在这里指切割。|跨境页区分 emerald-cut diamond 和 emerald gemstone。|ring stud pendant
Princess-Cut|公主方形切割|公主方形切割|Princess Cut|常呈方形轮廓与尖角，刻面具明亮式特征。|「{}每颗都是圆角方形。」——公主方形与枕形轮廓不同。|可拍尖角镶座，说明佩戴保养。|ring stud pendant
Oval-Cut|橢圓形切割|椭圆形切割|Oval Cut|轮廓比圆形更修长，具体比例依实际宝石而定。|「{}的长宽比全部一样。」——每颗石头的比例可不同。|写清实际长宽尺寸，不从形状推定克拉重。|ring stud pendant
Pear-Shaped|梨形|梨形|Teardrop Cut|一端圆、一端尖，外形也常被称水滴形。|「{}两端都一样尖。」——那更接近马眼形。|港繁可补「水滴形」，正面图标示佩戴方向。|ring stud pendant
Marquise-Cut|馬眼形切割|马眼形切割|Navette Cut|细长轮廓的两端收成尖点，也称船形。|「{}只有一端尖。」——马眼形两端通常都尖。|可列实测长宽比例并展示尖端保护。|ring stud pendant
Cushion-Cut|枕形切割|枕形切割|Cushion Cut|多为圆角方形或长方轮廓，具体刻面依切工设计而异。|「{}每一颗都同样方正。」——枕形有长方和方形差异。|优先写「枕形」，也可在款式页注明圆角方形。|ring stud pendant
Radiant-Cut|雷迪恩切割|雷迪恩切割|Radiant Cut|常有切角的方形或长方形外轮廓，配以偏明亮的刻面设计。|「{}就是所有长方形钻石。」——形状不能单独确定刻面。|可同时列报告切工类型和实际轮廓。|ring stud pendant
Heart-Shaped|心形|心形|Heart Cut|轮廓包含上端凹口与下端尖点，常用于礼赠款式。|「{}由两个半圆钻拼成。」——心形通常指单石轮廓。|先确定单石切割或组合造型，再写英文。|ring stud pendant
Asscher-Cut|阿斯切切割|阿斯切切割|Asscher Cut|多见方形阶梯刻面和切角外观，与长方祖母绿形可区分。|「{}有任何阶梯纹就能叫阿斯切。」——切工类型应按报告。|不确定是否为特定切工时，用客观形状与报告描述。|ring stud pendant
"""
DIAMOND_FORMS = """
ring|{} Diamond Ring|{}鑽石戒指|{}钻石戒指|按钻石形状和刻面选购戒指|Try the {} alongside other cuts to compare its outline on the hand.|將{}同其他切割款並排試戴，睇清上手輪廓。|把{}和其他切形一起试戴，对比上手的轮廓。|证书规格以单件实物为准。
stud|{} Diamond Studs|{}鑽石耳釘|{}钻石耳钉|比较耳饰中钻石的形状与比例|See how the {} sit from the front and side before choosing a pair.|揀選{}前，先睇試戴正面同側面。|选{}之前，先从正面和侧面看看佩戴效果。|成对商品注明标的是单颗重还是总重。
pendant|{} Diamond Pendant|{}鑽石吊墜|{}钻石吊坠|按钻石切形选择吊坠|Compare the {} against your neckline to see how the shape reads at different chain lengths.|用唔同頸鏈長度試襯{}，睇吓輪廓同領口點樣配合。|试试不同链长的{}，看它和衣领怎么搭。|宣传图可示范链长，配链情况要另列。
"""

WATCH_FEATURES = """
Automatic|自動上鏈|自动机械|Self-Winding|通过佩戴时摆陀运动给机械发条储能。|「{}靠更换电池来上链。」——自动机械机芯与电池供电不同。|内地也说「自动上链」，实际动力储备另列。|dress dive pilot
Hand-Wound|手動上鏈|手动上链|Manual-Wind|通过手动转动表冠为机械机芯发条储能。|「{}需要每天更换电池。」——机械上链不依赖电池。|说明上链方式和厂方推荐的间隔。|dress pilot chrono
Quartz|石英|石英|Quartz Movement|以石英振荡作为计时基准，供能方式应看机芯规格。|「{}一定需要频繁换电池。」——石英也有不同供能形式。|「石英」描述计时方式，电池或太阳能另说明。|dress dive chrono
Solar-Powered|太陽能|光动能|Solar-Charged|通过光线为腕表储能，实际续航与光照和型号有关。|「{}永远不需要光线也能走。」——储能须由光补充。|没有品牌授权时「太阳能／光能」比专有商标稳妥。|dress dive pilot
Titanium|鈦金屬|钛金属|Titanium-Cased|以钛或钛合金作为所指零件的材料卖点。|「{}所有零件都必定是纯钛。」——要核对材质所在部件。|注明表壳、链带或底盖，不把局部材质写成整表。|dress dive chrono
Ceramic|陶瓷|陶瓷|Ceramic-Cased|以陶瓷为表壳、表圈或链带材质之一，应列明部位。|「{}是永不碎的陶瓷。」——耐刮与抗撞击不同。|分开说明陶瓷部位和保养，别称绝对不刮花。|dress dive chrono
Skeleton|鏤空|镂空|Skeletonised|机芯或表盘有开放式结构，可见一部分内部零件。|「{}整枚机芯每颗零件都看得见。」——开放程度依设计而异。|全镂空与局部开芯别混写，配实物图。|dress pilot chrono
Luminous-Dial|夜光錶盤|夜光表盘|Lumed Dial|表盘标记或指针可在暗处辅助读时，持续时间受材料影响。|「{}漆黑环境永久发光。」——发光强度和时长随条件变。|列清楚夜光是指针、刻度还是全盘。|dive pilot chrono
Sapphire-Crystal|藍寶石水晶鏡面|蓝宝石水晶表镜|Sapphire Watch Glass|使用蓝宝石晶体作为表镜卖点，通常并非取自天然宝石。|「{}表镜是整块天然蓝宝石。」——应核实材料来源。|港繁常用「鏡面」，内地常用「表镜」，勿承诺不碎。|dress dive pilot
Enamel-Dial|琺瑯錶盤|珐琅表盘|Enamel Watch Face|以珐琅工艺做表盘外观，具体工序依产品而异。|「{}任何亮面涂料都属于珐琅。」——材料和工艺需核实。|可注明大明火或其他实际工艺，不以光泽推断。|dress pilot chrono
"""
WATCH_FORMS = """
dress|{} Dress Watch|{}正裝腕錶|{}正装腕表|按工艺和驱动形式挑选正装表|Try the {} under a shirt cuff and check the case height.|將{}襯恤衫袖口試戴，留意錶殼厚度。|把{}搭衬衫袖口试戴，看看表壳厚度。|正装定位不能代替尺寸说明。
dive|{} Dive Watch|{}潛水腕錶|{}潜水腕表|按实际防水规格挑选潜水风格腕表|Check the depth rating and the manufacturer's usage guide for the {}.|想配戴{}下水，先確認防水規格同廠方指引。|戴{}下水前，先看防水标注和厂商使用说明。|潜水外观和符合潜水用途不是一回事。
pilot|{} Pilot Watch|{}飛行員腕錶|{}飞行员腕表|比较飞行风格腕表的显示和配置|Compare the dial layout of the {} in daylight before trying it on.|試戴{}前，可先喺日光睇清錶盤佈局。|试戴{}前，到自然光下看看表盘布局。|pilot 可指设计风格，不代表具备航空认证。
chrono|{} Chronograph|{}計時腕錶|{}计时码表|选购带独立计时显示的腕表|Ask for a demonstration of the {} so you can see how the elapsed-time display works.|可請店員示範{}，睇吓經過時間點樣顯示。|请店员演示{}，看看经过时长怎么读。|chronograph 与 chronometer 概念不同。
"""

OUTERWEAR = """
Packable|可摺疊收納|可折叠收纳|Packs Down|可折进袋或随附收纳套，方便携带。|「{}可以折到完全没有体积。」——应提供实测收纳尺寸。|展示收纳后大小及是否附袋。|jacket parka gilet coat
Insulated|保暖夾層|填充保暖|Thermal Fill|带有隔热或保温夹层，保暖程度取决于实际材料和环境。|「{}在任何温度都能保暖。」——不应作无条件温度承诺。|说明填充材质，温度数据须附测试条件。|jacket parka gilet coat
Water-Repellent|跣水|防泼水|Water-Shedding|面料可减少水滴停留，不能等同长时间防水。|「{}下暴雨浸水一整天也不会湿。」——防泼水和防水不同。|港繁口语可用「跣水」，正式可写「防潑水」。|jacket parka gilet coat
Wind-Resistant|防風|防风|Wind-Blocking|结构或织物帮助减少风穿透，不代表任何风况都适用。|「{}什么风速都完全吹不进来。」——防风效果依测试条件。|讲明是面料、里层还是挡风门襟提供保护。|jacket parka gilet coat
Quilted|絎縫|绗缝|Quilt-Stitched|通过线迹把夹层固定，形成格纹或其他外观。|「{}每针一定是纯手工。」——看见线迹不能判定工艺。|可展示表面纹样，核实手缝或机缝再写。|jacket parka gilet coat
Reversible|兩面著|双面穿|Double-Sided Wear|内外两面均设计为可穿的外观。|「{}剪掉洗标就能双面穿。」——需检查接缝、扣件与袋口设计。|两面都应展示开合与口袋。|jacket parka gilet coat
Hooded|連帽|连帽|With Hood|领口带有帽子，是否能拆卸以款式为准。|「{}的帽子一定可拆。」——连帽可能固定。|图文分清固定帽与可拆帽。|jacket parka gilet coat
Fleece-Lined|抓毛內裡|抓绒内里|Fleece Lining|内侧有抓毛层，触感及保暖性依面料而变。|「{}一定是羊毛内里。」——fleece 也常用合成纤维制作。|港繁「抓毛」，内地「抓绒」，按标签写具体纤维。|jacket parka gilet coat
Down-Filled|羽絨填充|羽绒填充|Down Insulation|夹层使用羽绒填充，规格应查羽绒种类与实际填充量。|「{}里有少量羽绒就称百分百羽绒。」——含绒标示须准确。|分别列充绒量和绒子含量，避免和蓬松度混淆。|jacket parka gilet coat
Padded|夾棉|夹棉|Padded Insulation|有柔软填充层，填充材料并不一定是棉。|「{}的填充一定是纯天然棉。」——padded 只表示含填充。|如实际用聚酯或其他填充，商品详情应注明。|jacket parka gilet coat
"""
OUTER_FORMS = """
jacket|{} Outdoor Jacket|{}戶外外套|{}户外夹克|按户外衣料和结构选择短外套|Pack the {} as a light outer layer and check the care label after use.|將{}放入背囊作輕便外層，使用後按洗標護理。|带上{}作户外外层，用完按洗标护理。|说明使用场景，不以户外名称暗示专业防护。
parka|{} Parka|{}派克外套|{}派克大衣|按结构和保暖材料选择派克外套|Try the {} over your usual layers and test the pocket access before heading out.|用日常內搭試著{}，出門前試吓袋位是否順手。|把{}套在日常内搭上试试，再看看口袋好不好用。|派克指款式，填充、防水和帽子配置分开写。
gilet|{} Gilet|{}戶外背心|{}户外马甲|作为无袖叠搭层挑选外衣|Layer the {} over a sweatshirt for a little extra coverage without bulky sleeves.|用{}襯衛衣，加多一層又唔阻住手袖。|卫衣外叠一件{}，多一层又不用加厚袖子。|英式 gilet、美式 vest；写清是否含填充。
coat|{} Winter Coat|{}冬日大褸|{}冬季大衣|按内外层配置选择冬日大衣|Try the {} with a knit underneath and check how the hem sits when seated.|用針織上衣試襯{}，坐低時睇清下擺位置。|用针织衫试搭{}，坐下时看看衣摆位置。|按产品测量附衣长和袖长。
"""


def build_fashion_terms():
    yield from editorial_terms(CATEGORY, LUXURY, ANCHORS)
    for platforms, attributes, forms in (
        (APPAREL, FABRICS, FABRIC_FORMS),
        (APPAREL, CUTS, CUT_FORMS),
        (LUXURY, BAG_FEATURES, BAG_FORMS),
        (LUXURY, SETTINGS, SETTING_FORMS),
        (LUXURY, DIAMOND_CUTS, DIAMOND_FORMS),
        (LUXURY, WATCH_FEATURES, WATCH_FORMS),
        (APPAREL, OUTERWEAR, OUTER_FORMS),
    ):
        yield from matrix_terms(CATEGORY, platforms, attributes, forms)
