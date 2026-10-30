"""The questions Google suggests for a list of seed keywords, in one CSV.

    python question_keywords.py "keyword research" "link building" "technical seo" --country us

Runs the "questions" probe family for each seed and writes questions.csv with
the seed, the question, Google's relevance score and the probe that surfaced
it, sorted by relevance within each seed: the raw list for FAQ sections, blog
briefs and "People also ask" style content.
"""

import argparse

from quanticdata_keyword_research_tool import KeywordResearch, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("seeds", nargs="+")
    parser.add_argument("--country", default="us")
    parser.add_argument("--lang", default="en")
    parser.add_argument("--per-seed", type=int, default=100, help="questions per seed (max 500)")
    parser.add_argument("--out", default="questions.csv")
    args = parser.parse_args()

    kw = KeywordResearch()
    rows = []
    for seed in args.seeds:
        run = kw.ideas(seed, modes=["questions"], country=args.country, lang=args.lang, max_results=args.per_seed)
        found = sorted(run, key=lambda k: k.get("relevance") or 0, reverse=True)
        rows.extend({"seed": seed, "question": k["keyword"], "relevance": k.get("relevance"),
                     "probe": k.get("probe")} for k in found)
        print(f"{seed!r}: {len(found)} questions, top: {found[0]['keyword'] if found else '-'}")

    write(rows, args.out)
    print(f"{len(rows)} questions written to {args.out}")


if __name__ == "__main__":
    main()
