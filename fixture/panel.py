"""Grader panel: several LLM judges vote on one answer, the panel returns one grade.

Each vote is "C" (correct), "I" (incorrect), "P" (partial),
or None when a judge's output could not be parsed.
"""
from collections import Counter


def decide(votes):
    """Return the panel's grade for `votes`, or None when the panel has no verdict."""
    counted = [v for v in votes if v is not None]
    if not counted:
        return None
    return Counter(counted).most_common(1)[0][0]
