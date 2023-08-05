# pylint: disable=missing-docstring,no-self-use,protected-access

import copy
import os
import re

from dump2polarion import utils as d2p_utils
from dump2polarion.exporters import transform

from cfme_testcases import testcases, testsuites, utils
from cfme_testcases.collector import filters, missing
from tests import conf

TESTS_JSON = os.path.join(conf.DATA_PATH, "tests_data.json")
INIT_LOG = os.path.join(conf.DATA_PATH, "job-init.log")


def get_testcases_transform(config, plugin_name):
    """Return test cases transformation function for Insights."""

    parametrize = config.get("insights_parametrize", True)
    testcase_append = plugin_name
    seen_ids = set()

    def testcase_transform(testcase):
        """Test cases transform for Insights."""
        testcase = copy.deepcopy(testcase)

        transform.setup_parametrization(testcase, parametrize)

        testcase_id = transform.get_testcase_id(testcase, testcase_append)
        testcase["id"] = testcase_id

        if parametrize and testcase_id in seen_ids:
            return None
        seen_ids.add(testcase_id)

        transform.parse_rst_description(testcase)
        transform.add_unique_runid(testcase, "id123")
        transform.add_automation_link(testcase)

        return testcase

    return testcase_transform


def get_xunit_transform(config, plugin_name):
    """Return result transformation function for Insights."""
    skip_searches = ["SKIPME:", "Skipping due to these blockers", "BZ ?[0-9]+", "GH ?#?[0-9]+"]
    skips = re.compile("(" + ")|(".join(skip_searches) + ")")

    parametrize = config.get("insights_parametrize", True)
    testcase_append = plugin_name

    def results_transform(result):
        """Results transform for Insights."""
        verdict = result.get("verdict")
        if not verdict:
            return None

        result = copy.deepcopy(result)

        transform.setup_parametrization(result, parametrize)
        transform.include_class_in_title(result)
        transform.insert_source_info(result)

        result["id"] = transform.get_testcase_id(result, testcase_append)

        verdict = verdict.strip().lower()
        # we want to submit PASS and WAIT results
        if verdict in transform.Verdicts.PASS + transform.Verdicts.WAIT:
            return result
        comment = result.get("comment")
        # ... and SKIP results where there is a good reason (blocker etc.)
        if verdict in transform.Verdicts.SKIP and comment and skips.search(comment):
            # found reason for skip
            result["comment"] = comment.replace("SKIPME: ", "").replace("SKIPME", "")
            return result
        if verdict in transform.Verdicts.FAIL and comment and "FAILME" in comment:
            result["comment"] = comment.replace("FAILME: ", "").replace("FAILME", "")
            return result
        # we don't want to report this result if here
        return None

    return results_transform


def test_filtered(config):
    fname = "testcases_updated.xml"

    testsuites_root = testsuites.get_testsuites_xml_root(
        config,
        TESTS_JSON,
        testrun_id="IMPORT123",
        transform_func=get_xunit_transform(config, "vulnerability"),
    )
    testcases_root = testcases.get_testcases_xml_root(
        config,
        TESTS_JSON,
        set_requirements=False,
        transform_func=get_testcases_transform(config, "vulnerability"),
    )

    missing_testcases = missing.get_missing_in_polarion(config, testcases_root, INIT_LOG, None)
    xmls_container = utils.XMLsContainer()
    xmls_container.testcases = testcases_root
    xmls_container.testsuites = testsuites_root
    filters.add_filtered_xmls(xmls_container, missing_testcases, data_in_code=True)
    # pylint: disable=no-member
    updated_testcases = d2p_utils.prettify_xml(xmls_container.updated_testcases)

    with open(os.path.join(conf.DATA_PATH, fname), encoding="utf-8") as input_xml:
        parsed = input_xml.read()
    assert parsed == updated_testcases
