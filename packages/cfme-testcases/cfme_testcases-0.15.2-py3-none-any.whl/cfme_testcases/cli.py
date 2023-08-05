"""
Main CLI.
"""

import argparse
import logging

from dump2polarion import configuration
from dump2polarion import utils as d2p_utils
from dump2polarion.dumper_cli import process_args

from cfme_testcases import pytest_collect, requirements, submit, testcases, testsuites, utils
from cfme_testcases.collector import xmls_collector
from cfme_testcases.exceptions import Dump2PolarionException, NothingToDoException

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


def get_args(args=None):
    """Get command line arguments."""
    parser = argparse.ArgumentParser(description="cfme-testcases")
    parser.add_argument("-t", "--testrun-id", help="Polarion test run id")
    parser.add_argument("-o", "--output_dir", help="Directory for saving generated XML files")
    parser.add_argument(
        "-n", "--no-submit", action="store_true", help="Don't submit generated XML files"
    )
    parser.add_argument(
        "--testrun-init", action="store_true", help="Create and initialize new testrun"
    )
    parser.add_argument("--testrun-title", help="Title to set for the new testrun")
    parser.add_argument(
        "--data-in-code",
        action="store_true",
        help="Source code is an authoritative source of data.",
    )
    parser.add_argument("--user", help="Username to use to submit to Polarion")
    parser.add_argument("--password", help="Password to use to submit to Polarion")
    parser.add_argument("--tests-data", help="Path to JSON file with tests data")
    parser.add_argument("--config", help="Path to polarion_tools config YAML")
    parser.add_argument("--dry-run", action="store_true", help="Dry run, don't update anything")
    parser.add_argument("--no-requirements", action="store_true", help="Don't import requirements")
    parser.add_argument(
        "--no-testcases-update", action="store_true", help="Don't update existing testcases"
    )
    parser.add_argument("--no-verify", action="store_true", help="Don't verify import success")
    parser.add_argument(
        "--verify-timeout",
        type=int,
        default=900,
        metavar="SEC",
        help="How long to wait (in seconds) for verification of submission success"
        " (default: %(default)s)",
    )
    parser.add_argument(
        "--use-svn", metavar="SVN_REPO", help="Path to SVN repo with Polarion project"
    )
    parser.add_argument(
        "--mark-missing", action="store_true", help="Mark testcases missing in source code"
    )
    parser.add_argument("--log-level", help="Set logging to specified level")
    parsed = parser.parse_args(args)

    if parsed.mark_missing and not (parsed.use_svn and parsed.data_in_code):
        parser.error("The --mark-missing argument requires --use-svn and --data-in-code")
    if parsed.testrun_title and not parsed.testrun_init:
        parser.error("The --testrun-title argument requires --testrun-init")

    return parsed


def process_config(args, config):
    """Makes all configuration data available under config."""
    testrun_id = args.testrun_id or d2p_utils.get_testrun_id_config(config)
    submit_args = utils.get_submit_args(args, testrun_id=testrun_id) if not args.no_submit else {}

    config["_args"] = args
    config["_submit_args"] = submit_args
    config["_testrun_id"] = testrun_id

    return config


def update_testcases(
    args,
    config,
    requirements_data=None,
    requirements_transform_func=None,
    xunit_transform_func=None,
    testcases_transform_func=None,
):
    """Testcases update main function."""
    assert isinstance(requirements_data, list) if requirements_data is not None else True

    args = process_args(args)
    config = process_config(args, config)

    try:
        __, tests_data_json = pytest_collect.collect(config.get("pytest_collect"), args.tests_data)

        requirements_root = None

        if not args.no_requirements:
            requirements_root = requirements.get_requirements_xml_root(
                config,
                tests_data_json,
                requirements_data=requirements_data,
                transform_func=requirements_transform_func,
            )

        testsuites_root = testsuites.get_testsuites_xml_root(
            config, tests_data_json, transform_func=xunit_transform_func
        )
        testcases_root = testcases.get_testcases_xml_root(
            config,
            tests_data_json,
            set_requirements=requirements_root is not None,
            transform_func=testcases_transform_func,
        )

        xmls_container = xmls_collector.get_xmls(config, testsuites_root, testcases_root)
        xmls_container.requirements = requirements_root

        if args.no_submit or args.output_dir:
            utils.save_xmls(args.output_dir, xmls_container)

        submit.submit_all(config, xmls_container, args.output_dir)
    except NothingToDoException as einfo:
        logger.info(einfo)
        return 0
    except Dump2PolarionException as err:
        logger.fatal(err)
        return 1
    return 0


def main(
    args=None,
    requirements_transform_func=None,
    xunit_transform_func=None,
    testcases_transform_func=None,
):
    """Main function for CLI."""
    args = get_args(args)
    d2p_utils.init_log(args.log_level)

    try:
        config = configuration.get_config(args.config)
    except Dump2PolarionException as err:
        logger.fatal(err)
        return 1

    return update_testcases(
        args,
        config,
        requirements_transform_func=requirements_transform_func,
        xunit_transform_func=xunit_transform_func,
        testcases_transform_func=testcases_transform_func,
    )
