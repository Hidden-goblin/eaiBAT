# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
from datetime import timedelta
from logging import getLogger

log = getLogger(__name__)


def response_time_validation(context, max_time):
    """
    Valid that the response time is lower or equal to max_time
    :param context: behave.runner.context form the step definition
    :param max_time: The maximum time in milliseconds
    :return: None
    :raise AssertionError if the validation fails
    """
    try:
        time_limit = timedelta(milliseconds=float(max_time))
        assert context.response.elapsed < time_limit, "The response time is over the requirement"
        context.model.push_event(f"Response received in {context.response.elapsed}")
    except AssertionError as assertion:
        log.error(assertion.args)
        context.model.push_event("Response is over the max time.\n "
                                 f"Received in {context.response.elapsed}")
        raise AssertionError(assertion.args) from assertion


def status_code_validation(context, status: int):
    """
    Valid that the http status code is as expected
    :param context: behave.runner.context form the step definition
    :param status: int, expected status
    :return: None
    """
    try:
        assert context.response.status_code == status, ("The response status code is not "
                                                        f"as expected.\n"
                                                        f" Received {context.response.status_code}"
                                                        f" expected {status}")
        context.model.push_event("Response http status is as expected")
    except AssertionError as assertion:
        log.error(assertion.args)
        context.model.push_event("The response status code is not "
                                 f"as expected.\n"
                                 f" Received {context.response.status_code}"
                                 f" expected {status}")
        raise AssertionError(assertion.args) from assertion


def string_to_bool(input_string: str) -> bool:
    if input_string.casefold() == 'True'.casefold():
        return True
    elif input_string.casefold() == 'False'.casefold():
        return False
    else:
        raise ValueError(f"Cannot convert {input_string} to a boolean."
                         f" Expecting only True or False")


