"""Skin, makeup, hair, and fragrance expressions for three markets."""

from data.seed_vertical_matrix import editorial_terms, matrix_terms


CATEGORY = "美妆与个护"
SKIN = ("IG", "小红书", "天猫", "Shopify")
MAKEUP = ("IG", "小红书", "抖音")
HAIR = ("IG", "小红书", "天猫")
FRAGRANCE = ("IG", "小红书", "专柜")

ANCHORS = """
Niacinamide|煙酰胺|烟酰胺|Vitamin B3;維他命B3;维生素B3|常见于护肤配方的维生素 B3 衍生物，消费者常用它查找提亮或控油类产品。|「烟酰胺一涂就能漂白。」——配方的实际效果不能由成分名直接推断。|Meet our niacinamide formula for skin that looks a little dull after a long week.|忙碌一星期，肌膚少了光澤？試試加入煙酰胺的日常護理。|皮肤最近有点暗沉？可以从含烟酰胺的日常护肤开始。|香港成分表可见「維他命B3」，内地详情页通常写「烟酰胺」。百分比应与实际配方一致。|A form of vitamin B3 used in skincare, commonly highlighted in moisturising, brightening and oil-control formulas.
Retinol|視黃醇|视黄醇|Vitamin A retinol;維A醇;A醇|视黄醇常用于夜间护肤。首次使用时应参照产品指引，留意干燥或刺激。|「任何肤质每天都可以刷高浓度 A 醇。」——忽略耐受度和用法。|New to retinol? Start with the evening routine on the label and build up only as directed.|第一次用視黃醇？先按包裝指引於晚間使用，留意肌膚反應。|新手入门 A 醇，先按说明安排晚间使用频率，别急着叠加其他活性。|内地社媒常简称「A醇」，港繁详情可写「視黃醇」。不要把视黄醇与视黄醛当成同一种成分。|A form of vitamin A often used in night skincare. Start according to the product directions and watch for dryness or irritation.
Hyaluronic Acid|透明質酸|透明质酸|HA moisturiser ingredient;玻尿酸;保濕透明質酸|一种常见保湿成分，也常被叫作玻尿酸。护肤品中的用法与注射场景不同。|「这瓶玻尿酸涂了就像打了水光针。」——混淆日用化妆品和医美。|Our hyaluronic acid formula leaves skin feeling comfortably hydrated.|透明質酸配方，洗面後為肌膚補充水分。|透明质酸配方，洁面后用来补水，肤感清爽。|香港产品常写「透明質酸」，内地社媒也搜「玻尿酸」。不要把外用保湿描述成注射填充。|A water-binding ingredient used in topical moisturisers and serums. Those cosmetics are distinct from injectable fillers.
Pro-Xylane|玻色因|玻色因|Hydroxypropyl Tetrahydropyrantriol;羥丙基四氫吡喃三醇;羟丙基四氢吡喃三醇|玻色因是消费者熟悉的成分宣传叫法，标示时应核对配方的实际成分名称。|「只要叫玻色因就和原品牌同源同效。」——名称不能证明原料来源或效果。|Look for hydroxypropyl tetrahydropyrantriol in the full ingredient list.|想了解玻色因配方？可於完整成分表查看羥丙基四氫吡喃三醇。|想看玻色因成分，详情页可以对照完整配方表。|两地口语都可能称「玻色因」，品牌资料须核实商标与配方，不宜自行套用他牌专有说法。|A cosmetic ingredient trade name for hydroxypropyl tetrahydropyrantriol. Check the ingredient list when comparing formulas.
Skin Barrier Care|肌膚屏障護理|皮肤屏障护理|barrier support;保護皮膚屏障;屏障修护|以保湿、减少刺激等方式照顾皮肤表层，文案宜描述化妆品使用感和有依据的作用。|「一瓶治疗屏障受损和皮炎。」——把化妆品当作治疗方案。|Keep dry-feeling skin comfortable with a simple barrier-care routine.|用簡單保濕程序照顧肌膚屏障，乾燥日子也可保持舒適。|换季觉得干紧，可以先精简步骤，把保湿和屏障护理做好。|「屏障修护」应符合产品实际功效资料。皮炎、湿疹等医学表述不应混入普通护肤促销。|Cosmetic care that supports the skin's outer protective layer through measures such as moisturising and limiting irritation.
Counter Skin Consultation|專櫃肌膚諮詢|专柜肤况咨询|counter skin assessment;專櫃護膚諮詢;专柜测肤体验|顾客在门店了解肤感和试用产品的服务，可帮助选择保湿和底妆等日用品。|「专柜免费确诊皮肤疾病。」——试用咨询不提供医疗诊断。|Book a counter consultation and feel the difference between our gel and cream textures.|預約專櫃肌膚諮詢，即場試清爽啫喱及滋潤乳霜。|约一次专柜肤况咨询，现场对比凝胶和面霜的肤感。|香港零售多说「專櫃試用」，内地社媒也写「测肤体验」。有收费、预约或名额限制要写清。|An in-store session where customers discuss how their skin feels and try products such as moisturisers or foundation.
Empties Review|空樽用後感|空瓶记|empties roundup;空瓶分享;用完再评|用完产品后总结肤感、使用周期和是否回购的内容。|「只用一次就写成真实空瓶记。」——与宣称的体验周期不符。|Three empties from this month: one I would repurchase, and two I would skip.|今個月空樽用後感：一款會回購，另外兩款未必再入手。|本月空瓶记，三样都用完了，回购清单只留一件。|「空樽」适合港式分享，「空瓶记」在内地笔记更常见。赠品和广告合作需要如实注明。|A review written after finishing a product that describes its use over time and whether the reviewer would buy it again.
Fragrance Layering|疊香配搭|叠香搭配|scent layering;香水疊噴;香水叠喷|将两种香调或同系列的身体护理与香水分层搭配，营造不同气味层次。|「喷得越多，气味越高级。」——忽略浓度与环境。|Try one spray of citrus over a soft musk base and see how the notes settle.|先以淡麝香打底，再輕噴柑橘調，感受疊香後嘅層次。|柔麝香打底，加一喷柑橘调，等香气落下来再闻。|两地都可写「疊香／叠香」。浓度、喷洒距离和留香受配方、天气与个人差异影响。|Wearing two scents together, or pairing scented body care with perfume, to create a layered scent.
Patch Test|局部試用|局部试用|skin patch check;局部皮膚測試;耳后试用|按说明在小范围皮肤先试用产品，观察是否出现不适。日常试用与医用过敏原检测有区别。|「局部试用通过，永远不会过敏。」——小范围试用无法排除后续反应。|Try a small amount on a limited area as directed before using it more widely.|先按使用指引在小範圍肌膚試用，確認沒有不適再用於其他位置。|先按说明做局部试用，有不适及时停用。|香港常说「局部試用」，内地也搜「耳后试用」。具体部位和时间以产品说明为准。|A small-area trial done according to the product directions to check for irritation before wider use. Clinical allergy testing is a separate procedure.
"""

