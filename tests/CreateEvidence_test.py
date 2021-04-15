# Author: eric.aivayan@free.fr
# Licence: under GPLv3
import os
from shutil import copyfile

import requests
import requests_mock
from src.eaiBat import EaiBat
from tests.helpers import hash_file


class TestCreateEvidence:
    def setup_class(self):
        self.my_eai = EaiBat()

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
            self.my_eai.create_evidence("TEST1.md", "markdown")

            expected = hash_file(os.path.abspath(f"{os.getcwd()}/tests/resources/test_one_json.md"))
            produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.md")
            assert expected == produced

        with requests_mock.Mocker() as mock:
            mock.get("https://mock.com",
                     status_code=200,
                     text="<xml><one>one</one><two><item>one</item><item>two</item></two></xml>",
                     headers={"Content-Type": "application/json"})
            response = requests.get("https://mock.com")
            self.my_eai.step = ("When", "last")
            self.my_eai.push_event(response)
            self.my_eai.create_evidence("TEST2.md", "markdown")
            expected = hash_file(os.path.abspath(
                f"{os.getcwd()}/tests/resources/test_one_json_one_xml.md"))
            produced = hash_file(f"{self.my_eai.evidence_location}/TEST2.md")
            assert expected == produced

    def test_text(self, tmp_path):
        self.my_eai.clear_history()
        self.my_eai.evidence_location = tmp_path
        self.my_eai.step = ("Given", "please follow")
        self.my_eai.push_event("A silly text")
        self.my_eai.create_evidence("TEST1.md", "markdown")

        expected = hash_file(os.path.abspath(f"{os.getcwd()}/tests/resources/test_one_text.md"))
        produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.md")
        assert expected == produced

    def test_dictionary(self, tmp_path):
        self.my_eai.clear_history()
        self.my_eai.evidence_location = tmp_path
        self.my_eai.step = ("Given", "please follow")
        self.my_eai.push_event({"element1": "an image", "element2": "ringing bell"})
        self.my_eai.create_evidence("TEST1.md", "markdown")

        expected = hash_file(os.path.abspath(f"{os.getcwd()}/tests/resources/test_one_dictionary.md"))
        produced = hash_file(f"{self.my_eai.evidence_location}/TEST1.md")
        assert expected == produced

    def test_file(self, tmp_path):
        copyfile("tests/resources/a_text.txt", f"{tmp_path}/a_text.txt")
        self.my_eai.clear_history()
        self.my_eai.evidence_location = tmp_path
        self.my_eai.step = ("Given", "please follow")
        self.my_eai.push_event(("a_text.txt", "markdown"))
        self.my_eai.create_evidence("TEST1.md", "markdown")
