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
        results_dict = [{"index":item[0], "name":item[1], "project":item[2], "key":item[8], "start_time":item[9],
                         "end_time":item[10], "duration": self.benchmark_db.get_duration(item[9], item[10]),
                         "environment": self.benchmark_db.get_env_by_index(item[0]),
                         "summary_report": self.benchmark_db.get_summary_report_by_index(item[0]),
                         "configuration": self.benchmark_db.get_test_config(item[0])} for item in results]
        return results_dict

    def get_real_time_results(self, index):
        real_time_table_name = self.benchmark_db.get_spec_index(index, "real_time_index")
        command = "SELECT * FROM {}".format(real_time_table_name)
        results = self.benchmark_db.execute_sql_command(command)
        results_dict = [{"index":item[0], "time":item[6], "read_iops": item[1], "read_bw":item[2], "write_iops":item[3],
                         "write_bw":item[4], "temperature": item[5]} for item in results]
        return results_dict

    def get_test_state(self, index):
        return self.benchmark_db.get_test_state(index)




if __name__ == '__main__':
    P = PerfDBClient()
    TESTS = P.search()
    print(TESTS)
    TEST = TESTS[-1]
    print(P.get_test_state(TEST["index"]))