ACTIVES = """
Retinol|視黃醇|视黄醇|Vitamin A Retinol|视黄醇是维生素 A 的一种形式，成分表须与其他维 A 衍生物区分。|「{}再浓也能直接每天用。」——使用频率要考虑耐受和产品说明。|内地可简称「A醇」，港繁常写「視黃醇」。按说明逐步建立耐受。|serum cream oil|{product} formulated with retinol, a form of vitamin A distinct from other retinoids.
Retinal|視黃醛|视黄醛|Retinaldehyde|配方标示中的视黄醛，与视黄醇是不同成分。|「{}和同浓度视黄醇效果完全一样。」——不同成分与配方不能直接比较。|用「醛」字区分视黄醇，浓度对比应说明配方与证据。|serum cream eye|{product} formulated with retinaldehyde, a vitamin A derivative distinct from retinol.
Niacinamide|煙酰胺|烟酰胺|Vitamin B Niacinamide|消费者常凭烟酰胺检索提亮、控油或保湿产品。|「{}一周漂白肤色。」——成分名不能保证特定效果。|英文消费者页可补充 vitamin B3。宣称应以成品证据为准。|serum cream toner|{product} with niacinamide, a form of vitamin B3 commonly used in brightening, oil-control and moisturising formulas.
Hyaluronic Acid|透明質酸|透明质酸|HA Hydrating|透明质酸属于常见保湿成分，用于配方中帮助肌肤保持水分。|「{}的效果等于注射填充。」——混淆外用护肤与医美。|「玻尿酸」是常见检索词，港繁详情页可优先用「透明質酸」。|serum cream mask|{product} with hyaluronic acid, an ingredient that binds water and helps retain moisture.
Ceramide|神經醯胺|神经酰胺|Ceramides|用作保湿配方中的脂质成分，常见于屏障护理产品。|「{}能治好湿疹。」——普通护肤品不应用治疗用语。|香港也可见「神經酰胺」。成分类型或含量写法应以标签为准。|cream cleanser lotion|{product} containing ceramides, lipids often used in moisturising formulas for skin barrier care.
Vitamin C|維他命C|维C|Ascorbic Acid|常见于提亮护理产品，具体成分可能是抗坏血酸或其衍生物。|「{}里所有维C衍生物都是同一种。」——成分形式和稳定性不同。|港繁「維他命C」、内地「维C」。要明确是哪一种成分，谨慎使用原型维C说法。|serum cream mask|{product} formulated with vitamin C for brightening care. The ingredient may be ascorbic acid or a derivative.
Azelaic Acid|壬二酸|壬二酸|Azelaic|名称指壬二酸本身，应与壬二酸衍生物区分。|「{}能治好所有痘痘。」——容易把护肤产品写成药物。|各地区对浓度和宣称的限制可不同。化妆品页面避免照搬药用描述。|serum cream gel|{product} with azelaic acid itself. Check the ingredient list to distinguish it from azelaic acid derivatives.
Salicylic Acid|水楊酸|水杨酸|BHA Salicylic|水杨酸常用于角质护理或油性肤况清洁配方。|「{}每天叠加多种酸也不会刺激。」——应按说明并观察耐受。|英文可补充 BHA，酸类不宜用「越刺越有效」推销。|serum toner cleanser|{product} containing salicylic acid, a beta hydroxy acid commonly used in exfoliating or oily-skin formulas.
Lactic Acid|乳酸|乳酸|AHA Lactic|乳酸可用于角质护理，具体用途随浓度、酸碱度和配方而变。|「{}擦上就能剥掉一层旧皮。」——描述夸张且不恰当。|如写 AHA，记得说明乳酸是哪种果酸。不要只凭酸的种类判断温和程度。|serum toner lotion|{product} formulated with lactic acid. Its role in exfoliation depends on the concentration, pH and overall formula.
Glycolic Acid|甘醇酸|乙醇酸|AHA Glycolic|一种果酸，在香港也称甘醇酸或乙醇酸，常用于焕肤配方。|「{}可以天天代替所有洁面步骤。」——使用频率不能照搬其他产品。|跨区成分资料可并列「甘醇酸／乙醇酸」。说明用法并避免医美暗示。|toner serum cleanser|{product} containing glycolic acid, an alpha hydroxy acid used in exfoliating skincare.
Panthenol|泛醇|泛醇|Provitamin B Panthenol|泛醇亦称维生素原 B5，常用于保湿和舒缓护理。|「{}能代替烧伤药。」——保湿护理不等于处理创伤。|「維他命原B5」适合香港说明，「维生素原B5」适合内地。|cream serum mask|{product} with panthenol, also called provitamin B5, commonly used in moisturising and soothing formulas.
Centella|積雪草|积雪草|Cica Centella|积雪草提取物常见于舒缓类配方，具体所含提取成分须核对标签。|「{}含积雪草，所以过敏一定马上消失。」——夸大作用。|Cica 适合做检索别名。提取物和积雪草苷是不同成分。|cream serum mask|{product} with an ingredient derived from Centella asiatica, a plant often used in soothing formulas. Check the label for the specific extract.
Squalane|角鯊烷|角鲨烷|Squalane Emollient|角鲨烷常作润肤成分，与化学性质不同的角鲨烯要区分。|「{}因为名字里有鲨，所以一定来自鲨鱼。」——来源不能由名称判断。|涉及植物来源须有供应商资料。跨境包装仔细核对 squalane 和 squalene。|oil cream cleanser|{product} with squalane, an emollient distinct from the less stable lipid squalene.
Peptide|胜肽|肽|Peptide Skincare|肽类是多种不同分子的统称，配方用途和依据应具体到产品。|「{}内任意一种肽都能媲美注射。」——夸大并混淆外用与医美。|香港护肤文案常写「胜肽」，内地常用「多肽」或具体肽名。|serum cream eye|{product} with one or more peptides. Their roles and the evidence for any benefits depend on the peptide and formula.
Bakuchiol|補骨脂酚|补骨脂酚|Plant Bakuchiol|来源于植物的护肤成分，有些配方以它作为夜间护理卖点。|「{}是天然 A 醇，任何人都不会刺激。」——并非视黄醇且不能保证耐受。|品牌可写成分来源，别把「植物A醇」当正式成分名。|serum oil cream|{product} with bakuchiol, a plant-derived ingredient often highlighted in evening skincare.
Oat|燕麥|燕麦|Avena Sativa Oat|燕麦来源成分常用于干燥或敏感肤感的护理配方。|「{}含天然燕麦，所有敏感皮都能用。」——植物成分也可能不适合部分人。|胶体燕麦、燕麦油和提取物的成分标示不同，请核对配方。|cream cleanser lotion|{product} with oat-derived ingredients, which are often used in formulas for dry-feeling or sensitive skin.
"""
ACTIVE_FORMS = """
serum|{} Serum|{}精華|{}精华液|洁面后的精华护理|Smooth the {} over freshly cleansed skin, then follow with moisturiser.|潔面後薄搽{}，再搽保濕霜。|洁面后薄涂{}，再用面霜收尾。|精华页写明步骤和建议用量。|a facial serum
cream|{} Moisturiser|{}保濕霜|{}保湿面霜|护肤末段的保湿护理|Finish your routine with the {}, applying a little more where skin feels dry.|護膚最後一步搽{}，乾燥位置可按需要加少少。|最后一步用{}保湿，偏干的位置可以多涂一点。|说明适用部位与建议使用频率。|a moisturiser
oil|{} Face Oil|{}面部精華油|{}护肤油|面部油类润肤护理|Warm a few drops of the {} between your hands and press gently onto the face.|在掌心暖開幾滴{}，輕按面部肌膚。|把几滴{}在掌心搓开，轻按上脸。|别把油类润肤直接写成补充水分。|a face oil
eye|{} Eye Cream|{}眼霜|{}眼霜|眼周护理|Tap a small amount of the {} around the eye contour as directed.|按說明取少量{}，沿眼周輕印。|按说明取少量{}，轻点在眼周。|清楚区分眼周使用与直接接触眼睛。|an eye cream
toner|{} Toner|{}爽膚水|{}化妆水|洁面后的水状护理|After cleansing, pat a light layer of the {} onto your skin.|洗面後輕拍一層{}，再按需要搽精華。|洗脸后轻拍一层{}，再接着用精华。|按配方区别一般化妆水与角质护理产品。|a facial toner
mask|{} Sheet Mask|{}面膜|{}贴片面膜|短时间敷贴护理|Unfold the {}, smooth it onto clean skin and remove it at the time stated on the pack.|潔面後敷上{}，到包裝建議時間就可以取下。|洁面后贴上{}，到包装标注的时间取下。|时长以包装为准，别暗示敷越久越好。|a sheet mask
cleanser|{} Cleanser|{}潔面乳|{}洁面乳|冲洗型清洁|Massage the {} over damp skin and rinse thoroughly with lukewarm water.|濕面後輕輕打圈使用{}，再用微暖清水沖淨。|打湿脸部后用{}轻揉，再用温水洗净。|冲洗型产品的接触时间不同于留敷型。|a rinse-off cleanser
lotion|{} Body Lotion|{}潤膚乳|{}身体乳|身体肌肤的日常保湿|Apply the {} after a shower, paying particular attention to elbows and knees.|沖涼後搽{}，手踭和膝頭位置也別忘記。|洗澡后涂{}，手肘和膝盖这些偏干处也记得照顾。|以实际可用部位与肤感作为卖点。|a body lotion
gel|{} Face Gel|{}面部護理啫喱|{}面部护理凝胶|面部薄涂护理|Apply a thin layer of the {} as directed on the pack.|按包裝指引薄搽一層{}。|按包装说明薄涂一层{}。|不要把凝胶剂型本身写成药用证明。|a face gel
"""

