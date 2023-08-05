"""
Methods for generating and working with testsuites XML files.
"""

import datetime
import logging

from dump2polarion import utils as d2p_utils
from dump2polarion.exporters import xunit_exporter

from cfme_testcases import utils
from cfme_testcases.exceptions import TestcasesException

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


def gen_testsuites_xml_str(config, testrun_id, tests_data_json, transform_func=None):
    """Generates the testsuites XML string."""
    assert testrun_id
    try:
        results = utils.load_json_file(tests_data_json)["results"]
    except Exception as err:
        raise TestcasesException("Cannot load results from `{}`: {}".format(tests_data_json, err))
    testsuites_data = xunit_exporter.ImportedData(results, testrun_id)
    testsuites = xunit_exporter.XunitExport(testrun_id, testsuites_data, config, transform_func)
    return testsuites.export()


def get_testsuites_xml_root(config, tests_data_json, transform_func=None, testrun_id=None):
    """Returns content of testsuite XML file for xunit importer."""
    testrun_id = (
        testrun_id
        or config.get("_testrun_id")
        or "IMPORT_{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
    )
    testsuites_str = gen_testsuites_xml_str(
        config, testrun_id, tests_data_json, transform_func=transform_func
    )
    return d2p_utils.get_xml_root_from_str(testsuites_str)
