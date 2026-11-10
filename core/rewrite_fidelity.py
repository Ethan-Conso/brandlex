"""Check explicit offer facts before showing model-generated marketing copy."""

from collections import Counter
from datetime import date
from decimal import Decimal
import re
import unicodedata

from core.rewrite_errors import RewriteFailure

_URL = re.compile(r"https?://[^\s<>\"`“”‘’「」『』，。；！？、：）】》]+", re.IGNORECASE)
_DIGITS = r"(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?:\.[0-9]+)?"
_HAN_DIGITS = {char: value for value, char in enumerate("零一二三四五六七八九")}
_HAN_DIGITS.update({"〇": 0, "兩": 2, "两": 2})
_HAN_UNITS = {"十": 10, "百": 100, "千": 1000, "萬": 10000, "万": 10000}
_HAN_NUMBER = r"[零〇一二兩两三四五六七八九廿十百千萬万]{1,16}(?:[點点][零〇一二兩两三四五六七八九]{1,8})?"
_EN_DIGITS = dict(zip(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
    "seventeen eighteen nineteen".split(), range(20),
))
_EN_DIGITS.update(zip("twenty thirty forty fifty sixty seventy eighty ninety".split(), range(20, 100, 10)))
_EN_ORDINALS = dict(zip(
    "first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth "
    "fifteenth sixteenth seventeenth eighteenth nineteenth twentieth".split(), range(1, 21),
))
_EN_ORDINALS.update({"thirtieth": 30, "fortieth": 40, "fiftieth": 50, "sixtieth": 60,
                     "seventieth": 70, "eightieth": 80, "ninetieth": 90})
