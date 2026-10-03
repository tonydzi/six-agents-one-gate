import hashlib, os, time, unittest

from panel import decide

HERE = os.path.dirname(os.path.abspath(__file__))


class TestPanel(unittest.TestCase):
    def test_unanimous(self):
        self.assertEqual(decide(["C", "C", "C"]), "C")

    def test_verdict_does_not_depend_on_judge_order(self):
        # One judge failed to parse. The other two disagree. Order must not decide.
        self.assertEqual(decide(["C", None, "I"]), decide(["I", None, "C"]))


def tearDownModule():
    # Receipt, written AFTER the tests ran: time + hash of the panel.py they ran against.
    code = hashlib.sha256(open(os.path.join(HERE, "panel.py"), "rb").read()).hexdigest()
    with open(os.path.join(HERE, ".test_receipts"), "a") as f:
        f.write(f"{time.time():.0f} {code}\n")


if __name__ == "__main__":
    unittest.main()
