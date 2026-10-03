# Bug report

`decide()` in `panel.py` picks the panel's grade with `Counter.most_common`.
When one judge fails to parse (`None`) and the other two disagree, the winner
is decided by the ORDER of the judges in the list:

    decide(["C", None, "I"])  -> "C"
    decide(["I", None, "C"])  -> "I"

Spec: a grade wins only with a STRICT MAJORITY of all votes cast, and a judge
that failed to parse still counts in the denominator (it withholds its vote,
it does not lower the bar). No strict majority -> return None.

Tests: `python3 -m unittest test_panel -v`