_EN_UNITS = {"hundred": 100, "thousand": 1000, "million": 1000000}
_EN_CARDINAL = "(?:" + "|".join(sorted(_EN_DIGITS.keys() | _EN_UNITS.keys(), key=lambda s: (-len(s), s))) + ")"
_EN_ORDINAL = "(?:" + "|".join(sorted(_EN_ORDINALS, key=lambda s: (-len(s), s))) + ")"
_EN_NUMBER = rf"(?<![a-z]){_EN_CARDINAL}(?:(?:[ -]+(?:and[ -]+)?){_EN_CARDINAL}){{0,7}}(?![a-z])"
_EN_ORDINAL_DAY = rf"(?<![a-z])(?:{_EN_CARDINAL}[ -]+)?{_EN_ORDINAL}(?![a-z])"
_ORDINAL_DAY = rf"(?:[0-9]{{1,2}}(?:st|nd|rd|th)|{_EN_ORDINAL_DAY})"
_NUMBER = rf"(?:(?<![0-9])(?<![0-9]\.)(?!(?<=[0-9],)[0-9]{{3}}(?![0-9])){_DIGITS}(?![0-9])|{_HAN_NUMBER}|{_EN_NUMBER})"
_DAY = rf"(?:[0-9]{{1,2}}(?:st|nd|rd|th)?|{_HAN_NUMBER}|{_EN_ORDINAL_DAY}|{_EN_NUMBER})"
_MONTHS = {
    name: i for i, names in enumerate((
        ("january", "jan"), ("february", "feb"), ("march", "mar"), ("april", "apr"), ("may",),
        ("june", "jun"), ("july", "jul"), ("august", "aug"), ("september", "sept", "sep"),
        ("october", "oct"), ("november", "nov"), ("december", "dec"),
    ), 1) for name in names
}
_MONTH = r"(?<![a-z])(?:" + "|".join(_MONTHS) + r")(?![a-z])\.?"
_DASH = r"[-~〜至到]"
_DASHES = str.maketrans(dict.fromkeys("‐‑‒–—―−", "-"))
_EN_SPAN = rf"(?:{_DASH}|to\b|through\b|until\b|and\b)"
_ZH_YEAR = r"(?:(?P<y>[0-9]{4})\s*年\s*)?"
_EN_YEAR = r"(?:,?\s+(?P<y>[0-9]{4})(?![0-9]))?"
_DATE_RANGES = (
    re.compile(rf"{_ZH_YEAR}(?:(?P<m>{_NUMBER})\s*月\s*)?(?P<a>{_DAY})\s*[日號号]?\s*{_DASH}\s*"
               rf"(?:(?P<n>{_NUMBER})\s*月\s*)?(?P<b>{_DAY})\s*[日號号]"),
    re.compile(rf"(?P<m>{_MONTH})\s+(?P<a>{_DAY})\s*{_EN_SPAN}\s*(?:(?P<n>{_MONTH})\s+)?"
               rf"(?P<b>{_DAY})(?![a-z0-9]){_EN_YEAR}", re.ASCII),
    re.compile(rf"(?<![a-z0-9])(?P<a>{_DAY})\s*{_EN_SPAN}\s*(?P<b>{_DAY})\s+(?P<m>{_MONTH}){_EN_YEAR}", re.ASCII),
    re.compile(rf"(?<![a-z0-9])(?P<a>{_DAY})\s+(?P<m>{_MONTH})\s*{_EN_SPAN}\s*"
               rf"(?P<b>{_DAY})\s+(?P<n>{_MONTH}){_EN_YEAR}", re.ASCII),
    re.compile(rf"\b(?:from|between)\s+(?:the\s+)?(?P<a>{_ORDINAL_DAY})\s*{_EN_SPAN}\s*"
               rf"(?:the\s+)?(?P<b>{_ORDINAL_DAY})(?![a-z0-9])", re.ASCII),
)
_DATES = (
    re.compile(rf"{_ZH_YEAR}(?P<m>{_NUMBER})\s*月\s*(?P<d>{_DAY})\s*[日號号]"),
    re.compile(r"(?<![0-9])(?P<y>[0-9]{4})[-/](?P<m>[0-9]{1,2})[-/](?P<d>[0-9]{1,2})(?![0-9])"),
    re.compile(rf"(?P<m>{_MONTH})\s+(?:the\s+)?(?P<d>{_DAY})(?![a-z0-9]){_EN_YEAR}"),
    re.compile(rf"(?<![a-z0-9])(?P<d>{_DAY})\s+(?P<m>{_MONTH}){_EN_YEAR}"),
    re.compile(rf"(?P<d>{_DAY})\s*[日號号](?=\s*(?:起|止|截止|推出|[發发]售|開售|开售|上[線线市]|[開开]放|[結结]束))"),
    re.compile(rf"\bon\s+(?:the\s+)?(?P<d>{_ORDINAL_DAY})(?![a-z0-9])", re.ASCII),
)
_MONTH_ONLY = re.compile(
    rf"(?P<n>{_NUMBER})\s*月(?![份龄齡])|(?<![a-z])(?P<m>january|jan|february|feb|april|apr|june|jun|"
    r"july|jul|august|aug|september|sept|sep|october|oct|november|nov|december|dec)(?![a-z])"
    r"|\b(?:in|from|during|until|this|by)\s+"
    rf"(?P<short>{_MONTH})",
    re.ASCII,
)
_CURRENCIES = {
    "hkd": ("hk$", "hkd$", "hkd", "港幣", "港币", "港元", "港圓", "港圆", "hong kong dollar", "hong kong dollars"),
    "usd": ("us$", "usd$", "usd", "$", "美元", "美金", "us dollar", "us dollars"),
    "cny": ("cn¥", "rmb", "cny", "¥", "人民幣", "人民币", "元", "圓", "圆", "yuan", "chinese yuan"),
    "eur": ("eur", "€", "歐元", "欧元", "euro", "euros"),
    "gbp": ("gbp", "£", "英鎊", "英镑", "pound sterling", "pounds sterling"),
    "sgd": ("sg$", "sgd", "新加坡元"),
    "twd": ("nt$", "twd", "新台幣", "新台币"),
    "jpy": ("jp¥", "jpy", "日圓", "日圆", "日元"),
}
_CURRENCY_CODES = {label: code for code, labels in _CURRENCIES.items() for label in labels}
_CURRENCY = "|".join(map(re.escape, sorted(_CURRENCY_CODES, key=lambda s: (-len(s), s))))
_MONEY = re.compile(
    rf"(?:(?<![a-z])(?P<before>{_CURRENCY})\s*(?P<amount>{_NUMBER})(?:\s*[元圓圆])?|"
    rf"(?P<suffix_amount>{_NUMBER})\s*(?P<after>{_CURRENCY})(?![a-z]))",
)
_BARE_PRICE = re.compile(
    rf"(?:(?:[售定原特][價价])(?:為|为)?\s*:?\s*|\bprice\s*:\s*|"
    rf"\b(?:priced\s+at|price\s+(?:is|of)|costs?)\s+)(?P<n>{_NUMBER})",
    re.ASCII,
)
_SPEND = rf"(?:(?:{_CURRENCY})\s*)?{_NUMBER}(?:\s*(?:{_CURRENCY})(?![a-z]))?"
_THRESHOLDS = (
    (re.compile(rf"(?:滿|满|最低(?:消[費费]|金[額额])|至少(?:消[費费]|[購购][買买]))\s*(?P<v>{_SPEND})"), "at_least"),
    (re.compile(rf"(?:超[過过]\s*|\b(?:orders?\s+)?(?:over|above|more\s+than)\s+)(?P<v>{_SPEND})", re.ASCII), "over"),
    (re.compile(rf"\b(?:orders?\s+of\s+|spend\s+|free shipping\s+at\s+)?(?P<v>{_SPEND})\s+"
                r"(?:or\s+more|and\s+(?:above|up)|or\s+above)\b", re.ASCII), "at_least"),
    (re.compile(rf"\b(?:free shipping\s+from|minimum spend(?:\s+of)?|spend\s+at\s+least|"
                rf"orders?\s+(?:of\s+)?at\s+least)\s+(?P<v>{_SPEND})", re.ASCII), "at_least"),
    (re.compile(rf"\b(?:orders?(?:\s+of)?|spend|free shipping(?:\s+(?:at|from))?)\s+(?P<v>{_SPEND})\s*\+(?![0-9])", re.ASCII),
     "at_least"),
    (re.compile(rf"(?P<v>{_SPEND})\s*(?:或以上|及以上|以上)(?!的)"), "at_least"),
)
_FOLD = re.compile(rf"(?P<n>{_NUMBER})\s*折")
_OFF = re.compile(rf"(?:(?:\bsave\s+|立[減减]|省)\s*(?P<before>{_NUMBER})\s*%|(?P<after>{_NUMBER})\s*%\s*(?:off\b|折扣|[優优]惠))", re.ASCII)
_PERCENT = re.compile(rf"(?P<n>{_NUMBER})\s*%")
_CLOCK_TOKEN = r"(?:[0-9]{1,2}:[0-9]{2}(?:\s*[ap]\.?m\.?(?![a-z]))?|[0-9]{1,2}\s*[ap]\.?m\.?(?![a-z]))"
_CLOCK_RANGE = re.compile(rf"(?<![0-9])(?P<a>{_CLOCK_TOKEN})\s*(?:{_DASH}|to\b)\s*(?P<b>{_CLOCK_TOKEN})(?![0-9])", re.ASCII)
_CLOCK_BETWEEN = re.compile(rf"\bbetween\s+(?P<a>{_CLOCK_TOKEN})\s+and\s+(?P<b>{_CLOCK_TOKEN})(?![0-9])", re.ASCII)
_CLOCK = re.compile(rf"(?<![0-9])(?P<t>{_CLOCK_TOKEN})(?![0-9])")
_DURATION = re.compile(
    rf"(?<!同)(?P<lead>[為为]期|[僅仅]限|限[時时]|持[續续]|呢|[這这]|\b(?:for|only|lasts?)\s+)?\s*"
    rf"(?P<n>{_NUMBER})\s*(?P<dash>-)?\s*(?:days?\b|[個个]?天|[個个]?日(?![期子]))(?P<tail>[以]?[內内]|\s+only\b)?",
    re.ASCII,
)
_FIRST_GUESTS = re.compile(
    rf"(?:首|前)\s*(?P<han>{_NUMBER})\s*(?:位|名|人)|"
    rf"\bfirst\s+(?P<en>{_NUMBER})\s+(?:guests?|visitors?|customers?|shoppers?|people|attendees?|to\s+arrive)\b",
    re.ASCII,
)
_QUANTITY_LABELS = {
    "bottle": "瓶 bottle bottles", "box": "盒 box boxes", "cup": "杯 cup cups", "piece": "件 piece pieces item items",
    "set": "套 set sets",
    "person": "位 名 人 guest guests visitor visitors customer customers person people shopper shoppers attendee attendees",
    "portion": "份 portion portions serving servings", "unit": "台 臺 unit units", "strip": "條 条 strip strips",
    "sheet": "張 张 sheet sheets", "pair": "雙 双 pair pairs", "occurrence": "次 time times", "pack": "包 pack packs",
    "minute": "分鐘 分钟 minute minutes", "hour": "小時 小时 hour hours",
    "ml": "毫升 ml milliliter milliliters millilitre millilitres", "l": "升 l liter liters litre litres",
    "cm": "厘米 釐米 公分 cm centimeter centimeters centimetre centimetres",
    "mm": "毫米 mm millimeter millimeters millimetre millimetres",
    "g": "克 g gram grams", "kg": "公斤 千克 kg kilogram kilograms",
}
_QUANTITY_UNITS = {label: unit for unit, labels in _QUANTITY_LABELS.items() for label in labels.split()}
_HAN_QUANTITY = "|".join("包(?![郵邮])" if label == "包" else label
                         for label in sorted((label for label in _QUANTITY_UNITS if not label.isascii()),
                                             key=len, reverse=True))
