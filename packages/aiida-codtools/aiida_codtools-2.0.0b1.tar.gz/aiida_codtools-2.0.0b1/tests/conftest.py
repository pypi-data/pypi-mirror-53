# pylint: disable=redefined-outer-name
"""Initialise a text database and profile for pytest."""
from __future__ import absolute_import

import io
import os
import shutil
import tempfile

import pytest

from aiida.manage.fixtures import fixture_manager


@pytest.fixture(scope='session')
def fixture_environment():
    """Setup a complete AiiDA test environment, with configuration, profile, database and repository."""
    with fixture_manager() as manager:
        yield manager


@pytest.fixture(scope='session')
def fixture_work_directory():
    """Return a temporary folder that can be used as for example a computer's work directory."""
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)


@pytest.fixture(scope='function')
def fixture_sandbox_folder():
    """Return a `SandboxFolder`."""
    from aiida.common.folders import SandboxFolder
    with SandboxFolder() as folder:
        yield folder


@pytest.fixture(scope='function')
def fixture_computer_localhost(fixture_work_directory):
    """Return a `Computer` instance mocking a localhost setup."""
    from aiida.orm import Computer
    computer = Computer(
        name='localhost',
        hostname='localhost',
        transport_type='local',
        scheduler_type='direct',
        workdir=fixture_work_directory
    ).store()
    computer.set_default_mpiprocs_per_machine(1)
    yield computer


@pytest.fixture(scope='function')
def fixture_database(fixture_environment):
    """Clear the database after each test."""
    yield
    fixture_environment.reset_db()


@pytest.fixture
def generate_code_localhost():
    """Return a `Code` instance configured to run calculations of given entry point on localhost `Computer`."""

    def _generate_code_localhost(entry_point_name, computer):
        from aiida.orm import Code
        plugin_name = entry_point_name
        remote_computer_exec = [computer, '/bin/true']
        return Code(input_plugin_name=plugin_name, remote_computer_exec=remote_computer_exec)

    return _generate_code_localhost


@pytest.fixture
def generate_calc_job():
    """Fixture to construct a new `CalcJob` instance and call `prepare_for_submission` for testing `CalcJob` classes.

    The fixture will return the `CalcInfo` returned by `prepare_for_submission` and the temporary folder that was
    passed to it, into which the raw input files will have been written.
    """

    def _generate_calc_job(folder, entry_point_name, inputs=None):
        """Fixture to generate a mock `CalcInfo` for testing calculation jobs."""
        from aiida.engine.utils import instantiate_process
        from aiida.manage.manager import get_manager
        from aiida.plugins import CalculationFactory

        manager = get_manager()
        runner = manager.get_runner()

        process_class = CalculationFactory(entry_point_name)
        process = instantiate_process(runner, process_class, **inputs)

        calc_info = process.prepare_for_submission(folder)

        return process, calc_info

    return _generate_calc_job


@pytest.fixture
def generate_calc_job_node():
    """Fixture to generate a mock `CalcJobNode` for testing parsers."""

    def _generate_calc_job_node(entry_point_name, computer, test_name, attributes=None):
        """Fixture to generate a mock `CalcJobNode` for testing parsers.

        :param entry_point_name: entry point name of the calculation class
        :param computer: a `Computer` instance
        :param test_name: relative path of directory with test output files in the `fixtures/{entry_point_name}` folder
        :param attributes: any optional attributes to set on the node
        :return: `CalcJobNode` instance with an attached `FolderData` as the `retrieved` node
        """
        from aiida.common.links import LinkType
        from aiida.orm import CalcJobNode, FolderData
        from aiida.plugins.entry_point import format_entry_point_string

        entry_point = format_entry_point_string('aiida.calculations', entry_point_name)

        node = CalcJobNode(computer=computer, process_type=entry_point)
        node.set_attribute('input_filename', 'aiida.in')
        node.set_attribute('output_filename', 'aiida.out')
        node.set_attribute('error_filename', 'aiida.err')
        node.set_option('resources', {'num_machines': 1, 'num_mpiprocs_per_machine': 1})
        node.set_option('max_wallclock_seconds', 1800)

        if attributes:
            node.set_attribute_many(attributes)

        node.store()

        basepath = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(basepath, 'parsers', 'fixtures', entry_point_name[len('codtools.'):], test_name)

        retrieved = FolderData()
        retrieved.put_object_from_tree(filepath)
        retrieved.add_incoming(node, link_type=LinkType.CREATE, link_label='retrieved')
        retrieved.store()

        return node

    return _generate_calc_job_node


@pytest.fixture
def generate_parser():
    """Fixture to load a parser class for testing parsers."""

    def _generate_parser(entry_point_name):
        """Fixture to load a parser class for testing parsers.

        :param entry_point_name: entry point name of the parser class
        :return: the `Parser` sub class
        """
        from aiida.plugins import ParserFactory
        return ParserFactory(entry_point_name)

    return _generate_parser


@pytest.fixture
def generate_cif_data():
    """Return a `CifData` instance for the given element a file for which should exist in `tests/fixtures/cif`."""

    def _generate_cif_data(element):
        """Return `UpfData` node."""
        from aiida.orm import CifData

        filename = os.path.join('tests', 'fixtures', 'cif', '{}.cif'.format(element))
        filepath = os.path.abspath(filename)

        with io.open(filepath, 'r') as handle:
            cif = CifData(file=handle.name)

        return cif

    return _generate_cif_data
