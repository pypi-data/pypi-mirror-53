import os
import tempfile
import time

import pytest

from influxdb_pytest_plugin.influxdb_components import Influxdb_Components
from influxdb_pytest_plugin.suite_result_DTO import SuiteResultDTO
from influxdb_pytest_plugin.test_result_DTO import TestResultDTO

test_result_dto_session_dict = dict()
session_dict = {'test_result_dto_session_dict': test_result_dto_session_dict}

file_path = '/test_results.txt'
first_test_time_path = '/first_test_time.txt'
db_measurement_name_for_test = 'test_result'


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    report = __multicall__.execute()
    setattr(item, "rep_" + report.when, report)
    return report


@pytest.fixture(scope='function', autouse=True)
def test_result(request, run, pytestconfig, get_influxdb, project, version, shared_directory):
    if pytestconfig.getoption('--influxdb-pytest'):
        set_shared_directory_path(str(shared_directory))
        full_file_path = shared_directory + file_path
        first_test_time_full_path = shared_directory + first_test_time_path
        test_name = request.node.nodeid
        test_result_dto_dict = session_dict.get('test_result_dto_session_dict')
        test_result_dto_dict.update({test_name: TestResultDTO()})
        test_result_dto = test_result_dto_dict.get(test_name)
        test_result_dto.set_test(test_name)
        open(full_file_path, 'a')
        set_first_test_time_in_mils(first_test_time_full_path)

        def fin():
            report_outcome = request.node.rep_call
            run_id_value = run
            project_name = project
            release_version = version

            if run_id_value is None:
                run_id_value = pytestconfig.getini('run_id')
            if project_name is None:
                project_name = pytestconfig.getini('project')
            if release_version is None:
                release_version = pytestconfig.getini('version')
            ##Setting the variables for a test
            if project_name != '':
                test_result_dto.set_project(project_name)
            if release_version != '':
                test_result_dto.set_version(release_version)
            if run_id_value != '':
                test_result_dto.set_run(run_id_value)
            test_result_dto.set_duration_sec(report_outcome.duration)
            test_result_dto.set_status(report_outcome.outcome)
            ##Saving the test results in the shared directory
            retry_count = get_retry_count(full_file_path, test_result_dto)
            test_result_dto.set_retries(retry_count)
            test_json = test_result_dto.get_test_json(db_measurement_name_for_test)
            ##Sending the test results to influxdb
            influxdb_components = session_dict.get('influxdb')
            if influxdb_components is None:
                session_dict.update({'influxdb': get_influxdb})
                influxdb_components = session_dict.get('influxdb')
            influxdb_components.get_client().write_points(test_json)

        request.addfinalizer(fin)


def pytest_exception_interact(node, call, report):
    if report.failed:
        test_name = node.nodeid
        test_result_dto = session_dict.get('test_result_dto_session_dict').get(test_name)
        if test_result_dto is not None:
            stack_trace = node.repr_failure(call.excinfo)
            stack_trace = str(stack_trace).replace('"', "'")
            test_result_dto.set_exception(stack_trace)


def pytest_configure(config):
    config.getini("run_id")
    config.getini("project")
    config.getini("version")
    config.getini("db_host")
    config.getini("db_port")
    config.getini("db_user")
    config.getini("db_password")
    config.getini("db_name")
    config.getini("project")

    if is_master(config):
        config.shared_directory = tempfile.gettempdir()


def pytest_addoption(parser):
    group = parser.getgroup('influxdb-pytest')
    group.addoption("--influxdb-pytest", action="store_true",
                    help="influxdb-pytest: enable influxdb data collection")
    parser.addoption(
        "--run_id", action="store", default=None, help="my option: run_id"
    )
    parser.addoption(
        "--db_host", action="store", default=None, help="my option: db_host"
    )
    parser.addoption(
        "--db_port", action="store", default=None, help="my option: db_port"
    )
    parser.addoption(
        "--db_user", action="store", default=None, help="my option: db_username"
    )
    parser.addoption(
        "--db_password", action="store", default=None, help="my option: db_password"
    )
    parser.addoption(
        "--db_name", action="store", default=None, help="my option: db_name"
    )
    parser.addoption(
        "--project", action="store", default=None, help="my option: project name"
    )
    parser.addoption(
        "--code_version", action="store", default=None, help="my option: version"
    )
    parser.addini(
        'run_id',
        help='my option: run_id')
    parser.addini(
        'project',
        help='my option: project')
    parser.addini(
        'version',
        help='my option: version')
    parser.addini(
        'db_host',
        help='my option: db_host')
    parser.addini(
        'db_port',
        help='my option: db_port')
    parser.addini(
        'db_name',
        help='my option: db_name')
    parser.addini(
        'db_user',
        help='my option: db_user')
    parser.addini(
        'db_password',
        help='my option: db_password')


@pytest.fixture
def run(request, pytestconfig):
    return request.config.getoption("--run_id")


