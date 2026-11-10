"""Regenerate the public demo cache with first-party DeepSeek responses.

Run this manually with a local DeepSeek key. The Pages build uses the resulting
JSON and never runs this generator or needs credentials.
"""

from concurrent.futures import ThreadPoolExecutor
from itertools import product
import json
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.ai_rewriter import MODEL, rewrite_copy
from core.configuration import load_environment
from core.rewrite_errors import RewriteFailure
from core.rewrite_fidelity import _verify_factual_fidelity
from core.search_engine import SearchEngine


DATA = ROOT / "data"
MARKETS = ("hk", "cn", "en")
TONES = ("standard", "social", "concise")
REPORT_FIELDS = ("primary_copy", "alt_copy", "adaptations", "cta_options", "counts", "source_counts",
                 "engine", "target_market", "tone")
RETRYABLE = {"rate_limited", "timeout", "service_unavailable", "invalid_response",
             "incomplete_response", "incomplete_translation", "factual_mismatch"}


def read_data(filename):
    return json.loads((DATA / filename).read_text(encoding="utf-8"))


def load_drafts():
    frontend = (ROOT / "static/js/main.js").read_text(encoding="utf-8")
    homepage = re.search(r"^\s*const HOME_DRAFT = '([^'\\]+)';$", frontend, re.MULTILINE)
    if not homepage:
        raise SystemExit("Could not locate the homepage draft in static/js/main.js.")
    return [{"id": "home", "text": homepage[1]},
            *({"id": draft["id"], "text": draft["text"]} for draft in read_data("sample_drafts.json"))]


def cache_case(case, glossary):
    draft, market, tone = case
    for attempt in range(3):
        report = rewrite_copy(draft["text"], market, tone, glossary)
        live = report["engine"] == "deepseek"
        if live and 3 <= len(report["adaptations"]) <= 6 and len(set(report["cta_options"])) == 2:
            return {**{field: report[field] for field in REPORT_FIELDS},
                    "matched_term_ids": [term["id"] for term in report["matched_glossary_terms"]]}
        error = "incomplete_sample" if live else report["error_code"]
        if (not live and error not in RETRYABLE) or attempt == 2:
            break
        time.sleep(2 ** attempt)
    raise RuntimeError(f"{draft['id']} {market}:{tone} failed ({error}).")


def generate(drafts, glossary):
    cases = list(product(drafts, MARKETS, TONES))
    # Check connectivity and credentials once before scheduling the other cases.
    results = [cache_case(cases[0], glossary)]
    print(f"1/{len(cases)} DeepSeek rewrites verified.", flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(cache_case, case, glossary) for case in cases[1:]]
        for index, future in enumerate(futures, start=2):
            results.append(future.result())
            if index % 9 == 0 or index == len(cases):
                print(f"{index}/{len(cases)} DeepSeek rewrites verified.", flush=True)
    by_draft = {draft["id"]: {} for draft in drafts}
    for (draft, market, tone), report in zip(cases, results, strict=True):
        by_draft[draft["id"]][f"{market}:{tone}"] = report
    return {"version": 1, "model": MODEL,
            "drafts": [{**draft, "rewrites": by_draft[draft["id"]]} for draft in drafts]}


def write_cache(cache, key):
    validate_fidelity(cache)
    content = json.dumps(cache, ensure_ascii=False, separators=(",", ":")) + "\n"
    if key in content or re.search(r"\bsk-[A-Za-z0-9]{20,}\b", content):
        raise RuntimeError("The generated cache contains a possible credential and was rejected.")
    with NamedTemporaryFile(dir=DATA, encoding="utf-8", mode="w", delete=False) as temporary:
        path = Path(temporary.name)
        try:
            temporary.write(content)
            temporary.close()
            path.replace(DATA / "pages_rewrites.json")
        finally:
            path.unlink(missing_ok=True)


def validate_fidelity(cache):
    for draft in cache["drafts"]:
        for variant, report in draft["rewrites"].items():
            try:
                _verify_factual_fidelity(draft["text"], report["primary_copy"], report["alt_copy"],
                                         report["cta_options"], report["target_market"])
            except RewriteFailure as error:
                raise RuntimeError(f"{draft['id']} {variant} failed ({error.code}).") from error


def main():
    load_environment(ROOT / ".env")
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key or key == "your_deepseek_api_key_here":
        raise SystemExit("Set DEEPSEEK_API_KEY locally to regenerate the demo cache.")
    # The public demo cache must have first-party provenance. Keep the normal
    # Flask configuration independent of this one-off generator.
    os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com"
    try:
        cache = generate(load_drafts(), SearchEngine(read_data("glossary_seed.json")))
        write_cache(cache, key)
    except RuntimeError as error:
        raise SystemExit(str(error)) from None


if __name__ == "__main__":
    main()
