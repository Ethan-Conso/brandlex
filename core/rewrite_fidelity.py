"""Check explicit numeric facts before showing model-generated marketing copy."""

from datetime import date
from decimal import Decimal
import re
import unicodedata

from core.rewrite_errors import RewriteFailure
from core.rewrite_grounding import _SCAN_URL

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
               rf"(?P<b>{_DAY})(?![a-z0-9]){_EN_YEAR}"),
    re.compile(rf"(?<![a-z0-9])(?P<a>{_DAY})\s*{_EN_SPAN}\s*(?P<b>{_DAY})\s+(?P<m>{_MONTH}){_EN_YEAR}"),
    re.compile(rf"(?<![a-z0-9])(?P<a>{_DAY})\s+(?P<m>{_MONTH})\s*{_EN_SPAN}\s*"
               rf"(?P<b>{_DAY})\s+(?P<n>{_MONTH}){_EN_YEAR}"),
    re.compile(rf"\b(?:from|between)\s+(?:the\s+)?(?P<a>{_ORDINAL_DAY})\s*{_EN_SPAN}\s*"
               rf"(?:the\s+)?(?P<b>{_ORDINAL_DAY})(?![a-z0-9])"),
)
_DATES = (
    re.compile(rf"{_ZH_YEAR}(?P<m>{_NUMBER})\s*月\s*(?P<d>{_DAY})\s*[日號号]"),
    re.compile(r"(?<![0-9])(?P<y>[0-9]{4})[-/](?P<m>[0-9]{1,2})[-/](?P<d>[0-9]{1,2})(?![0-9])"),
    re.compile(rf"(?P<m>{_MONTH})\s+(?:the\s+)?(?P<d>{_DAY})(?![a-z0-9]){_EN_YEAR}"),
    re.compile(rf"(?<![a-z0-9])(?P<d>{_DAY})\s+(?P<m>{_MONTH}){_EN_YEAR}"),
    re.compile(rf"(?P<d>{_DAY})\s*[日號号](?=\s*(?:起|止|截止|推出|[發发]售|開售|开售|上[線线市]|[開开]放|[結结]束))"),
    re.compile(rf"\bon\s+(?:the\s+)?(?P<d>{_ORDINAL_DAY})(?![a-z0-9])"),
)
_MONTH_ONLY = re.compile(
    rf"(?P<n>{_NUMBER})\s*月(?![份龄齡])|(?<![a-z])(?P<m>january|jan|february|feb|april|apr|june|jun|"
    r"july|jul|august|aug|september|sept|sep|october|oct|november|nov|december|dec)(?![a-z])"
    r"|\b(?:in|from|during|until|this|by)\s+"
    rf"(?P<short>{_MONTH})",
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
)
_SPEND = rf"(?:(?:{_CURRENCY})\s*)?{_NUMBER}(?:\s*(?:{_CURRENCY})(?![a-z]))?"
_THRESHOLDS = (
    (re.compile(rf"(?:滿|满|最低(?:消[費费]|金[額额])|至少(?:消[費费]|[購购][買买]))\s*(?P<v>{_SPEND})"), "at_least"),
    (re.compile(rf"(?:超[過过]\s*|\b(?:orders?\s+)?(?:over|above|more\s+than)\s+)(?P<v>{_SPEND})"), "over"),
    (re.compile(rf"\b(?:orders?\s+of\s+|spend\s+|free shipping\s+at\s+)?(?P<v>{_SPEND})\s+"
                r"(?:or\s+more|and\s+(?:above|up)|or\s+above)\b"), "at_least"),
    (re.compile(rf"\b(?:free shipping\s+from|minimum spend(?:\s+of)?|spend\s+at\s+least|"
                rf"orders?\s+(?:of\s+)?at\s+least)\s+(?P<v>{_SPEND})"), "at_least"),
    (re.compile(rf"\b(?:orders?(?:\s+of)?|spend|free shipping(?:\s+(?:at|from))?)\s+(?P<v>{_SPEND})\s*\+(?![0-9])"),
     "at_least"),
    (re.compile(rf"(?P<v>{_SPEND})\s*(?:或以上|及以上|以上)(?!的)"), "at_least"),
)
_FOLD = re.compile(rf"(?P<n>{_NUMBER})\s*折")
_OFF = re.compile(rf"(?:(?:\bsave\s+|立[減减]|省)\s*(?P<before>{_NUMBER})\s*%|(?P<after>{_NUMBER})\s*%\s*(?:off\b|折扣|[優优]惠))")
_PERCENT = re.compile(rf"(?P<n>{_NUMBER})\s*%")
_CLOCK_TOKEN = r"(?:[0-9]{1,2}:[0-9]{2}(?:\s*[ap]\.?m\.?(?![a-z]))?|[0-9]{1,2}\s*[ap]\.?m\.?(?![a-z]))"
_CLOCK_RANGE = re.compile(rf"(?<![0-9])(?P<a>{_CLOCK_TOKEN})\s*(?:{_DASH}|to\b)\s*(?P<b>{_CLOCK_TOKEN})(?![0-9])")
_CLOCK_BETWEEN = re.compile(rf"\bbetween\s+(?P<a>{_CLOCK_TOKEN})\s+and\s+(?P<b>{_CLOCK_TOKEN})(?![0-9])")
_CLOCK = re.compile(rf"(?<![0-9])(?P<t>{_CLOCK_TOKEN})(?![0-9])")
_DURATION = re.compile(
    rf"(?<!同)(?P<lead>[為为]期|[僅仅]限|限[時时]|持[續续]|呢|[這这]|\b(?:for|only|lasts?)\s+)?\s*"
    rf"(?P<n>{_NUMBER})\s*(?P<dash>-)?\s*(?:days?\b|[個个]?天|[個个]?日(?![期子]))(?P<tail>[以]?[內内]|\s+only\b)?",
)
_FIRST_GUESTS = re.compile(
    rf"(?:首|前)\s*(?P<han>{_NUMBER})\s*(?:位|名|人)|"
    rf"\bfirst\s+(?P<en>{_NUMBER})\s+(?:guests?|visitors?|customers?|shoppers?|people|attendees?)\b",
)
_QUANTITY = re.compile(
    rf"(?P<han>{_NUMBER})\s*(?:瓶|盒|杯|件|套|位|名|人|份|台|條|条|張|张|雙|双|次|分鐘|分钟|小時|小时)"
    rf"|(?P<en>{_NUMBER})\s+(?:bottles?|boxes?|cups?|pieces?|units?|sets?|guests?|visitors?|customers?|people|"
    r"items?|packs?|pairs?|minutes?|hours?)\b",
)
_RAW_NUMBER = re.compile(_DIGITS)


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
    raw = match["han"] or match["en"]
    amount = _number(raw)
    # Idiomatic 一杯 and "one of" can be indefinite in marketing copy.
    return (("number", amount),) if amount != 1 or re.fullmatch(_DIGITS, raw) else ()


