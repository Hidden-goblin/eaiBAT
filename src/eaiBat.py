# Author: eric.aivayan@free.fr
# Licence: under GPLv3
import json
import os
import string
from collections import OrderedDict
from io import TextIOWrapper
from pathlib import Path
from shutil import copyfile, move
from typing import TextIO
from xml.dom import minidom

from behave.model import Step
from requests.models import Response
from urllib.parse import urlparse


class EaiBat:
    def __init__(self):
        self.__step = None
        self.__history = OrderedDict()
        self.__evidence_location = None
        self.__url = None

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str):
        if not isinstance(url, str) or not url:
            raise AttributeError("url must be a non-empty string")
        parsed_url = urlparse(url)
        allowed_characters = set(string.ascii_letters + string.digits + '-.')
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
        return self.__step

    @step.setter
    def step(self, step):
        if not isinstance(step, tuple) and not isinstance(step, Step):
            raise AttributeError("Step is either a behave.model.step or a tuple")
        if isinstance(step, tuple) and len(step) != 2:
            raise AttributeError("Step is a length 2 tuple")
        if isinstance(step, tuple) and not all([isinstance(item, str) or isinstance(item, int)
                                                for item in step]):
            raise AttributeError("Step's tuple contains int or string")

        if isinstance(step, tuple):
            self.__step = step
        else:
            self.__step = (step.keyword, step.name)

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
        with open(f"{self.evidence_location}/{filename}", "w", encoding="utf-8") as evidence:
            evidence.write(f"# {filename}\n")
            external_file = None
            for step, events in self.history.items():
                evidence.write(f"## {step[0]}: {step[1]}\n")
                for event in events:
                    if isinstance(event, str):
                        evidence.write(f"{event}\n")
                    elif isinstance(event, tuple):
                        if external_file is None:
                            external_file = Path(f"{self.evidence_location}/"
                                                 f"{filename.split('.')[0]}_file")
                            os.mkdir(external_file)

                        EaiBat._file_to_evidence(evidence, event, external_file)
                    elif isinstance(event, dict):
                        EaiBat._dict_to_evidence(evidence, event)
                    else:
                        EaiBat._response_to_evidence(evidence, event)

    @staticmethod
    def _file_to_evidence(file_stream: TextIO, event: tuple, destination_folder: Path):
        file_path = Path(f"{destination_folder.parent}/{event[0]}")
        if file_path.exists() and file_path.is_file():
            move(file_path, f"{destination_folder}/{file_path.name}")
            file_stream.write(f"{event[1]} file is located "
                              f"at {destination_folder}/{file_path.name}")
        else:
            file_stream.write(f"{event[1]} file is located at {event[0]} (but not found)")

    @staticmethod
    def _dict_to_evidence(file_stream: TextIO, event: dict):
        for key, value in event.items():
            file_stream.write(f"### {key}\n")
            if isinstance(value, Response):
                EaiBat._response_to_evidence(file_stream, value, sub_level=True)
            else:
                file_stream.write(f"{value}\n\n")

    @staticmethod
    def _response_to_evidence(file_stream: TextIO,
                              event: Response,
                              sub_level: bool = False):
        if sub_level:
            section_number = "#### "
        else:
            section_number = "### "

        file_stream.write(f"{section_number}URL\n"
                          f"{event.url}\n"
                          f"{section_number}VERB\n"
                          f"{event.request.method}\n"
                          f"{section_number}Request headers\n"
                          f"{event.request.headers}\n")
        if event.request.body is not None:
            file_stream.write(f"{section_number}Body\n"
                              f"{event.request.body}\n")
        file_stream.write(f"{section_number}Response status code\n"
                          f"{event.status_code}\n")
        file_stream.write(f"{section_number}Response headers\n"
                          f"{event.headers}\n")
        try:
            response = json.dumps(event.json(), indent="  ")
            file_stream.write(f"{section_number} Response content\n\n"
                              f"~~~json\n{response}\n~~~\n\n")
            return
        except Exception as exception:
            pass

        try:
            response = minidom.parseString(event.text).toprettyxml(indent="   ")
            file_stream.write(f"{section_number} Response content\n\n"
                              f"~~~xml\n{response}\n~~~\n\n")
            return
        except Exception as exception:
            pass

        file_stream.write(f"{section_number} Response content\n"
                          f"{event.text}\n")

