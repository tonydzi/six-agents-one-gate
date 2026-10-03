"""Reference fix (used only by _test_demo.py to prove the gate turns green)."""
from collections import Counter


def decide(votes):
    counted = [v for v in votes if v is not None]
    if not counted:
        return None
    grade, n = Counter(counted).most_common(1)[0]
    return grade if n * 2 > len(votes) else None
