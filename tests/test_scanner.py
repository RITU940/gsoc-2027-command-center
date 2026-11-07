import sys
from pathlib import Path
import unittest
from datetime import datetime, timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "scripts"))
from scan_issues import calculate_score, normalize_issue

class ScannerTests(unittest.TestCase):
    def test_beginner_labels_are_priority(self):
        base = {"title": "Write unit tests", "labels": [], "assignees": [], "comments": 0,
                "updated_at": "2026-11-01T00:00:00Z"}
        rated = dict(base, labels=[{"name": "good first issue"}])
        t = datetime(2026,11,8,tzinfo=timezone.utc)
        self.assertGreater(calculate_score(rated, 4, t),calculate_score(base,4,t))
    def test_assignment_deprioritizes(self):
        base={"title":"small fix","labels":[],"assignees":[],"comments":1}
        self.assertGreater(calculate_score(base),calculate_score(dict(base,assignees=[{"login":"someone"}])))
    def test_normalization(self):
        issue={"number":31,"title":"Fix typo","html_url":"https://github.com/o/r/issues/31",
            "labels":[{"name":"help wanted"}],"comments":2,"assignees":[],"updated_at":"2026-11-01T00:00:00Z"}
        x=normalize_issue(issue,"o/r",4)
        self.assertEqual(x["labels"],["help wanted"])
        self.assertEqual(x["repo"],"o/r")
        self.assertGreater(x["score"],0)

if __name__=="__main__":unittest.main()
