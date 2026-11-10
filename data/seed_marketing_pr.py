"""Event publicity and guest operations for offline campaigns."""

EVENTS = """
Press Conference|記者會|新闻发布会|Email,线下活动|our press conference|今次記者會|本次新闻发布会|涉及正式消息時，備妥可引用聲明及發佈時間。
Product Launch Event|新品發佈活動|新品发布活动|IG,线下活动|our product launch|今次新品發佈|本次新品发布活动|展示樣品與正式上市規格須分清楚。
Collection Preview|系列預覽會|系列预览会|IG,线下活动|our collection preview|今次系列預覽會|本次系列预览会|預覽不等於可現場購買，邀請函須分開寫。
Flagship Opening|旗艦店開幕|旗舰店开业|IG,线下门店|our flagship opening|旗艦店開幕日|旗舰店开业活动|安排傳媒及公眾入場的不同時段。
Pop-up Launch|期間限定店開幕|快闪店开幕|小红书,线下门店|our pop-up opening|期間限定店開幕日|快闪店开幕活动|附商場樓層、營業日期和實際入口。
Brand Showcase|品牌展演|品牌展示活动|IG,线下活动|our brand showcase|今次品牌展演|本次品牌展示活动|把有展演的環節與自由參觀時段分開。
Gallery Opening|展覽開幕|展览开幕|IG,线下活动|our exhibition opening|展覽開幕日|展览开幕活动|提醒有攝影限制或版權要求的展區。
Trade Show|商貿展覽|行业展会|LinkedIn,线下活动|our trade show|今次商貿展覽|本次行业展会|註明是否只限業界人士及所需證明。
Networking Reception|交流酒會|交流酒会|LinkedIn,线下活动|our networking reception|今次交流酒會|本次交流酒会|有酒精飲品時，另交代年齡要求及無酒精選擇。
Panel Discussion|專題座談|圆桌讨论|LinkedIn,线下活动|our panel discussion|今次專題座談|本次圆桌讨论|先確認講者可公開的職銜及引述。
Fireside Chat|爐邊對談|炉边对谈|LinkedIn,线下活动|our fireside chat|今次爐邊對談|本次炉边对谈|區分交流形式與講座，交代有否觀眾問答。
Industry Summit|行業峰會|行业峰会|LinkedIn,线下活动|our industry summit|今次行業峰會|本次行业峰会|更新分場會議的時段和場地。
Community Workshop|社群工作坊|社群工作坊|微信,线下活动|our community workshop|今次社群工作坊|本次社群工作坊|工作坊需注明材料供應、名額和參與要求。
Charity Gala|慈善晚宴|慈善晚宴|Email,线下活动|our charity gala|今次慈善晚宴|本次慈善晚宴|捐款與票款分開寫，受惠機構名稱須獲核實。
Awards Ceremony|頒獎典禮|颁奖典礼|Email,线下活动|our awards ceremony|今次頒獎典禮|本次颁奖典礼|避免提前公開受禁發安排限制的得獎名單。
Book Launch|新書發佈會|新书发布会|小红书,线下活动|our book launch|今次新書發佈會|本次新书发布会|簽書或合照另設名額時，請列明。
Partner Roadshow|合作夥伴巡迴展|合作伙伴路演|LinkedIn,线下活动|our partner roadshow|今次合作夥伴巡迴展|本次合作伙伴路演|逐站列出日期及合作方，不宜只用總日程。
Film Screening|電影放映會|影片放映活动|IG,线下活动|our film screening|今次電影放映會|本次影片放映活动|寫明片長、字幕語言及是否有映後分享。
Cultural Festival|文化節|文化节|微信,线下活动|our cultural festival|今次文化節|本次文化节|戶外場地須另備天氣與改期指引。
"""