_EN_QUANTITY = "|".join(sorted((label for label in _QUANTITY_UNITS if label.isascii() and len(label) > 1),
                               key=len, reverse=True))
_LIMIT_PREFIX = (r"(?:限量(?:供應|供应|發售|发售)?|(?:只|僅|仅)(?:有|限|得|剩|餘|余|售)|[僅仅]|"
                 r"\b(?:limited\s+stock|stock\s+limit)(?=\s*:)|"
                 r"\b(?:only|limited\s+to|capped\s+at|up\s+to)\s+)")
_LIMIT_SUFFIX = r"(?:\s*(?:限量(?:供應|供应|發售|发售)?|[為为]限)|\s+(?:only|available\s+in\s+total|in\s+total)\b)"
_QUANTITY = re.compile(
    rf"(?:(?P<prefix>{_LIMIT_PREFIX})\s*:?)?\s*(?P<amount>{_NUMBER})"
    rf"(?:\s*(?P<han_unit>{_HAN_QUANTITY})|\s*(?P<symbol>ml|cm|mm|kg|l|g)(?![a-z0-9])"
    rf"|(?:\s+|\s*-\s*)(?:(?:gift|starter|sample|trial|travel|limited-edition)\s+)?(?P<en_unit>{_EN_QUANTITY})(?![a-z0-9]))"
    rf"(?P<suffix>{_LIMIT_SUFFIX})?",
    re.ASCII,
)
_RAW_NUMBER = re.compile(_DIGITS)
_PRICE_BREAK = re.compile(r"[\n;。；!?！？、]|(?<![0-9])[.,，]|[.,，](?![0-9])|\b(?:and|while|whereas)\b", re.ASCII)
_SENTENCE_BREAK = re.compile(r"[\n;。；!?！？]|(?<![0-9])\.|\.(?![0-9])")
_PRICE_LIST_JOIN = re.compile(r"\s*(?:\b(?:and|or)\b|[,，、及和與与])\s*", re.ASCII)
_PAIRED_PRICES = re.compile(r"\brespectively\b|分[別别]", re.ASCII)
_PRICE_LATIN = re.compile(r"[a-z][a-z0-9]*")
_PRICE_HAN = re.compile(r"[\u3400-\u9fff]+")
_PRICE_STOP = set(
    "a an are at and as available buy choose cost costs discover each for from get is just now of on only our per price priced "
    "prices purchase retail shop the then to today was were while with you your hkd usd rmb cny".split()
)
_PRICE_HAN_STOP = {"價格", "价格", "價錢", "价钱", "售價", "售价", "定價", "定价", "現售", "现售", "只需"}
_MEMBER_OFFER = re.compile(
    r"(?<!非)[會会][員员]|[會会]籍|(?<!non-)\bvips?\b|\bloyalty\s+cardholders?\b|"
    r"\b(?:with|through)\s+(?:(?:your|our|a|the)\s+)?membership\b|"
    r"\bmembership\s+(?:benefits?|discount|offer|perks?|price)\b|"
    r"(?<!non-)(?<!non )\bmembers?\b(?!\s+of\s+(?!(?:(?:our|the|a)\s+)?(?:loyalty|rewards)\b))", re.ASCII,
)
_MEMBER_UNRESTRICTED = re.compile(
    r"非[會会][員员](?:也|亦|均|同[樣样])?(?:可|能|享|[領领])|(?:[無无]需|不需(?:要)?|毋須)(?:成[為为])?[會会][員员]|"
    r"\bnon[- ]?members?\s+(?:(?:can|may|also)\s+)?(?:save|get|enjoy|qualif(?:y|ies))\b|"
    r"\bno\s+membership\s+(?:is\s+)?(?:required|needed|necessary)\b|\bincluding\s+(?:all\s+)?(?:members|vips?)\b",
    re.ASCII,
)
_HONG_KONG = r"(?:香港|(?<![a-z0-9])(?:hong\s+kong|hk)(?![a-z0-9$]))"
_HONG_KONG_WORD = re.compile(_HONG_KONG)
_FREE_SHIPPING = re.compile(
    r"包[郵邮]|免[運运](?:[費费])?|免[郵邮][費费]|[運运][費费](?:全免|豁免)|"
    r"\b(?:free|complimentary)\s+(?:(?:local|hong\s+kong|hk)\s+)?(?:shipping|delivery)\b|"
    r"\b(?:shipping|delivery)\b[^.!?;，,]{0,50}\b(?:is\s+(?:free|on\s+us)|at\s+no\s+(?:extra\s+)?charge)\b|"
    r"\bships?\s+free\b",
    re.ASCII,
)
_ORDER_ZH = r"(?:[訂订][單单]|下[單单]|[購购][買买]|[銷销]售|接受|受理)"
_ONLY_ZH = r"(?:[僅仅只](?:限[於于]?|供|接受)|限[於于]|限定[於于]?|限制[於于]?)"
_ORDER_SCOPE = re.compile(
    rf"{_ORDER_ZH}(?:地[區区]|[範范][圍围])?\s*{_ONLY_ZH}\s*{_HONG_KONG}"
    rf"|{_ONLY_ZH}\s*(?:{_ORDER_ZH}\s*)?{_HONG_KONG}\s*(?:地[區区]|[顧顾]客|用[戶户]|居民)?\s*{_ORDER_ZH}"
    rf"|\b(?:orders?|purchases?|checkout)\s+(?:(?:are|is|will\s+be)\s+)?(?:restricted|limited)\s+to\s+{_HONG_KONG}"
    rf"|\b(?:only\s+(?:accept|process|allow|take)|(?:accept|process|allow|take)\s+only)\s+"
    rf"(?:orders?\s+(?:from|in|within)\s+{_HONG_KONG}|{_HONG_KONG}\s+orders?)"
    rf"|\bonly\s+{_HONG_KONG}(?:-based)?\s+(?:customers?|shoppers?|residents?)\s+(?:can|may)\s+(?:order|purchase|buy)\b"
    rf"|(?:只|僅|仅)(?:可|能)(?:在|於|于)\s*{_HONG_KONG}(?:地[區区])?\s*{_ORDER_ZH}"
    rf"|\b(?:orders?|purchases?)\s+(?:can|may)\s+only\s+be\s+(?:placed|made)\s+(?:in|within|from)\s+{_HONG_KONG}"
    rf"|\b(?:order|buy|purchase)\s+only\s+(?:in|from|within)\s+{_HONG_KONG}"
    rf"|\bonly\s+(?:customers?|shoppers?|residents?)\s+(?:in|from|within)\s+{_HONG_KONG}\s+"
    rf"(?:can|may)\s+(?:order|purchase|buy|place\s+orders?)\b",
    re.ASCII,
)
_AMBIGUOUS_ORDER_SCOPE = re.compile(
    rf"{_ONLY_ZH}\s*{_HONG_KONG}|\b(?:only\s+{_HONG_KONG}\s+orders?|{_HONG_KONG}\s+orders?\s+only|"
    rf"orders?\s+(?:from|in|within)\s+{_HONG_KONG}\s+only)\b",
    re.ASCII,
)
_OFFER_CLAUSE = re.compile(r"[\n.!?;。！？；]")


