"""Watch what Google autocomplete suggests for your brand or product names.

    python suggest_watch.py "notion" "notion ai" --country us

Reads the current suggestions of each query, compares them with the previous
run (kept in suggest_state.json) and prints the suggestions that appeared or
dropped out. Every suggestion is also appended to suggest_log.csv with the
date, so you can see how the list moves over weeks. Run it daily from cron:

    0 9 * * *  cd /path/to/here && python suggest_watch.py "notion" "notion ai"

Needs a login (`keyword-research login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import json
import os
from datetime import datetime, timezone

from quanticdata_keyword_research_tool import KeywordResearch

FIELDS = ["day", "query", "rank", "suggestion", "relevance", "type"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("queries", nargs="+")
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--state", default="suggest_state.json")
    parser.add_argument("--log", default="suggest_log.csv")
    args = parser.parse_args()

    previous = {}
    if os.path.exists(args.state):
        with open(args.state, encoding="utf-8") as fh:
            previous = json.load(fh)

    kw = KeywordResearch()
    day = datetime.now(timezone.utc).date().isoformat()
    current = {}
    new_log = not os.path.exists(args.log)
    with open(args.log, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_log:
            writer.writeheader()
        for query in args.queries:
            run = kw.suggest(query, country=args.country, lang=args.lang, max_results=20)
            current[query] = [s["suggestion"] for s in run]
            for s in run:
                writer.writerow({"day": day, "query": query, **s})
            before = set(previous.get(query, []))
            now = set(current[query])
            if query in previous:
                for s in sorted(now - before):
                    print(f"{query!r}: new      {s}")
                for s in sorted(before - now):
                    print(f"{query!r}: dropped  {s}")
            print(f"{query!r}: {len(now)} suggestions")

    with open(args.state, "w", encoding="utf-8") as fh:
        json.dump(current, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
