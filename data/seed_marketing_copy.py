"""Editorial components that change with message purpose and page placement."""

EMAILS = """
Welcome Email|迎新電郵|欢迎邮件|Email,Shopify|Explore your member benefits|查看會員禮遇|查看会员福利|新會員未買過貨時，不宜稱「感謝再次選購」。
Order Confirmation Email|訂單確認電郵|订单确认邮件|Email,Shopify|View your order details|查看訂單詳情|查看订单详情|確認訂單與確認出貨是兩件事。
Dispatch Email|出貨通知電郵|发货通知邮件|Email,Shopify|Track your parcel|查閱送貨進度|查看物流进度|有運單不一定已由速遞收件。
Delivery Update Email|送貨進度電郵|配送进度邮件|Email,Shopify|See the latest delivery estimate|查看最新預計送達時間|查看最新预计送达时间|預計送達不能寫成保證送達。
Pickup Reminder Email|取貨提示電郵|取货提醒邮件|Email,线下门店|Check your pickup hours|查看取貨時間|查看自提时段|香港寫「門市自取」，內地寫「到店自提」。
Cart Reminder Email|購物車提示電郵|购物车提醒邮件|Email,Shopify|Review the items in your cart|查看購物車內的貨品|查看购物车里的商品|未保留存貨時，不宜說貨品已留起。
Restock Alert Email|補貨通知電郵|到货提醒邮件|Email,Shopify|Check current stock|查看現時存貨|查看当前库存|補貨通知不是購買保證。
Price Drop Alert Email|減價通知電郵|降价提醒邮件|Email,Shopify|See the updated price|查看最新售價|查看最新价格|需核對所追蹤款式與新舊價格。
Trial Start Email|試用開始電郵|试用开通邮件|Email,App|Set up your trial account|設定試用帳戶|设置试用账号|試用期間和扣款時間宜同屏說明。
Trial Ending Email|試用到期提示電郵|试用到期提醒邮件|Email,App|Manage your trial before it ends|在試用期屆滿前管理帳戶|在试用到期前管理账号|有自動續費，應提早交代關閉方法。
Subscription Renewal Email|訂閱續期電郵|订阅续费邮件|Email,App|Review your renewal date|查看續期日期|查看续费日期|用下次收費日期，不只寫「即將續期」。
Appointment Reminder Email|預約提示電郵|预约提醒邮件|Email,线下活动|Confirm or change your appointment|確認或更改預約|确认或更改预约|列明改期方法及限期。
Feedback Request Email|意見邀請電郵|反馈邀请邮件|Email,Shopify|Tell us how your order went|分享今次購物感受|分享本次购物体验|邀請真實評價，勿用贈品交換好評。
Loyalty Statement Email|會員積分結算電郵|会员积分账单邮件|Email,Shopify|Check your points balance|查看會員積分結餘|查看会员积分余额|香港用「結餘」，內地用「余额」。
Win-Back Email|舊客再訪邀請電郵|老客召回邮件|Email,Shopify|See what's new since your last visit|睇吓上次到訪之後有咩新變化|看看上次到访后有哪些新变化|提到過往互動時，避免讓收件人感到被監視。
"""