def _number(raw):
    if re.fullmatch(_DIGITS, raw):
        return Decimal(raw.replace(",", ""))
    if re.fullmatch(r"[0-9]{1,2}(?:st|nd|rd|th)", raw):
        return Decimal(raw[:-2])
    if re.fullmatch(_HAN_NUMBER, raw):
        whole, _, fraction = raw.replace("廿", "二十").replace("點", "点").partition("点")
        if any(char in _HAN_UNITS for char in whole):
            total, section, current = 0, 0, 0
            for char in whole:
                if char in _HAN_DIGITS:
                    current = _HAN_DIGITS[char]
                elif _HAN_UNITS[char] < 10000:
                    section += (current or 1) * _HAN_UNITS[char]
                    current = 0
                else:
                    total += (section + current or 1) * 10000
                    section, current = 0, 0
            integer = str(total + section + current)
        else:
            integer = "".join(str(_HAN_DIGITS[char]) for char in whole)
        return Decimal(integer + ("." + "".join(str(_HAN_DIGITS[char]) for char in fraction) if fraction else ""))
    total, current = 0, 0
    for word in re.split(r"[ -]+", raw):
        if word == "hundred":
            current = (current or 1) * 100
        elif word in ("thousand", "million"):
            total += (current or 1) * _EN_UNITS[word]
            current = 0
        elif word != "and":
            current += _EN_DIGITS[word] if word in _EN_DIGITS else _EN_ORDINALS[word]
    return Decimal(total + current)


