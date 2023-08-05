# coding=utf-8
# pylint: disable=wrong-import-position, relative-import
from resources.benchmark_db_resource import BenchmarkDBResource


class PerfDBClient(object):

    def __init__(self):
        self.benchmark_db = BenchmarkDBResource(db_name="performance_test")

    def search(self, project_name=None, begin_time=None, end_time=None, test_name=None):
        """

        :param project_name: project name, like tahoe, alpha
        :param begin_time: format: '%Y%m%d', e.g. 20170601
        :param end_time: format: '%Y%m%d', e.g. 20170601
        :param test_name:
        :return:
        """
        search_str = self.benchmark_db.get_search_match_string(project_name, begin_time, end_time, test_name)
        print(search_str)
        results = self.benchmark_db.execute_sql_command(search_str)
        return results

    def get_summary_report_by_index(self, index):
        report_index = self.benchmark_db.get_spec_index(index, "summary_report_index")
        command = "SELECT * FROM _summary_test_results WHERE `index`={}".format(report_index)
        results = self.benchmark_db.execute_sql_command(command)
        report = results[0] if results else None
        return report

    def get_env_by_index(self, index):
        env_index = self.benchmark_db.get_spec_index(index, "test_env_index")
        command = "SELECT * FROM _environment WHERE `index`={}".format(env_index)
        results = self.benchmark_db.execute_sql_command(command)
        env = results[0] if results else None
        return env

    def get_real_time_results(self, index):
        real_time_table_name = self.benchmark_db.get_spec_index(index, "real_time_index")
        command = "SELECT * FROM {}".format(real_time_table_name)
        results = self.benchmark_db.execute_sql_command(command)
        reports = results if results else None
        return reports


# P = PerfDBClient()
# tests = P.search(begin_time="20190924", end_time="20190924", project_name="alpha")
# print(tests)
# for test in tests:
#     print(P.get_env_by_index(test[0]))
#     print(P.get_summary_report_by_index(test[0]))
#     print(P.get_real_time_results(test[0]))