EMAIL_PARTS = """
{en} Subject Line|{hk}主旨|{cn}主题行|subject for {en}|收件人在邮箱列表看到的{cn}标题，宜直接说清事项。|「重要通知，速看！」沒有指出是哪件事。|Next step: {context_en}|下一步：{context_hk}|下一步：{context_cn}|香港電郵介面多寫「主旨」，內地團隊常寫「主题行」。
{en} Preheader|{hk}預覽文字|{cn}预览摘要|preview text for {en}|邮箱收件列表在{cn}主题行附近显示的补充短句。|預覽文字只重複主旨，沒有新資訊。|You can do this from your account: {context_en}.|登入帳戶即可處理：{context_hk}。|登录账号即可操作：{context_cn}。|用一個新資訊點補足主旨，預覽時檢查截斷位置。
{en} Opening Line|{hk}開首句|{cn}开场句|opening sentence for {en}|在{cn}首段交代写信目的或读者可采取的下一步。|「謹藉此通知閣下查閱如下內容。」冗長卻沒說目的。|Here's what you can do next: {context_en}.|以下係你而家可以做嘅一步：{context_hk}。|接下来你可以直接操作：{context_cn}。|先交代關鍵事項，再寫禮貌問候。
{en} Button Label|{hk}按鈕文字|{cn}按钮文案|button text for {en}|{cn}行动按钮上简短、能预测下一步的文字。|全部按鈕只寫「按這裡」，無法預判會打開甚麼。|{context_en}|{context_hk}|{context_cn}|按鈕用動詞開頭，不應暗示按下已完成交易。
{en} Text Link|{hk}文字連結|{cn}文字链接|inline link for {en}|{cn}正文里可以点开的文字，适合为主要按钮提供替代入口。|用裸網址當連結標題，讀屏器只會逐字讀出。|Can't see the button? Use the link marked “{context_en}”.|睇唔到按鈕？請使用「{context_hk}」文字連結。|看不到按钮？请使用“{context_cn}”文字链接。|動作相同時，文字連結和按鈕用一致字眼。
{en} Help Line|{hk}支援提示句|{cn}客服提示语|support line for {en}|{cn}末段告知读者遇到困难时如何寻求帮助。|寫「請直接回覆」，寄件信箱卻不收回覆。|Need help with “{context_en}”? Reply to this email and we'll take a look.|「{context_hk}」時遇到問題？回覆呢封電郵，我哋會跟進。|操作“{context_cn}”时遇到问题？回复这封邮件，我们会帮你查看。|只有有人處理回覆時才可承諾回信支援。
{en} Image Alt Text|{hk}圖片替代文字|{cn}图片替代文本|image description for {en}|为{cn}功能性图片写出能替代图片传达用途的短文字。|按鈕圖片的替代文字只寫「藍色圖案」。|Button image: {context_en}|按鈕圖片：{context_hk}|按钮图片：{context_cn}|功能圖片應寫用途，純裝飾圖片宜留空。
{en} Plain-Text Version|{hk}純文字版本|{cn}纯文本版本|plain text for {en}|{cn}在不支持图文显示时仍可阅读、含必要指引的版本。|純文字版本只叫讀者「按上圖」，沒有替代操作。|To continue, sign in to your account and select “{context_en}”.|請登入帳戶，再選「{context_hk}」繼續。|请登录账号，再选择“{context_cn}”继续。|不要把重要條件留在僅有的圖片內。
"""

PAGES = """
Product Detail Page|商品詳情頁|商品详情页|Shopify,天猫|a refillable bottle|可補充飲品樽|可续装水瓶|先交代實際規格，不讓美感形容詞代替功能。
Collection Page|系列商品頁|系列商品页|Shopify,天猫|a range of travel essentials|一系列旅行用品|一系列出行用品|系列頁先說共同特色，再讓用家挑選規格。
Launch Page|新品發佈頁|新品发布页|Shopify,小红书|a fold-flat tote|可摺疊手提袋|可折叠托特包|發佈日與實際開售日若不同，分開標示。
Campaign Microsite|活動專題網站|活动专题站|官网,微信|a weekend design market|週末設計市集|周末设计市集|用短連結跳到最重要的日期及場地。
Event Registration Page|活動登記頁|活动报名页|官网,微信|a local maker workshop|本地手作工作坊|本地手作体验课|送出表格是否即報名成功要寫清。
Product Comparison Page|產品比較頁|产品对比页|官网,天猫|a pair of travel adapters|兩款旅行轉插|两款旅行转换插头|同一規格欄使用相同量度單位。
Gift Guide Page|送禮指南頁|礼品选购页|Shopify,小红书|a handpicked host gift|精選到訪禮物|精选伴手礼|把禮品到貨截止日放在可見位置。
Membership Page|會員計劃頁|会员计划页|Shopify,微信|a repair credit for members|會員維修禮遇|会员维修权益|列清入會條件與退出方式。
Subscription Page|訂閱計劃頁|订阅方案页|Shopify,App|a monthly refill plan|每月補充配送計劃|每月补充装配送方案|說明每期收費、扣款日及取消方式。
Booking Page|網上預約頁|在线预约页|官网,微信|a personal styling session|一節個人造型諮詢|一节个人穿搭咨询|列出時區、預約長度及改期規則。
App Store Listing|應用程式商店介紹|应用商店介绍|App Store,应用商店|a digital wardrobe planner|電子衣櫃規劃工具|电子衣橱整理工具|商店截圖須符合實際介面，不寫未上線功能。
Product Waitlist Page|到貨候補登記頁|到货候补登记页|Shopify,微信|a limited-run notebook|小批量製作的記事簿|小批量制作的笔记本|候補登記只收必要資料，勿承諾優先購買。
Service Overview Page|服務介紹頁|服务介绍页|官网,微信|an at-home repair service|上門維修服務|上门维修服务|覆蓋地區、可維修產品與費用須分開說明。
Store Locator Page|門市搜尋頁|门店查询页|官网,微信|a shop with refill facilities|設補充站的門市|设补充站的门店|營業時間和服務項目應按實際分店更新。
"""

