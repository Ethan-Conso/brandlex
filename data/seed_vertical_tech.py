"""Consumer technology phrases grounded in feature and device contexts."""

from data.seed_vertical_matrix import editorial_terms, matrix_terms


CATEGORY = "数码与科技"
PRODUCT = ("品牌官网", "京东", "YouTube")
SOCIAL = ("IG", "小红书", "YouTube")
GAME = ("Steam", "YouTube", "小红书")

ANCHORS = """
On-Device AI|裝置端 AI|端侧 AI|local AI inference;本機AI;端侧推理|在装置上执行部分 AI 任务。是否离线、支持哪些任务，要按实际功能说明。|「本地 AI 绝不接触网络。」——不同功能的数据处理路径可以不同。|This transcription feature processes recordings on the device on supported models.|指定型號支援在裝置端處理錄音轉寫。|支持的机型可在端侧完成录音转写。|香港可写「裝置端」，内地常用「端侧」。分别核对联网和数据上传要求。|AI processing that takes place on the user's device. The tasks supported and whether they work offline depend on the product.
Over-the-Air Update|無線更新|OTA 升级|OTA update;韌體無線更新;空中下载升级|通过网络下载并安装软件或固件，不需要线缆连电脑。|「以后全部功能都能自动升级。」——功能与支持周期不能由更新机制推断。|Install the wireless update to get the camera fixes listed in the release notes.|安裝無線更新，即可套用版本說明所列嘅相機修正。|安装 OTA 升级，获取版本说明里列出的相机修复。|港台常说「無線更新」，内地常说「OTA」。写明更新内容、机型及推送节奏。|A software or firmware update downloaded and installed over a network without connecting the device to a computer by cable.
Image Sensor|影像感應器|图像传感器|camera imaging sensor;感光元件;影像传感器|把光转换成电信号的部件，是相机成像系统的一部分。|「感应器越大，所有照片一定越好。」——镜头、光线和处理算法也有影响。|Compare the sensor specifications alongside the lens and sample images.|比較影像感應器規格時，不妨一併參考鏡頭同實拍相片。|对比图像传感器时，可以一起看镜头和实拍样张。|港繁用「感應器」，内地用「传感器」。尺寸写法以规格为准。|A camera component that converts incoming light into electrical signals used to produce an image.
Variable Refresh Rate|可變更新頻率|可变刷新率|VRR display timing;可變刷新率;自适应刷新率|显示刷新节奏可依输入帧率或内容调整。不同协议和范围不能互相替代。|「开启可变刷新率就能把所有游戏帧率翻倍。」——它协调显示刷新与输入帧。|Enable variable refresh rate on compatible devices to match the display to game output.|喺兼容裝置開啟可變更新頻率，令畫面更新配合遊戲輸出。|兼容设备开启可变刷新率后，屏幕可配合游戏输出节奏。|港繁「更新頻率」、内地「刷新率」。标明支持范围、端口和设备要求。|Display operation that changes how often the screen refreshes to match incoming frames within a supported range.
Optical Image Stabilisation|光學影像防震|光学防抖|optical image stabilization;OIS camera;光學防手震|通过移动光学元件或感光组件减小手抖影响。效果随场景与模式而变。|「开光学防抖就永远没有动态模糊。」——主体运动仍会影响成像。|Optical stabilisation helps steady handheld shots in compatible modes.|指定拍攝模式支援光學影像防震，手持拍攝更易保持穩定。|兼容模式支持光学防抖，手持拍摄更容易拍稳。|港繁可见「防震／防手震」，内地「防抖」。不要与电子防抖混用。|Camera hardware that moves lens elements or the sensor to compensate for some camera shake.
Active Noise Cancellation|主動消噪|主动降噪|active noise cancelling;ANC audio;主動降噪|使用麦克风和信号处理减弱部分外界声音，效果受环境、佩戴和频段影响。|「戴上后外界所有声音完全消失。」——消噪效果并非全频绝对隔绝。|Switch on active noise cancellation to soften steady train noise on the commute.|通勤時開啟主動消噪，減少列車運行聲嘅干擾。|通勤打开主动降噪，减轻列车持续噪声的干扰。|可写典型低频背景声，不说完全静音。香港也常用「主動降噪」。|A system that uses microphones and audio processing to reduce some external noise. Its effect depends on sound frequency, fit and surroundings.
Transparency Mode|通透模式|通透模式|ambient sound mode;環境聲模式;环境音模式|把环境声音适度传进耳机，让佩戴者在需要时留意周围。|「通透模式保证过马路绝对安全。」——功能不能代替留心交通。|Turn on transparency mode when you want to hear a café announcement without removing your earbuds.|想聽清咖啡店叫號，可開通透模式，唔使除低耳機。|想听清咖啡店叫号，可以打开通透模式，不必摘下耳机。|不同品牌也叫环境声模式。不要用安全保证推广。|A headphone mode that plays back some outside sound so the wearer can hear their surroundings.
Spatial Audio|空間音訊|空间音频|spatial sound;空間聲效;沉浸式空间声|通过音频处理营造具有方向或包围感的听觉体验，支持情况依内容与设备而异。|「所有音源都支持动态头部追踪。」——空间效果和头部追踪是不同功能。|Try a compatible track to hear how spatial audio places instruments around you.|播放支援曲目，感受空間音訊帶來嘅樂器方位。|用支持的曲目试听空间音频，感受乐器分布的位置。|香港「音訊」、内地「音频」。应列出音源、设备和头部追踪要求。|Audio processing that makes sound seem to come from different directions or surround the listener. Support depends on the content and device.
Battery Life|電池使用時間|续航时间|battery runtime;電量續航;电池续航|一次充电可运行的时间，取决于亮度、联网、负载和电池状况。|「只要开机就保证跟测试条件一样耐用。」——不同用法会改变时长。|Check the battery-life estimate for video playback and everyday browsing separately.|睇電池使用時間時，可分開比較影片播放同日常瀏覽。|比较续航时，可以分别看视频播放和日常浏览的估算。|港繁常写「電池使用時間」，内地可简写「续航」。公布时附测试条件。|How long a device runs on one charge under stated conditions, such as screen brightness, connectivity and workload.
Peak Brightness|峰值亮度|峰值亮度|peak luminance;峰值光度;屏幕峰值亮度|特定条件下达到的最高显示亮度，不等于全屏持续亮度。|「峰值亮度适用于整块屏幕的每个画面。」——显示测试条件可能只覆盖局部。|Peak brightness applies under the display conditions stated in the specifications.|峰值亮度以規格所列嘅顯示條件為準。|峰值亮度只在规格页所列条件下适用。|分开写典型、全屏、户外与局部 HDR 峰值。|The highest brightness a screen reaches under specified conditions, which can differ from its sustained full-screen brightness.
Wi-Fi Backhaul|Wi-Fi 回程連線|Wi-Fi 无线回程|wireless mesh backhaul;無線回程;组网回程|网状网络节点用无线链路交换数据，实际速度受距离和干扰影响。|「无线回程永远和网线一样快。」——网络条件不同。|Place the mesh node where its wireless backhaul has a strong signal.|將網狀網絡節點放喺無線回程訊號夠強嘅位置。|把组网节点放在无线回程信号较强的位置。|香港常说「網絡」，内地「网络」，区分回程和客户端连接。|The wireless link that carries traffic between mesh Wi-Fi nodes. Distance and interference affect its speed.
Fast Charging|快速充電|快充|quick charging;高速充電;快速充电|在兼容设备和配件间以较高功率充电，峰值不等于全程功率。|「任何充电器都会以同样速度快充。」——协议、线材、温度和电量都有影响。|Use a compatible adapter and cable to enable fast charging.|使用兼容火牛同充電線，即可啟用快速充電。|搭配兼容充电器和线材，才能启用快充。|香港可用「快速充電」，内地多说「快充」。宣传功率时说明兼容组合。|Charging at higher power with compatible hardware. Actual power can vary over a charging session.
Foldable Display|摺疊式屏幕|折叠屏|foldable screen;摺屏;折叠显示屏|可随铰链折合的显示屏。折痕、防护及耐久数据应以实际产品为准。|「折叠屏没有任何使用限制。」——材质和使用指引仍重要。|Unfold the display for maps and documents, then fold it away for the commute.|打開摺疊式屏幕睇地圖同文件，通勤時再摺好收起。|展开折叠屏查看地图和文件，通勤时折好收起来。|港繁常写「摺疊」，内地「折叠」。不承诺无折痕或无限折叠。|A flexible screen designed to fold as a hinged device opens or closes. The crease, protection and durability vary by model.
Firmware Support Period|韌體支援年期|固件支持期限|firmware lifecycle;安全更新支援期;固件维护周期|厂商预计为设备提供指定固件或安全更新的时间。|「仍能用就代表还有安全更新。」——可使用与仍受维护不同。|Check the firmware support period before buying a device for long-term use.|計劃長期使用，選購前先睇清韌體支援年期。|计划长期使用，买之前先确认固件支持期限。|香港「韌體」，内地「固件」。更新时间计算起点和覆盖项目须明确。|The period for which a manufacturer plans to provide specified firmware or security updates for a device.
Trade-In Credit|以舊換新折抵額|以旧换新抵扣额|device trade-in value;舊機回贈;旧机抵扣|回收旧设备后用于购买或按规则发放的抵扣额，通常根据估价及验机确定。|「任何旧机都保证按最高价抵扣。」——抵扣金额依资格和验机。|Get an estimate for your old phone, then confirm the trade-in credit after inspection.|先估舊機價，驗機後確認以舊換新折抵額。|先给旧手机估价，验机后确认以旧换新的抵扣额。|核对回赠形式、机型限制和最终金额确认条件。|An amount applied to a purchase or issued under a trade-in programme when an eligible used device is accepted. Its value depends on appraisal and condition.
"""