@pytest.fixture
def db_host(request, pytestconfig):
    return request.config.getoption("--db_host")


@pytest.fixture
def db_port(request, pytestconfig):
    return request.config.getoption("--db_port")


@pytest.fixture
def db_user(request, pytestconfig):
    return request.config.getoption("--db_user")


@pytest.fixture
def db_password(request, pytestconfig):
    return request.config.getoption("--db_password")


@pytest.fixture
def db_name(request, pytestconfig):
    return request.config.getoption("--db_name")


@pytest.fixture
def project(request, pytestconfig):
    return request.config.getoption("--project")


@pytest.fixture
def version(request, pytestconfig):
    return request.config.getoption("--code_version")


@pytest.fixture()
def get_influxdb(pytestconfig, db_host, db_port, db_name, db_user, db_password):
    if pytestconfig.getoption('--influxdb-pytest'):
        if db_host is None:
            db_host = pytestconfig.getini("db_host")
        if db_name is None:
            db_name = pytestconfig.getini("db_name")
        if db_port is None:
            db_port = pytestconfig.getini("db_port")
        if db_port is None:
            db_port = 8086
        if db_user is None:
            db_user = pytestconfig.getini("db_user")
        if db_password is None:
            db_password = pytestconfig.getini("db_password")
        influxdb_components = Influxdb_Components(db_host, db_port, db_user, db_password, db_name)
        return influxdb_components


@pytest.fixture()
def screenshot_url(request, pytestconfig):
    current_test = request.node.nodeid

    def _foo(*args, **kwargs):
        test_result_dto = session_dict.get('test_result_dto_session_dict').get(current_test)
        if pytestconfig.getoption('--influxdb-pytest'):
            test_result_dto.set_screenshot(args[0])
        return (args, kwargs)

    return _foo


@pytest.mark.tryfirst
def pytest_collection_modifyitems(config, items):
    try:
        open('/tmp/collected_tests.txt')
    except FileNotFoundError:
        f = open('/tmp/collected_tests.txt', "a")
        f.write(str(len(items)))
        f.write('\n')
        for item in items:
            f.write(item.nodeid)
            f.write('\n')


def get_retry_count(full_path, test_result_dto):
    file = open(full_path).readlines()
    all_tests = ''
    same_test_lines = 0
    for line in file:
        all_tests += line
    if test_result_dto.get_test() not in all_tests:
        file = open(full_path, "a")
        test_json = test_result_dto.get_test_json_for_suite_level()
        file.write(str(test_json))
        file.write('\n')
        return 0
    else:
        for line in file:
            test_name_in_file = f"'{test_result_dto.get_test()}'"
            if test_name_in_file in line:
                same_test_lines += 1
                test_result_dto = TestResultDTO().parse_json_to_test_result_dto(line)
                test_result_dto.set_retries(same_test_lines)
        test_json = test_result_dto.get_test_json_for_suite_level()
        file = open(full_path, "a")
        file.write(str(test_json))
        file.write('\n')
    return test_result_dto.get_retries()


def get_total_test_count():
    collected_tests_lines = open('/tmp/collected_tests.txt').readlines()
    return int(collected_tests_lines[0])


def get_finished_tests(full_path):
    list = []
    file = open(full_path).readlines()
    total_tests_count_with_retry = 0
    tests_dict = {}
    for line in file:
        test_result_dto = TestResultDTO().parse_json_to_test_result_dto(line)
        if tests_dict.get(test_result_dto.get_test()) is None:
            tests_dict.update({test_result_dto.get_test(): test_result_dto})
        else:
            if test_result_dto.get_retries() >= tests_dict.get(test_result_dto.get_test()).get_retries():
                tests_dict[test_result_dto.get_test()] = test_result_dto
    for key in tests_dict:
        total_tests_count_with_retry += 1
        total_tests_count_with_retry += tests_dict.get(key).get_retries()
    list.append(tests_dict)
    list.append(total_tests_count_with_retry)
    return list


def get_suite_results_object(finished_tests_dict):
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    total_retries = 0
    duration_sec = 0
    suite_results = SuiteResultDTO()
    for test_name in finished_tests_dict:
        real_test = finished_tests_dict.get(test_name)
        if real_test.get_status() == 'passed':
            total_passed += 1
        if real_test.get_status() == 'failed':
            total_failed += 1
        if real_test.get_status() == 'skipped':
            total_skipped += 1
        total_retries += real_test.get_retries()
        suite_results.set_run(real_test.get_run())
        suite_results.set_project(real_test.get_project())
        suite_results.set_version(real_test.get_version())
    suite_results.set_passed(total_passed)
    suite_results.set_failed(total_failed)
    suite_results.set_skipped(total_skipped)
    suite_results.set_duration_sec(duration_sec)
    suite_results.set_retries(total_retries)
    return suite_results