def _month(raw):
    if not raw:
        return 0
    name = raw.rstrip(".")
    return _MONTHS[name] if name in _MONTHS else int(_number(raw))


def _date_facts(match, *, span=False):
    fields = match.groupdict()
    month = _month(fields.get("m"))
    year = int(fields.get("y") or 0)
    day = int(_number(fields["a" if span else "d"]))
    if not 0 <= month <= 12 or not 1 <= day <= 31:
        return ()
    if not span:
        return (("date", year, month, day),)
    end_month = _month(fields.get("n")) or month
    end_day = int(_number(fields["b"]))
    if not 0 <= end_month <= 12 or not 1 <= end_day <= 31:
        return ()
    return (("date_range", year, month, day, end_month, end_day),)


def _money_amount(value):
    match = _MONEY.fullmatch(value)
    if not match:
        return "", _number(value)
    return _CURRENCY_CODES[match["before"] or match["after"]], _number(match["amount"] or match["suffix_amount"])


def _time(raw):
    hour, minute, period = re.fullmatch(r"([0-9]{1,2})(?::([0-9]{2}))?\s*(?:([ap])\.?m\.?)?", raw).groups()
    hour, minute = int(hour), int(minute or 0)
    if period:
        if not 1 <= hour <= 12:
            return ()
        hour = hour % 12 + (12 if period == "p" else 0)
    return (hour, minute) if hour < 24 and minute < 60 else ()


