# Bug report

Our grader panel gives different grades for the same answer depending on the
order of the judges. When one judge's output can't be parsed (`None`) and the
other two disagree:

    decide(["C", None, "I"])  -> "C"
    decide(["I", None, "C"])  -> "I"

The panel's verdict should not depend on judge order. Please fix `decide()` in
`panel.py`.

Tests: `python3 -m unittest test_panel -v`
