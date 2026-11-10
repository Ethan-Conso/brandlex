"""Acquisition-channel terms for reporting, experimentation and forecasting."""

CHANNELS = """
Branded Search|品牌字搜尋|品牌词搜索|Google Ads,百度营销|shoppers already looking for us|已經在搜尋品牌的顧客|已主动搜索品牌的消费者|品牌字與非品牌字流量分開比較。
Non-Branded Search|通用字搜尋|非品牌词搜索|Google Ads,百度营销|new shoppers searching by product need|按產品需要搜尋的新客|按产品需求搜索的新客|別把品牌拼寫變體算入通用字。
Shopping Ads|購物廣告|商品广告|Google Ads,淘宝|visitors from product listings|從商品廣告入站的訪客|从商品广告进店的访客|比較前先確認商品供應和價格一致。
Display Ads|展示廣告|展示广告|Google Ads,腾讯广告|visitors from display placements|由展示版位入站的訪客|从展示广告位进入的访客|把瀏覽後轉化和點擊後轉化分開。
Video Ads|影片廣告|视频广告|YouTube,抖音|visitors from video placements|由影片版位入站的訪客|从视频广告位进入的访客|播放量別當成有效到站量。
Podcast Ads|Podcast 廣告|播客广告|Spotify,小宇宙|listeners from the host-read spot|聽到主持人口播的聽眾|听到主播口播的听众|口播廣告可配專屬優惠碼核對來源。
Influencer Ads|KOL 合作廣告|达人合作广告|IG,小红书|visitors from the sponsored creator post|由合作帖文入站的訪客|从达人合作内容进入的访客|先區分創作者自然流量與付費加推。
Affiliate Traffic|聯盟導流|联盟推广流量|Shopify,淘宝|visitors referred by affiliate partners|由聯盟伙伴帶來的訪客|由联盟伙伴引入的访客|聯盟佣金和退款須用同一個結算口徑。
Paid Social|付費社交推廣|社媒付费投放|IG,抖音|visitors from sponsored social posts|從贊助帖文入站的訪客|从付费内容进入的访客|同一平台自然觸及與付費觸及要分開。
Organic Social|自然社交流量|社媒自然流量|IG,小红书|visitors from unpaid social posts|從非付費帖文入站的訪客|从非付费内容进入的访客|未加追蹤參數的分享容易被歸入直接流量。
Organic Search|自然搜尋|自然搜索|Google,百度|visitors from unpaid search results|由自然搜尋結果入站的訪客|从自然搜索结果进入的访客|跟付費搜尋分開標記。
Email Campaign|電郵推廣|邮件营销|Email,Shopify|visitors from the campaign email|由推廣電郵入站的訪客|从营销邮件进入的访客|安全掃描器也可能觸發電郵連結點擊。
Newsletter|電子通訊|电子简报|Email,Shopify|readers who came from the newsletter|透過電子通訊入站的讀者|通过电子简报进入的读者|定期通訊與一次性推廣郵件應分開統計。
SMS Campaign|短訊推廣|短信营销|SMS,淘宝|visitors from the campaign text|由推廣短訊入站的訪客|从营销短信进入的访客|短連結宜帶獨立的追蹤參數。
Referral Program|推薦計劃|推荐奖励计划|Shopify,微信|friends invited by existing customers|由現有顧客邀請的親友|由老客户推荐的亲友|留意重複登記和自我推薦。
App Push|應用程式推送|应用消息推送|App,App Store|visitors who opened the push notification|經推送通知進入的訪客|通过推送通知进入的访客|送達不等於已開啟，報表應分欄。
QR Campaign|二維碼推廣|二维码营销|线下门店,微信|visitors from the in-store QR code|掃描門市二維碼入站的訪客|扫码进入的门店访客|各場地用不同追蹤碼，才可辨別來源。
Community Referral|社群推薦導流|社群推荐流量|WhatsApp,微信|visitors from member-shared links|由會員分享連結帶來的訪客|从群成员分享链接进入的访客|留意群組轉發造成歸因遺漏。
Marketplace Traffic|網購平台導流|电商平台导流|HKTVmall,天猫|visitors from the marketplace listing|由網購平台商品頁入站的訪客|从电商平台商品页进入的访客|第三方平台與自有站點的購買事件須分開。
"""