def _clock_facts(match):
    if "t" in match.groupdict():
        instant = _time(match["t"])
        return (("time", *instant),) if instant else ()
    start, end = _time(match["a"]), _time(match["b"])
    return (("time_range", *start, *end),) if start and end else ()


def _duration(match):
    amount = _number(match["n"])
    if amount == 1 and not (re.fullmatch(_DIGITS, match["n"]) or match["lead"] or match["dash"] or match["tail"]):
        return ()  # A generic 一天 or "one day" can describe ordinary life.
    return (("duration", amount),)


def _quantity(match):
    raw = match["amount"]
    amount = _number(raw)
    unit = _QUANTITY_UNITS[match["han_unit"] or match["symbol"] or match["en_unit"]]
    if match["prefix"] or match["suffix"]:
        return (("quantity", unit, amount), ("limited_quantity", unit, amount))
    # Idiomatic 一杯 and "one cup" can be indefinite in marketing copy.
    explicit = amount != 1 or re.fullmatch(_DIGITS, raw) or match["symbol"] or unit in {"ml", "l", "cm", "mm", "g", "kg"}
    return (("quantity" if explicit else "optional_quantity", unit, amount),)


def _url_destination(match):
    raw = match[0]
    previous = match.string[match.start() - 1:match.start()]
    if previous == "<" and match.string[match.end():match.end() + 1] == ">":
        return raw
    if previous == "'" and raw.endswith("'"):
        raw = raw[:-1]
    opening = {")": "(", "]": "[", "}": "{"}
    counts = Counter(raw)
    end = len(raw)
    while end:
        tail = raw[end - 1]
        if tail not in ".!,;:" and not (tail in opening and counts[tail] > counts[opening[tail]]):
            break
        counts[tail] -= 1
        end -= 1
    return raw[:end]


