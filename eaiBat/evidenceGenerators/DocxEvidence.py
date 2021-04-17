# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
import os
import json

from docx import Document
from docx.shared import Cm
from logging import getLogger
from pathlib import Path
from shutil import move
from xml.dom import minidom
from requests.models import Response

log = getLogger(__name__)


def generate_docx_evidence(evidence_folder, evidence_filename, history):
    evidence_document = Document()
    evidence_document.add_heading(evidence_filename, 0)
    external_file = None
    for step, events in history.items():
        evidence_document.add_heading(f"{step[0]}: {step[1]}", 2)
        for event in events:
            if isinstance(event, str):
                evidence_document.add_paragraph(event)
            elif isinstance(event, tuple):
                if external_file is None:
                    # Create the evidence subfolder
                    external_file = Path(f"{evidence_folder}/"
                                         f"{evidence_filename.split('.')[0]}_file")
                    os.mkdir(external_file)

                _file_to_evidence(evidence_document, event, external_file)
            elif isinstance(event, dict):
                _dict_to_evidence(evidence_document, event)
            else:
                _response_to_evidence(evidence_document, event)
    evidence_document.save(f"{evidence_folder}/{evidence_filename}")


def _file_to_evidence(docx_document: Document, event: tuple, destination_folder: Path):
    file_path = Path(f"{destination_folder.parent}/{event[0]}")
    if file_path.exists() and file_path.is_file():
        move(file_path, f"{destination_folder}/{file_path.name}")
        if event[1].casefold() == "img":
            docx_document.add_picture(file_path, width=Cm(18))
            docx_document.add_page_break()
        else:
            docx_document.add_paragraph(f"A file has been produced or retrieved within this step."
                                        f"You could see it there : '{destination_folder}/"
                                        f"{file_path.name}'")
    else:
        docx_document.add_paragraph(f"{event[1]} file is located at {event[0]} (but not found)")


def _dict_to_evidence(docx_document: Document, event: dict):
    for key, value in event.items():
        docx_document.add_heading(f"{key}", 3)
        if isinstance(value, Response):
            _response_to_evidence(docx_document, value, sub_level=True)
        else:
            docx_document.add_paragraph(value)


def _response_to_evidence(docx_document: Document,
                          event: Response,
                          sub_level: bool = False):

    section_number = 4 if sub_level else 3

    docx_document.add_heading("URL", section_number)
    docx_document.add_paragraph(str(event.url))
    docx_document.add_heading("VERB", section_number)
    docx_document.add_paragraph(str(event.request.method))
    docx_document.add_heading("Request headers", section_number)

    if event.request.body is not None:
        docx_document.add_heading("Body", section_number)
        docx_document.add_paragraph(event.request.body)

    docx_document.add_heading("Response status code", section_number)
    docx_document.add_paragraph(str(event.status_code))
    docx_document.add_heading("Response headers", section_number)
    docx_document.add_paragraph(event.headers)
    docx_document.add_heading("Response content")
    try:
        response = json.dumps(event.json(), indent="  ")
        docx_document.add_paragraph("Json response")
        docx_document.add_paragraph(response)
        return
    except Exception as exception:
        log.info(f"Response is not a json.\n Get {exception.args[0]}")

    try:
        response = minidom.parseString(event.text).toprettyxml(indent="   ")
        docx_document.add_paragraph("XML response")
        docx_document.add_paragraph(response)
        return
    except Exception as exception:
        log.info(f"Response is not a XML.\n Get {exception.args[0]}")

    docx_document.add_paragraph("Raw response")
    docx_document.add_paragraph(event.text)