METRICS = """
{en} Sessions|{hk}工作階段|{cn}访问会话数|{en} visits|统计{cn}带来的访问会话。同一访客可以产生多次会话。|The number of visits attributed to {topic}, counting separate sessions from the same visitor individually.|把{hk}工作階段直接當作獨立訪客。|Track sessions from {context_en} separately from returning traffic.|將{hk}工作階段和獨立訪客分開看。|先看{cn}带来的会话数，再核对访客去重口径。|香港報表也可寫「造訪次數」，內地常寫「会话数」。
{en} New Users|{hk}新訪客|{cn}新增访客|new users from {en}|在统计时段内首次由{cn}访问的人或设备，取决于去重方式。|People or devices first identified via {topic} during the reporting period, using the chosen deduplication method.|將每次點擊都記作{hk}新訪客。|Review first-time visits from {context_en} before adjusting the acquisition plan.|調整拉新安排前，先核對{hk}帶來的新訪客。|调整拉新计划前，先确认{cn}的新访客有没有重复计算。|說明使用者識別方式，跨裝置有機會重複。
{en} Engaged Sessions|{hk}互動工作階段|{cn}互动会话数|engaged visits from {en}|来自{cn}且达到所用工具互动门槛的会话。|Sessions from {topic} that meet the analytics tool's engagement criteria.|用總會話數代替{hk}互動工作階段。|Check whether {context_en} are staying long enough to explore the page.|用{hk}互動工作階段觀察訪客有沒有繼續瀏覽。|用{cn}互动会话数看进站后有没有进一步浏览。|不同工具的互動門檻不同，匯報時附定義。
{en} Add-to-Cart Rate|{hk}加入購物車比率|{cn}加购率|add-to-cart rate from {en}|来自{cn}的会话中有加入购物车动作的比例。|The share of sessions from {topic} in which a visitor adds an item to the cart.|把加購件數除以訪客數，說是{hk}加入購物車比率。|Compare add-to-cart rates for {context_en} on the same product page.|用同一商品頁比較{hk}加入購物車比率。|在同一商品页比较{cn}加购率，避免商品差异干扰。|事先約定分母用訪客還是會話。
{en} Checkout Starts|{hk}開始結帳次數|{cn}发起结算次数|checkout starts from {en}|来自{cn}的流量触发结算流程的次数。|The number of times visits attributed to {topic} begin the checkout process.|將{hk}開始結帳次數當成付款宗數。|See how many of {context_en} start checking out after adding an item.|對照{hk}加入購物車與開始結帳次數。|对照{cn}加购和发起结算次数，找出掉单的环节。|用事件統計時，重複觸發須先排除。
{en} Purchase Rate|{hk}成交比率|{cn}购买转化率|purchase rate from {en}|衡量{cn}带来的会话中最终下单的比例。|The proportion of sessions from {topic} that end in a completed purchase.|把{hk}的商品詳情點擊當作已成交。|Compare completed purchases from {context_en} against all tracked sessions.|以完成訂單計算{hk}成交比率。|只把订单实际完成的会话计入{cn}购买转化率。|英文報表宜用 purchase 標明具體轉化。
{en} Cost per Order|{hk}每宗訂單成本|{cn}单笔订单成本|order cost from {en}|把{cn}可分摊的获客支出除以归因订单数。|The acquisition cost attributable to {topic} divided by the number of attributed orders.|只用廣告支出核算包含製作費的{hk}每宗訂單成本。|Include partner fees when calculating order costs for {context_en}.|計算{hk}每宗訂單成本時，把可分攤開支一起列出。|核算{cn}单笔订单成本时，先对齐佣金与制作费口径。|寫清是投放開支還是完整推廣開支。
{en} Net Sales|{hk}淨銷售額|{cn}净销售额|net sales from {en}|由{cn}归因的销售额，扣除折扣与退款后汇总。|Sales attributed to {topic} after deducting discounts and refunds.|未扣退款就報出{hk}淨銷售額。|Report sales from {context_en} after discounts and returns.|扣除折扣和退款後，再匯報{hk}淨銷售額。|减去折扣和退款后，再核算{cn}净销售额。|稅項和運費是否計入，需按會計口徑註明。
{en} Revenue per Visit|{hk}每次造訪收入|{cn}单次访问收入|RPV for {en}|把{cn}带来的归因收入除以访问会话数。|Revenue attributed to {topic} divided by the number of attributed visits.|將{hk}每次造訪收入與客單價混用。|Use revenue per visit to compare {context_en} with other acquisition sources.|比較渠道時，把{hk}每次造訪收入與平均每單消費分開。|用{cn}单次访问收入对比流量质量，别拿它替代客单价。|收入用淨額或總額都可，報表須保持一致。
{en} Assisted Conversions|{hk}輔助轉化|{cn}辅助转化|assists from {en}|用户最终完成转化前曾通过{cn}接触品牌，但该渠道并非最后触点。|Conversions where {topic} contributed an earlier touchpoint in the customer journey.|把{hk}輔助轉化直接加到最後接觸的成交數上。|Review journeys where {context_en} later returned through another channel and bought.|看看{hk}在哪些成交路徑擔任前段接觸點。|查看{cn}在哪些转化路径中起到了前期助攻作用。|跨渠道加總會重複計數，別當作新增成交。
{en} Landing Page Engagement|{hk}推廣專頁互動|{cn}落地页互动|page engagement from {en}|跟踪{cn}进入推广页后发生的滚动、按钮点击或内容展开。|Actions such as scrolling, button clicks or content expansion by visitors arriving on a campaign page via {topic}.|用{hk}曝光量代替專頁互動。|Check what {context_en} do after reaching the campaign page.|核對{hk}訪客進入推廣專頁後按了哪個按鈕。|核对{cn}访客在落地页的滚动和点击行为。|香港多寫「推廣專頁」，內地多寫「落地页」。
{en} Attribution Report|{hk}成效歸因報告|{cn}归因报告|attribution breakdown for {en}|按约定归因方式列出{cn}对转化的贡献和时间范围。|A report showing the conversion credit assigned to {topic} under a defined attribution method and time window.|用不同模型的{hk}歸因結果直接比較。|Apply the same attribution window when reporting results for {context_en}.|用一致的成效歸因時段整理{hk}報告。|统一归因窗口后，再出{cn}归因报告。|說明最後點擊或多接觸點，避免同名報表口徑不一。
{en} Incremental Lift|{hk}增量成效|{cn}增量提升|incremental impact of {en}|与可比对照组相比，估计{cn}带来的额外成果。|The additional outcome estimated for {topic} by comparing a group exposed to it with a comparable control group.|把{hk}所有歸因訂單當成增量。|Hold out a comparable audience to estimate the lift from reaching {context_en}.|保留可比較的對照組，估算{hk}增量成效。|设置可比对照组，再估算{cn}带来的增量提升。|說明對照方法、樣本量和觀察時段。
"""

BLOCKS = ((CHANNELS, METRICS),)