def _price_anchors(text):
    latin = set(_PRICE_LATIN.findall(text)) - _PRICE_STOP
    han = {run[i:i + 2] for run in _PRICE_HAN.findall(text) for i in range(len(run) - 1)}
    return latin | (han - _PRICE_HAN_STOP)


def _paired_price_anchors(prose, occurrences):
    """Read named lists such as 'A and B cost $5 and $8, respectively'."""
    first, last = occurrences[0][0], occurrences[-1][1]
    if not _PAIRED_PRICES.search(prose[max(0, first - 40):first] + " " + prose[last:last + 40]):
        return None
    if not all(_PRICE_LIST_JOIN.fullmatch(prose[left[1]:right[0]]) for left, right in zip(occurrences, occurrences[1:])):
        return None
    clause = _SENTENCE_BREAK.split(prose[:first])[-1]
    labels = [label for label in _PRICE_LIST_JOIN.split(_PAIRED_PRICES.sub("", clause)) if label.strip()]
    if len(labels) != len(occurrences):
        return []  # The ordered amounts still constrain translations of unrecognized lists.
    return [_price_anchors(label) for label in labels]


def _clause_price_anchors(prose, occurrences):
    for index, (start, end, _) in enumerate(occurrences):
        previous_end = occurrences[index - 1][1] if index else 0
        next_start = occurrences[index + 1][0] if index + 1 < len(occurrences) else len(prose)
        before = _PRICE_BREAK.split(prose[previous_end:start])[-1][-80:]
        after_parts = _PRICE_BREAK.split(prose[end:next_start], maxsplit=1)
        after = after_parts[0][:80] if len(after_parts) > 1 or index + 1 == len(occurrences) else ""
        yield _price_anchors(before) | _price_anchors(after)


def _price_assignments(prose, occurrences):
    occurrences.sort()
    prices = tuple(dict.fromkeys(value for _, _, value in occurrences))
    anchors = {}
    if not prices:
        return prices, anchors
    labels = _paired_price_anchors(prose, occurrences) if len(prices) > 1 else None
    if labels is None:
        labels = _clause_price_anchors(prose, occurrences)
    for (_, _, price), tokens in zip(occurrences, labels):
        for token in tokens:
            anchors.setdefault(token, set()).add(price)
    return prices, anchors


def _same_price_assignments(expected, actual, *, required):
    prices, anchors = expected
    if len(prices) < 2:
        return True
    actual_prices, actual_anchors = actual
    shared = {token for token in anchors.keys() & actual_anchors.keys() if len(anchors[token]) == 1}
    if any(anchors[token] != actual_anchors[token] for token in shared):
        return False
    # For translated labels with no common anchors, retain the source sequence.
    verified = set().union(*(anchors[token] for token in shared))
    if not required:
        verified.update(set(prices) - set(actual_prices))
    return tuple(price for price in prices if price not in verified) == tuple(
        price for price in actual_prices if price not in verified)


