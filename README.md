# Keyword Research Tool

[![ci](https://github.com/quantumproxies/keyword-research-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/keyword-research-tool/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Keyword research from Python or the command line: expand one seed into up to 500 keywords people actually type in Google, through question, alphabet, preposition and comparison probes, each with Google's relevance score and the exact probe that surfaced it; or read the raw autocomplete suggestions of any query. The code is free and open source (MIT). It runs on the QuanticData Data API, so there is no Google Ads account to open and no proxy to rotate: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/keyword-research-tool
keyword-research login
keyword-research ideas "keyword research" --modes questions --country us --max-results 100 -o questions.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=keyword-research-tool).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `keyword-research ideas` | seed keyword | Keyword, relevance score, probe, expansion, 7 fields per row ([fields and price](https://quanticdata.io/collectors/keyword-research-api/?utm_source=github&utm_medium=readme&utm_campaign=keyword-research-tool)) | up to 500 |
| `keyword-research suggest` | partial query | Suggestion, relevance score, type, 5 fields per row ([fields and price](https://quanticdata.io/collectors/google-autocomplete-api/?utm_source=github&utm_medium=readme&utm_campaign=keyword-research-tool)) | up to 20 |

Any Google market: `--country us --lang en`, `--country de --lang de`, `--country it --lang it`. `ideas --modes` picks the probe families; every row says which `mode` and which `probe` surfaced the keyword.

## Sample output

A real row from `keyword-research ideas "keyword research" --modes questions --country us --lang en --max-results 3` (2026-10-23):

```json
{
  "mode": "questions",
  "rank": 1,
  "seed": "keyword research",
  "type": "QUERY",
  "probe": "how to keyword research",
  "keyword": "how to keyword research for seo",
  "relevance": 1250
}
```

## Python

```python
from quanticdata_keyword_research_tool import KeywordResearch

kw = KeywordResearch()  # saved login, or QUANTICDATA_API_KEY

ideas = kw.ideas("keyword research", modes=["questions", "comparisons"], country="us", max_results=200)
for k in sorted(ideas, key=lambda k: k["relevance"] or 0, reverse=True)[:20]:
    print(k["relevance"], k["mode"], k["keyword"])
ideas.to_csv("keyword_ideas.csv")

now = kw.suggest("keyword research", country="us")
print([s["suggestion"] for s in now])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Questions people ask**: The question-style suggestions for a list of seeds in one CSV, the raw material for FAQ sections and blog briefs. See [`examples/question_keywords.py`](examples/question_keywords.py).
- **Keyword list from one seed**: All five probe families for one seed, de-duplicated and sorted by Google's relevance score, with the probe that surfaced each keyword. See [`examples/keyword_list.py`](examples/keyword_list.py).
- **Autocomplete monitoring**: Log what Google suggests for your brand or product names on every run and print the suggestions that appeared or dropped out since the last one. See [`examples/suggest_watch.py`](examples/suggest_watch.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `keyword-research run <id> -o out.csv` collects it later.

### `keyword-research ideas`

Keyword suggestions people actually type, expanded from one seed.

```
keyword-research ideas SEED [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `SEED` | string |  | The keyword to expand, e.g. "keyword research". |
| `--modes` | seed / alphabet / questions / prepositions / comparisons | `seed, questions, alphabet` | Which probe families to run: seed, alphabet, questions, prepositions, comparisons (default seed, questions and alphabet). |
| `--country` | string |  | Google market, as an ISO country code (us, gb, de...). |
| `--lang` | string |  | Interface language, e.g. en, it, de. |
| `--max-results` | integer | `50` | How many keywords to deliver at most (1–500). You pay only for delivered keywords. |

### `keyword-research suggest`

Raw Google autocomplete suggestions for one seed query, with Google's relevance score.

```
keyword-research suggest QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | The query to complete, e.g. "keyword research" or a partial one like "keyword res". |
| `--country` | string |  | Google market, as an ISO country code (us, gb, de...). |
| `--lang` | string |  | Interface language, e.g. en, it, de. |
| `--max-results` | integer | `10` | How many suggestions to deliver at most (1–20). You pay only for delivered suggestions. |

## Output fields

<details><summary><code>keyword-research ideas</code>: 7 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based delivery order. |
| `keyword` | string | The suggested query. |
| `seed` | string | The seed it was expanded from. |
| `probe` | string | The exact autocomplete probe that surfaced it. |
| `mode` | string | Probe family: seed, alphabet, questions, prepositions, comparisons. |
| `relevance` | number or null | Google's relevance score for the suggestion. |
| `type` | string or null | Suggestion type as returned (QUERY, NAVIGATION…). |

</details>

<details><summary><code>keyword-research suggest</code>: 5 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | Suggestion order as Google returns it. |
| `suggestion` | string | The suggested query. |
| `relevance` | integer or null | Google's relevance score, when provided. |
| `type` | string or null | Suggestion kind (QUERY, ENTITY…), when provided. |
| `seed` | string | The seed that produced this suggestion. |

</details>

## Sign-in and API keys

- `keyword-research login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `keyword-research login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `keyword-research login --api-key`.
- `keyword-research logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=keyword-research-tool).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/keyword_ideas/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"seed": "keyword research", "modes": ["questions"], "country": "us", "lang": "en", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=keyword-research-tool) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=keyword-research-tool) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this keyword research tool free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need a Google Ads account or proxies?**

No. There is no Ads account, Google key or proxy to set up: you send a seed and get the keywords back; the requests run on QuanticData's side.

**Where do the keywords come from?**

From Google autocomplete. Each keyword is a suggestion Google showed for a probe built from your seed; the row carries that probe, its family (mode) and Google's relevance score.

**How many keywords can one run return?**

Up to 500 keywords per ideas run and 20 suggestions per suggest call; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o keywords.csv (or .json, .jsonl). One keyword per row, so the file opens cleanly in Excel or Google Sheets and sorts by relevance.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/suggest_watch.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Google Trends Scraper](https://github.com/quantumproxies/google-trends-scraper): Google Trends scraper and API for Python and the command line.
- [Google SERP API](https://github.com/quantumproxies/google-serp-api): Google SERP API for Python and the command line.
- [Bing Search API](https://github.com/quantumproxies/bing-search-api): Bing Search API alternative for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=keyword-research-tool).
