import builtins
import psycopg2
import psycopg2.extras
import unittest
from unittest import mock, TestCase
from .dal import Dal


class TestDal(TestCase):

    def setUp(self) -> None:
        self.open_2 = builtins.open
        psycopg2.connect = mock.MagicMock()
        psycopg2.connect.cursor = mock.MagicMock()
        self.dal = Dal("Testing")

    def test_execute_query(self):
        self.dal.connection.cursor().fetchall.return_value = ['Stacy']
        results = self.dal.execute_query("select 1", "test parameter")
        self.dal.connection.cursor().execute.assert_called_with('select 1', 'test parameter')
        self.assertEqual(results[0], "Stacy")

    @mock.patch("builtins.open", create=False)
    def test_execute_file(self, mock_open):
        mock_open.side_effect = [mock.mock_open(read_data="select 1;").return_value]
        self.dal.execute_file("/file_test", "test parameter")
        self.dal.connection.cursor().execute.assert_called_with('select 1;', 'test parameter')

    def test_execute_cmd(self):
        self.dal.execute_cmd("select 1;", "test parameter")
        self.dal.connection.cursor().execute.assert_called_with('select 1;', 'test parameter')

    # Testing rowcount returned as expected
    @mock.patch("builtins.open", create=False)
    def test_copy_to_table(self, mock_open):
        self.dal.connection.cursor().rowcount = 1234

        rowcount = self.dal.copy_to_table("test_table_name", "/file/path/test.csv", True, True, ",", "")
        self.assertEqual(rowcount, 1234)
        self.dal.connection.cursor().copy_expert.assert_called_with(
            """copy public.test_table_name 
            from stdin with  delimiter ',' csv header encoding 'utf8'  ;""", mock.ANY)
        assert self.dal.connection.commit.called

    # Testing columns list was placed as expected
    @mock.patch("builtins.open", create=False)
    def test_copy_to_table_columns_list(self, mock_open):
        self.dal.connection.cursor().fetchall.return_value = [("column_a",), ("column_b",), ("column_c",), ("column_d",), ]
        self.dal.copy_to_table("test_table_name", "/file/path/test.csv", True, True, "|", "", "column_e")
        self.dal.connection.cursor().copy_expert.assert_called_with(
            """copy public.test_table_name (column_a,column_b,column_c,column_d)
            from stdin with  delimiter '|' csv header encoding 'utf8'  ;""", mock.ANY)
        assert self.dal.connection.commit.called
        mock.MagicMock().reset_mock()

    # Testing encoding was placed as expected
    @mock.patch("builtins.open", create=False)
    def test_copy_to_table_encoding(self, mock_open):
        self.dal.copy_to_table("test_table_name", "/file/path/test.csv", True, True, "|", "", encoding="LATIN1")
        self.dal.connection.cursor().copy_expert.assert_called_with(
            """copy public.test_table_name 
            from stdin with  delimiter '|' csv header encoding 'LATIN1'  ;""", mock.ANY)
        assert self.dal.connection.commit.called

    def test_switch_tables(self):
        expected_query = """drop table if exists public.test_table_dest_old; 
                    alter table if exists public.test_table_dest rename to test_table_dest_old; 
                    alter table if exists public.test_table_src rename to test_table_dest;"""
        self.dal.switch_tables("public", "test_table_src", "test_table_dest", "old")
        self.dal.connection.cursor().execute.assert_called_with(expected_query, None)

    def test_commit(self):
        self.dal.commit()
        assert self.dal.connection.commit.called

    def test_close(self):
        self.dal.close()
        assert self.dal.connection.close.called
        assert self.dal.connection.commit.called

    def tearDown(self) -> None:
        self.open_2 = builtins.open
        mock.MagicMock().reset_mock()


if __name__ == '__main__':
    unittest.main()