def _facts(copy):
    facts = set()
    normalized = unicodedata.normalize("NFKC", _SCAN_URL.sub(" ", copy)).lower().translate(_DASHES)
    remaining = re.sub(r"\s+", " ", normalized)

    def take(pattern, parse):
        def consume(match):
            found = parse(match)
            if found:
                facts.update(found)
                return "\0"  # Do not let later patterns join text across a consumed fact.
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
    return facts


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
    """Require numeric claims in both drafts and allow shorter, grounded CTAs."""
    expected = _facts(source)
    required = {fact for fact in expected if fact[0] != "number"}
    allowed = expected | _range_lengths(expected)
    # A separate mention of a month is consistent with a complete date.
    allowed |= {("month", fact[2]) for fact in expected if fact[0] == "date" and fact[2]}
    allowed |= {("month", month) for fact in expected if fact[0] == "date_range" for month in (fact[2], fact[4]) if month}
    allowed |= {("time", *instant) for fact in expected if fact[0] == "time_range" for instant in (fact[1:3], fact[3:5])}
    for output in (primary_copy, alt_copy):
        actual = _facts(output)
        if not required <= actual <= allowed:
            raise RewriteFailure("factual_mismatch")
    if any(not _facts(cta) <= allowed for cta in cta_options):
        raise RewriteFailure("factual_mismatch")