@pytest.fixture()
def shared_directory(request):
    if is_master(request.config):
        return request.config.shared_directory
    else:
        return request.config.slaveinput['shared_dir']


def pytest_configure_node(node):
    node.slaveinput['shared_dir'] = node.config.shared_directory


def is_master(config):
    return not hasattr(config, 'slaveinput')


def set_first_test_time_in_mils(full_path):
    try:
        open(full_path)
    except FileNotFoundError:
        file = open(full_path, 'w')
        file.write(str(round(time.time())))


def get_first_test_time_in_mils(full_path):
    try:
        line = open(full_path).readline()
        return int(line)
    except FileNotFoundError:
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(config, terminalreporter):
    yield
    if config.getoption('--influxdb-pytest') and len(terminalreporter.stats) > 0:
        db_host = config.getoption("--db_host")
        if db_host is None:
            db_host = config.getini("db_host")
        db_port = config.getoption('--db_port')
        if db_port is None:
            db_port = config.getini("db_port")
        if db_port is None:
            db_port = 8086
        db_user = config.getoption("--db_user")
        if db_user is None:
            db_user = config.getini("db_user")
        db_password = config.getoption("--db_password")
        if db_password is None:
            db_password = config.getini("db_password")
        db_name = config.getoption("--db_name")
        if db_name is None:
            db_name = config.getini("db_name")
        influxdb_components = Influxdb_Components(db_host, db_port, db_user, db_password, db_name)
        full_file_path = get_shared_directory_path() + file_path
        first_test_time_full_path = get_shared_directory_path() + first_test_time_path
        db_measurement_name_for_suite = 'suite_result'
        finished_tests_dict = get_finished_tests(full_file_path)[0]
        suite_result_dto = get_suite_results_object(finished_tests_dict)
        ##Sending to DB skipped tests
        collected_tests = open('/tmp/collected_tests.txt').readlines()
        enabled_tests = open(get_shared_directory_path() + file_path).readlines()
        all_tests_string = ''
        disabled_tests_count = 0
        for test in enabled_tests:
            all_tests_string += str(test)
        for test_line_index in range(1, len(collected_tests)):
            full_collected_test = f"'{collected_tests[test_line_index][:-1]}'"
            if full_collected_test not in all_tests_string:
                disabled_tests_count += 1
                test_result_dto = TestResultDTO()
                test_result_dto.set_test(str(collected_tests[test_line_index][:-1]))
                test_result_dto.set_run(str(suite_result_dto.get_run()))
                test_result_dto.set_version(str(suite_result_dto.get_version()))
                test_result_dto.set_project(str(suite_result_dto.get_project()))
                disabled_test_json = test_result_dto.get_test_json(db_measurement_name_for_test)
                influxdb_components.get_client().write_points(disabled_test_json)
        run_id_value = suite_result_dto.get_run()
        if run_id_value != '' and run_id_value != 'UNDEFINED':
            current_time_in_mils = int(round(time.time()))
            first_test_time_in_mils = get_first_test_time_in_mils(first_test_time_full_path)
            suite_result_dto.set_run(run_id_value)
            suite_result_dto.set_duration_sec(int(current_time_in_mils - first_test_time_in_mils))
            suite_result_dto.set_disabled(disabled_tests_count)
            ##Checking if there's an existing record
            existing_suite_result = influxdb_components.get_client().query(
                f"SELECT * FROM {db_measurement_name_for_suite} WHERE run='{run_id_value}'")
            old_suite_list = list(existing_suite_result.get_points(measurement=f'{db_measurement_name_for_suite}'))
            if len(old_suite_list) != 0:
                old_suite_total_count = old_suite_list[0]['pass'] + old_suite_list[0]['fail'] + old_suite_list[0][
                    'skip']
                old_disabled_tests_count = old_suite_list[0]['disabled']
                suite_result_dto.set_passed(
                    old_suite_total_count - suite_result_dto.get_failed() - suite_result_dto.get_skipped())
                suite_result_dto.set_disabled(old_disabled_tests_count)
                influxdb_components.get_client().query(
                    f"DELETE FROM {db_measurement_name_for_suite} WHERE run='{run_id_value}'")
            ##Sending suite data to influxdb
            suite_json = suite_result_dto.get_suite_json(db_measurement_name_for_suite)
            influxdb_components.get_client().write_points(suite_json)
            remove_temp_files()


def set_shared_directory_path(shared_directory_path):
    file = open('/tmp/shared_directory_path.txt', 'w')
    file.write(str(shared_directory_path))


def get_shared_directory_path():
    line = open('/tmp/shared_directory_path.txt').readline()
    return line


def remove_temp_files():
    os.remove('/tmp/collected_tests.txt')
    os.remove(get_shared_directory_path() + first_test_time_path)
    os.remove(get_shared_directory_path() + file_path)
    os.remove('/tmp/shared_directory_path.txt')
