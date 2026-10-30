"""Keyword Research Tool: Keyword research tool for Python and the command line: expand one seed into up to 500 Google autocomplete keywords (questions, alphabet, prepositions, comparisons) with Google's relevance score, or read the raw suggestions of any query, as JSON or CSV. Free and open source; no Google Ads account or proxies needed.

    from quanticdata_keyword_research_tool import KeywordResearch

    scraper = KeywordResearch()   # saved login (`keyword-research login`) or QUANTICDATA_API_KEY
    run = scraper.ideas(...)   # keyword ideas expanded from one seed
    run = scraper.suggest(...)   # Google autocomplete suggestions for one query
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["KeywordResearch", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class KeywordResearch:
    """Keyword Research Tool on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="keyword-research/0.1.0 (+https://github.com/quantumproxies/keyword-research-tool)", timeout=timeout)

    def ideas(
        self, seed: str,
        *,
        modes: Optional[Union[str, Sequence[str]]] = None,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Keyword suggestions people actually type, expanded from one seed.

        Args:
            seed: The keyword to expand, e.g. "keyword research".
            modes: Which probe families to run: seed, alphabet, questions, prepositions, comparisons (default seed, questions and alphabet). One of: seed, alphabet, questions, prepositions, comparisons.
            country: Google market, as an ISO country code (us, gb, de...).
            lang: Interface language, e.g. en, it, de.
            max_results: How many keywords to deliver at most (1–500). You pay only for delivered keywords.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 500 rows, one per keyword: see ``types.KeywordIdeasRow``.
        """
        payload = {
            "seed": seed,
            "modes": _as_list(modes),
            "country": country,
            "lang": lang,
            "max_results": max_results,
        }
        return self.client.run_collector("keyword_ideas", payload, wait=wait, timeout=timeout)

    def suggest(
        self, query: str,
        *,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Raw Google autocomplete suggestions for one seed query, with Google's relevance score.

        Args:
            query: The query to complete, e.g. "keyword research" or a partial one like "keyword res".
            country: Google market, as an ISO country code (us, gb, de...).
            lang: Interface language, e.g. en, it, de.
            max_results: How many suggestions to deliver at most (1–20). You pay only for delivered suggestions.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 20 rows, one per suggestion: see ``types.GoogleAutocompleteRow``.
        """
        payload = {
            "query": query,
            "country": country,
            "lang": lang,
            "max_results": max_results,
        }
        return self.client.run_collector("google_autocomplete", payload, wait=wait, timeout=timeout)