def _facts(copy):
    facts = {("url", _url_destination(match)) for match in _URL.finditer(copy)}
    prose = unicodedata.normalize("NFKC", _URL.sub(" ", copy)).lower().translate(_DASHES)
    prose = re.sub(r"\s+", lambda match: "\n" if "\n" in match[0] else " ", prose)
    if _MEMBER_UNRESTRICTED.search(prose):
        facts.add(("membership_unrestricted",))
    if _MEMBER_OFFER.search(_MEMBER_UNRESTRICTED.sub(" ", prose)):
        facts.add(("membership",))
    for clause in _OFFER_CLAUSE.split(prose):
        shipping = _HONG_KONG_WORD.search(clause) and _FREE_SHIPPING.search(clause)
        if shipping:
            facts.add(("shipping", "hk"))
        # A bare regional restriction may instead qualify free shipping.
        if _ORDER_SCOPE.search(clause) or (not shipping and _AMBIGUOUS_ORDER_SCOPE.search(clause)):
            facts.add(("orders", "hk"))
    remaining = prose
    prices = []

    def take(pattern, parse):
        def consume(match):
            found = parse(match)
            if found:
                facts.update(found)
                for fact in found:
                    if fact[0] == "money":
                        prices.append((match.start(), match.end(), fact[1:]))
                # Keep price offsets and do not join prose across a recognized fact.
                return "\0" * len(match[0])
            return match[0]

        return pattern.sub(consume, remaining)

    for pattern in _DATE_RANGES:
        remaining = take(pattern, lambda match: _date_facts(match, span=True))
    for pattern in _DATES:
        remaining = take(pattern, _date_facts)
    remaining = take(_MONTH_ONLY, lambda match: (("month", _month(match["n"] or match["m"] or match["short"])),))
    remaining = take(_CLOCK_BETWEEN, _clock_facts)
    remaining = take(_CLOCK_RANGE, _clock_facts)
    remaining = take(_CLOCK, _clock_facts)
    for pattern, comparator in _THRESHOLDS:
        remaining = take(pattern, lambda match: (("threshold", comparator, *_money_amount(match["v"])),))
    remaining = take(_MONEY, lambda match: (("money", *_money_amount(match[0])),))
    remaining = take(_BARE_PRICE, lambda match: (("money", "", _number(match["n"])),))
    remaining = take(_FOLD, lambda match: (("discount", _fold_discount(_number(match["n"]))),))
    remaining = take(_OFF, lambda match: (("discount", _number(match["before"] or match["after"])),))
    remaining = take(_PERCENT, lambda match: (("percent", _number(match["n"])),))
    remaining = take(_DURATION, _duration)
    remaining = take(_FIRST_GUESTS, lambda match: (("first_guests", _number(match["han"] or match["en"])),))
    remaining = take(_QUANTITY, _quantity)
    facts.update(("number", _number(match[0])) for match in _RAW_NUMBER.finditer(remaining))
    return facts, _price_assignments(prose, prices)


def _fold_discount(pay):
    return 100 - (pay * 10 if pay <= 10 else pay)


def _range_lengths(facts):
    lengths = set()
    for kind, *parts in facts:
        if kind != "date_range":
            continue
        known_year, month, start, end_month, end = parts
        for year in (known_year,) if known_year else (2000, 2001):
            try:
                first = date(year, month or 1, start)
                last = date(year + (end_month < month), end_month or month or 1, end)
            except ValueError:
                continue
            if last >= first:
                lengths.add(("duration", (last - first).days + 1))
    return lengths


def _verify_factual_fidelity(source, primary_copy, alt_copy, cta_options, market):
    """Require offer facts in both drafts and allow shorter, grounded CTAs."""
    expected, prices = _facts(source)
    required = {fact for fact in expected if fact[0] not in ("number", "optional_quantity")}
    allowed = expected | _range_lengths(expected)
    allowed |= {("quantity", *fact[1:]) for fact in expected if fact[0] == "optional_quantity"}
    # A separate mention of a month is consistent with a complete date.
    allowed |= {("month", fact[2]) for fact in expected if fact[0] == "date" and fact[2]}
    allowed |= {("month", month) for fact in expected if fact[0] == "date_range" for month in (fact[2], fact[4]) if month}
    allowed |= {("time", *instant) for fact in expected if fact[0] == "time_range" for instant in (fact[1:3], fact[3:5])}
    for index, output in enumerate((primary_copy, alt_copy, *cta_options)):
        actual, actual_prices = _facts(output)
        optional_quantities = {fact for fact in actual if fact[0] == "optional_quantity"}
        actual -= optional_quantities
        actual |= {("quantity", *fact[1:]) for fact in optional_quantities if ("quantity", *fact[1:]) in allowed}
        full_draft = index < 2
        if (not actual <= allowed or (full_draft and not required <= actual)
                or not _same_price_assignments(prices, actual_prices, required=full_draft)):
            raise RewriteFailure("factual_mismatch")
