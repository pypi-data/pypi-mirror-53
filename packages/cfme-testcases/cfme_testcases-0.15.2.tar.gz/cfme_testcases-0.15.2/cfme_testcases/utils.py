"""
Utils for CLI.
"""

import datetime
import json
import logging
import os

from box import Box
from dump2polarion import utils as d2p_utils

from cfme_testcases import consts
from cfme_testcases.exceptions import TestcasesException

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)

SUBMIT_ARGS = ("testrun_id", "user", "password", "no_verify", "verify_timeout", "dry_run")


class XMLsContainer:
    """Container for generated XMLs."""

    __slots__ = tuple(consts.OUT_FILES) + ("imported", "processed")

    def __init__(self):
        for prop in consts.OUT_FILES:
            setattr(self, prop, None)
        self.imported = set()
        self.processed = set()


def get_submit_args(args, **defaults):
    """Gets arguments for the `submit_and_verify` method."""
    submit_args = {}
    for item in SUBMIT_ARGS:
        value = args.get(item) or defaults.get(item)
        if value is not None:
            submit_args[item] = value
    return Box(submit_args, frozen_box=True, default_box=True)


def get_job_logname(file_type, output_dir):
    """Returns filename for saving the log file."""
    return get_filename(file_type, output_dir, "job", "log")


def get_import_file_name(file_type, output_dir):
    """Generates filename for saving XML output."""
    return get_filename(file_type, output_dir, "import", "xml")


def get_filename(file_type, output_dir, prefix, ext):
    """Generates filename for file saving."""
    rec = consts.OUT_FILES.get(file_type)
    if not rec:
        raise TestcasesException("Unknown file type `{}`".format(file_type))
    key, file_name = rec

    key = "-{}".format(key) if key else ""
    file_name = "-{}".format(file_name) if file_name else ""
    stamp = "{:%Y%m%d%H%M%S}".format(datetime.datetime.now())

    return os.path.join(output_dir, "{}-{}{}{}.{}".format(prefix, stamp, key, file_name, ext))


def save_xmls(output_dir, xmls_container):
    """Saves the generated XML files if instructed to do so."""
    output_dir = output_dir or os.curdir

    for file_type in consts.OUT_FILES:
        xml_file = getattr(xmls_container, file_type, None)
        if xml_file is not None:
            d2p_utils.write_xml_root(xml_file, get_import_file_name(file_type, output_dir))


def check_lookup_methods(config):
    """Checks that lookup methods are configured correctly.

    Returns lookup method.
    """
    xunit_props = config.get("xunit_import_properties") or {}
    xunit_lookup = xunit_props.get("polarion-lookup-method") or "id"

    testcase_props = config.get("testcase_import_properties") or {}
    testcase_lookup = testcase_props.get("lookup-method") or "id"

    if xunit_lookup != testcase_lookup:
        raise TestcasesException("The lookup-method for test cases and XUnit must be the same.")

    if xunit_lookup != "custom":
        return xunit_lookup

    xunit_custom = xunit_props.get("polarion-custom-lookup-method-field-id")
    testcase_custom = testcase_props.get("polarion-custom-lookup-method-field-id")
    if xunit_custom != testcase_custom:
        raise TestcasesException(
            "The polarion-custom-lookup-method-field-id for test cases and "
            "XUnit must be the same."
        )

    return xunit_lookup


def load_json_file(json_file):
    """Returns content of JSON file."""
    with open(json_file, encoding="utf-8") as input_json:
        return json.load(input_json)
