"""Purchase offers differentiated by eligibility and redemption mechanics."""

OFFERS = """
First Order|首單|首单|Shopify,天猫|your first order|首張訂單|首笔订单|以帳戶還是收貨人判斷首購，要寫清楚。
New Member|新會員|新会员|Shopify,微信|new members|新登記會員|新注册会员|香港常寫「迎新禮遇」，內地常寫「新人福利」。
Returning Customer|舊客回購|老客复购|Shopify,淘宝|returning customers|再次選購的顧客|再次下单的老客|以已完成訂單辨認回購，退款單另行處理。
Birthday|生日月|生日月|Shopify,微信|members celebrating their birthday month|生日月份的會員|生日月会员|如只限生日當天，勿寫成整月。
Student|學生專享|学生专享|Shopify,天猫|verified students|完成驗證的學生|已完成认证的学生|說明認可的學生資格和驗證方法。
App Exclusive|App 專享|App 专享|App,App Store|orders placed in the app|經 App 提交的訂單|在 App 内提交的订单|確認手機網頁落單是否適用。
Online Exclusive|網店專享|线上专享|Shopify,天猫|orders placed online|經網店提交的訂單|在线上店铺提交的订单|要註明門市是否同時適用。
Store Exclusive|門市專享|门店专享|线下门店,微信|purchases at participating stores|於指定門市購物|在指定门店购买|列出參與門市，以免客人白行一趟。
Referral|好友推薦|好友推荐|Shopify,微信|eligible orders from invited friends|獲邀親友的合資格訂單|受邀好友的合格订单|分清推薦人和新客各自所得禮遇。
Subscriber|訂戶專享|订阅用户专享|Shopify,Email|active subscribers|訂閱仍然有效的顧客|订阅状态有效的用户|說明一次性購買是否適用。
Loyalty Tier|會員等級專享|会员等级专享|Shopify,天猫|members in eligible tiers|指定級別會員|指定等级会员|以兌換當刻級別或發券時級別為準，要註明。
Product Launch|新品上市|新品首发|Shopify,小红书|eligible launch items|指定新登場產品|指定首发商品|列明指定款式與首發時間。
Festive|節慶|节日|Shopify,天猫|eligible festive purchases|節慶指定商品訂單|节日活动指定商品订单|送禮活動須交代最後可送達日期。
Seasonal Clearance|季末清貨|换季清仓|Shopify,淘宝|items in the seasonal clearance|季末清貨指定貨品|换季清仓指定商品|清貨也要寫明退換安排及原價口徑。
Anniversary|店慶|店庆|Shopify,淘宝|anniversary campaign orders|店慶活動訂單|店庆活动订单|活動時間以結帳完成時間或下單時間為準。
Pre-Launch|上市前|首发前|Shopify,微信|purchases before the public launch|正式公開發售前的購買|正式开售前的购买|把可發貨日期和付款日期分開。
Weekend|週末|周末|Shopify,小红书|qualifying weekend orders|週末合資格訂單|周末符合条件的订单|跨區推廣要寫明開始、結束時間及時區。
Win-Back|舊客回流|老客召回|Shopify,Email|customers invited to shop with us again|獲邀再次選購的顧客|收到回购邀请的老客|說明未購買多久才符合資格。
Gift Registry|禮物清單|礼品心愿单|Shopify,微信|purchases from a gift registry|從禮物清單選購的訂單|通过礼品心愿单购买的订单|由送禮人還是清單建立者享優惠，要交代。
"""