TEXTURES = """
Water-Gel|水感啫喱|水感凝胶|Watery Gel|肤感偏轻薄，通常以清爽的水感为卖点。|「{}就是液态水，没有其他成分。」——肤感描述并非配方说明。|港繁用「啫喱」，内地用「凝胶」。别把水感当含水比例。|moisturiser sleeping sunscreen|{product} with a light, water-like gel texture that spreads easily.
Gel-Cream|凝霜|啫喱面霜|Gel Cream|介于凝胶和面霜之间的质地，常用于兼顾清爽与润泽的产品。|「{}一定适合所有油皮。」——质地不能单独决定适用肤质。|香港可写「凝霜」，内地也可用「凝胶面霜」。|moisturiser sleeping sunscreen|{product} with a texture between a light gel and a richer cream.
Silky|絲滑|丝滑|Silk Finish|形容推开时顺滑，强调触感而非成分中含蚕丝。|「{}等于真丝敷脸。」——感官比喻不能作成分承诺。|英文 silky 表示手感，实际含丝蛋白时另行说明。|moisturiser lotion sunscreen|{product} that glides smoothly on application. The term describes feel and does not establish silk content.
Lightweight|輕盈|轻薄|Light Texture|形容涂开后负担感较轻，不代表保湿程度高低。|「{}轻得像没涂，所以不必用够量。」——某些产品用量会影响实际效果。|香港常用「輕盈」，内地底妆和防晒多说「轻薄」。|moisturiser lotion sunscreen|{product} that feels light on the skin. The term describes texture rather than how much moisture the formula provides.
Whipped|慕絲感|绵密慕斯|Air-Whipped|强调质地蓬松或柔软，形容涂抹感受。|「{}一定是含打发奶油。」——形容质地不等于含食品成分。|香港「慕絲」与内地「慕斯」均适合质地文案。|moisturiser lotion cleanser|{product} with a soft, airy texture, often compared with a mousse.
Rich|豐潤|丰润|Rich Texture|强调涂抹后的润泽感，适合在干燥季护理中介绍。|「{}越厚重越能深入治疗干燥。」——夸大实际功效。|不要用「油腻」直译 rich，写丰润或滋润。|moisturiser sleeping lotion|{product} with a full, emollient feel, often marketed for dry weather or dry-feeling skin.
Fast-Absorbing|易吸收|吸收快|Quick-Absorbing|用来形容涂后较快收干的肤感，不等于进入皮肤深层。|「{}三秒直达真皮。」——收干速度不能证明进入皮肤的深度。|无吸收速度测试时可写「易推开、肤感不黏」。|moisturiser lotion hand|{product} that settles or dries quickly after application. The term describes surface feel.
Non-Greasy|不油膩|不油腻|Grease-Free Feel|形容涂后残留的油腻感较弱，配方仍可能含油。|「{}绝对无油。」——肤感与配方成分是两件事。|如要写无油，要另外核对配方。|moisturiser lotion hand|{product} that leaves little oily residue. It may still contain oils.
Cooling|清涼感|清凉感|Cool Touch|强调涂抹时短暂的清凉肤感，不是降温治疗。|「{}能让皮肤体温持续降下来。」——短暂肤感不支持体温承诺。|若含薄荷或挥发性成分，提醒读者按说明避开眼周。|moisturiser sleeping lotion|{product} that gives a brief cool sensation on application.
Melting|一抹化開|一抹融化|Melt-In|形容配方触肤后容易推开，在文案里常强调触感。|「{}会在皮肤下面融掉脂肪。」——把质地变化误写成身体改变。|港繁「一抹化開」较自然，内地可写「抹开就化」。|moisturiser sleeping cleanser|{product} that softens and spreads easily as it comes into contact with skin.
Bouncy|彈潤|弹润|Bouncy Texture|形容质地弹润，挖取和推开时都有一定弹性。|「{}一抹就让皮肤永久恢复弹性。」——质地形容不能当长期功效。|除非有成品功效依据，把弹润限定在触感而非肤龄。|moisturiser sleeping lotion|{product} with a springy gel texture when scooped or spread.
Cushiony|柔潤厚實|柔软绵润|Cushion Feel|形容涂抹时质地有柔软的厚度，常用于滋润型配方。|「{}有气垫作用，能保护脸部免受撞击。」——cushiony 指肤感。|可用「柔潤」或「绵润」描述，别直译成垫子。|moisturiser sleeping hand|{product} with a soft, substantial texture that feels padded as it spreads.
"""
TEXTURE_FORMS = """
moisturiser|{} Face Cream|{}面霜|{}面霜|选购面霜时比较涂抹感|Try the {} on the back of your hand to get a feel for how it spreads.|先在手背試搽{}，感受質地推開時有幾順滑。|先在手背试抹{}，看看推开的质感合不合心意。|面霜质地可以上手演示，别只列参数。|a face cream
sleeping|{} Sleeping Mask|{}晚安面膜|{}睡眠面膜|挑选夜间免洗敷护|Make the {} the last step of your evening routine, following the pack instructions.|晚間護膚最後一步薄搽{}，用法以包裝指引為準。|晚间护肤收尾用{}，薄涂即可，用法看包装。|是否可过夜按产品指引说明。|an overnight mask
sunscreen|{} Sunscreen|{}防曬|{}防晒霜|比较防晒配方的日常肤感|See how the {} wears under your usual makeup; apply it generously as directed.|試試{}配平日底妝嘅效果，用量記得跟說明。|想看{}会不会和底妆打架？先按说明用够量，再试叠涂。|质地不影响按标签用足量的原则。|a sunscreen
lotion|{} Body Moisturiser|{}身體乳|{}身体乳|比较大面积涂抹的润肤感受|Apply the {} to arms and legs after bathing and see how it feels under clothes.|沖涼後搽{}喺手腳，感受著衫後嘅膚感。|洗完澡用{}涂手臂和腿，试试穿衣后的肤感。|身体乳试用可描述穿衣是否黏腻。|a body moisturiser
cleanser|{} Facial Cleanser|{}洗面乳|{}洗面奶|展示冲洗型清洁产品的质地变化|Add a little water to the {} and feel the texture change as you massage.|取少量{}加水，輕輕按摩，感受質地變化。|给{}加少量水，揉开看看质地怎么变。|起泡情况应以实际剂型为准。|a facial cleanser
hand|{} Hand Cream|{}潤手霜|{}护手霜|比较护手产品搽后触感|Keep the {} by the sink for dry-feeling hands after washing.|將{}放喺洗手盆旁邊，洗手後順手搽。|把{}放洗手台旁，洗完手干了就涂一点。|港繁「潤手霜」、内地「护手霜」。|a hand cream
"""

