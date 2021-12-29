# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
import os
import requests
import requests_mock

from shutil import copyfile
from freezegun import freeze_time

from eaiBat import EaiBat
from tests.helpers import hash_file


class TestDocxInsertTextSqlFile:
    def setup_class(self):
        self.my_eai = EaiBat()

    @freeze_time("2021-02-08 08:00:00")
    def test_sql_file(self, tmp_path):
        copyfile("tests/resources/a_sql_script.sql", f"{tmp_path}/a_sql_script.sql")
        self.my_eai.clear_history()
        self.my_eai.evidence_location = tmp_path
        self.my_eai.step = ("Given", "please follow")
        self.my_eai.push_event(("a_sql_script.sql", "sql"))
        self.my_eai.push_event("A very helpful text")
        self.my_eai.create_evidence("TEST1.docx", "word")

        assert (tmp_path / "included_files" / "a_sql_script.sql").exists(), ("The file has "
                                                                             "not been moved")
        expected = hash_file(os.path.abspath(
            f"{os.getcwd()}/tests/resources/test_insert_sql.docx"))
        produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.docx")
        assert expected == produced
