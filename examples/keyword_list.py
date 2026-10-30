"""A full keyword list from one seed: every probe family, de-duplicated.

    python keyword_list.py "running shoes" --country us --max 500

Runs all five probe families (seed, alphabet, questions, prepositions,
comparisons) on the seed, keeps each keyword once with its best relevance
score and the families that found it, and writes keywords.csv sorted by
relevance. The number of words per keyword is added, to split head terms from
long-tail ones.
"""

import argparse

from quanticdata_keyword_research_tool import KeywordResearch, write

MODES = ["seed", "alphabet", "questions", "prepositions", "comparisons"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("seed")
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--max", type=int, default=500, help="keywords to collect (max 500)")
    parser.add_argument("--out", default="keywords.csv")
    args = parser.parse_args()

    kw = KeywordResearch()
    run = kw.ideas(args.seed, modes=MODES, country=args.country, lang=args.lang, max_results=args.max)

    best = {}
    for k in run:
        key = k["keyword"].strip().lower()
        entry = best.setdefault(key, {"keyword": k["keyword"], "relevance": None, "modes": set(), "probe": k.get("probe")})
        entry["modes"].add(k.get("mode"))
        if (k.get("relevance") or 0) > (entry["relevance"] or 0):
            entry["relevance"], entry["probe"] = k.get("relevance"), k.get("probe")

    rows = [{"keyword": e["keyword"], "words": len(e["keyword"].split()), "relevance": e["relevance"],
             "modes": "; ".join(sorted(m for m in e["modes"] if m)), "probe": e["probe"]}
            for e in best.values()]
    rows.sort(key=lambda r: r["relevance"] or 0, reverse=True)

    write(rows, args.out)
    print(f"{len(run)} suggestions, {len(rows)} unique keywords written to {args.out}")


if __name__ == "__main__":
    main()