SUN = """
Broad-Spectrum|廣譜|广谱|UVA UVB Protection|表示防晒范围覆盖 UVA 和 UVB，标签标准随市场而异。|「{}能隔绝所有紫外线。」——广谱不代表全阻隔。|如写广谱防护，须以当地标签规则及测试为准。|lotion stick|{product} labelled for protection against both UVA and UVB. Labelling standards vary by market.
Mineral|物理|物理|Inorganic UV Filter|以无机紫外线过滤成分为配方卖点，常见如氧化锌。|「{}只有反射作用，完全不吸收紫外线。」——机理被过度简化。|「矿物」及「物理」都是常见说法。说明实际防晒成分。|lotion stick|{product} formulated with mineral UV filters such as zinc oxide.
Water-Resistant|防水型|耐水型|Water Resistance|在特定测试时长和条件下保持一定防护，仍须补涂。|「{}遇水不脱，游一整天都不用补。」——绝对防水说法失实。|可按标签写测试时长，不承诺全天防水。|lotion stick|{product} tested to retain specified protection during water exposure for a stated time. Reapply according to the label.
Tinted|潤色|润色|Tone-Tinted|含色料，可呈现轻微调色效果。防晒功能仍看标签标示。|「{}涂一点就同时足够防晒和遮瑕。」——底妆用量与防晒用量可能不同。|展示不同肤色的上脸效果，同时说明用量。|lotion stick|{product} with pigments that add a wash of colour. Check its UV protection on the label.
Fragrance-Free|不含香料|无添加香精|No Added Perfume|配方未加入香料的描述需要按成分核实，仍可能有原料气味。|「{}闻不到任何气味，绝对不过敏。」——无香料不等于无气味或零风险。|香港常写「不含香料」，内地常写「无添加香精」。|lotion stick|{product} formulated without added fragrance. The raw ingredients may still have a scent.
Sheer|透薄|轻透|Sheer-Finish|强调在肌肤上铺开的透明或透薄肤感。|「{}任何肤色都绝不泛白。」——无泛白需要相应试用依据。|用自然光展示肤感，深浅肤色最好分开示范。|lotion stick|{product} designed to leave a light, largely transparent finish when spread over skin.
Matte-Finish|霧面|哑光|Matte UV Finish|强调防晒涂后呈低反光肤感，不是对出油量的保证。|「{}可以永久停止出油。」——妆效不能等同皮脂控制。|香港常用「霧面」，内地常用「哑光」。|lotion stick|{product} designed to leave a low-shine finish on the skin after application.
Dewy-Finish|水光|水光感|Glowy UV Finish|强调完成涂抹后较有光泽的外观，区别于透亮功效。|「{}能把肌肤永久变成水光肌。」——肤感是暂时呈现。|可用窗边自然光演示，不宜用滤镜当成效果证明。|lotion stick|{product} designed to leave a visible, light-reflecting sheen after application.
"""
SUN_FORMS = """
lotion|{} Sunscreen Lotion|{}防曬乳|{}防晒乳|选择适合日常涂抹的防晒乳剂|Apply the {} evenly before heading out and reapply as directed.|外出前均勻搽上{}，並按說明補搽。|出门前均匀涂抹{}，补涂时间以说明为准。|防护系数和用量信息以标签为准。|a sunscreen lotion
stick|{} Sunscreen Stick|{}防曬棒|{}防晒棒|选择方便携带的固体防晒|Take the {} with you, and follow the label's directions for even coverage.|出門帶埋{}，按指引來回搽勻。|把{}放进随身包，按说明来回涂匀。|防晒棒也需要足量覆盖，便携不是一次划过就够。|a sunscreen stick
"""

