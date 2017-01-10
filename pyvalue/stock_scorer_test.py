import unittest

from pyvalue import stock_scorer
from pyvalue.morningstar import financial
from pyvalue.morningstar import db


class StockScorerTest(unittest.TestCase):

    @staticmethod
    def test_debt_to_assert_scorer():
        db_conn = db.Database()
        db_conn.connect()
        apple = financial.Financial('AAPL')
        assert db_conn.retrieve_fundamentals(apple)
        debt_assert_scorer = stock_scorer.DebtToAssertScorer()
        score = debt_assert_scorer.score(apple)
        assert score == 0
        google = financial.Financial('GOOG')
        assert db_conn.retrieve_fundamentals(google)
        debt_assert_scorer = stock_scorer.DebtToAssertScorer()
        score = debt_assert_scorer.score(google)
        assert score == 1.0
        db_conn.close()

    @staticmethod
    def test_current_ratio_scorer():
        db_conn = db.Database()
        db_conn.connect()
        apple = financial.Financial('AAPL')
        assert db_conn.retrieve_fundamentals(apple)
        scorer = stock_scorer.CurrentRatioScorer()
        score = scorer.score(apple)
        assert score == 0
        google = financial.Financial('GOOG')
        assert db_conn.retrieve_fundamentals(google)
        scorer = stock_scorer.CurrentRatioScorer()
        score = scorer.score(google)
        assert score == 1.0
        db_conn.close()


if __name__ == '__main__':
    unittest.main()