DISPLAY = """
OLED|OLED|OLED|Organic LED|以自发光像素显示，表现还受调校与使用场景影响。|「{}绝无任何老化。」——应以保养与质保条款为准。|不要将面板技术与亮度、寿命等具体数值等同。|phone laptop monitor|{product} that produces images with self-emitting pixels rather than a separate backlight.
Mini-LED|Mini-LED 背光|Mini-LED 背光|Mini LED Backlit|使用小型 LED 作液晶背光，具体控光分区与型号有关。|「{}每一个像素都是独立发光。」——Mini-LED 背光与 OLED 不同。|将背光技术和液晶面板结构写清楚。|laptop monitor tv|{product} that uses a backlight made up of small LEDs. The number of dimming zones varies by model.
High-Refresh-Rate|高更新頻率|高刷新率|High Refresh|可在指定模式以较高频率更新画面，输入也须配合。|「{}会自动提升所有游戏的实际帧率。」——显示刷新和渲染帧率有区别。|附最高频率对应解像度、接口和模式。|phone laptop monitor|{product} that can refresh the picture more frequently in supported modes. The input device or content must also support the rate.
Adaptive-Refresh|自適應更新頻率|自适应刷新率|Adaptive Refresh Rate|刷新频率可随内容或输入信号变化，范围以设备为准。|「{}所有应用可用同样的刷新范围。」——可能有应用、端口或省电限制。|香港「更新頻率」，内地「刷新率」。|phone laptop monitor|{product} that adjusts its refresh rate to suit the content or input signal within a supported range.
Anti-Glare|防眩光|防眩光|Reduced Reflection|通过表面处理减弱部分反光，不能保证任何角度完全无反光。|「{}在任何太阳直射角度都看得清。」——效果受光线与亮度影响。|防眩光不等于防反射涂层规格，按厂方说明。|laptop monitor tv|{product} with a surface treatment that reduces some reflections.
HDR|HDR 高動態範圍|HDR 高动态范围|High Dynamic Range|支持显示较宽明暗范围的相容内容，表现依面板和格式而异。|「{}会把所有旧片变成原生 HDR。」——原生格式和增强处理不同。|写明格式、亮度测试与输入要求。|phone monitor tv|{product} that can show compatible high-dynamic-range content. The visible range of highlights and shadows depends on the panel and format.
Wide-Colour-Gamut|廣色域|广色域|Wide Color Gamut|表示覆盖较广的色域，实际范围须标明参照标准。|「{}保证每种颜色都完全准确。」——色域宽和色准不同。|分别列色域覆盖与色彩校准数据。|phone laptop monitor|{product} that covers a broad range of colours, measured against a named colour standard.
Matte|霧面|雾面|Matte Panel|表面呈较低镜面反射的观感，颗粒感依涂层而异。|「{}完全不会有光线反射。」——雾面以散射等方式改变反光。|港繁常用「霧面」，内地也称「磨砂屏」。|laptop monitor tv|{product} with a low-reflection surface finish. Its visible texture depends on the coating.
Touch-Enabled|觸控|触控|Touchscreen|支持在屏幕上直接操作，触点、手写笔和手势支持按规格。|「{}兼容所有手写笔。」——触控与笔协议不是一回事。|区别手指触控、被动笔和主动笔。|phone laptop monitor|{product} with direct touch input. Support for multiple touches, a stylus and specific gestures varies by model.
Edge-to-Edge|窄邊框|窄边框|Near-Bezel-Less|强调边框较窄的观感，并非没有任何边缘。|「{}外壳与显示之间绝对零边框。」——边框仍可存在。|若使用全面屏或屏占比，核对测量口径。|phone laptop monitor|{product} designed with narrow bezels so the image fills more of the device's front surface.
"""
DISPLAY_FORMS = """
phone|{} Smartphone Display|{}手機屏幕|{}手机屏幕|比较手机显示观感|Try the {} with your usual videos and apps before settling on a brightness setting.|用平日睇開嘅影片同應用程式試{}，再揀適合嘅亮度。|用常看的视频和应用试试{}，再调到适合的亮度。|手机显示表现可随环境光和省电模式变化。|a smartphone display
laptop|{} Laptop Display|{}手提電腦屏幕|{}笔记本屏幕|选购笔记本的显示规格|View a document and a photo side by side on the {} to compare the settings.|喺{}並排睇文件同相片，比較唔同顯示設定。|在{}上并排打开文档和照片，对比显示设置。|香港「手提電腦」，内地「笔记本」。|a laptop display
monitor|{} Monitor|{}顯示器|{}显示器|选购外接显示器的图像表现|Check how your device connects to the {} and which display settings the input supports.|連接{}前，確認接駁方法同輸入支援嘅顯示設定。|连接{}之前，先看接口支持哪些显示设置。|注明同一模式下的解像度和刷新率。|a monitor
tv|{} TV|{}電視|{}电视|按观看环境挑选电视|Compare the {} with a familiar scene in both daylight and low light.|用熟悉嘅畫面，分別喺日光同昏暗環境試睇{}。|用熟悉的画面，在明亮和较暗的环境各试一次{}。|使用同一信号源比较画质。|a TV
"""