FINISHES = """
Soft-Matte|柔霧|柔雾|Soft Matte Finish|妆面反光较少，保留柔和的质感。|「{}会永久磨皮。」——妆效无法改变皮肤纹理。|香港常说「柔霧」，内地常说「柔雾」。|lip tint blush foundation powder|{product} that leaves a softly diffused finish with little shine.
Satin|緞光|缎光|Satin Finish|带有较细腻的光泽，介于明显亮面和全哑光之间。|「{}因为像缎子，所以成分一定含真丝。」——妆效不等于成分。|缎光的直观区别是柔和反光，可用斜侧光拍摄。|lip tint blush foundation|{product} with a subtle sheen between matte and high-gloss finishes.
Velvet|絲絨霧感|丝绒哑光|Velvety Finish|低反光但强调柔滑或绒感的妆面。|「{}能把唇纹永久抹平。」——暂时遮饰不可写成永久变化。|港繁常写「絲絨霧感」，内地「丝绒哑光」更常见。|lip tint blush powder|{product} with a low-shine finish that looks soft and smooth like velvet.
Sheer-Finish|透薄妝感|轻透妆效|Sheer Coverage Finish|显色较淡，保留底色可见，适合少量叠涂。|「{}涂一层就盖住所有瑕疵。」——轻透妆效不等于完全遮盖。|展示一层与叠层效果，避免滤镜影响颜色判断。|lip tint blush foundation|{product} that adds light coverage or colour while letting the underlying tone show through.
Dewy|水潤光澤|水润光泽|Dew Finish|妆面有类似湿润肌肤的柔亮反光。|「{}用一次就能把皮肤变成水润肌。」——妆面与肤质不同。|港繁常写「水潤妝感」，内地也说「水光感」。|lip tint blush foundation|{product} that leaves a soft, light-reflecting finish like freshly moisturised skin.
Blurred|柔焦|柔焦|Soft-Focus|妆效强调柔化纹理视觉，具体效果受光线及涂法影响。|「{}直接消除毛孔。」——视觉柔化不等于毛孔消失。|可写「柔焦妆效」，不要将影像滤镜当实拍表现。|lip tint foundation powder|{product} with a soft-focus finish that makes surface texture look less pronounced under some lighting.
Buildable|可逐層加深|可叠涂加深|Buildable Coverage|用量可从少量开始分层，色彩或遮盖度随叠涂增强。|「{}厚涂无上限，永远不卡纹。」——实际表现受用量影响。|用一层与两层实拍说明叠涂差别。|lip tint blush foundation|{product} that can be layered to increase its colour intensity or coverage.
Luminous|亮澤|透亮光泽|Glow Finish|呈现可见亮泽，通常用来描述妆面在光线下的效果。|「{}所有肤色涂上都会白一个色号。」——亮泽不是改变肤色。|「亮澤」描述妆效，肤色变化另说明。|lip blush foundation powder|{product} designed to catch the light and leave a visibly radiant finish.
Natural-Finish|自然妝感|自然妆效|Skin-Like Finish|妆面尽量贴近自然的颜色与纹理，不追求厚重遮盖。|「{}肯定肉眼看不出化了妆。」——自然程度视色号和用量而异。|试色可用同一个光源展示上妆前后，减少视觉误导。|blush foundation powder|{product} intended to give subtle coverage or colour and a finish close to the natural surface.
"""
FINISH_FORMS = """
lip|{} Lipstick|{}唇膏|{}口红|比较棒状唇妆的上色和反光|Swipe on the {} and check the finish in daylight before adding another layer.|薄搽一層{}，喺日光下睇妝效，再決定加唔加深。|薄涂一层{}，在自然光下看妆效，再按需叠涂。|港繁常用「唇膏」，内地彩妆页常用「口红」。|a lipstick
tint|{} Lip Tint|{}染唇液|{}唇釉|比较液体唇彩的显色和妆面|Dot the {} onto the centre of the lips and blend out with a fingertip.|將{}輕點唇中央，用指腹向外暈開。|把{}点在唇中，用指腹往外晕开。|染唇液与唇釉的具体留色方式要按实际配方描述。|a lip tint
blush|{} Blush|{}胭脂|{}腮红|按腮部妆效选颜色与质地|Blend a little {} upwards along the cheekbones and build the colour gradually.|取少量{}沿顴骨向上暈開，顏色可以慢慢加深。|少量{}沿颧骨向上晕开，颜色一点点叠。|「胭脂／腮紅」均见于香港，内地电商常用「腮红」。|a blush
foundation|{} Foundation|{}粉底|{}粉底液|按底妆呈现效果选粉底|Use the {} where you want even coverage, and blend softly towards the hairline.|想均勻膚色嘅位置搽少量{}，向髮際慢慢推開。|在想均匀肤色的位置用{}，往发际线晕开。|粉底剂型和色号在商品详情中另列。|a foundation
powder|{} Setting Powder|{}定妝粉|{}定妆散粉|按定妆后妆面选择粉类|Dust the {} lightly over the centre of the face with a fluffy brush.|用鬆身化妝掃喺面部中央輕掃{}。|用蓬松粉刷在面部中央薄扫一层{}。|实际是压盘还是散粉，按产品包装标注。|a setting powder
"""

EYE_FORMULAS = """
Waterproof|防水|防水|Water-Resistant Eye Makeup|强调眼妆遇水时的持妆表现，须有相应测试。|「{}怎么卸都不会掉。」——防水和无法卸除不同。|写清抗水条件与适配卸妆方式。|mascara liner brow|{product} tested to resist water exposure under stated conditions.
Smudge-Resistant|不易暈染|不易晕染|Smudgeproof|强调眼妆不易因摩擦或出油晕开，效果因使用条件而异。|「{}一整天怎么揉眼都不掉。」——夸大适用条件。|有测试时写明时长、汗水或出油条件。|mascara liner brow|{product} designed to resist smearing caused by rubbing or skin oil.
Long-Wear|持久|持妆型|Long-Lasting|强调佩戴时的持续性，应以实际测试和试用为依据。|「{}永久定色。」——长效妆容与永久纹色不同。|别把「持久」写成无条件全天无瑕。|mascara liner brow|{product} designed to keep its colour or hold for extended wear. Claimed wear time should reflect testing.
Quick-Dry|快乾|快干|Fast-Setting|强调涂开后的成膜或干燥速度。|「{}开盖半秒就干。」——误把上妆干燥速度写成配方结块。|用实拍比较上妆后定妆，说明需要等多久。|mascara liner brow|{product} designed to dry or form a film shortly after application.
Washable|易洗卸|易卸型|Easy-Rinse Makeup|强调依产品指引可用相对简单的方式卸除。|「{}不用卸妆，睡一晚自己掉。」——易卸不等于免卸。|写清温水、洁面或卸妆用品的实际要求。|mascara liner brow|{product} designed for easy removal when washed off as directed.
Low-Transfer|不易轉印|不易沾染|Transfer-Resistant|强调定妆后较少蹭到相邻部位或物品。|「{}未乾也绝对不会沾。」——往往需等待定妆。|视频演示先等妆面干透，并交代摩擦条件。|mascara liner brow|{product} designed to rub off less onto adjacent skin or objects after it has set.
Flexible-Hold|柔韌定型|柔韧定型|Flexible Film|强调成膜后定形但没有僵硬的感受。|「{}像胶水一样把眼皮固定。」——将妆感误写成黏合。|适合演示定妆后的触感和上妆顺序。|mascara liner brow|{product} that forms a flexible film to hold shape without feeling stiff.
Humidity-Resistant|耐潮濕|耐湿型|Humidity-Proof Makeup|强调较潮湿环境下的持妆表现，不能与防水或全天持妆等同。|「{}游水都不用补妆。」——耐潮湿不等于游泳测试。|区分潮湿天气、汗液和入水三种情境。|mascara liner brow|{product} designed to hold up in humid conditions. Its resistance to liquid water is a separate claim.
"""
EYE_FORMS = """
mascara|{} Mascara|{}睫毛液|{}睫毛膏|按妆面需求选择睫毛用品|Sweep the {} from root to tip and let each coat set before adding more.|由睫毛根部向上掃{}，等第一層乾透再疊搽。|从睫毛根部刷到尾端，等{}干了再加一层。|香港常用「睫毛液」，内地常用「睫毛膏」。|a mascara
liner|{} Liquid Eyeliner|{}眼線液|{}眼线液|挑选液体眼线和持妆表现|Trace along the lash line with the {} and allow the line to set.|沿睫毛根部畫上{}，稍等乾透。|用{}沿睫毛根部画线，稍等片刻定妆。|强调线条效果时留意实际刷头形状。|a liquid eyeliner
brow|{} Brow Gel|{}眉毛定型啫喱|{}眉毛定型凝胶|整理眉毛走向并比较定型后的妆感|Brush the {} through your brows in the direction you want them to sit.|用{}順住眉毛方向向上梳理。|用{}顺着眉毛生长方向轻刷，整理毛流。|拍前后对比时保持同一角度和光线。|a brow gel
"""

