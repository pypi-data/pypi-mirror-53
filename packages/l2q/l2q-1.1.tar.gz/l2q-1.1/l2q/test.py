import unittest

from l2q.query_builder import QueryBuilder


class QueryBuilderTest(unittest.TestCase):

    def test_simple_excel(self):
        expected_query = '"blue" OR "black" OR "silver" OR "white"'
        actual_query = QueryBuilder.build_query_from_excel('test/simple.xlsx', 'Sheet1')
        self.assertEqual(expected_query, actual_query)

    def test_simple_word_doc(self):
        expected_query = '"Blue" OR "Black" OR "Silver" OR "White"'
        actual_query = QueryBuilder.build_query_from_word_doc('test/simple.docx')
        self.assertEqual(expected_query, actual_query)

    def test_simple_txt(self):
        expected_query = '"blue" OR "black" OR "silver" OR "white"'
        actual_query = QueryBuilder.build_query_from_txt('test/simple.txt')
        self.assertEqual(expected_query, actual_query)