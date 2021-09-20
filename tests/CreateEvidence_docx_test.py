# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
import os
import requests
import requests_mock

from freezegun import freeze_time
from shutil import copyfile
from eaiBat import EaiBat
from tests.helpers import hash_file


class TestCreateEvidenceDocx:
    def setup_class(self):
        self.my_eai = EaiBat()

    @freeze_time("2021-02-08 08:00:00")
    def test_request(self, tmp_path):
        self.my_eai.evidence_location = tmp_path
        with requests_mock.Mocker() as mock:
            mock.get("https://mock.com",
                     status_code=200,
                     json={"one": "one", "two": ["one", "two"]},
                     headers={"Content-Type": "application/json"})
            response = requests.get("https://mock.com")
            self.my_eai.step = ("Given", "please follow")
            self.my_eai.push_event(response)
            self.my_eai.create_evidence("TEST1.docx", "word")

            expected = hash_file(os.path.abspath(
                f"{os.getcwd()}/tests/resources/test_one_json.docx"))
            produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.docx")
            assert expected == produced

        with requests_mock.Mocker() as mock:
            mock.get("https://mock.com",
                     status_code=200,
                     text="<xml><one>one</one><two><item>one</item><item>two</item></two></xml>",
                     headers={"Content-Type": "application/json"})
            response = requests.get("https://mock.com")
            self.my_eai.step = ("When", "last")
            self.my_eai.push_event(response)
            self.my_eai.create_evidence("TEST2.docx", "word")
            expected = hash_file(os.path.abspath(
                f"{os.getcwd()}/tests/resources/test_one_json_one_xml.docx"))
            produced = hash_file(f"{self.my_eai.evidence_location}/TEST2.docx")
            assert expected == produced

    @freeze_time("2021-02-08 08:00:00")
    def test_text(self, tmp_path):
        self.my_eai.clear_history()
        self.my_eai.evidence_location = tmp_path
        self.my_eai.step = ("Given", "please follow")
        self.my_eai.push_event("A silly text")
        self.my_eai.create_evidence("TEST1.docx", "word")

        expected = hash_file(os.path.abspath(f"{os.getcwd()}/tests/resources/test_one_text.docx"))
        produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.docx")
        assert expected == produced

    @freeze_time("2021-02-08 08:00:00")
    def test_dictionary(self, tmp_path):
        self.my_eai.clear_history()
        self.my_eai.evidence_location = tmp_path
        self.my_eai.step = ("Given", "please follow")
        self.my_eai.push_event({"element1": "an image", "element2": "ringing bell"})
        self.my_eai.create_evidence("TEST1.docx", "word")

        expected = hash_file(os.path.abspath(
            f"{os.getcwd()}/tests/resources/test_one_dictionary.docx"))
        produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.docx")
        assert expected == produced

    @freeze_time("2021-02-08 08:00:00")
    def test_file(self, tmp_path):
        copyfile("tests/resources/a_text.txt", f"{tmp_path}/a_text.txt")
        self.my_eai.clear_history()
        self.my_eai.evidence_location = tmp_path
        self.my_eai.step = ("Given", "please follow")
        self.my_eai.push_event(("a_text.txt", "txt"))
        self.my_eai.create_evidence("TEST1.docx", "word")

        expected = hash_file(os.path.abspath(
            f"{os.getcwd()}/tests/resources/test_one_file.docx"))
        produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.docx")
        assert expected == produced

    @freeze_time("2021-02-08 08:00:00")
    def test_dictionary_nested(self, tmp_path):
        self.my_eai.clear_history()
        self.my_eai.evidence_location = tmp_path
        self.my_eai.step = ("Given", "please follow")
        self.my_eai.push_event({"dictionary": {"element1": "test", "element2": {"nested": "one"},
                                               "list": ["one", "two", ["three", "four"]],
                                               "element3": {"nested":
                                                            {"nest":
                                                             {"renested": "value"}}}}})
        self.my_eai.create_evidence("TEST1.docx", "word")
        expected = hash_file(os.path.abspath(
            f"{os.getcwd()}/tests/resources/test_nested_structure.docx"))
        produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.docx")
        assert expected == produced
