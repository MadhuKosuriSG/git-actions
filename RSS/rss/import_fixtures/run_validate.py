"""Call the RSS validate API for every fixture and write report.md + report.json.

Auth comes from an env file (never commit it):  CSRF=...  XSRF=...  COOKIE=...
Usage: python3 run_validate.py <auth.env> [file-filter-substring]
"""
import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

API = "https://ufseneca.pathfactory-development.com/authoring/v2/content-feeds/rss/validate"
BASE = "https://madhukosurisg.github.io/git-actions/RSS/rss/import_fixtures"
HERE = os.path.dirname(os.path.abspath(__file__))

auth = dict(l.strip().split("=", 1) for l in open(sys.argv[1]) if "=" in l)
auth = {k: v.strip("'\"") for k, v in auth.items()}
filt = sys.argv[2] if len(sys.argv) > 2 else ""

# fixtures + expectations from the README manifest
cases, sec = [], None
for l in open(os.path.join(HERE, "README.md")):
    if l.startswith("## "): sec = l[3:].strip()
    elif l.startswith("| `"):
        c = [x.strip() for x in l.split("|")]
        path = f"{sec}/{c[1].strip('`')}"
        if filt in path: cases.append({"file": path, "category": c[2], "expected": c[3]})

def should_accept(c):
    if c["category"] == "valid": return True
    if c["category"] in ("corrupted", "security") or c["expected"].startswith("reject:"): return False
    return None  # "X or Y" / partial-import cases: judge manually

def call(c):
    url = f"{BASE}/{c['file']}"
    req = urllib.request.Request(API, method="POST", data=json.dumps({"sourceUrl": url, "name": "Test"}).encode(), headers={
        "Accept": "application/json, text/plain, */*", "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
        "Origin": "https://ufseneca.pathfactory-development.com",
        "Referer": "https://ufseneca.pathfactory-development.com/authoring/v2/content-feeds",
        "CSRF-Token": auth["CSRF"], "X-CSRF-Token": auth["CSRF"], "X-XSRF-TOKEN": auth["XSRF"], "Cookie": auth["COOKIE"]})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=90) as r: status, body = r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e: status, body = e.code, e.read().decode("utf-8", "replace")
    except Exception as e: status, body = None, f"{type(e).__name__}: {e}"
    try: parsed = json.loads(body)
    except ValueError: parsed = None
    valid = parsed.get("valid") if isinstance(parsed, dict) else None
    want = should_accept(c)
    verdict = "REVIEW" if want is None or valid is None else ("PASS" if want == valid else "FAIL")
    return {**c, "url": url, "http": status, "seconds": round(time.time() - t, 2), "valid": valid, "verdict": verdict, "response": parsed if parsed is not None else body[:2000]}

# ponytail: 4 workers to stay gentle on the shared dev server; raise if it copes
with ThreadPoolExecutor(4) as ex: results = list(ex.map(call, cases))

json.dump(results, open(os.path.join(HERE, "report.json"), "w"), indent=2)
count = lambda v: sum(r["verdict"] == v for r in results)
with open(os.path.join(HERE, "report.md"), "w") as f:
    f.write(f"# RSS validate API report\n\nAPI: `{API}`  \nRun: {time.strftime('%Y-%m-%d %H:%M %Z')}  \nFeeds: {len(results)}\n\n"
            f"| PASS | FAIL | REVIEW |\n|---|---|---|\n| {count('PASS')} | {count('FAIL')} | {count('REVIEW')} |\n\n"
            "PASS/FAIL compares `valid` with the fixture's expectation; REVIEW = expectation is \"X or Y\", or no JSON `valid` field.\n")
    sec = None
    for r in results:
        top = r["file"].split("/")[0]
        if top != sec:
            sec = top
            f.write(f"\n## {top}\n\n| Verdict | File | Category | Expected | HTTP | valid | Response |\n|---|---|---|---|---|---|---|\n")
        resp = json.dumps(r["response"]) if not isinstance(r["response"], str) else r["response"]
        resp = resp.replace("|", "\\|").replace("\n", " ")[:300]
        f.write(f"| {r['verdict']} | [`{r['file'].split('/', 1)[1]}`]({r['url']}) | {r['category']} | {r['expected']} | {r['http']} | {r['valid']} | `{resp}` |\n")
print(f"{len(results)} calls: PASS {count('PASS')}  FAIL {count('FAIL')}  REVIEW {count('REVIEW')}")
