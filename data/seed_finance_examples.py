"""Finance glossary sources, organized by customer-facing payment journeys."""

FINANCE_ANCHORS = """
Electronic Wallet|電子錢包|电子钱包|在手机上保存付款凭证或余额，用于消费、转账或收款的工具。 EN: A digital tool that stores payment credentials or a balance on a device for purchases, transfers and receipts.|钱包里的钱随时会自动生息。|Link a card or add funds to your digital wallet before you check out.|結帳前可先將卡加入電子錢包，或按需要增值。|结账前可先在电子钱包绑定银行卡，或按需充值。|港版多写「電子錢包／增值」，内地多写「电子钱包／充值」。余额与绑卡支付是两种方式。|digital wallet;e-wallet
Stored Value Facility|儲值支付工具|储值支付工具|通过预存价值完成支付的产品，卡片、手机账户等都可能采用这种方式。 EN: A payment product that lets customers spend value loaded in advance, through a card or digital account.|跟银行存款一样，所有余额都享同样保障。|Use your stored balance at participating merchants.|可於指定商戶使用儲值餘額付款。|可在活动指定商户使用储值余额付款。|面对用户写清「儲值額／储值余额」以及使用、退款条件，别把余额写成银行存款。|SVF;stored-value facility
Faster Payment System|轉數快|香港快速支付系统|香港用于实时支付的系统，支持参与机构之间用账户号码或合资格识别资料过数。 EN: Hong Kong's real-time payment system for transfers between participating institutions using account numbers or supported identifiers.|内地任意扫码都能通过转数快付款。|Send money via FPS after confirming the recipient shown on screen.|核對畫面上嘅收款人資料，再用轉數快過數。|使用香港快速支付系统转账前，请核对页面显示的收款人。|香港消费者更熟悉「轉數快」，内地文案加「香港」说明适用网络，别泛指全部即时转账。|FPS;转数快
Cashback|現金回贈|消费返现|消费满足活动条件后返还一部分金额，可能进入卡账、钱包或指定账户。 EN: Money returned after a purchase meets the offer terms, usually credited to a card, wallet or designated account.|下单就立即折现到银行卡，不限金额。|Earn cashback on eligible purchases. Check the cap before you pay.|合資格簽賬可享現金回贈，付款前請先查閱回贈上限。|符合条件的消费可享返现，付款前请查看返现上限。|回赠不一定即时到账，也不是折扣。港版优先「現金回贈」，内地常用「消费返现」。|cash back;cash reward
Interest-Free Instalments|免息分期付款|免息分期|把款项拆成数期偿还，指定期间不收利息，但仍可能有手续费或逾期费用。 EN: A payment plan that splits a balance into scheduled instalments without interest during the stated period. Handling and late fees may still apply.|免息等于整笔交易没有任何费用。|Choose interest-free instalments at checkout. Check for any handling fees before confirming.|結帳時可選免息分期，確認前請先查閱有冇手續費。|结账可选免息分期，确认前请查看是否另收手续费。|港版可写「免息分期」，内地常写「分期免息」。只有确认无费用，才可另写免手续费。|interest-free installment plan;分期免息
Account Opening Bonus|開戶迎新獎賞|开户奖励|新开账户且完成约定动作后获得的奖励，例如存入指定金额或使用指定服务。 EN: A reward for opening an account and completing stated steps, such as depositing funds or using a qualifying service.|注册填手机号就一定立领现金。|New customers may qualify for a bonus after meeting the opening and funding requirements.|新客戶完成開戶及指定存款要求後，有機會獲迎新獎賞。|新用户完成开户并满足入金要求后，可按活动规则领取奖励。|港版「迎新獎賞」，内地「开户奖励」；开通、入金、领取是否是分开的步骤，要写明。|new-account incentive;開戶禮;开户礼
Cross-Border Remittance|跨境匯款|跨境汇款|通过金融机构或支付服务向另一地区的收款人汇出资金。 EN: A transfer of funds to a recipient in another market through a bank or payment service.|全球转账一律秒到且免费。|See the estimated arrival date and recipient amount before sending your remittance.|匯款前先查閱預計到賬日期及收款金額。|提交跨境汇款前，先查看预计到账日期和收款金额。|别把付款时间当作到账时间；还应分开列出汇率、汇费和可能的中转行收费。|international money transfer;overseas remittance
Payment Link|付款連結|收款链接|商家生成的链接，客户打开后可在指定页面完成付款。 EN: A merchant-generated link that opens a page where a customer can review and pay an amount.|把银行卡密码发给我们就能创建收款链接。|Open the secure payment link in your invoice to review the amount and pay.|打開發票內嘅付款連結，核對金額後再付款。|打开账单内的收款链接，核对金额后再完成支付。|港版从付款者角度用「付款連結」，内地从商家角度用「收款链接」，标明链接来源。|pay by link;支付链接
Contactless Payment|感應式付款|非接触式支付|将卡片或具备支付功能的设备靠近终端完成付款。 EN: Payment made by tapping a compatible card or device near a reader.|一拍即付，不论金额都无需验证。|Tap your card on the reader. Additional verification may be requested.|將卡貼近讀卡器付款，部分交易或須額外認證。|把卡片靠近读卡终端即可支付，部分交易可能需要额外验证。|消费者页面香港可写「拍卡付款」，内地可写「碰一碰付款」，有专属品牌时勿泛化。|tap to pay;tap-and-pay;拍卡付款
QR Code Payment|掃碼付款|扫码支付|通过扫描商户二维码，或出示自己的付款码，让终端发起交易。 EN: Payment initiated by scanning a merchant's QR code or presenting a customer payment code.|扫到任何二维码都可以付款。|Scan the merchant’s QR code and check the name and amount before you pay.|掃描商戶二維碼後，先核對商戶名稱及金額。|扫码后先核对商户名称和付款金额，再确认支付。|区分扫商户码与出示付款码，两种流程的按钮指引不同。|QR payment;二维码支付
Dynamic Currency Conversion|動態貨幣轉換|动态货币转换|境外商户或终端把交易金额换算为持卡人熟悉的货币，供持卡人选择。 EN: A checkout option in which a merchant or terminal converts the transaction into the cardholder's home or other familiar currency.|选择人民币结算就一定更划算。|Review the conversion rate and total before choosing your billing currency.|揀結算貨幣前，先睇清楚兌換匯率同總額。|选择结算币种前，请核对换算汇率和应付总额。|写清谁提供汇率及费用，保留本地币种选项，不承诺某一币种一定更省。|DCC;merchant currency conversion
Foreign Transaction Fee|外幣簽賬手續費|外币交易手续费|发生指定外币或境外交易时，发卡方可能按条款收取的费用。 EN: A charge a card issuer may apply to qualifying foreign-currency or overseas purchases.|用本币支付就绝对没有任何境外手续费。|Check the card’s fee schedule before paying in a foreign currency.|外幣簽賬前，先查閱信用卡收費表。|进行外币交易前，请先查看银行卡收费标准。|跨境地点和交易币种可能是不同计费条件，别只凭展示货币判断。|FX transaction fee;foreign purchase fee
Mid-Market Exchange Rate|市場中間匯率|市场中间汇率|同一时点买入与卖出报价之间的中间值，常用于对照兑换报价。 EN: The midpoint between buy and sell exchange rates at a given time, used as a benchmark for customer quotes.|按中间汇率换汇，所以绝无其他费用。|Compare our quoted rate with the mid-market rate shown at the same time.|可用同一時間顯示嘅市場中間匯率，比較實際兌換報價。|可将实际换汇报价与同一时点的市场中间汇率进行对比。|中间汇率只是参照，实际成交价和收费另列，并注明报价时点。|interbank mid-rate;mid-market rate
Exchange Rate Lock|鎖定兌換匯率|锁汇|在指定期限或满足条件时保留一个兑换报价，减少付款时的报价变动。 EN: An arrangement that holds a quoted exchange rate until a stated deadline or while specified conditions are met.|锁汇以后，不论何时付款都享原价。|Complete payment before the quote expires to keep this exchange rate.|請於報價到期前完成付款，以保留本次兌換匯率。|请在报价失效前完成支付，以保留本次锁定汇率。|港版说「鎖定匯率」，内地可缩写「锁汇」。清楚写出截止时间和触发条件。|locked FX quote;rate guarantee window
Beneficiary Details|收款人資料|收款人信息|用于识别收款账户的姓名、号码及其他必要信息。 EN: The name, account number and other information needed to identify the recipient of a payment.|名字填个简称就行，账号错了也能自动退回。|Match the beneficiary’s name and account details against their bank instructions.|按對方銀行提供嘅資料核對收款人姓名同戶口號碼。|按收款方银行提供的信息核对收款人姓名和账号。|香港常写「戶口號碼」，内地写「银行账号」。姓名、币种、代码的字段随渠道而异。|payee details;recipient details
Receiving Bank Fee|收款銀行收費|收款行手续费|收款机构按当地规则或账户条款从入账款项中扣取或另行收取的费用。 EN: A fee charged by the receiving bank, sometimes deducted from the money being transferred.|我们免汇费，所以收款方肯定全额收到。|The receiving bank may deduct its own fee from the transfer amount.|收款銀行或會按其收費表扣除費用。|收款行可能按其收费标准从汇款金额中扣收手续费。|付款页的「免手續費」需写清是哪一方免收，避免把所有银行费用一起承诺。|beneficiary bank fee;receiving charges
Transfer Reference|轉賬備註|转账附言|随转账提交的识别文字，帮助收款人把入账和发票或订单对应起来。 EN: Text or a reference number sent with a transfer so the recipient can match it to an invoice or order.|附言填写身份证号方便对账。|Add your invoice number to the transfer reference so we can match your payment.|請於轉賬備註填上發票編號，方便核對款項。|请在转账附言填写发票编号，便于核对入账。|界面空间不足时可写「備註／附言」，勿引导用户在此填写密码等敏感资料。|payment reference;remittance reference
Direct Debit|自動轉賬繳費|自动扣款|经账户持有人授权后，由指定收款方按约定从账户发起扣款。 EN: An authorised arrangement that allows a payee to collect money from an account under agreed terms.|绑定账号就默认允许任意扣款。|Review the amount and schedule before authorising direct debit.|授權自動轉賬前，請核對扣賬金額同日期。|开通自动扣款前，请核对扣款金额和时间。|香港「自動轉賬」也可泛指预约付款，文案注明由谁发起扣款及取消方式。|autopay;direct debit instruction
Recurring Payment|定期付款|周期性扣款|按约定周期重复发生的付款，常见于订阅、会员及账单。 EN: A payment repeated on a schedule, commonly for a subscription, membership or bill.|体验期结束后扣费，无需提前告知。|Your membership renews monthly unless you cancel before the next billing date.|除非喺下個收費日前取消，會籍將按月續期。|如未在下一扣费日前取消，会员将按月自动续费。|写清续费时间、金额和取消入口，别只在页脚写「适用条款」。|scheduled recurring charge;automatic renewal payment
Standing Order|常行指示|定期转账指令|由付款人设定，在固定时间转出指定金额的银行付款指令。 EN: A bank instruction set by the payer to send a fixed amount on specified dates.|设定后，收款人随时可以改变扣款额。|Set a standing order to transfer a fixed amount on your chosen date.|設定常行指示，於指定日期轉出固定款項。|设置定期转账指令，在指定日期转出固定金额。|与商户发起的自动扣款不同，定期转账金额和时间通常由付款人设定。|standing payment instruction;定期过数
Payment Authorisation|付款授權|支付授权|发卡方或付款网络核验请求并同意交易，授权成功并不等于商户已结算。 EN: Approval of a transaction by the card issuer or payment network before the merchant captures or settles the charge.|授权成功说明款项已经入商户账户。|Your payment is authorised. The final charge will appear once the merchant processes it.|付款已獲授權，商戶完成交易處理後會顯示正式扣賬。|支付已授权，商户完成交易处理后将显示实际扣款。|港版「授權」与「入賬」分开写，内地「授权」与「扣款／结算」也不混用。|payment authorization;card approval
Pre-Authorisation Hold|預授權暫扣|预授权冻结|酒店或租车等商户先占用部分余额或额度，待最终金额确认后结算或解除。 EN: A temporary reservation of funds or credit, commonly placed by a hotel or car rental firm until the final charge is known.|只要没扣款，额度就不会受影响。|The hotel may place a temporary hold at check-in. Ask when the unused amount will be released.|酒店辦理入住時或會暫扣預授權金額，請查詢未使用款項何時解除。|酒店办理入住时可能冻结预授权金额，请询问未使用额度何时解冻。|应区分占用额度、正式扣款与解除时间；港版「暫扣」，内地常用「冻结」。|preauthorization hold;card hold
Payment Capture|確認扣賬|支付请款|商家在授权后确认要收取的金额，进入实际扣账与后续结算。 EN: The merchant's confirmation of the amount to collect after payment approval, which moves the transaction towards settlement.|订单付款只要发起授权就不可撤销。|We capture payment when your order is ready to ship.|訂單備妥出貨時，我哋先會確認扣賬。|订单备货完成后，我们会发起请款并确认扣款。|开发文档可写「请款」，消费者页面用「確認扣賬／实际扣款」更直白。|capture payment;charge capture
Payment Reversal|付款撤銷|支付冲正|交易未完成或需要纠正时撤回原交易，处理方式随支付网络和交易阶段而异。 EN: The cancellation or correction of an original transaction, often before it has settled.|所有支付冲正都等于售后退款。|The unsuccessful payment was reversed. Check your balance for the release.|未完成嘅付款已撤銷，請查看戶口餘額有冇恢復。|未完成的支付已冲正，请查看账户余额是否恢复。|客服可把「冲正」解释成「撤回未完成扣款」，勿将其和完成后的退款混称。|transaction reversal;payment void
Chargeback|信用卡退款爭議|信用卡拒付|持卡人通过发卡方对卡交易提出争议，能否退回款项取决于原因和审核。 EN: A card payment dispute raised through the issuer that can result in reversal of the charge after review.|发起拒付就一定能收回全部款项。|If you don’t recognise a charge, contact your card issuer to discuss your dispute options.|如唔認得一筆簽賬，可聯絡發卡機構了解爭議處理方式。|如发现不认识的信用卡扣款，可联系发卡机构了解拒付申请流程。|商户端常说「拒付」，面对香港持卡人可写「交易爭議／退款申索」，不预先承诺结果。|card chargeback;card dispute
Refund to Original Payment Method|按原付款方式退款|原路退款|款项经原先用于付款的卡、钱包或账户退回。 EN: A refund sent back through the card, wallet or account used for the original purchase.|退款申请成功，钱会立即到另一张卡。|Your refund will go back to the card used at checkout.|退款會退回結帳時使用嘅信用卡。|退款将原路退回至下单时使用的支付账户。|写明退款退回哪里，以及商户处理与金融机构入账可能分开计时。|refund to original tender;original route refund
Pending Transaction|待入賬交易|待入账交易|支付记录已出现，但尚未完成最终扣账、清算或入账的交易。 EN: A recorded payment that has yet to complete processing or appear as a final charge.|待入账就是支付失败，立即重付。|This transaction is still pending. Check its status before trying again.|交易尚待入賬，重試前請先核對狀態。|该笔交易尚待入账，请先查看状态再尝试支付。|视界面区分付款处理中与入账处理中，避免让客户误以为要重复支付。|pending card charge;awaiting posting
Settlement Currency|結算貨幣|结算币种|支付服务商将款项划给商户时采用的货币，可能与买家所付币种不同。 EN: The currency in which a payment service pays out funds to a merchant.|客户看的是港币，商户肯定收到同样的港币金额。|Choose the settlement currency for your merchant account before accepting payments.|接受付款前，請為商戶戶口設定結算貨幣。|开始收款前，请为商户账户设置结算币种。|区分标价、持卡人付款和商户结算货币，单独说明换汇是否收费。|payout currency;merchant settlement currency
Merchant Category Code|商戶類別代碼|商户类别码|收单机构按主营业务为商户归类的代码，卡优惠可能按类别识别。 EN: A code used to classify a merchant's main business, which can determine eligibility for card rewards.|便利店买机票也肯定按旅游类回赠计算。|Check how your issuer classifies the merchant before counting on the category bonus.|享用指定類別回贈前，請查閱發卡機構嘅商戶分類。|享受指定品类返现前，请先查看发卡机构如何识别商户类别。|MCC 适合条款或后台，前台优先列出适用商户，并说明分类认定口径。|MCC;merchant classification code
Cash Advance|信用卡現金透支|信用卡预借现金|持卡人从信用额度提取现金或使用等同现金的交易方式，费用可能与消费不同。 EN: Cash drawn against a credit line or a cash-like transaction, often subject to different fees and interest from purchases.|刷信用卡取现，跟普通消费一样免息。|Check the cash advance fee and when interest starts before withdrawing.|提取現金前，請查閱現金透支收費同利息起計日。|预借现金前，请查看取现手续费和计息起始日。|港版可说「現金透支」，内地可说「信用卡取现」，费用和计息要分开写。|credit card cash withdrawal;card cash advance
Available Credit|可用信用額|可用额度|扣除已使用、待入账或被占用金额后仍可使用的信用额度。 EN: The portion of a credit limit still available after posted charges, pending transactions and holds.|总额度就是此刻能全部刷的金额。|Check your available credit before making a large purchase.|大額簽賬前，先查閱可用信用額。|大额消费前，先查看信用卡可用额度。|区分总信用额、可用信用额与临时额度，用户需要知道可用金额是否实时更新。|remaining credit limit;available card limit
Statement Balance|月結單結欠|账单应还金额|账单周期结束时列出的结欠金额，未必等于查询当天的实时余额。 EN: The amount owed at the close of a billing cycle, as shown on the statement.|当前未出账消费全部都在这期账单里。|Pay the statement balance by the due date shown on your bill.|請按月結單所示嘅到期日繳清結欠。|请在账单所示还款日之前归还本期应还金额。|港版「月結單」，内地「账单」。已出账、未出账和当前欠款分列。|billed balance;statement amount
Minimum Payment Due|最低還款額|最低还款额|账单要求在到期日前至少支付的金额，未偿清部分可能继续计息。 EN: The least amount due by the stated date. Interest may still accrue on the unpaid balance.|还最低金额就跟全额还清一样。|Pay at least the minimum by the due date. Interest may still apply to the balance.|請於到期日前繳付最低還款額，未清結欠仍可能計息。|请在还款日之前至少归还最低还款额，剩余欠款仍可能产生利息。|勿将最低还款描述成免息方案，也别用「只需还」掩盖剩余欠款。|minimum amount due;minimum repayment
Grace Period|免息還款期|免息期|在符合还款等条件时，指定消费不收取利息的期间。 EN: A period in which eligible purchases do not accrue interest if the repayment terms are met.|任何信用卡交易都有同样长的免息期。|Pay your purchase balance as required to keep the purchase grace period.|按條款繳清簽賬結欠，先可享免息還款期。|按约定归还消费欠款，符合条件方可享免息期。|写明适用交易类型和起算、截止时间，现金透支可能按不同规则计息。|interest-free period;purchase grace period
Annual Fee Waiver|豁免信用卡年費|信用卡免年费|发卡机构按活动条件免收信用卡年费，可有指定期限或消费要求。 EN: An offer that removes a card's annual fee for a stated period or after a qualifying spend or action.|首年免年费等于终身免费。|Your first-year annual fee is waived. Check the conditions for later years.|首年年費獲豁免，往後年度請查閱豁免條件。|首年免年费，后续年度请查看免年费条件。|港版用「豁免年費」，内地用「免年费」。首年、续年、附属卡分开说明。|card fee waiver;annual membership fee waiver
Supplementary Card|附屬信用卡|信用卡附属卡|由主卡账户授权另一位持卡人使用的卡片，额度和账务安排以发卡条款为准。 EN: An additional card issued to an authorised user under the primary cardholder's account.|附属卡消费和主卡账单毫无关系。|Set a spending limit for your supplementary card if your issuer offers this control.|如發卡機構支援，可為附屬信用卡設定簽賬限額。|如发卡机构支持，可为附属卡单独设置消费限额。|英语也常见 additional card；区分主卡人承担账务与附属卡持有人使用权限。|additional card;add-on card
Virtual Card|虛擬卡|虚拟银行卡|可在应用内获取或使用的数字卡，可能有独立卡号及使用限制。 EN: A digital payment card that may have its own number and usage limits.|虚拟卡不需要保护任何卡片资料。|Use your virtual card details at supported online checkouts.|可於支援嘅網上商戶使用虛擬卡付款。|可在支持的线上商户使用虚拟银行卡支付。|不要与已绑定实体卡的手机钱包混淆，写清卡号、渠道及限额适用范围。|virtual payment card;digital-only card
One-Time Passcode|一次性密碼|一次性验证码|在有限时间内使用一次的验证码，用于核实登录、付款或资料更新。 EN: A short-lived verification code that can be used once to confirm a login, payment or account change.|把短信验证码告诉店员完成付款。|Enter the one-time code only on the verification screen you opened.|只可喺你自己開啟嘅驗證畫面輸入一次性密碼。|只在你主动打开的验证页面输入一次性验证码。|OTP 可放在说明页，香港常写「一次性密碼」，内地常写「短信验证码」并按实际渠道调整。|OTP;one-time password
Merchant Settlement Report|商戶結算報表|商户结算报表|按结算批次汇总交易、退款、手续费和划款的文件。 EN: A record of sales, refunds, fees and payouts grouped by settlement batch.|报表的交易总额就是银行实际入账金额。|Compare your settlement report with the net amount paid into your bank account.|將結算報表同銀行戶口嘅實際入賬淨額核對。|请用结算报表核对银行账户的实际入账净额。|同时标明交易总额和结算净额，列明差异项便于商户对账。|payout report;settlement statement
Next-Business-Day Settlement|下一個工作天結算|下一工作日结算|按结算规则在下一个工作日划拨款项，节假日、截单时间可能影响日期。 EN: A payout scheduled for the next business day under the provider's cutoff and holiday rules.|明天一定到账，包括节假日。|Eligible payments settle on the next business day, subject to the cut-off.|合資格款項會於下一個工作天結算，截數時間以通知為準。|符合条件的款项于下一工作日结算，具体以截单时间为准。|港版「工作天／截數」，内地「工作日／截单」；结算发出与到账分开说明。|next-day payout;T+1 settlement
Payment Reconciliation|付款對賬|支付对账|把订单、支付记录与入账数据核对，识别漏收、退款、手续费等差异。 EN: The process of matching orders, payments and bank entries to account for missing funds, refunds and fees.|今天账面总额一样，就不用核对任何明细。|Match each order to its payment and refund records before closing the day.|埋數前，將每張訂單同付款及退款紀錄核對。|日终结账前，请逐笔核对订单、支付和退款记录。|港版多用「對賬／埋數」，内地用「对账」。建议对照同一时区和日期口径。|transaction reconciliation;payment matching
Merchant Service Charge|商戶服務費|商户收单服务费|商户为接受指定支付交易按约定付给收单机构或服务商的费用。 EN: The fee a merchant pays its acquirer or payment service for accepting qualifying transactions.|商户服务费就是顾客要付的附加费。|Review the merchant service charge in your pricing schedule before activating card payments.|開通信用卡收款前，請先查閱價目表上嘅商戶服務費。|开通银行卡收款前，请查看价目表中的收单服务费。|区分商户承担的收单费用与顾客侧费用，适用交易和计费方式应单独列明。|MSC;merchant discount rate
Buy Now Pay Later|先買後付|先享后付|先取得商品或服务，稍后一次或分期支付的安排。 EN: A purchase arrangement that lets the customer receive goods or services before paying in one later payment or in instalments.|先享后付等于不用支付这笔订单。|Review the repayment dates and any charges before choosing pay later.|選用先買後付前，請查閱還款日期同相關費用。|选择先享后付前，请先核对还款日期和相关费用。|BNPL 适合行业说明；前台写清分期、逾期、退款和实际支付义务。|BNPL;pay later
Early Repayment|提早還款|提前还款|在原定期限前偿还部分或全部欠款，可能要申请或承担费用。 EN: The repayment of part or all of a balance before its original due date, sometimes subject to fees or notice.|提前还款一定无条件减免所有费用。|Ask for an early repayment quote before paying off the loan.|清還貸款前，可先索取提早還款報價。|提前结清贷款前，请先查询应还金额及相关费用。|区分部分提前还款与全额结清，并提示收费、利息计算和申请步骤。|early settlement;prepayment
Fixed Deposit|定期存款|定期存款|按约定存期和条件存放资金，利息、到期续存和提前支取以产品条款为准。 EN: A deposit held for an agreed term, with interest, renewal and early withdrawal governed by the account terms.|随存随取、任何时候都按定期利率计算。|Choose a term after checking the rate and what happens if you withdraw early.|揀選存款期前，先查閱利率同提早提款安排。|选择定期存款期限前，请先查看利率和提前支取规则。|标明币种、期限和利率适用条件，勿把年利率直接写成单个存期收益。|time deposit;term deposit
Annualised Interest Rate|年利率|年化利率|把指定利率以一年为单位表达，便于比较不同期限，但实际利息受条款影响。 EN: An interest rate expressed on a one-year basis so rates for different periods can be compared.|三个月存款也能拿到页面所示的全年收益。|The rate is annualised. Use the deposit calculator to estimate interest for your chosen term.|所示為年利率，可用計算機估算所選存款期嘅利息。|页面展示年化利率，请按所选存期估算实际利息。|如同时有基础利率和额外奖励利率，应写明各自条件与计算口径。|annualized rate;interest rate per annum
Deposit Maturity Instruction|定期存款到期指示|定期存款到期安排|预先选择存款到期时提取本息、续存本金或连本带息续存。 EN: A choice made in advance about what happens at maturity, such as paying out the funds or rolling over the principal or interest.|到期自动续存一律沿用原利率。|Choose whether to renew or withdraw at maturity. Renewal uses the rate available at that time.|請設定到期續存或提取，到期續存按當時適用利率辦理。|请选择到期续存或支取，续存按届时适用利率办理。|港版「到期指示」，内地「到期安排／转存方式」。列出本金和利息是否一并处理。|maturity instruction;renewal instruction
"""