OPERATIONS = """
{en} Invitation|{hk}邀請函|{cn}邀请函|invite for {en}|给目标来宾发送{context_cn}的地点、时间和回复方法。|「誠邀出席」，無地址、日期或回覆方式。|You're invited to {context_en}. Please confirm attendance by Thursday so we can send your arrival details.|誠邀出席{context_hk}。請於星期四前回覆，稍後會收到到場指引。|诚邀参加{context_cn}。请在周四前确认出席，随后会收到入场指引。|香港正式邀請常用「敬請回覆」。
{en} RSVP Deadline|{hk}回覆出席限期|{cn}出席确认截止时间|response deadline for {en}|来宾确认能否出席{context_cn}的最后时间。|只寫「盡快回覆」，不給實際限期。|Please let us know by Thursday at noon whether you'll attend {context_en}.|敬請於星期四中午前回覆能否出席{context_hk}。|请在周四中午前确认是否参加{context_cn}。|RSVP 指回覆邀請，不等於公開報名。
{en} Guest List|{hk}嘉賓名單|{cn}嘉宾名单|attendee list for {en}|列出{context_cn}预计或已确认来宾，供接待团队核对。|公開分享含私人電話的完整嘉賓名單。|Mark confirmed guests for {context_en} and share only the fields needed for check-in.|更新{context_hk}已確認嘉賓，報到同事只需查看必要資料。|更新{context_cn}已确认名单，只给签到人员查看必要字段。|內部聯絡資料不應列在公開名單。
{en} Waitlist|{hk}候補名單|{cn}候补名单|waiting list for {en}|{context_cn}名额满时登记候补，出现空位后按规则通知。|候補成功被當成已確認入場。|Join the waitlist for {context_en}. We'll email you if a place opens up.|可登記{context_hk}候補名單，有位會以電郵通知。|可加入{context_cn}候补名单，有空位会邮件通知。|勿把「候補登記」按鈕寫成「確認入場」。
{en} Arrival Instructions|{hk}到場指引|{cn}到场指引|arrival guide for {en}|告诉参加{context_cn}的人使用哪个入口、何时到达以及如何报到。|只發地圖定位，沒有商場樓層或入口。|For {context_en}, use the east entrance and follow the signs to the registration desk.|出席{context_hk}，請由東面入口入場，再跟指示前往登記處。|参加{context_cn}请从东入口进入，按指示前往签到台。|文字地址和現場路標應一致。
{en} Check-In Desk|{hk}報到處|{cn}签到台|registration desk for {en}|{context_cn}现场核实来宾资料、发放证件或安排入场的位置。|將 check-in desk 譯成「打卡位」，讓人誤以為是影相位置。|Show your confirmation email at the check-in desk for {context_en}.|出席{context_hk}，請在報到處出示確認電郵。|参加{context_cn}，请在签到台出示确认邮件。|香港「報到／登記」與社交「打卡」不同。
{en} Access Pass|{hk}入場證|{cn}入场凭证|entry credential for {en}|参加{context_cn}时验证入场资格的纸本或电子凭证。|未落實多區通行就寫「全場通行」。|Keep your pass ready at the entrance to {context_en}. It admits one guest to the main hall.|出席{context_hk}請預備入場證，每張只供一位來賓進入主場。|参加{context_cn}请提前准备入场凭证，每张限一人进入主会场。|列清適用場地、名額與能否轉讓。
{en} Accessibility Notice|{hk}無障礙安排提示|{cn}无障碍服务提示|access information for {en}|写清{context_cn}的无障碍入口、设施和额外协助联系方式。|未向場地核實便宣稱「完全無障礙」。|Step-free access to {context_en} is available through the east entrance. Contact us if you need a reserved seat.|出席{context_hk}可經東面入口使用無梯級通道。如需預留座位，請聯絡我們。|参加{context_cn}可从东入口走无台阶通道。需要预留座位请联系我们。|描述具體設施，避免籠統保證。
{en} Run of Show|{hk}活動流程表|{cn}活动执行流程表|show flow for {en}|给{context_cn}现场团队列出时间点、人员和切换提示的流程。|流程表只有對外節目名稱，沒有執行人或接駁時間。|For {context_en}, the floor manager cues the welcome when all guests are seated.|{context_hk}待嘉賓坐定，由台務發出開場提示。|等{context_cn}嘉宾就座后，由现场负责人发出开场提示。|區分內部流程表與嘉賓節目單。
{en} Photo Call|{hk}傳媒拍攝環節|{cn}媒体拍摄环节|press photo opportunity at {en}|{context_cn}预先安排供媒体拍摄人物或展示内容的时段。|將拍攝環節承諾成一對一專訪。|Photographers can attend the photo call after the opening remarks at {context_en}.|{context_hk}開場致辭後設傳媒拍攝環節。|{context_cn}开场致辞后安排媒体拍摄环节。|列出集合位置和拍攝時間，別混用採訪邀請。
{en} Press Accreditation|{hk}傳媒採訪登記|{cn}媒体采访报名|press registration for {en}|媒体提交身份或采访需求，由{context_cn}主办方确认采访权限。|提交表格就寫成已獲採訪資格。|Media attending {context_en} should apply by Wednesday and wait for written confirmation.|傳媒採訪{context_hk}請於星期三前登記，並等候書面確認。|媒体采访{context_cn}请于周三前报名，资格以书面确认为准。|登記、資格確認和領取證件可分三步。
{recap_en} Event Recap|{recap_hk}活動回顧|{recap_cn}活动回顾|highlights from {en}|整理{context_cn}结束后的真实片段、参与者反馈和可公开成果。|將預估人數寫成已核實出席數。|Missed {context_en}? Catch up with the moments our guests shared.|錯過{context_hk}？一齊重溫嘉賓分享嘅精彩片段。|错过{context_cn}？来看看嘉宾分享的现场片段。|先核實人數、引述和照片授權。
{en} Guest Thank-You Note|{hk}嘉賓致謝短箋|{cn}嘉宾感谢信|attendee follow-up for {en}|在{context_cn}后向来宾致谢，并补充已承诺的资料或下一步。|寄出批量感謝信卻未隱藏收件人地址。|Thank you for joining {context_en}. Here's the follow-up material we promised.|多謝出席{context_hk}，隨函附上早前答應提供嘅資料。|感谢参加{context_cn}，这里是现场承诺会发给大家的资料。|不把活動致謝當成未經同意的推廣訂閱。
"""

BLOCKS = ((EVENTS, OPERATIONS),)
