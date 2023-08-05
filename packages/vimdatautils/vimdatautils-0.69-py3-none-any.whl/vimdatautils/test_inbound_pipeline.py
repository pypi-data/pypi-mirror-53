import builtins
import os
import psycopg2
from unittest import TestCase
from unittest.mock import MagicMock
from jinja2 import Template
from .inbound_pipeline import InboundPipeline


class TestInboundPipeline(InboundPipeline):
    def pre_load_logic(self):
        pass

    def post_load_logic(self):
        pass


class TestInbound(TestCase):

    def setUp(self):
        psycopg2.connect = MagicMock()
        psycopg2.connect.cursor = MagicMock()
        Template.render = MagicMock()
        builtins.open = builtins.open

        self.inbound = TestInboundPipeline("vimdatautils/test_config.json", "test")
        self.inbound.aws = MagicMock()
        self.inbound.dal = MagicMock()
        self.inbound.execute_jinja_file = MagicMock()

    def test_download_file(self):
        self.inbound.download_files(self.inbound.config.download_s3_files)
        self.inbound.execute()
        assert self.inbound.aws.download_latest_file.called

    def test_rename_tables(self):
        self.inbound.rename_tables(self.inbound.sync_date, self.inbound.config.tables_to_load)
        assert self.inbound.dal.switch_tables.called

    def test_load_data(self):
        os.path.isfile = MagicMock()
        self.inbound.load_data(self.inbound.config.local_dir, self.inbound.config.tables_to_load, self.inbound.scripts_location, self.inbound.sync_date)
        assert self.inbound.dal.copy_to_table.called

    def test_cleanup(self):
        self.inbound.dal.execute_cmd = MagicMock()
        os.system = MagicMock()
        self.inbound.cleanup(self.inbound.config, self.inbound.sync_date)
        assert self.inbound.dal.execute_cmd.called
        assert os.system.called


if __name__ == '__main__':
    unittest.main()
