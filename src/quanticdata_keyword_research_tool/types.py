"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class KeywordIdeasRow(TypedDict, total=False):
    """One row of `keyword-research ideas` (keyword_ideas v1.0.1)."""

    rank: int
    """1-based delivery order."""
    keyword: str
    """The suggested query."""
    seed: str
    """The seed it was expanded from."""
    probe: str
    """The exact autocomplete probe that surfaced it."""
    mode: str
    """Probe family: seed, alphabet, questions, prepositions, comparisons."""
    relevance: Optional[float]
    """Google's relevance score for the suggestion."""
    type: Optional[str]
    """Suggestion type as returned (QUERY, NAVIGATION…)."""

class GoogleAutocompleteRow(TypedDict, total=False):
    """One row of `keyword-research suggest` (google_autocomplete v1.0.1)."""

    rank: int
    """Suggestion order as Google returns it."""
    suggestion: str
    """The suggested query."""
    relevance: Optional[int]
    """Google's relevance score, when provided."""
    type: Optional[str]
    """Suggestion kind (QUERY, ENTITY…), when provided."""
    seed: str
    """The seed that produced this suggestion."""
