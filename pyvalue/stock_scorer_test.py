import unittest

import stock_scorer


class StockScorerTest(unittest.TestCase):

    @staticmethod
    def test_debt_to_assert_scorer():
        db = db.MorningStartDB()
        db.connect()
        apple = db.retrieve('AAPL')
        debt_assert_scorer = stock_scorer.DebtToAssertScorer()
        score = debt_assert_scorer.score(apple)
        assert score == 0
        google = db.retrieve('GOOG')
        debt_assert_scorer = stock_scorer.DebtToAssertScorer()
        score = debt_assert_scorer.score(google)
        assert score == 1.0
        db.close()

    @staticmethod
    def test_current_ratio_scorer():
        db = db.MorningStartDB()
        db.connect()
        apple = db.retrieve('AAPL')
        scorer = stock_scorer.CurrentRatioScorer()
        score = scorer.score(apple)
        assert score == 0
        google = db.retrieve('GOOG')
        scorer = stock_scorer.CurrentRatioScorer()
        score = scorer.score(google)
        assert score == 1.0
        db.close()


if __name__ == '__main__':
    unittest.main()
