"""
_summary_
"""


import unittest
from application.upload.ingestion_utility import IngestionUtility


class TestIngestionUtility(unittest.TestCase):
    """
    _summary_
    """

    def test_close_logger(self):
        close_logger = IngestionUtility(None, None)
        pass


if __name__ == '__main__':
    unittest.main()