PAGE_PARTS = """
{en} Hero Headline|{hk}首屏主標題|{cn}首屏主标题|main headline for {en}|在{cn}顶部用短标题说清受众会看到什么。|只寫「開啟精彩無限」，看不出頁面是做甚麼。|Discover {context_en}|探索{context_hk}|了解{context_cn}|不要讓品牌口號掩蓋頁面主題。
{en} Supporting Line|{hk}輔助標題|{cn}辅助标题|subheading for {en}|跟在{cn}主标题后，补充一个具体事实或行动指引。|副標原樣再寫一次主標。|See what's included in {context_en} before you decide.|先睇清楚{context_hk}包含嘅內容，再作決定。|先看清{context_cn}包含什么，再做决定。|補充能影響決定的資料，不必再堆形容詞。
{en} Eyebrow Copy|{hk}眉題|{cn}眉题文案|eyebrow label for {en}|{cn}主标题上方的小字，帮助读者识别内容类别。|眉題寫一整段背景，搶去主標焦點。|In focus: {context_en}|焦點：{context_hk}|焦点：{context_cn}|香港設計簡報亦會寫「小標」，要與副標區分。
{en} Primary Button Copy|{hk}主要按鈕文字|{cn}主按钮文案|primary button text for {en}|{cn}最重要的行动按钮文案，直接反映点击结果。|按鈕寫「立即購買」，實際只會打開詳情。|View details|查看詳情|查看详情|連往詳情、開始預約和完成付款應用不同動詞。
{en} Evidence Line|{hk}實證短句|{cn}证据短句|proof point for {en}|在{cn}卖点附近补上能查证的事实、出处或更新日期。|只寫「業界第一」，沒有來源或比較範圍。|Details about {context_en} were checked by our team this week.|{context_hk}的資料已由團隊於本週核對。|{context_cn}的资料已由团队在本周核对。|發布時替換成實際核對日期或可查證資料。
{en} Eligibility Note|{hk}適用條件註釋|{cn}适用条件说明|eligibility wording for {en}|在{cn}主要行动附近列清读者要满足的条件。|條件只藏在頁尾，主文卻暗示人人適用。|Check whether {context_en} is available in your area.|先查看你所在地區是否提供{context_hk}。|先确认你所在地区是否提供{context_cn}。|重要門檻需靠近承諾，不要只靠星號。
{en} Image Alt Description|{hk}圖片替代描述|{cn}图片替代描述|accessible image copy for {en}|描述{cn}图片中对理解内容有帮助的可见信息。|替代文字塞關鍵字，沒有描述實際畫面。|A close-up showing {context_en} on display.|{context_hk}的展示近鏡。|展示{context_cn}的近景。|依實際畫面改寫，勿虛構顏色、位置或人物。
{en} Frequently Asked Questions|{hk}常見問題|{cn}常见问题|FAQ for {en}|以读者会使用的问法回答{cn}购买、预约或使用前的疑问。|以口號回答問題，沒有給可執行資訊。|Is {context_en} available where I live? Check your postcode in the availability section.|我所在嘅地區有冇{context_hk}？可喺供應地區一欄查閱。|我所在地区有{context_cn}吗？可在服务范围栏查看。|地區查詢方式按市場調整，香港不能照搬郵遞區號。
{en} Accessibility Microcopy|{hk}無障礙介面短句|{cn}无障碍界面提示语|accessible microcopy for {en}|让使用读屏器或键盘操作的人清楚知道{cn}交互元素的用途。|多個不同內容的連結全部標「了解更多」。|Read the details for {context_en}.|查閱{context_hk}的詳情。|查看{context_cn}的详情。|連結脫離上下文朗讀時，仍須能識別用途。
"""

BLOCKS = ((EMAILS, EMAIL_PARTS), (PAGES, PAGE_PARTS))