AUDIO = """
Noise-Cancelling|主動消噪|主动降噪|Active Noise Cancelling|主动处理可减弱某些外界噪声，实际效果因声音种类而异。|「{}戴上后所有声音都消失。」——消噪不是绝对静音。|注明主动消噪适用场景与佩戴要求。|headphones earbuds headset|{product} with active processing to reduce some surrounding noise. The effect varies by type of sound.
Open-Ear|開放式|开放式|Open Ear|让耳道保持开放，听者能较容易听见部分周围声音。|「{}可完全保证外出安全。」——听见环境不等于绝对安全。|区分开放式、开放背板与骨传导。|headphones earbuds headset|{product} that leaves the ear canal open so the listener can hear more of their surroundings.
Wireless|無線|无线|Cordless Audio|音频信号通过无线方式传送，连接协议以规格为准。|「{}无线就是无需充电。」——多数无线设备仍需供电。|写明蓝牙或专用接收器，别只写无线。|headphones earbuds headset|{product} that receives audio without a cable between it and the source device. Check the supported wireless protocol.
Low-Latency|低延遲|低延迟|Reduced Audio Lag|着重减短画面或操作与出声之间的时间差。|「{}所有设备永远零延迟。」——延迟受接收端、编码与模式影响。|若有毫秒数据，附模式和测试环境。|headphones earbuds headset|{product} designed to shorten the delay between on-screen action or input and the sound the listener hears.
Multipoint|多點連接|多设备连接|Bluetooth Multipoint|可保持连接多台兼容设备，实际切换与数量依产品。|「{}可以同时混播任何设备的音频。」——多点连接不一定支持混音。|写明可配对和可同时连接的数量。|headphones earbuds headset|{product} that can maintain connections to more than one compatible source device. Switching behaviour varies by model.
Water-Resistant|抗水|防水溅|Water Resistance|在指定试验条件下有一定抗水能力。|「{}可以随意浸在水里。」——抗水能力有等级和时长。|分别核对耳机和充电盒的防护标示。|headphones earbuds headset|{product} designed to withstand water exposure under specified test conditions.
Sweat-Resistant|防汗|耐汗|Sweat Resistance|强调运动时对汗液的耐受表现，须按规格与清洁要求使用。|「{}防汗就等于可戴着游泳。」——防汗不等于浸水。|用运动场景示例，不套用游泳级文案。|headphones earbuds headset|{product} designed to withstand sweat during exercise under the stated use and cleaning conditions.
Lightweight|輕身|轻量|Light Fit|强调重量较轻，舒适感还受压力、形状及佩戴时间影响。|「{}再长时间佩戴都不可能夹耳。」——佩戴感因人而异。|建议给净重与测量是否含盒。|headphones earbuds headset|{product} designed to weigh relatively little. Fit, pressure and wear time also affect comfort.
Bass-Boost|低音增強|低音增强|Bass Boost Mode|强调低频调校或模式，声音偏好由听者决定。|「{}低音加重就能修复所有音源。」——调音不能补全原始录音。|写清是预设模式还是默认调音。|headphones earbuds headset|{product} tuned to emphasise bass frequencies or equipped with a mode that does so.
Voice-Assistant-Compatible|支援語音助理|支持语音助手|Voice Assistant Support|可通过兼容设备呼出指定语音助理，支持情况依系统和地区。|「{}能直接运行任意语音助理。」——可能需配对手机及网络。|列明系统、应用、语言及地区要求。|headphones earbuds headset|{product} that can invoke a supported voice assistant through a compatible device. Availability varies by system and region.
USB-C-Rechargeable|USB-C 充電|USB-C 充电|USB-C Charging Audio|通过 USB-C 接口充电，是否支持音频或快充要另核对。|「{}有 USB-C 就能接所有数字音频。」——充电口不一定传音频。|区分充电线和音频线。|headphones earbuds headset|{product} that recharges through a USB-C port. Audio and fast-charging support are separate specifications.
Custom-EQ|自訂等化器|自定义均衡器|Adjustable Equalizer|允许在指定软件中改变频段音量或套用预设。|「{}均衡器一调就能输出无损音频。」——调校不改变音源压缩方式。|说明所需应用和可调整的频段。|headphones earbuds headset|{product} that lets the listener adjust frequency levels or apply sound presets in supported software.
"""
AUDIO_FORMS = """
headphones|{} Headphones|{}頭戴式耳機|{}头戴式耳机|选购头戴式耳机的佩戴与听音功能|Try the {} with a familiar track and check how the headband sits.|用熟悉曲目試聽{}，同時感受頭帶貼合度。|用熟悉的歌试听{}，顺便感受头梁贴合度。|区分头戴佩戴方式和音频连接方式。|a pair of headphones
earbuds|{} Earbuds|{}耳塞式耳機|{}耳塞式耳机|挑选随身耳机的功能与佩戴方式|Wear the {} for a short walk and see how they sit as you move.|戴住{}行一陣，感受走動時嘅貼合度。|戴{}走一小段路，感受走动时稳不稳。|耳塞式与入耳式按具体结构说明。|a pair of earbuds
headset|{} Headset|{}通話耳機|{}通话耳麦|选购兼顾收听及麦克风通话的耳机|Make a short test call with the {} to check your microphone and audio settings.|用{}試打一個短電話，檢查咪高峰同音訊設定。|用{}打一通测试电话，检查麦克风和音频设置。|区分耳机听感和对方收到的收音效果。|a headset
"""