SHADES = """
Rosewood|玫瑰木色|玫瑰木色|Rose Wood|带灰棕感的玫瑰色，在不同底色上深浅有别。|「{}所有人上脸都一模一样。」——唇色和肤色会影响呈现。|色号页可给自然光实拍，不要把木色写成原料。|lip tint blush|{product} in a rose shade with muted grey-brown undertones.
Dusty Rose|灰粉玫瑰色|灰粉玫瑰色|Muted Rose|饱和度较低的玫瑰粉，常用于偏柔和的日常妆。|「{}本色是灰尘。」——dusty 指降饱和色调。|香港可写「柔霧玫瑰粉」，内地也搜「灰调玫瑰」。|lip tint blush|{product} in a muted, low-saturation rose pink.
Muted Mauve|灰紫粉|灰调紫粉|Dusty Mauve|紫色里带灰与粉调，颜色变化与底色有关。|「{}属于所有冷白皮的唯一色号。」——肤色偏好不宜一概而论。|给深浅肤色试色，不用适合某类肤色当承诺。|lip tint blush|{product} in a muted pink-purple shade with grey undertones.
Terracotta|陶土色|赤陶色|Burnt Clay Shade|带暖红和棕调的陶土色，饱和度依色号而异。|「{}就是砖块原料。」——色名不等于配方来源。|内地也常说「砖红棕」，可补照片而非只靠形容。|lip tint blush|{product} in a warm reddish-brown shade reminiscent of fired clay.
Peach Nude|蜜桃裸色|蜜桃裸色|Nude Peach Shade|带蜜桃暖调的低饱和裸色，适合展示薄涂妆感。|「{}是所有人的原生肤色。」——裸色并非统一色值。|用「蜜桃裸色」说明倾向，注明底色会影响试色。|lip tint blush|{product} in a subdued nude shade with warm peach undertones.
Coral Pink|珊瑚粉|珊瑚粉|Pink Coral Shade|带橙调的粉色，比中性粉更暖。|「{}含珊瑚，所以颜色天然。」——命名不能推断配方。|试色照标注光源，避免将珊瑚色与珊瑚成分混淆。|lip tint blush|{product} in a warm pink with noticeable orange undertones.
Berry Plum|莓果梅子色|莓果梅子色|Plum Berry Shade|深莓紫红色，薄涂和厚涂的饱和度差异较明显。|「{}是一种带果汁的妆品。」——颜色名不表示食品级。|可用「莓果調／莓果调」说明色相，别暗示可食用。|lip tint blush|{product} in a deep berry shade with red-purple tones that intensify when layered.
Fig Rose|無花果玫瑰色|无花果玫瑰色|Fig Pink Rose|偏灰粉棕的玫瑰色，以无花果色调作联想。|「{}的颜色来自无花果。」——配方来源需要核实。|色名适合社媒导购，色卡应补实际色号。|lip tint blush|{product} in a fig-inspired rose shade with muted pink-brown tones.
Caramel Nude|焦糖裸色|焦糖裸色|Nude Caramel Shade|带暖棕调的裸色，常用于通勤或大地色系搭配。|「{}等同于所有人的裸色。」——不同肤色的裸色不相同。|提供深肤色和浅肤色试色，避免靠白底手臂代表所有人。|lip tint blush|{product} in a warm brown nude shade that pairs with earthy colours.
Cool Pink|冷調粉紅|冷调粉色|Cool-Toned Pink|以蓝调为主的粉色，与暖珊瑚色有所区别。|「{}擦完能让肤色变成冷白皮。」——这是暂时的颜色搭配。|写清「冷調」是色相，不用滤镜当美白效果。|lip tint blush|{product} in a pink shade with cool blue undertones.
"""
SHADE_FORMS = """
lip|{} Lip Colour|{}唇膏|{}唇膏|按唇部颜色表现选择色号|Wear the {} alone or tap a lighter shade onto the centre of the lips.|單搽{}已經有層次，亦可以喺唇中央印少少淺色。|{}可以单涂，也可以在唇中叠一点浅色。|英文 lip colour 可泛指唇彩，实际剂型另写。|a lip colour
tint|{} Lip Stain|{}持色唇彩|{}染色唇釉|了解唇彩留色和薄涂表现|For a soft wash, apply the {} to the centre of the lips and blend before it sets.|想妝感自然，將{}點喺唇中，趁未乾向外暈開。|想要清透感，把{}点在唇中，成膜前晕开。|若写留色时长，需区分初涂与卸妆后残色。|a lip stain
blush|{} Cheek Colour|{}胭脂|{}腮红|根据肤色和底妆挑选颊彩|Tap a little {} onto the cheeks and build colour in daylight.|喺面頰輕印少少{}，用日光睇色再慢慢加。|在脸颊少量点拍{}，到自然光下看再叠涂。|不要直接拿唇色试色替代面颊效果。|a cheek colour
"""

