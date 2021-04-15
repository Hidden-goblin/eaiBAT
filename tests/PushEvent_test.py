# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
import pytest
from requests.models import Response
from src.eaiBat import EaiBat


class TestPushEvent:
    def setup_class(self):
        self.my_eai = EaiBat()
        self.my_eai.step = ("Given", "first")

    def test_limited_event(self):
        error_message = ("Event is either a string or a dictionary or "
                         "a length 2 tuple or a requests's Response object")

        with pytest.raises(AttributeError) as attr_error:
            self.my_eai.push_event(3)

        assert str(attr_error.value) == error_message

        with pytest.raises(AttributeError) as attr_error:
            self.my_eai.push_event(["one", "two"])

        assert str(attr_error.value) == error_message

        with pytest.raises(AttributeError) as attr_error:
            self.my_eai.push_event(True)

        assert str(attr_error.value) == error_message

        with pytest.raises(AttributeError) as attr_error:
            self.my_eai.push_event(("one", "two", "three"))

        assert str(attr_error.value) == error_message

        with pytest.raises(AttributeError) as attr_error:
            self.my_eai.push_event(EaiBat())

        assert str(attr_error.value) == error_message

    def test_add_to_history(self):
        # New step in the history
        self.my_eai.push_event("test")
        assert self.my_eai.history == {("Given", "first"): ["test"]}

        # Existing step in the history
        self.my_eai.push_event("new test")
        assert self.my_eai.history == {("Given", "first"): ["test", "new test"]}

        # New step
        self.my_eai.step = ("Given", "second")
        self.my_eai.push_event("same test")
        assert self.my_eai.history == {("Given", "first"): ["test", "new test"],
                                       ("Given", "second"): ["same test"]}

        # Moving to the first step
        self.my_eai.step = ("Given", "first")
        self.my_eai.push_event("moving back to previous")
        assert self.my_eai.history == {("Given", "first"): ["test", "new test",
                                                            "moving back to previous"],
                                       ("Given", "second"): ["same test"]}

    def test_clear_history(self):
        assert self.my_eai.history == {("Given", "first"): ["test", "new test",
                                                            "moving back to previous"],
                                       ("Given", "second"): ["same test"]}
        self.my_eai.clear_history()
        assert self.my_eai.history == dict()

    def test_push_file_event(self):
        self.my_eai.push_event(("tests/resources/a_text.txt", "txt"))
        assert self.my_eai.history == {("Given", "first"): [("tests/resources/a_text.txt", "txt")]}