PERIPHERALS = """
Wireless|無線|无线|Cordless|不需经数据线连接主设备，可能通过蓝牙或接收器使用。|「{}绝不需要任何电源。」——无线设备仍需供电。|列出连接和供电方式。|keyboard mouse controller|{product} that sends input to a host without a data cable, often through Bluetooth or a dedicated receiver.
Bluetooth|藍牙|蓝牙|Bluetooth-Enabled|可与兼容的蓝牙主机配对，支持功能依系统而异。|「{}可以配对任意主机并使用全部功能。」——兼容性需要核对。|写明系统、配对模式和需要额外软件的功能。|keyboard mouse controller|{product} that pairs with compatible hosts via Bluetooth. Supported functions depend on the system.
Wired|有線|有线|Cable-Connected|通过线缆与主机传输操作，供电与端口以规格为准。|「{}任意线材都能通用。」——连接头和协议各有要求。|给端口种类及是否附转接头。|keyboard mouse controller|{product} that sends input through a cable. Check the power and port requirements for the host device.
Rechargeable|可充電|可充电|Built-In Rechargeable Battery|设备有可充电电池，续航随用法变化。|「{}充一次就终身不用再充。」——续航不是永久。|给充电接口、测试续航和是否可边充边用。|keyboard mouse controller|{product} powered by a battery that can be recharged. Running time varies with use.
Low-Latency|低延遲|低延迟|Fast Input Response|着重缩短操作与主机接收之间的时间差。|「{}能让所有游戏同步达到零延迟。」——整机链路并非只由配件决定。|写明测量模式，勿把回报率直接换成延迟。|keyboard mouse controller|{product} designed to minimise the delay between the user's action and the host receiving the input.
Multi-Device|多裝置切換|多设备切换|Multi-Host|支持切换已配对的多台设备，数量和方法依型号。|「{}可以同时控制任何数量的装置。」——多设备切换并非无限同时操作。|写明切换键、配对上限及系统要求。|keyboard mouse controller|{product} that can switch between paired devices. The number of devices and switching method vary by model.
Compact|纖巧|紧凑型|Compact Layout|强调尺寸较小，按键和握持空间可能有所取舍。|「{}尺寸小，但按键布局一定与标准版完全一样。」——布局应按实物。|提供尺寸与对照图，说明删减按键。|keyboard mouse controller|{product} with a relatively small footprint, sometimes with less room for keys or grip.
Travel-Friendly|方便攜帶|便携型|Travel-Ready|定位为外出易收纳和使用，便携性依重量与保护设计。|「{}放行李里就绝不会损坏。」——仍需妥善收纳。|可列尺寸、重量与是否附保护套。|keyboard mouse controller|{product} designed to pack and use away from a regular setup. Portability depends on its weight and protective design.
Programmable|可自訂按鍵|可编程按键|Remappable Controls|可改变部分键位或分配操作，支持内容依软件与平台。|「{}每个键都能在所有平台做任意宏。」——可配置范围有条件。|标明映射、宏功能和应用程序要求。|keyboard mouse controller|{product} with controls that can be reassigned or set to run supported actions, depending on the software and platform.
RGB-Lit|RGB 燈效|RGB 灯效|RGB Lighting|可显示多色灯光，分区、同步与电量影响要看型号。|「{}的灯光越亮性能越强。」——灯效不证明输入性能。|交代灯效可否关闭及同步条件。|keyboard mouse controller|{product} with multicolour lighting. The lighting zones, synchronisation and effect on battery life depend on the model.
Ergonomic|人體工學|人体工学|Ergonomic Design|轮廓着重支持较自然的操作姿态，舒适度与使用者有关。|「{}可治疗腕管问题。」——形态设计不能作疗效。|展示手型和握姿，不保证所有人舒适。|keyboard mouse controller|{product} shaped to support a more natural operating posture. Comfort depends on the user and fit.
Quiet-Click|靜音按鍵|静音按键|Quiet Switches|着重按压声较轻，响度和触感依结构变化。|「{}所有操作完全无声。」——静音设计并非绝对零声。|对比音量宜标同一距离与环境。|keyboard mouse controller|{product} designed to make less sound when its controls are pressed.
"""
PERIPHERAL_FORMS = """
keyboard|{} Keyboard|{}鍵盤|{}键盘|挑选文字输入或快捷键配件|Type a short paragraph on the {} to check the layout and feel.|用{}打段短文，感受鍵位同手感。|用{}打一小段文字，试试布局和手感。|键位区域和布局语言另标。|a keyboard
mouse|{} Mouse|{}滑鼠|{}鼠标|比较指针控制配件的连接和操作|Try the {} on your usual desk surface and check how the buttons fall under your fingers.|喺平日枱面試用{}，睇吓手指掂到按鍵嘅位置。|在平时的桌面上试用{}，看按键是否顺手。|香港「滑鼠」，内地「鼠标」。|a mouse
controller|{} Game Controller|{}遊戲手掣|{}游戏手柄|挑选适配游戏平台的操作手柄|Check compatibility, then test the {} in a game you already play.|先確認兼容性，再用熟悉嘅遊戲試{}。|先确认兼容平台，再用熟悉的游戏试{}。|香港「手掣」，内地「手柄」。|a game controller
"""