APPLICATORS = """
Angled|斜角|斜角|Slanted Applicator|斜切形状便于贴合特定部位，使用时可换角度控制宽度。|「{}可以自动描好每个人的轮廓。」——形状仍要配合手法。|说明斜面适用的角度和部位。|brush brow|{product} with a slanted tip that follows contours and gives different stroke widths at different angles.
Tapered|尖頭|锥形尖头|Pointed Applicator|顶端逐渐收窄，可帮助控制点涂的范围。|「{}的尖头可以刺进皮肤。」——彩妆工具只用于表面。|港繁「尖頭」较清楚，内地也用「锥形」。|brush shadow|{product} with a narrowing tip for more control over where colour lands.
Flat|扁平|扁平|Paddle Applicator|扁面有利于把颜色按压在较明确的位置。|「{}能把凹凸皮肤刷平。」——刷头形状不改变肌肤。|描述铺色或点拍位置，避免医学效果。|brush shadow|{product} with a flat contact surface for pressing colour onto a defined area.
Fluffy|鬆身|蓬松|Soft Fluff|刷毛相对松软，可帮助薄扫粉类及晕染。|「{}越软就一定越能遮瑕。」——柔软度与遮盖力不同。|港式常说「鬆身掃」，内地常用「蓬松刷」。|brush shadow|{product} with soft, loosely packed bristles for lightly applying and blending powder.
Dual-Ended|雙頭|双头|Double-Ended Applicator|工具两端有不同形状或功能，适合在一个流程内切换。|「{}两头完全一样，随便用。」——购买时需要知道两端用途。|分别展示两端的形状和使用位置。|brush brow|{product} with a different applicator or tool at each end.
Retractable|可伸縮|伸缩式|Twist-Up Applicator|刷头或笔芯可收回，方便携带并保护尖端。|「{}可以永不磨损。」——可收回不等于没有耗损。|写清是旋转出芯还是抽拉式刷头。|brush brow|{product} with a tip that retracts into its casing for easier carrying and protection.
Fine-Tip|幼尖|细尖头|Precision Tip|较小的接触面适合描画细节，粗细仍受手法影响。|「{}可在皮肤上永久刻线。」——化妆工具只作暂时上色。|港繁用「幼尖」，内地可写「细头」。|brow shadow|{product} with a small tip for drawing details. Line width still depends on technique.
Rounded|圓頭|圆头|Round-Tip Applicator|圆润边缘适合柔化颜色边界或局部扫匀。|「{}圆头能校正眼睛形状。」——工具只影响妆面视觉。|试拍扫头与上色范围的比例，更易说明用途。|brush shadow|{product} with a rounded head for blending edges or sweeping over a small area.
"""
APPLICATOR_FORMS = """
brush|{} Makeup Brush|{}化妝掃|{}化妆刷|选择适合上妆手法的工具|Use the {} to blend colour where you want a softer edge.|用{}喺需要嘅位置掃開顏色，邊緣更柔和。|用{}把颜色边缘轻轻晕开。|港繁「化妝掃」，内地「化妆刷」。|a makeup brush
brow|{} Brow Pencil|{}眉筆|{}眉笔|选择描画眉形的笔头|Use short strokes with the {} to fill sparse areas without blocking out the whole brow.|用{}輕畫幾筆補眉毛疏落位置，保留自然眉形。|用{}顺着毛流补几笔眉毛稀疏处，别整块填满。|商品页注明笔芯粗细和另一端的工具。|a brow pencil
shadow|{} Eyeshadow Brush|{}眼影掃|{}眼影刷|选用上色或晕染眼影的刷具|Pick up a small amount of colour with the {} and blend lightly over the lid.|用{}沾少少眼影，喺眼皮輕輕暈開。|用{}少量取色，在眼皮上轻轻晕开。|刷毛可依用途说明柔软度与接触面。|an eyeshadow brush
"""

SCALP = """
Clarifying|深層清潔|净澈型|Deep-Cleansing|强调清除多余油脂或造型残留的清洁需求。|「{}可把毒素从毛囊排出来。」——把清洁写成排毒。|说清去的是油脂还是造型残留，勿称排毒。|shampoo scrub rinse|{product} for removing excess oil and styling-product buildup from the scalp.
Balancing|油脂平衡|水油平衡|Scalp Balance|强调清洁后油腻或干紧感觉的平衡，具体表现因人而异。|「{}能永久关闭油脂分泌。」——夸大生理改变。|以洗后肤感和适用头皮状态说明，不承诺永久控油。|shampoo serum rinse|{product} intended to address oily or tight scalp feel. Results vary by person and formula.
Soothing|舒緩|舒缓|Calming Scalp|用于头皮护理时强调舒适感，不能替代疾病诊疗。|「{}能治愈各种头皮炎。」——将化妆品宣传成治疗用品。|可写洗后感觉，涉及异常症状应咨询专业人士。|shampoo serum rinse|{product} formulated to help the scalp feel more comfortable.
Hydrating|補濕|补水|Moisturising Scalp|强调给偏干头皮提供保湿护理。|「{}几次就能彻底治好脱屑。」——干燥与其他头皮问题要区分。|香港「補濕」，内地「补水／保湿」，勿与去屑药效混写。|shampoo serum rinse|{product} designed to add moisture to a dry-feeling scalp.
Cooling|清涼|清凉|Refreshing Scalp|形容使用时头皮感觉凉爽，与临床降温效果无关。|「{}可以治疗头皮发热。」——凉感只是感受。|添加薄荷等凉感配方时说明使用部位，避开眼睛。|shampoo scrub serum|{product} that gives the scalp a temporary cooling sensation during use.
Exfoliating|去角質|去角质|Scalp Exfoliant|用于清理头皮表面角质及残留，不宜过度摩擦。|「{}天天大力搓才能深层净化。」——可能刺激头皮。|分别说明物理颗粒和酸类方式，按说明使用。|shampoo scrub rinse|{product} for loosening dead skin and buildup on the scalp surface.
Tea Tree|茶樹|茶树|Melaleuca Scalp|表示配方采用茶树来源成分，气味和使用感依配方而变。|「{}有茶树成分，所以绝对无刺激。」——天然成分也有个体反应。|按标签区分茶树油和茶树提取物，勿宣称治病。|shampoo scrub serum|{product} with a tea tree-derived ingredient. Its scent and feel depend on the formula.
Gentle|溫和|温和|Mild Scalp Care|表示温和感受或配方定位，不等于适合所有人。|「{}任何敏感头皮用都安全。」——风险不能用单个形容词排除。|有试用数据才说明温和测试范围。|shampoo scrub rinse|{product} formulated or marketed for a mild feel on the scalp. Individual tolerance varies.
"""
SCALP_FORMS = """
shampoo|{} Scalp Shampoo|{}頭皮洗頭水|{}头皮洗发水|清洗头皮时照顾不同需求|Massage the {} into a wet scalp and rinse thoroughly.|頭皮濕水後用{}輕輕按摩，再沖洗乾淨。|打湿头皮后用{}轻轻按摩，再冲洗干净。|港繁口语「洗頭水」、内地「洗发水」。|a scalp shampoo
scrub|{} Scalp Scrub|{}頭皮磨砂|{}头皮磨砂膏|冲洗型头皮深层清洁|Work the {} gently over a wet scalp, then rinse as directed.|濕髮時將{}喺頭皮輕輕打圈，按指引沖淨。|在湿润头皮上用{}轻揉，按说明冲净。|说明使用频次，避免抓挠或破损处。|a scalp scrub
serum|{} Scalp Serum|{}頭皮精華|{}头皮精华液|按分区涂抹头皮护理产品|Part the hair and apply the {} to the scalp as directed.|撥開髮線，按用法將{}輕點頭皮。|分开发缝，按说明把{}涂在头皮上。|强调冲洗或免洗以实际说明为准。|a scalp serum
rinse|{} Scalp Rinse|{}頭皮沖洗液|{}头皮冲洗液|以冲洗步骤照顾头皮肤感|Use the {} as a rinse step, following the timing on the label.|按說明於沖洗步驟用{}，停留時間跟包裝指引。|按包装提示在冲洗步骤用{}，停留时间看说明。|明确是否接在洗发前或后使用。|a scalp rinse
"""