FINANCE_MATRICES = (
    (
        """
Dining|餐飲|餐饮|餐厅及指定餐饮商户消费
Grocery|超市|商超|指定超市与食品杂货消费
Transit|公共交通|公共出行|指定公共交通支付
Fuel|入油|加油|指定加油站及油品消费
Streaming|串流訂閱|流媒体订阅|符合规则的串流平台订阅
Pharmacy|藥房|药店|指定药店商户消费
Hotel|酒店住宿|酒店住宿|符合条件的酒店预订或到店消费
Tuition|學費|学费|指定教育机构学费支付
Utilities|公用服務賬單|生活缴费|活动覆盖的水电燃气缴费
Overseas In-Store|海外實體店|境外线下|指定境外实体商户支付
""",
        """
{en} Cashback|{hk}現金回贈|{cn}消费返现|针对{scope}的卡或支付活动，满足条件后返还部分金额。 EN: A card or payment offer that returns part of eligible {english} spending once the terms are met.|只要有{cn}就无限额返现。|Earn cashback on eligible {english} purchases. See the offer details before paying.|指定{hk}簽賬可享現金回贈，付款前請先查閱活動條款。|符合条件的{cn}消费可享返现，支付前请查看活动规则。|「回贈／返现」不是当场减价。{scope}的入账日期和付款渠道可能影响资格。|{en} cash rewards
{en} Cashback Cap|{hk}回贈上限|{cn}返现上限|对{scope}设定的返现金额上限，可按每人、单笔或周期计算。 EN: The maximum cashback payable on {english} spending per person, transaction or offer period.|每笔{cn}消费无论金额都按相同金额返现。|Check the {english} cashback cap and how much of it you have used this month.|本月{hk}回贈仲剩幾多？付款前可查閱已用同剩餘上限。|付款前可查看本月{cn}返现上限及剩余额度。|「上限」对应返还额，和最低消费门槛是两回事；{scope}可能与其他类别共享额度。|{en} cash reward ceiling
Eligible {en} Spend|合資格{hk}簽賬|符合条件的{cn}消费|按商户、付款方式、入账时间等规则计入活动的{scope}。 EN: {en} spending that counts towards an offer under its merchant, payment and posting rules.|只要支付页面写着{cn}，就肯定计入活动。|Check which {english} transactions count towards this offer.|想累積{hk}簽賬？先查閱邊啲交易計入活動。|准备参加活动？先查看哪些{cn}交易计入合格消费。|活动页宜给出可核对的适用渠道和排除项，不能只写{scope}即可。|Qualifying {en} Purchases
""", ("银行 App", "信用卡活动页")),
    (
        """
Cross-Border Bank Transfer|跨境銀行轉賬|跨境银行转账|汇入境外银行账户
Cash Pickup Remittance|現金提取匯款|现金领取汇款|由收款人到服务点提取现金
Wallet Remittance|電子錢包匯款|钱包汇款|汇入支持的电子钱包账户
Card-to-Card Transfer|卡對卡轉賬|卡间转账|按支持的卡网络向卡账户转入款项
Instant Domestic Transfer|本地即時轉賬|境内实时转账|经本地实时支付网络过账
Scheduled Bank Transfer|預設日期轉賬|预约转账|按预设日期向银行账户付款
Batch Payout|批量發款|批量付款|通过同一指令向多个账户付款
""",
        """
{en} Processing Fee|{hk}手續費|{cn}手续费|发起{scope}所收取的服务费用，可能与收款方费用分别计算。 EN: The provider's charge for sending funds by {english}, separate from any recipient-side fees.|{cn}显示免服务费，所有环节肯定免费。|Review the processing fee for your {english} before confirming the amount.|確認金額前，請先查閱{hk}手續費。|请在确认金额前，查看本次{cn}手续费。|手续费、换汇成本和第三方收费分开列明。{scope}也可能涉及不同费用承担方。|{en} service charge
{en} Daily Limit|{hk}每日限額|{cn}单日限额|在每日计算周期内，{scope}时允许发起的累计金额上限。 EN: The total amount a customer may send by {english} in one day under the provider's cutoff rules.|今天单笔没超额，所以可以不限次数{cn}。|Check your remaining daily limit before sending a {english}.|辦理{hk}前，可查閱今日剩餘限額。|办理{cn}前，可查询当天剩余可用额度。|分开写每笔与每日限额。若{scope}使用共享额度，界面应说明。|{en} daily cap
{en} Delivery Estimate|{hk}預計到賬時間|{cn}预计到账时间|按路线、支付状态与处理时间估算{scope}的预计完成时点。 EN: The expected time for funds sent by {english} to reach the recipient, based on the route and current processing status.|只要付款成功，{cn}就肯定立即到账。|Check the estimated delivery time for your {english} on the confirmation screen.|確認畫面會列出{hk}嘅預計到賬時間。|请在确认页查看{cn}预计到账时间。|港版常写「到賬／入賬」，内地常写「到账」。若{scope}仍需领取或确认，另写明动作。|{en} ETA
{en} Tracking|{hk}進度查詢|{cn}进度查询|按交易编号查看{scope}是否已受理、处理中、成功或未完成。 EN: Status information for a {english} transaction, retrieved by transaction reference.|{cn}显示受理，就告诉收款方钱已可用。|Track your {english} using the reference on your receipt.|用收據上嘅交易編號查詢{hk}進度。|使用凭证上的交易编号查询{cn}进度。|面向消费者用「查進度／查进度」更自然。区分{scope}的受理状态与实际完成。|{en} status lookup
{en} Cancellation Window|{hk}可取消時段|{cn}可撤销时间|尚可申请撤销{scope}的处理阶段或截止时点，并非每笔交易都支持。 EN: The period in which a customer can ask the provider to stop a {english} transaction before it becomes irreversible.|{cn}发出后任何时间都能撤回。|If your {english} is still eligible for cancellation, use the option on its status page.|如{hk}仍可取消，請喺交易詳情頁提出申請。|若该笔{cn}仍可撤销，请在交易详情页提交申请。|仅在确认支持撤销时展示入口。即时完成的{scope}不能照搬预约交易规则。|{en} cancellation deadline
""", ("银行 App", "汇款服务页")),
    (
        """
Debit Card|扣賬卡|借记卡|直接从绑定账户扣款的卡
Credit Card|信用卡|信用卡|使用获批信用额度进行交易的卡
Prepaid Card|預付卡|预付卡|使用已储值金额进行交易的卡
Virtual Card|虛擬卡|虚拟卡|可在应用内使用的数字卡
Travel Card|旅遊外幣卡|旅行外币卡|用于旅行中指定外币交易的卡
Corporate Card|公司卡|企业卡|供员工按公司规则办理业务支出的卡
""",
        """
{en} Spending Limit|{hk}簽賬限額|{cn}消费限额|使用{scope}消费时的单笔、每日或周期交易限额。 EN: The maximum amount a customer may spend using a {english} per transaction, day or billing period.|{cn}余额还有钱，就不受消费限制。|Check your {english} spending limit before a large purchase.|大額消費前，請先核對{hk}簽賬限額。|大额消费前，请先查看{cn}消费限额。|港版「限額」，内地「限额／额度」；讲清{scope}的消费限制和可用余额差异。|{en} purchase cap
{en} Foreign Currency Markup|{hk}外幣兌換加價|{cn}外币兑换加价|使用{scope}涉及外币换算时，报价相对参考汇率增加的部分。 EN: The amount added to a reference exchange rate when a {english} purchase is converted into the billing currency.|{cn}显示零手续费，换算价就一定等于市场中间价。|Compare the quoted conversion and any foreign currency markup before using your {english}.|使用{hk}前，可比較兌換報價同外幣兌換加價。|使用{cn}前，请比较换算报价与外币兑换加价。|说明{scope}采用的参照时点，不把汇率加价和另收手续费合并宣称为零。|{en} FX markup
{en} Transaction History|{hk}交易紀錄|{cn}交易明细|按日期或类型查看使用{scope}的交易及退款记录。 EN: A dated record of purchases, credits and refunds on a {english}.|{cn}记录没有这笔就一定从未扣款。|Open your {english} transaction history to check both pending and posted purchases.|開啟{hk}交易紀錄，可查看待入賬及已入賬簽賬。|打开{cn}交易明细，查看待入账和已入账的消费。|若{scope}的记录有延迟，提示刷新时间；已入账和预授权状态不要混用。|{en} activity log
{en} Transaction Alert|{hk}簽賬提示|{cn}交易提醒|使用{scope}付款时由短信、推送等渠道发出的通知。 EN: A push notification, text or other message sent when a transaction is made with a {english}.|收到{cn}交易提醒就代表资金已结算。|Turn on {english} transaction alerts to keep track of recent card activity.|開啟{hk}簽賬提示，方便留意近期交易。|开启{cn}交易提醒，及时了解近期交易动态。|通知不是结算凭证。营销页应注明{scope}支持的提醒渠道与适用交易类型。|{en} spend notification
{en} Freeze|{hk}暫時鎖卡|{cn}临时锁卡|临时限制使用{scope}发起部分新交易，解锁条件按发卡方规定。 EN: A temporary restriction on some new transactions made with a {english}, lifted under the issuer's rules.|一键锁定{cn}后，之前的交易会自动取消。|If you misplace your {english}, freeze it in the app and check which payments may still go through.|如暫時搵唔到{hk}，可喺程式鎖卡，再查閱邊類付款仍可能處理。|暂时找不到{cn}时，可在应用内锁卡，并查看仍可能处理的交易类型。|说明{scope}锁卡覆盖的渠道和自动扣款是否继续；怀疑盗用应提供联系入口。|Freeze {en}
""", ("银行 App", "信用卡服务页")),
    (
        """
Online Card|網上卡類|线上银行卡|网页或应用内的银行卡支付
In-Store Card|實體店卡類|线下银行卡|实体终端受理的银行卡支付
Wallet Checkout|電子錢包結帳|电子钱包收银|顾客使用电子钱包结账
Merchant QR|商戶掃碼|商户扫码|商户通过二维码受理付款
Bank Debit|銀行扣賬|银行代扣|经授权直接从付款账户扣款
Mobile POS|流動收款機|移动收银终端|使用移动终端接受线下支付
""",
        """
{en} Payout Schedule|{hk}結算時間表|{cn}结算周期|支付服务商把{scope}所得款项划给商户的日期规则。 EN: The timetable a provider uses to pay a merchant for {english} transactions.|{cn}交易一完成，钱就即时打入银行户口。|Check when {english} proceeds are due to reach your merchant account.|查閱{hk}結算時間表，了解款項預計何時入商戶戶口。|查看{cn}结算周期，了解款项预计何时划入商户账户。|写清{scope}的截单日、节假日安排及到账预估，别把收款时间等同结算时间。|{en} settlement timetable
{en} Settlement Currency|{hk}結算貨幣|{cn}结算币种|将{scope}的款项划入商户账户时使用的币种。 EN: The currency in which a merchant receives proceeds from {english} payments.|顾客用{cn}付什么币，商户总能原币结算。|Review the settlement currency for {english} before comparing your net proceeds.|比較收款淨額前，請先核對{hk}結算貨幣。|对比实收净额前，请先核对{cn}结算币种。|若{scope}发生币种转换，说明兑换时点与费用，别只显示顾客侧货币。|{en} payout currency
{en} Processing Fee|{hk}收款手續費|{cn}收款手续费|处理{scope}时，支付服务商向商户收取的交易费用。 EN: The transaction fee charged to a merchant for accepting {english} payments.|{cn}只列基础费率就行，其他费用不用说明。|See the processing fee and any per-transaction charges for {english}.|查閱{hk}收款手續費，留意有冇逐筆交易費用。|查看{cn}收款手续费，确认是否另有按笔收费。|说明{scope}按比例、按笔或混合计价，避免只宣传一个低费率。|{en} merchant fee
{en} Refund Timing|{hk}退款時間|{cn}退款时效|从发起退款到{scope}相关款项退回顾客的预计时长。 EN: The estimated time for money to reach a customer after the merchant initiates a refund on a {english} payment.|商户发起{cn}退款，客户一定马上收到。|Once the refund is issued, check the expected arrival time for {english} payments.|發出退款後，可查閱{hk}付款嘅預計到賬時間。|发起退款后，可查询{cn}支付的预计退款到账时间。|区分商家发出与顾客收到。{scope}的退款可能随支付机构处理时间变化。|{en} refund ETA
{en} Reconciliation|{hk}收款對賬|{cn}收款对账|按交易、退款和结算记录核对{scope}所得净额的过程。 EN: Matching sales, refunds and settlement entries to explain the net payout from {english} payments.|直接用{cn}的支付成功截图替代入账记录。|Reconcile {english} orders against the payout report before closing your books.|入賬前，請用結算報表核對{hk}訂單。|请用结算报表核对{cn}订单后再完成记账。|对账时统一{scope}订单时间与结算日期的口径，把退款和手续费分列。|{en} settlement matching
""", ("商户后台", "支付服务官网")),
    (
        """
Personal Loan|私人貸款|个人贷款|用于个人支出的贷款
Car Loan|汽車貸款|汽车贷款|用于购车的融资
Home Loan|住宅按揭|住房贷款|用于购置住房的借款
Education Loan|進修貸款|教育贷款|用于约定教育开支的贷款
Business Loan|商業貸款|企业贷款|用于企业经营的借款
Debt Consolidation Loan|結餘轉戶貸款|债务整合贷款|整合约定既有欠款的借款
Equipment Loan|設備貸款|设备贷款|用于购置设备的融资
""",
        """
{en} APR|{hk}實際年利率|{cn}年化综合成本|用年度口径呈现{scope}的借贷成本，计算包含哪些费用取决于披露标准。 EN: The annual percentage rate for the {english}, calculated under the applicable rules for including interest and fees.|{cn}月费率看起来低，总成本就一定低。|Compare the APR and total repayment for this {english} before applying.|申請{hk}前，請比較實際年利率同總還款額。|申请{cn}前，请比较年化综合成本和还款总额。|APR 不等于简单的名义利率。对{scope}应明确费用范围、适用条件和报价口径。|{en} annual percentage rate
{en} Repayment Schedule|{hk}還款時間表|{cn}还款计划表|列明{scope}每期应还款额、还款日及期数的安排。 EN: The due dates, amounts and number of instalments for the {english}.|{cn}展示首期金额就代表之后每期金额都一样。|Review each instalment in the repayment schedule for your {english}.|請查看{hk}還款時間表上每期嘅還款日同金額。|请查看{cn}还款计划表中每期的还款日期和金额。|对于{scope}，如首末期、浮动利率期或尾款金额不同，应逐项列清。|{en} amortisation schedule
{en} Origination Fee|{hk}開辦手續費|{cn}贷款办理费|安排{scope}时按条款收取的费用，可能单收、从放款扣除或计入贷款。 EN: An upfront charge for arranging the {english}, payable separately or included in the loan calculation.|{cn}办理费不单独扣账，所以相当于免费。|Check how the origination fee for your {english} affects the amount you receive.|請查閱{hk}開辦手續費點樣扣除，核對實收貸款額。|请查看{cn}办理费的收取方式，并核对实际到账金额。|对{scope}同时列出借款额、到手金额和收费方式，避免把费用隐藏在净放款里。|{en} arrangement fee
{en} Early Repayment Charge|{hk}提早還款費用|{cn}提前还款费用|在原定到期前归还{scope}的全部或部分款项时可能产生的费用。 EN: A possible fee for paying part or all of the {english} ahead of schedule.|只要提前结清{cn}，就一定没有额外费用。|Request an early repayment quote for your {english} before paying it off.|清還{hk}前，請先索取提早還款報價。|提前结清{cn}前，请先查询应还金额和提前还款费用。|交代{scope}的部分还款与全额结清是否采用不同费用，别把报价当永久固定。|{en} prepayment fee
{en} Late Payment Charge|{hk}逾期還款收費|{cn}逾期还款费用|未在约定日偿还{scope}应付款项时，按条款可能产生的额外收费。 EN: A charge that may apply when a scheduled payment on the {english} is overdue.|{cn}晚几天还不影响费用，也不用查看条款。|Check the late payment charge for your {english} if you may miss a repayment.|如未能依期還款，請查閱{hk}逾期收費安排。|如可能错过还款日，请先查看{cn}的逾期还款费用。|对{scope}应区分逾期费用与逾期利息，并提供及时查询或联系的入口。|{en} late fee
""", ("银行官网", "贷款详情页")),
    (
        """
Regular Savings|普通儲蓄|普通储蓄|常规活期储蓄账户
Online Savings|網上儲蓄|线上储蓄|通过线上渠道开立或管理的储蓄账户
Foreign-Currency Savings|外幣儲蓄|外币储蓄|以指定外币计价的储蓄账户
Fixed Deposit|定期存款|定期存款|有约定存期的存款
Notice Deposit|通知存款|通知存款|支取前需提前通知的存款
Junior Savings|兒童儲蓄|少儿储蓄|为未成年人设置的储蓄账户
Business Savings|商業儲蓄|企业储蓄|为企业开立的储蓄账户
Bonus Savings|額外息率儲蓄|加息储蓄|符合特定行为或余额要求时有额外利率的储蓄安排
""",
        """
{en} Rate|{hk}利率|{cn}利率|计算{scope}利息所用的利率，可能按余额、期限、币种或活动条件分档。 EN: The rate used to calculate interest on {english}, which may vary by balance, term, currency or promotional tier.|所有{cn}余额不论条件都享页面展示的最高利率。|See which {english} rate applies to your balance and term.|查閱你嘅結餘同存期適用邊個{hk}利率。|请查看对应余额和存期适用的{cn}利率。|如{scope}有分档利率，建议以实际存入金额展示适用利率及适用期间。|{en} interest rate
{en} Minimum Deposit|{hk}最低存款額|{cn}最低存入金额|开立或享用{scope}时可能要求达到的起存金额。 EN: The starting balance required to open or qualify for {english}.|{cn}开户无需存款，所以任何余额都能享活动利率。|Check the minimum deposit for {english} before funding the account.|入數前，請查閱{hk}嘅最低存款額。|存入前，请查看{cn}的最低存入金额。|分清{scope}的开户要求、起存金额和享息门槛，币种不得省略。|{en} opening deposit
{en} Withdrawal Conditions|{hk}提款條件|{cn}支取条件|从{scope}提取款项时需留意的通知、额度、期限或利息调整条件。 EN: The notice, amount limits, timing and interest consequences that apply to withdrawals from {english}.|{cn}的资金可随时提取，任何利息都不受影响。|Review the withdrawal conditions for {english} before moving your funds.|調動資金前，先睇清楚{hk}提款條件。|转出资金前，请先查看{cn}的支取条件。|「提款／支取」比「资金随用」明确；涉及{scope}的提前支取应另说明计息规则。|{en} withdrawal terms
{en} Interest Credit|{hk}利息入賬|{cn}利息到账|按计算周期把{scope}产生的利息记入约定账户。 EN: The posting of interest earned on {english} to the agreed account at the end of the calculation period.|{cn}每日计息就代表利息每天都可提取。|Check when interest from {english} is credited to your account.|查閱{hk}利息幾時會存入戶口。|请查看{cn}利息何时计入账户。|{scope}的起息、结息与入账日期可能不同，按实际到账规则写清。|{en} interest posting
""", ("银行 App", "存款详情页")),
    (
        """
Current Account|往來戶口|活期结算账户|用于日常收付的银行账户
Payroll Account|出糧戶口|工资账户|用于接收工资的银行账户
Multi-Currency Account|多種貨幣戶口|多币种账户|可管理多种货币余额的账户
Student Account|學生戶口|学生账户|面向合资格学生的账户
Merchant Account|商戶戶口|商户账户|用于商户收款或结算的账户
Business Transaction Account|企業往來戶口|企业结算账户|用于企业日常结算的账户
Joint Account|聯名戶口|联名账户|由多名账户持有人共同开立的账户
""",
        """
{en} Eligibility|{hk}開立資格|{cn}开户资格|申请{scope}时需符合的客户类型、身份和其他条件。 EN: The identity, customer type and other criteria an applicant must meet to open a {english}.|谁都可以开立{cn}，不用核实身份。|Check whether you are eligible for a {english} before starting your application.|提交申請前，請先查閱{hk}開立資格。|提交申请前，请先查看{cn}开户资格。|面对申请人列出{scope}的适用对象和所需材料，勿将初步符合写成审批通过。|{en} application eligibility
{en} Application Documents|{hk}開戶所需文件|{cn}开户申请材料|开立{scope}时需要提交的身份、地址、业务或其他证明材料。 EN: The identity, address or business documents needed to open a {english}.|申请{cn}，直接发身份证照片到任意客服聊天窗口。|Use the official upload page to submit the documents requested for your {english}.|請透過官方上載頁面提交{hk}所需文件。|请通过官方上传入口提交{cn}所需申请材料。|香港常写「文件／上載」，内地写「材料／上传」。{scope}资料应走安全渠道。|{en} opening checklist
{en} Monthly Fee|{hk}每月戶口費|{cn}账户月费|按月为维护{scope}收取的费用，可能有符合条件的减免。 EN: A recurring monthly charge for maintaining a {english}, sometimes waived when account conditions are met.|{cn}不收开户费，就代表所有账户服务永久免费。|Check the monthly fee and any waiver conditions for your {english}.|查閱{hk}每月收費，留意有冇豁免條件。|查看{cn}账户月费及适用的减免条件。|费用为零时要说明期限及原因。{scope}如另有跨境交易等收费，不宜笼统写全免。|{en} maintenance fee
{en} Closure|結束{hk}|{cn}销户|终止使用{scope}，通常需先处理余额、在途交易和关联指令。 EN: The process of closing a {english} after settling the remaining balance, pending transactions and linked instructions.|卸载应用就等于注销{cn}。|Before closing your {english}, check for outstanding payments and remaining funds.|結束{hk}前，請先處理未完成付款同戶口餘額。|办理{cn}销户前，请先处理在途款项和账户余额。|港版「結束戶口」，内地「销户」。{scope}如需多方确认，应在流程前告知。|Close {en}
""", ("银行 App", "账户申请页")),
)