CAMERA = """
High-Resolution|高解像度|高分辨率|High Resolution Capture|突出照片或影片的分辨率，不能单独代表成像质量。|「{}不管光线都能拍清所有细节。」——噪声、镜头和曝光同样重要。|注明模式和输出尺寸，并用样张说明。|phone action mirrorless|{product} with a high pixel count in specified photo or video modes. Resolution is one factor in image quality.
Low-Light|低光拍攝|暗光拍摄|Low Light Capture|强调昏暗场景的成像方式或表现，效果与光线及主体运动有关。|「{}在全黑环境也能还原所有颜色。」——没有足够光线会影响成像。|低光样张宜标实际条件和曝光时间。|phone action mirrorless|{product} with features or modes for shooting in dim light. Results depend on the scene and subject movement.
Wide-Angle|廣角|广角|Wide Field of View|可容纳较宽场景，具体视角和变形依镜头及模式。|「{}拍任何人都绝不变形。」——视角和距离会影响边缘形变。|用等效焦距或视角说明，不只写超大。|phone action compact|{product} that captures a broad field of view. The lens and shooting mode affect coverage and distortion.
Electronic-Stabilisation|電子防震|电子防抖|Electronic Stabilization|软件根据画面或传感器信息减少抖动，部分模式会裁切画面。|「{}稳拍不需要任何裁切。」——需查具体模式。|分清电子防抖和光学防抖。|phone action mirrorless|{product} that uses image processing or sensor data to reduce visible shake. Some modes crop the frame.
Slow-Motion|慢動作|慢动作|High-Frame-Rate Capture|高帧率录制或处理后以较慢速度播放，支持条件依规格。|「{}所有分辨率都可以同等慢放。」——帧率常受分辨率限制。|注明原始帧率、导出帧率和可能裁切。|phone action mirrorless|{product} that captures or processes footage for slowed playback. Supported frame rates and resolutions vary.
Time-Lapse|縮時攝影|延时摄影|Interval Capture|按时间间隔记录并把画面汇为加速变化的影片。|「{}是把普通快门的照片延迟上传。」——这里指间隔拍摄。|港繁「縮時」，内地「延时」。说明间隔和稳定架设。|phone action mirrorless|{product} that captures frames at intervals and combines them into a video that shows change at a faster pace.
Raw-Capture|RAW 格式拍攝|RAW 格式拍摄|Raw Photo Mode|保留较多原始影像数据供后期处理，具体格式依设备。|「{}文件可在任何设备直接打开。」——软件和格式有要求。|列出实际格式并说明后期软件支持。|phone mirrorless compact|{product} that can save relatively unprocessed image data for later editing. The raw format varies by device.
Log-Video|Log 影片|Log 视频|Log Profile|使用对数曲线记录影像，为后期调色保留空间，须按实际规格使用。|「{}不经调色就一定更鲜艳。」——Log 预览常较平淡。|香港「影片」，内地「视频」。说明色彩配置与后期要求。|phone action mirrorless|{product} that records video using a logarithmic tone curve to retain flexibility in colour grading.
Weather-Sealed|防風雨密封|防滴防尘密封|Weather Sealing|使用密封结构减轻环境尘水侵入的风险，不等于可浸水。|「{}可以带去深水潜摄。」——防滴规格不支持浸水推断。|镜头和机身的防护条件都要核对。|action mirrorless compact|{product} built with seals to reduce the risk of dust or water ingress. Follow the stated exposure limits.
Subject-Tracking|主體追蹤|主体追踪|Subject Tracking AF|识别并跟随支持的主体，可能用于对焦或画面构图。|「{}所有运动对象都能稳定锁定。」——场景和主体类型会影响识别。|区分自动对焦追踪和智能构图追踪。|phone action mirrorless|{product} that can recognise and follow supported subjects for focusing, framing or both.
"""
CAMERA_FORMS = """
phone|{} Smartphone Camera|{}手機相機|{}手机相机|按拍摄功能比较手机相机|Test the {} in a familiar scene and save the original file for comparison.|用熟悉場景試拍{}，保留原檔作比較。|用熟悉的场景试拍{}，留好原文件再对比。|比较照片时标明主镜头或其他镜头。|a smartphone camera
action|{} Action Camera|{}運動相機|{}运动相机|按记录动作的条件选择便携相机|Try the {} on a short outing and review the footage before changing settings.|帶{}出門試拍一段，睇返片再調校設定。|带{}出门试拍一段，看回放再调设置。|安装、支架和防水壳要求另列。|an action camera
mirrorless|{} Mirrorless Camera|{}無反相機|{}微单相机|按功能与镜头组合选购无反相机|Pair the {} with a compatible lens and compare sample shots in the same light.|替{}裝上兼容鏡頭，喺同一光線下試拍比較。|给{}配上兼容镜头，在相同光线下对比样张。|香港「無反」，内地可写「无反／微单」，不暗示品牌。|a mirrorless camera
compact|{} Compact Camera|{}輕便相機|{}便携相机|按便携需求选购固定镜头或小型相机|Take the {} on a day out and check how its files fit your editing routine.|帶{}出遊一日，睇吓檔案是否配合你嘅修圖習慣。|带{}出去拍一天，看看文件是否好接进平时的修图流程。|说明机身尺寸、重量和镜头类型。|a compact camera
"""

WEARABLE = """
GPS-Enabled|GPS 定位|GPS 定位|Built-In GPS|用于记录支持的户外活动位置，是否独立定位要核对。|「{}在所有室内外场景定位都一样准。」——遮挡和设备模式会影响定位。|区别内置定位和依赖配对手机定位。|watch tracker sport|{product} that uses GPS to record supported outdoor activities. Check whether it needs a paired phone for location data.
Heart-Rate-Tracking|心率追蹤|心率监测|Heart Rate Monitoring|记录佩戴过程中的心率估算，用途和精度依设备。|「{}可确诊任何心律异常。」——日常追踪不能直接等同诊断。|用作日常记录，医疗用途只按获准范围介绍。|watch tracker sport|{product} that estimates and records heart rate during wear. Accuracy and supported uses depend on the device.
Blood-Oxygen-Tracking|血氧追蹤|血氧监测|SpO2 Monitoring|估算或记录血氧相关读数，支持模式和适用性依机型。|「{}能代替医生判断缺氧。」——消费级功能不可作诊断承诺。|标明地区可用性与使用说明，不夸大临床用途。|watch tracker ring|{product} that estimates or records blood oxygen readings. Supported modes and intended uses vary by model.
Skin-Temperature-Tracking|皮膚溫度追蹤|皮肤温度监测|Skin Temperature Sensing|记录佩戴位置的皮肤温度变化，不等于医用体温计。|「{}可直接判断是否发烧。」——皮肤读数与体温测量用途不同。|说明是趋势或绝对读数以及测量条件。|watch tracker ring|{product} that tracks temperature changes at the contact point on the skin, distinct from clinical body temperature measurements.
Sleep-Tracking|睡眠追蹤|睡眠监测|Sleep Monitoring|估算睡眠时段或相关趋势，实际取决于佩戴和算法。|「{}能确诊所有睡眠障碍。」——趋势记录不等于诊断。|可展示睡眠时间与趋势，区分医疗检查。|watch tracker ring|{product} that estimates sleep periods or trends based on sensor data and software.
Swim-Ready|適合游泳|支持游泳佩戴|Swim Compatible|在规格允许的条件下可游泳佩戴，运动记录功能另行确认。|「{}只要能游泳就能深潜。」——不同水下活动的限制不一样。|写清泳池、海泳及深度范围。|watch tracker sport|{product} designed for wear during swimming within the stated water-use limits. Check activity tracking separately.
Always-On|常亮顯示|息屏显示|Always-On Display|屏幕待机时可显示部分信息，开启后会影响电耗。|「{}常亮完全不耗电。」——待机显示也会使用电量。|列支持画面及省电限制，不暗示所有信息持续显示。|watch tracker sport|{product} that can keep selected information visible when the display is idle, with a possible effect on battery life.
Stress-Tracking|壓力指標追蹤|压力指标监测|Stress Trend Tracking|基于部分传感数据估算压力趋势，不用于评价心理疾病。|「{}能准确读出你每时每刻的情绪。」——估算指标不等同情绪检测。|说明指标的计算用途与局限。|watch tracker ring|{product} that estimates stress trends from sensor readings, for general wellness use.
"""
WEARABLE_FORMS = """
watch|{} Smartwatch|{}智能手錶|{}智能手表|按记录功能挑选智能腕表|Try the {} with its companion app to see how your daily trends are displayed.|試用{}同配套應用程式，睇清日常趨勢點樣顯示。|搭配配套应用试用{}，看看日常趋势怎么显示。|注明手机系统、地区与账户限制。|a smartwatch
tracker|{} Fitness Tracker|{}運動手環|{}运动手环|选择随身记录日常活动的手环|Wear the {} as instructed and review your weekly trends in the app.|按指引戴好{}，喺應用程式睇一星期嘅趨勢。|按说明戴好{}，在应用里看看一周趋势。|实测运动和日常追踪模式分别交代。|a fitness tracker
sport|{} Sports Watch|{}運動腕錶|{}运动手表|按运动场景挑选可穿戴设备|Set up the {} before training and check which activity modes are available.|訓練前先設定{}，睇清楚支援嘅運動模式。|训练前设置好{}，看看支持哪些运动模式。|运动模式可用性以型号和固件为准。|a sports watch
ring|{} Smart Ring|{}智能戒指|{}智能戒指|选购以手指佩戴的记录装置|Use the sizing kit for the {} before ordering, then pair it with the app.|訂購前用{}嘅量度套裝確認尺寸，到手後再配對應用程式。|先用{}的量圈工具确认尺码，到手再连接应用。|注意不同手指适用范围和尺码。|a smart ring
"""

