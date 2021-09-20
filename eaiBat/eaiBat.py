# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
import string
from collections import OrderedDict

from logging import getLogger
from requests.models import Response
from behave.model import Step
from urllib.parse import urlparse

from .evidenceGenerators.MdEvidence import generate_md_evidence
from .evidenceGenerators.DocxEvidence import generate_docx_evidence

log = getLogger(__name__)


class EaiBat:
    def __init__(self):
        self.__step = None
        self.__history = OrderedDict()
        self.__evidence_location = None
        self.__url = None

    @property
    def url(self) -> str:
        """The current base url"""
        return self.__url

    @url.setter
    def url(self, url: str):
        """URL contains http, https or ftp scheme and only ASCII letters, digits and - or . or :"""
        if not isinstance(url, str) or not url:
            raise AttributeError("url must be a non-empty string")
        parsed_url = urlparse(url)
        allowed_characters = set(string.ascii_letters + string.digits + '-.:')
        allowed_scheme = ['http', 'https', 'ftp']
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Url need a scheme and a net location")
        if not set(allowed_characters).issuperset(parsed_url.netloc):
            raise ValueError(f"Url should not contains characters out of {allowed_characters}")
        if parsed_url.scheme not in allowed_scheme:
            raise ValueError(f"Url scheme should be in {allowed_scheme}")
        self.__url = url

    @property
    def step(self) -> tuple:
        """
        The actual key in order to record events in the history
        :return: tuple
        """
        return self.__step

    @step.setter
    def step(self, step):
        """
        Set the history key using two elements either using a Behave's step object
        or a size 2 tuple of string or int
        :param step: a tuple or behave's step
        """
        if not isinstance(step, tuple) and not isinstance(step, Step):
            raise AttributeError("Step is either a behave.model.step or a tuple")
        if isinstance(step, tuple) and len(step) != 2:
            raise AttributeError("Step is a length 2 tuple")
        if isinstance(step, tuple) and not all(
            isinstance(item, (str, int)) for item in step
        ):
            raise AttributeError("Step's tuple contains int or string")

        self.__step = step if isinstance(step, tuple) else (step.keyword, step.name)

    @property
    def history(self) -> OrderedDict:
        return self.__history

    def clear_history(self):
        self.__history = OrderedDict()

    @property
    def evidence_location(self) -> str:
        return self.__evidence_location

    @evidence_location.setter
    def evidence_location(self, evidence_location: str):
        self.__evidence_location = evidence_location

    def push_event(self, event):
        """Tuple is for external file with first element the file path, second the type (img or
        txt or bin)"""
        if not isinstance(event, Response) \
                and not isinstance(event, str) \
                and not isinstance(event, dict) \
                and not (isinstance(event, tuple) and len(event) == 2):
            raise AttributeError("Event is either a string or a dictionary or "
                                 "a length 2 tuple or a requests's Response object")
        if self.__step in self.__history:
            self.__history[self.__step].append(event)
        else:
            self.__history[self.__step] = [event]

    def create_evidence(self, filename: str, evidence_type: str):
        if evidence_type.casefold() == "markdown":
            generate_md_evidence(self.evidence_location, filename, self.history)
        elif evidence_type.casefold() == "word":
            generate_docx_evidence(self.evidence_location, filename, self.history)
        else:
            log.warning(f"No generator for {evidence_type}")