NOTES = """
Citrus|柑橘調|柑橘调|Citrus Notes|以柑橘皮或果实联想为主的清新气味。|「{}是可以饮用的柑橘汁。」——香调不等于食品成分。|柑橘调是气味类别，原料和留香另行说明。|edp mist|{product} built around fresh notes that recall citrus peel or fruit.
White Floral|白花調|白花调|White Flower Accord|联想到茉莉、栀子等白色花香的香调。|「{}一定全用白花精油。」——香调可由多种香料调成。|如列出茉莉或晚香玉，注明是香气联想还是实际原料。|edp mist|{product} with notes reminiscent of white flowers such as jasmine or gardenia.
Woody Musk|木質麝香調|木质麝香调|Wood and Musk Accord|木香与麝香搭配，常呈现干燥温暖或贴肤的气味。|「{}必定使用动物麝香。」——气味名称不能证明来源。|可以说「木質麝香調／木质麝香调」，动物或合成来源按实际资料写。|edp mist|{product} combining woods and musk for a warm, dry or skin-like scent.
Tea-Scented|茶香調|茶香调|Tea Accord|以清茶、焙茶或茶叶的联想表现香气。|「{}可当茶水飲用。」——芳香产品不适用于饮用。|写清是清茶、焙茶还是茶汤感，避免空泛称天然。|edp mist|{product} with a scent inspired by fresh tea, roasted tea or tea leaves.
Amber|琥珀調|琥珀调|Ambery Accord|香水行业中常指温暖树脂感的香调，并非一定来自矿物琥珀。|「{}萃取自真正的琥珀矿石。」——香调与配方来源混淆。|香调表可写 amber accord，别等同于龙涎香。|edp mist|{product} with a warm, resin-like perfume accord.
Gourmand|美食調|美食调|Gourmand Notes|以香草、焦糖、甜点等可食气味为联想的香调。|「{}闻起来甜，所以喷嘴里也能吃。」——香氛产品不可食用。|港繁可写「甜點般香氣」，内地通常认得「美食调」。|edp mist|{product} with notes that recall foods such as vanilla, caramel or desserts.
Clean Musk|潔淨麝香調|皂感麝香调|Soapy Musk Accord|呈现干净衣物或淡皂感联想的麝香型气味。|「{}喷一下就相当于清洁消毒。」——干净是嗅觉联想。|英文 clean 描述气味时，勿据此宣称无毒或更安全。|edp mist|{product} with a soft musk scent that recalls fresh laundry or mild soap.
Marine|海洋調|海洋调|Aquatic Marine Accord|以海风、盐感或水汽为灵感，可能是合成调香。|「{}直接浓缩海水而成。」——灵感来源不是成分来源。|香港「海風氣息」、内地「海盐感」都可作为形容。|edp mist|{product} with an aquatic accord inspired by sea air, salt or water.
"""
NOTE_FORMS = """
edp|{} Eau de Parfum|{}淡香精|{}浓香水|按主香调选购淡香精|Try the {} on a blotter, then see how the dry-down feels on your skin.|先用試香紙聞{}，再試上皮膚感受尾調。|先在试香纸闻{}，喜欢的话上皮试试后调。|EDP 浓度不宜承诺固定留香时长。|an eau de parfum
mist|{} Body Mist|{}香氛噴霧|{}身体香氛喷雾|按香气挑选轻盈的身体喷雾|Mist the {} onto skin as directed for a light everyday scent.|按說明輕噴{}於身體肌膚，留下淡淡香氣。|按说明在身上喷一点{}，留一点轻柔香气。|区分皮肤用喷雾与织物或室内喷雾。|a body mist
"""

FORMULATION = """
Oil-Free|無油配方|无油配方|No Added Oils|表示未加入标签所指油类成分，适用范围要核对配方。|「{}一定不会长痘。」——无油配方不等于零致痘风险。|说明油类判定范围，不由不油腻肤感推断无油。|base serum cream|{product} made without oils covered by the label claim. Check the ingredient list for the scope of the claim.
Fragrance-Free|不含香料|不添加香精|Unscented Formula|表达没有添加香料，原料可能仍然带有气味。|「{}绝对无味也不会过敏。」——成分和个体反应须分开说明。|fragrance-free 与 unscented 的配方含义可能不同，检查实际成分。|base serum cream|{product} formulated without added fragrance. Its ingredients can still have a scent.
Silicone-Free|不含矽靈|无硅配方|No Silicones Added|说明未添加宣传所指硅类成分，不代表功效一定更好。|「{}不含硅，所以比其他配方更安全。」——比较安全性需要依据。|港繁可写「不含矽類成分」，内地常写「无硅」。|base serum cream|{product} made without the silicones covered by the label claim.
Vegan|純素配方|纯素配方|No Animal-Derived Ingredients|一般指不采用动物来源成分，具体范围随标准而异。|「{}纯素就等于没有做过动物实验。」——配方来源与测试政策不同。|清楚说明纯素判定依据，不把 vegan 和 cruelty-free 混为一谈。|base serum cream|{product} made without animal-derived ingredients under the stated standard.
"""
FORMULATION_FORMS = """
base|{} Makeup Primer|{}妝前底霜|{}妆前乳|在底妆前按配方偏好挑选妆前用品|Smooth a thin layer of the {} over moisturised skin before foundation.|保濕後薄搽{}，再上粉底。|护肤后薄涂{}，再叠底妆。|如同时宣称隔离或防晒，另核对产品实际标示。|a makeup primer
serum|{} Face Serum|{}面部精華|{}面部精华液|在精华护理中关注配方成分|Check the full ingredient list for our {}, then follow the routine on the label.|想了解{}用料，可睇完整成分表，再按包裝指引用。|先看{}的完整成分表，再按包装建议安排使用步骤。|无添加类说法应能对照成分表。|a face serum
cream|{} Face Moisturiser|{}面部保濕乳|{}面部保湿乳|按成分偏好比较面部保湿配方|Use the {} as your final moisturising step and check the label for any ingredient you avoid.|用{}完成保濕步驟，如有成分需要避開，可先睇標籤。|最后一步用{}保湿，有需要避开的成分先核对包装。|不能把成分偏好写成普遍医疗建议。|a face moisturiser
"""


def build_beauty_terms():
    yield from editorial_terms(CATEGORY, SKIN, ANCHORS)
    for platforms, attributes, forms in (
        (SKIN, ACTIVES, ACTIVE_FORMS),
        (SKIN, TEXTURES, TEXTURE_FORMS),
        (SKIN, SUN, SUN_FORMS),
        (MAKEUP, FINISHES, FINISH_FORMS),
        (MAKEUP, EYE_FORMULAS, EYE_FORMS),
        (MAKEUP, SHADES, SHADE_FORMS),
        (MAKEUP, APPLICATORS, APPLICATOR_FORMS),
        (HAIR, SCALP, SCALP_FORMS),
        (FRAGRANCE, NOTES, NOTE_FORMS),
        (SKIN, FORMULATION, FORMULATION_FORMS),
    ):
        yield from matrix_terms(CATEGORY, platforms, attributes, forms)