CHARGING = """
USB-C|USB-C|USB-C|Type-C|通过 USB-C 接口连接，功率、数据与视频支持取决于规格。|「{}有 USB-C 就支持所有协议。」——接口外形相同不代表支持内容相同。|按说明列端口角色和每口上限。|wall car bank|{product} with a USB-C port. Supported power levels and other functions depend on the specification.
USB-PD|USB-PD 電力傳輸|USB-PD 快充协议|USB Power Delivery|兼容设备间可协商供电，具体功率档位依充电配件和线缆。|「{}接任何线都能跑满功率。」——线缆额定规格同样重要。|以实际支持的档位和连接组合写卖点。|wall car bank|{product} that uses USB Power Delivery to negotiate power with compatible devices and cables.
Fast-Charging|快速充電|快充|Quick Charge Capable|在兼容组合下以较高速度供电，实际速度随电量与温度变化。|「{}所有设备都能同样快充。」——不同设备协商规格不同。|列出兼容设备、线材和测试电量区间。|wall car bank|{product} that supplies higher charging power in compatible setups. Speed can vary with battery level and temperature.
Dual-Port|雙插口|双口|Two-Port Charging|提供两个输出口，同时使用时可重新分配功率。|「{}的两个口同时用都一直跑单口峰值。」——总功率通常有限。|给单口和双口的分配示意。|wall car bank|{product} with two output ports. Using both at once may change the power available from each port.
Multi-Port|多插口|多口|Multi-Output Charging|提供多个输出，可接不同设备；同时输出受总功率限制。|「{}每多插一台就凭空多出额定功率。」——供电有总上限。|说明口数、接口类型与功率分配。|wall car bank|{product} with multiple outputs for charging several devices within a shared power limit.
Compact|纖巧|小体积|Space-Saving Charger|强调外形较小，适合携带或空间有限处。|「{}越小温度就一定越低。」——温升由设计和功率决定。|给净重和外形尺寸。|wall car bank|{product} designed to take up little space for carrying or use in a tight area.
Magnetic-Wireless|磁吸無線|磁吸无线|Magnetic Wireless Charging|通过磁吸辅助对位进行无线充电，兼容条件看设备和配件。|「{}任何有磁铁的手机都能无线充电。」——磁吸不代表兼容充电。|查设备、手机壳、支架及认证要求。|bank dock stand|{product} that uses magnets to align compatible devices for wireless charging.
Foldable|可摺疊|折叠式|Folding Charger|部分结构可折合，方便收起或放入包内。|「{}可以随便折任何位置。」——只能按设计方向折合。|标明可折的是插脚、支架还是底座。|wall dock stand|{product} with a part that folds away for storage or transport.
Travel|旅行用|旅行便携|Travel Charging|针对外出收纳和供电使用，地区插座、电压及运输条件另行确认。|「{}可不查规则带去任何国家。」——电压、插头和运输要求各异。|提供地区适配资料，电池产品另查航空规定。|wall bank dock|{product} intended for portable use. Check local socket and voltage compatibility and applicable transport rules.
Wireless|無線|无线|Cordless Charging|无需设备与底座之间直接插线，底座本身通常仍需供电。|「{}不用接任何电源就能一直充。」——需确认底座供电。|注明协议、对位、壳厚及所需电源。|bank dock stand|{product} that transfers charging power without plugging a cable into the device being charged. The charger may still require a power cable.
"""
CHARGING_FORMS = """
wall|{} Wall Charger|{}插牆充電器|{}墙插充电器|比较市电插座充电配件|Check your socket and cable before packing the {} for a trip.|帶{}去旅行之前，先確認插座同線材。|旅行带上{}前，先确认插座和充电线。|港式口语可写「火牛」，规格页写完整名称。|a wall charger
car|{} Car Charger|{}車用充電器|{}车载充电器|根据车辆电源和接口选择充电配件|Check the vehicle's outlet and connect the {} only as directed.|先睇清車內電源插口，再按指引接駁{}。|先确认车辆电源接口，再按说明连接{}。|写明车辆供电适用条件。|a car charger
bank|{} Power Bank|{}流動充電器|{}充电宝|选购外出补电的便携电池|Charge the {} before heading out and bring a cable for your device if needed.|出門前替{}充滿電，有需要再帶裝置用嘅充電線。|出门前给{}充好电，按需要带上设备的充电线。|香港也称「尿袋」，正式页用「流動充電器」。容量与可输出电量不同。|a power bank
dock|{} Charging Dock|{}充電座|{}充电底座|在固定位置集中放置和补电|Set the {} on a stable surface and check which devices it supports.|將{}放喺穩固平面，確認支援邊款裝置。|把{}放在稳固平面上，再确认支持哪些设备。|说明同时可充的装置与适配器。|a charging dock
stand|{} Charging Stand|{}充電支架|{}充电支架|按观看角度与兼容性选择充电支架|Try your phone on the {} and check that charging continues at your chosen angle.|將手機放上{}，睇吓揀好角度後有冇繼續充電。|把手机放上{}，确认选好的角度能保持充电。|标注横竖放置及相机凸起兼容性。|a charging stand
"""