MECHANICS = """
{en} Coupon|{hk}優惠券|{cn}优惠券|{en} voucher|指定给{context_cn}使用的购物优惠券。|A shopping voucher valid for {context_en}.|「人人有券」，實際只限{context_hk}。|Claim the voucher for {context_en} before you check out.|{context_hk}適用，結帳前記得領取優惠券。|{context_cn}适用，先领券再结算。|香港常用「優惠券／禮券」，內地常寫「领券」。
{en} Percentage Discount|{hk}折扣|{cn}折扣优惠|{en} percent off|按百分比为{context_cn}减免合资格商品价格。|A percentage reduction on eligible items for {context_en}.|「8% off」直接寫成「八折」，折扣額對不上。|Take 20% off eligible items. This offer applies to {context_en}.|指定貨品八折，{context_hk}適用。|指定商品八折，{context_cn}适用。|八折等於 20% off，不是 80% off。
{en} Fixed-Amount Discount|{hk}定額扣減|{cn}固定金额立减|{en} cash discount|从{context_cn}应付金额中扣减固定数额。|A fixed sum taken off the amount due for {context_en}.|只寫「即減 50」，沒列出幣別。|Save HK$50 at checkout. Available to {context_en}.|結帳即減 HK$50，{context_hk}適用。|下单立减 50 港元，{context_cn}适用。|固定金額折扣不等於現金回贈。
{en} Minimum Spend|{hk}最低消費額|{cn}起用门槛|{en} spending threshold|指定{context_cn}达到多少合资格消费额才可使用优惠。|The qualifying purchase amount required to use an offer for {context_en}.|未說明運費是否計入{hk}最低消費額。|The offer for {context_en} applies to baskets of HK$300 or more, before delivery fees.|{context_hk}購物滿 HK$300 即可用優惠，運費不計。|{context_cn}商品金额满 300 港元可用，不含运费。|清楚寫明滿額按折前還是折後計。
{en} Tiered Discount|{hk}分級滿額優惠|{cn}阶梯满减|{en} spend tier savings|按{context_cn}达到的不同消费档位给予对应减免。|An offer for {context_en} whose discount changes at stated spending thresholds.|並列所有檔位，卻未說明能否疊加。|For {context_en}: save HK$30 at HK$300 or HK$70 at HK$600. Only the higher eligible saving applies.|{context_hk}滿 HK$300 減 HK$30，滿 HK$600 減 HK$70，按最高合資格級別扣減。|{context_cn}满 300 港元减 30 港元，满 600 港元减 70 港元，按达到的最高档优惠。|每個檔位標清貨幣、門檻和是否累計。
{en} Free Delivery Threshold|{hk}免運費門檻|{cn}满额包邮门槛|{en} free shipping minimum|让{context_cn}达到规定消费额后免收适用配送方式的运费。|The eligible spend needed for {context_en} to receive an applicable delivery service at no extra charge.|只寫「全單免運費」，沒有送貨地區及門檻。|Get free standard delivery in Hong Kong on orders over HK$400. Available to {context_en}.|{context_hk}滿 HK$400 可享香港標準配送免運費。|{context_cn}满 400 港元享香港地区标准配送包邮。|免運費不代表偏遠地區附加費也免除。
{en} Bonus Points|{hk}額外積分|{cn}加赠积分|{en} extra reward points|在常规会员积分之外，向{context_cn}发放额外积分。|Extra loyalty points awarded above the standard amount for {context_en}.|將尚未入帳的額外積分說成即時可用。|Earn double points on eligible items. This applies to {context_en}.|{context_hk}選購指定貨品可獲雙倍會員積分。|{context_cn}购买指定商品可得双倍会员积分。|說明積分何時入帳及退貨會否扣回。
{en} Purchase Gift|{hk}購物贈品|{cn}下单赠品|{en} qualifying purchase gift|在{context_cn}满足活动条件时随单附送礼品。|A gift included with a qualifying order for {context_en}.|未確認存貨仍承諾「每單必送」。|A mini travel pouch is included with {context_en}, while supplies last.|{context_hk}加送迷你旅行袋，送完即止。|{context_cn}赠迷你收纳包，赠完即止。|贈品送完後須及時撤下承諾。
{en} Bundle Pricing|{hk}套裝定價|{cn}组合价|{en} eligible set price|给{context_cn}提供特定商品组合的整套价格。|A single price for a specified group of products, available for {context_en}.|只列「套裝低至」，不交代套裝包含甚麼。|Choose the wash-and-refill set at HK$180. This price applies to {context_en}.|清潔液連補充裝套裝 HK$180，{context_hk}適用。|清洁液加补充装组合价 180 港元，{context_cn}适用。|標出套裝內容及每件規格，勿只強調折扣。
{en} Excluded Items|{hk}不適用貨品|{cn}不参加活动商品|{en} offer exclusions|列明{context_cn}无法用优惠购买的指定款式或类别。|Products or categories that do not qualify for the offer for {context_en}.|主標寫「全店」，細則才列出整類不適用貨品。|Gift cards are excluded from the offer for {context_en}.|{context_hk}優惠不適用於禮品卡。|{context_cn}优惠不适用于礼品卡。|重要例外應靠近價格及優惠主張。
{en} Redemption Window|{hk}兌換時段|{cn}核销有效期|{en} redemption period|规定{context_cn}的优惠在什么时候可使用。|The time period when the offer applies to {context_en}.|將領取期限寫成使用截止時間。|Redeem by Sunday at 11:59 p.m. Hong Kong time. This applies to {context_en}.|{context_hk}請於星期日晚上 11:59（香港時間）前兌換。|{context_cn}请在周日 23:59（香港时间）前使用优惠。|跨區公告用絕對日期，不單用「今晚」。
{en} Redemption Limit|{hk}使用次數上限|{cn}限用次数|{en} single-use restriction|限定{context_cn}可用优惠的次数或可兑换数量。|A limit on the number or frequency of offer claims for {context_en}.|「只可用一次」，不說明按每人、每單還是每帳戶。|One redemption per account. Available to {context_en}.|{context_hk}每個帳戶可兌換一次。|{context_cn}每个账号限用一次。|分清每人限額與每單限額。
{en} Offer Stacking|{hk}優惠同時使用|{cn}优惠叠加|{en} combinable offers|说明{context_cn}能否同时使用其他券、积分或折扣。|Rules on combining this offer with other discounts, vouchers or points for {context_en}.|讓客人結帳後才知道優惠不可同時使用。|The offer for {context_en} cannot be combined with other discount codes.|{context_hk}優惠不可與其他優惠碼同時使用。|{context_cn}优惠不可与其他优惠码叠加。|英文常寫 cannot be combined with，香港多用「不可同時使用」。
"""

BLOCKS = ((OFFERS, MECHANICS),)
