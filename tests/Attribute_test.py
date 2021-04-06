# Author: eric.aivayan@free.fr
# Licence: under GPLv3
import pytest
import string
from behave.model import Step
from src.eaiBat import EaiBat


class TestAttribute:
    def setup_class(self):
        self.my_eai = EaiBat()

    def test_url(self):
        # Nominal case
        self.my_eai.url = "http://test.com"
        assert self.my_eai.url == "http://test.com"

    def test_url_not_a_string(self):
        with pytest.raises(AttributeError) as att_error:
            self.my_eai.url = 4
        assert str(att_error.value) == "url must be a non-empty string"

        with pytest.raises(AttributeError) as att_error:
            self.my_eai.url = ""
        assert str(att_error.value) == "url must be a non-empty string"

    def test_url_missing_scheme(self):
        with pytest.raises(ValueError) as val_error:
            self.my_eai.url = "test.com"

        assert str(val_error.value) == "Url need a scheme and a net location"

    def test_url_missing_netloc(self):
        with pytest.raises(ValueError) as val_error:
            self.my_eai.url = "http://"

        assert str(val_error.value) == "Url need a scheme and a net location"

    def test_url_allowed_characters(self):
        with pytest.raises(ValueError) as val_error:
            self.my_eai.url = "http://éa+(£test.com"
        allowed_characters = set(string.ascii_letters + string.digits + '-.')
        assert str(val_error.value) == f"Url should not contains characters out " \
                                       f"of {allowed_characters}"

    def test_url_allowed_scheme(self):
        with pytest.raises(ValueError) as val_error:
            self.my_eai.url = "file://test.txt"

        assert str(val_error.value) == "Url scheme should be in ['http', 'https', 'ftp']"

    def test_step(self):
        my_step = Step("toto.txt", 3, "Given", "Given", "I am under test")
        self.my_eai.step = my_step
        assert self.my_eai.step == ("Given", "I am under test")

        self.my_eai.step = (1, "I am under test")
        assert self.my_eai.step == (1, "I am under test")

        self.my_eai.step = ("element", "I am under test")
        assert self.my_eai.step == ("element", "I am under test")

    def test_step_not_correct_type(self):
        with pytest.raises(AttributeError) as att_error:
            self.my_eai.step = "toto"

        assert str(att_error.value) == "Step is either a behave.model.step or a tuple"

    def test_step_not_a_valid_tuple(self):
        with pytest.raises(AttributeError) as att_error:
            self.my_eai.step = ("one", "two", "three")

        assert str(att_error.value) == "Step is a length 2 tuple"

        with pytest.raises(AttributeError) as att_error:
            self.my_eai.step = (("one", "one"), "three")

        assert str(att_error.value) == "Step's tuple contains int or string"