HOME = """
Matter-Compatible|支援 Matter|兼容 Matter|Matter Smart Home|符合相应兼容要求时可接入支持的智能家居生态，功能范围依类型。|「{}所有平台的功能完全一样。」——平台和设备类型支持范围可不同。|列明控制平台、控制器及配置要求。|plug bulb switch|{product} designed to join supported smart-home systems using Matter. The functions available depend on the device and ecosystem.
Wi-Fi-Enabled|支援 Wi-Fi|支持 Wi-Fi|Wi-Fi Connected|可接入兼容无线网络，频段、账号与联网要求以规格为准。|「{}放在任何房间都一定连得到。」——信号与墙体会影响连接。|明确配网频段，避免只写无需网关。|plug bulb camera|{product} that connects to a compatible wireless network. Check supported bands, account setup and internet requirements.
Voice-Controlled|語音控制|语音控制|Voice Command Compatible|可通过兼容语音助手发指令，支持语种和操作范围依平台。|「{}听得懂所有口音和语言。」——语种与识别条件有限。|列出支持的语音助手、地区和指令范围。|plug bulb switch|{product} that accepts commands through a compatible voice assistant. Supported languages and functions vary by platform.
Energy-Monitoring|用電量監測|用电量监测|Power Monitoring|可以记录接入设备的部分用电数据，精度和范围以说明为准。|「{}用电读数就是正式电费账单。」——设备数据用途不同于结算计量。|说明实时功率与累计用电量的显示区别。|plug switch strip|{product} that measures some electricity usage of connected equipment. Measurement scope and accuracy vary by model.
Scheduled-Control|定時控制|定时控制|Scheduled Automation|按预设时间启停或调节设备，执行条件依联网和系统设置。|「{}停电断网也保证照常执行。」——是否离线运行须确认。|注明时区和断网时的行为。|plug bulb switch|{product} that can start, stop or adjust its operation at set times, subject to network and system settings.
Remote-Controlled|遙距控制|远程控制|App Remote Control|可从其他位置用兼容方式操作，网络和账户权限可能影响功能。|「{}无论有没有网络都能在外面遥控。」——遥距控制通常有连接条件。|区分局域网控制与外网遥控。|plug bulb switch|{product} that can be operated from another location using a compatible app or controller, subject to connectivity and permissions.
Local-Control|本機控制|本地控制|Local Network Control|部分操作可在本地或局域网完成，离线支持应按实际核对。|「{}既然支持本地控制就绝不会上传数据。」——其他功能仍可能联网。|把本地功能、云端功能和数据路径分开写。|plug bulb switch|{product} with functions that can be operated on the device or over a local network. Check which functions work without internet access.
Multi-User|多人共用|多人共享|Shared Access|同一设备可按权限分享给其他账号，角色能力依系统。|「{}分享后每个人都必定有管理员权限。」——访问范围可配置。|介绍邀请、撤回和角色设置。|plug switch camera|{product} that can be shared with additional accounts. The actions each user can take depend on their assigned role.
"""
HOME_FORMS = """
plug|{} Smart Plug|{}智能插頭|{}智能插座|按控制方式挑选插接式智能电源|Set up the {} with a compatible lamp and check the rated load before use.|用兼容座枱燈設定{}，使用前先確認額定負載。|用兼容台灯设置{}，使用前先确认额定负载。|标明插头标准与电器适用范围。|a smart plug
bulb|{} Smart Bulb|{}智能燈膽|{}智能灯泡|按联网及控制需求挑选灯泡|Match the {} to your fitting, then try the controls in the room where it will be used.|為{}配對應燈座，再喺使用房間試吓控制。|给{}找好适配灯座，再在要用的房间试试控制。|灯头型号和调光兼容性按规格。|a smart bulb
switch|{} Smart Switch|{}智能開關掣|{}智能开关|在选购智能墙面开关时比较控制功能|Check the wiring requirements for the {} before arranging installation.|安排安裝前，先確認{}嘅接線要求。|安排安装前先看{}对接线的要求。|是否需要零线和安装资格应清楚说明。|a smart switch
camera|{} Smart Home Camera|{}智能家居鏡頭|{}家用智能摄像头|根据接入方式挑选家用监看设备|Before using the {}, check who can view footage and where it is stored.|使用{}前，先確認邊個可睇影片同影片存放位置。|用{}前，确认谁能看视频以及录像存在哪里。|监看范围、云存储和授权设置要明确。|a smart-home camera
strip|{} Smart Power Strip|{}智能拖板|{}智能排插|按插孔数量和用电能力选择智能延长插座|Check the total rated load of the {} and whether outlets are individually controlled.|先睇{}嘅總額定負載，同每個插位可否獨立控制。|先看{}的总额定负载，再确认插位能不能单独控制。|香港「拖板」，内地「排插」，不要把监测当防护。|a smart power strip
"""

