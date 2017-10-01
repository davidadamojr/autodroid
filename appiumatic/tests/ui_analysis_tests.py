import unittest
from appiumatic.uianalysis import _get_actionable_widgets

class UIAnalysisTests(unittest.TestCase):

    def test_get_simple_actionable_widgets(self):
        page_source = open("data/page_source_clickable.xml").read().replace("\n", "").encode()
        actionable_widgets = _get_actionable_widgets(page_source)