STORAGE = """
Encrypted|加密|加密|Data Encryption|以加密方式保护资料，是否为硬件加密、如何解锁须按规格。|「{}丢了也绝不可能泄露。」——防护取决于密码、密钥与配置。|说明加密范围、密码恢复和使用前配置。|ssd flash nas|{product} that protects stored data with encryption. Check how it is implemented and how access is unlocked.
Password-Protected|密碼保護|密码保护|Passcode Protection|限制未授权访问，密码限制与完整磁盘加密不能直接等同。|「{}有密码就证明所有数据都已加密。」——需查看保护机制。|分开写访问密码、数据加密和账号权限。|ssd flash nas|{product} that limits access by requiring a password. Full-disk encryption is a separate feature.
USB-C|USB-C|USB-C|Type-C Data Port|使用 USB-C 接口，实际传输速率依线材、协议及主机。|「{}用了同样形状的插头就一定跑同样速度。」——端口外形不代表协议。|写明设备和线材支持，不把峰值当全程速度。|ssd flash reader|{product} with a USB-C connection. Transfer speed depends on the protocol, cable and host.
Shock-Resistant|抗震|抗震|Shock Resistance|结构针对特定震动或跌落条件设计，具体条件以试验为准。|「{}从任何高度跌落都不影响数据。」——防护测试存在范围。|注明高度、表面和是否通电的测试条件。|ssd flash reader|{product} designed to withstand specified impacts or vibrations. Check the tested conditions.
Portable|便攜|便携|Pocket-Sized Storage|方便外出携带，重量和所需线材按型号。|「{}便携就能在任何设备即插即用。」——系统、格式和电源可能有限制。|列尺寸、重量及连接附件。|ssd flash reader|{product} designed for carrying away from a fixed setup. Weight and cable requirements vary by model.
High-Speed|高速|高速|Fast Data Transfer|强调数据传输表现，实际速度依接口、文件和设备而异。|「{}所有文件都能一直跑标称峰值。」——大小和缓存会影响。|将顺序、随机及持续性能分开。|ssd flash reader|{product} designed for fast data transfer. Actual speed depends on the connection, files and host device.
Automatic-Backup|自動備份|自动备份|Scheduled Backup|通过内置或配套软件执行备份任务，范围与策略须设置。|「{}开启备份就不会再丢任何资料。」——需要核对覆盖和恢复方案。|写清所需应用、保留周期与恢复流程。|ssd flash nas|{product} that can back up specified data automatically after the backup settings are configured.
Rugged|強固防護|加固防护|Ruggedised Storage|针对较苛刻携带或使用环境设计，防护范围以实际等级。|「{}坚固所以浸水后也能随即通电。」——防护和操作限制仍须核对。|分开注明抗震、抗尘和抗水测试条件。|ssd flash reader|{product} built for more demanding conditions during use or transport. The tested protections are model-specific.
"""
STORAGE_FORMS = """
ssd|{} External SSD|{}外置固態硬碟|{}移动固态硬盘|按使用需求挑选外接固态存储|Test the {} with your usual project files and a compatible cable.|用平日嘅專案檔案同兼容線材試{}。|用平时的项目文件和兼容线材试试{}。|港繁「外置硬碟」，内地「移动硬盘」。|an external SSD
flash|{} USB Flash Drive|{}USB 手指|{}U盘|挑选插接式便携存储|Check the device format requirements before moving files to the {}.|將檔案搬去{}前，先確認裝置嘅格式要求。|把文件移到{}之前，先确认设备支持的格式。|港繁口语「手指」，规格页可写「USB 隨身碟」。|a USB flash drive
nas|{} Network Storage|{}網絡儲存裝置|{}网络存储设备|按访问与存储需求挑选联网存储|Set up user access on the {} before sharing a folder with others.|用{}分享資料夾前，先設定使用者權限。|用{}共享文件夹之前，先设置用户权限。|远程访问和同一局域网共享分别说明。|a network storage device
reader|{} Card Reader|{}讀卡器|{}读卡器|按卡种与传输要求选购读卡设备|Match the card and host connection before using the {} to import footage.|用{}匯入影片前，先確認記憶卡同主機接駁。|用{}导入视频之前，先核对存储卡和主机接口。|列实际支持的卡格式和速度等级。|a card reader
"""

GAMES = """
Cross-Platform|跨平台|跨平台|Cross-Play Enabled|允许不同平台在指定模式共同游玩，跨平台联机与存档同步不同。|「{}所有平台的存档和购买都能互通。」——联机、进度和购买互通要分别确认。|列出支持的模式、平台和版本。|party racing rpg|{product} that lets people on different supported platforms play together in selected modes. Progress syncing is a separate feature.
Local Co-op|本機合作|本地合作|Couch Co-op|在同一地点的设备上合作游玩，显示与人数限制依游戏。|「{}就是可以和全球玩家在线匹配。」——本地不等于联网。|注明同屏、分屏、手柄数及本地玩家人数。|party racing rpg|{product} with a cooperative mode for people playing in the same location. Screen and player limits vary by game.
Online Co-op|網上合作|在线合作|Network Co-op|通过网络与其他玩家共同进行指定任务或模式。|「{}支持全程任何剧情都能组队。」——合作内容可能受限制。|说明合作关卡、联机所需订阅与地区限制。|party racing rpg|{product} with missions or modes players can complete together over a network.
Controller-Friendly|手掣操作友善|适配手柄|Controller Support|界面或玩法支持兼容手柄，具体输入与按键映射依系统。|「{}所有型号手柄都可直接用。」——兼容性有范围。|注明是否全程用手柄，还是仍需键鼠。|party racing rpg|{product} whose gameplay or menus can be operated with a compatible controller. Button mappings may vary by system.
Free-to-Play|免費遊玩|免费游玩|Free Entry Game|可不支付基础购买费开始游玩，可能含付费内容。|「{}没有任何付费内容。」——免费入门不等于没有内购。|明示内购及付费道具，区分免费试玩。|party racing rpg|{product} that can be started without paying a base purchase price. Optional content or features may cost extra.
Early Access|搶先體驗|抢先体验|In-Development Release|在开发尚未结束时提前开放游戏版本，内容或表现仍可能变化。|「{}的路线图功能均已上线。」——计划内容不等于可玩内容。|分开写当前可玩内容和未来计划，不许诺未确定日期。|party racing rpg|{product} made playable while development is ongoing. Features and performance may change before the full release.
"""
GAME_FORMS = """
party|{} Party Game|{}派對遊戲|{}派对游戏|了解轻松多人游戏的参与方式|Invite a few friends to try a short round of the {} in a supported mode.|約幾位朋友，用支援模式試玩一局{}。|喊上几个朋友，在支持的模式里试一局{}。|写清最大人数和是否可临时加入。|a party game
racing|{} Racing Game|{}賽車遊戲|{}竞速游戏|了解竞速游戏的参与方式与支持模式|Start with a practice lap in the {} to get used to the handling.|喺{}先試跑一圈，熟習車輛操控。|先在{}里练一圈，熟悉车辆手感。|分开写休闲驾驶、竞速和赛事匹配模式。|a racing game
rpg|{} Action RPG|{}動作角色扮演遊戲|{}动作角色扮演游戏|按参与方式了解带角色成长的动作游戏|Try an early quest in the {} and see how its combat and progression fit together.|喺{}試玩初期任務，感受戰鬥同角色成長點樣配合。|在{}里试一段早期任务，看看战斗和角色成长怎么衔接。|说明联网支持是否覆盖主线及进度归属。|an action RPG
"""


def build_tech_terms():
    yield from editorial_terms(CATEGORY, PRODUCT, ANCHORS)
    for platforms, attributes, forms in (
        (PRODUCT, DISPLAY, DISPLAY_FORMS),
        (SOCIAL, AUDIO, AUDIO_FORMS),
        (PRODUCT, PERIPHERALS, PERIPHERAL_FORMS),
        (SOCIAL, CAMERA, CAMERA_FORMS),
        (SOCIAL, WEARABLE, WEARABLE_FORMS),
        (PRODUCT, CHARGING, CHARGING_FORMS),
        (PRODUCT, HOME, HOME_FORMS),
        (PRODUCT, STORAGE, STORAGE_FORMS),
        (GAME, GAMES, GAME_FORMS),
    ):
        yield from matrix_terms(CATEGORY, platforms, attributes, forms)
