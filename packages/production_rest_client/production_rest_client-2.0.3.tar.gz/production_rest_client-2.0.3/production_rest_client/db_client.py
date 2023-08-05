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
                         "end_time":item[10], "duration": item[10]-item[9],
                         "environment": self.get_env_by_index(item[0]),
                         "summary_report": self.get_summary_report_by_index(item[0])} for item in results]
        return results_dict

    def get_summary_report_by_index(self, index):
        result_dict = dict()
        report_index = self.benchmark_db.get_spec_index(index, "summary_report_index")
        command = "SELECT * FROM _summary_test_results WHERE `index`={}".format(report_index)
        results = self.benchmark_db.execute_sql_command(command)
        if results:
            result_dict = {"iops_read":results[0][1],
                           "bw_read":results[0][2],
                           "io_read":results[0][3],
                           "percent_9_read": results[0][4],
                           "percent_99_read": results[0][5],
                           "percent_999_read": results[0][6],
                           "percent_9999_read": results[0][7],
                           "percent_99999_read": results[0][8],
                           "percent_999999_read": results[0][9],
                           "iops_write": results[0][10],
                           "bw_write": results[0][11],
                           "io_write": results[0][12],
                           "percent_9_write": results[0][13],
                           "percent_99_write": results[0][14],
                           "percent_999_write": results[0][15],
                           "percent_9999_write": results[0][16],
                           "percent_99999_write": results[0][17],
                           "percent_999999_write": results[0][18]}
        return result_dict

    def get_env_by_index(self, index):
        results_dict = dict()
        env_index = self.benchmark_db.get_spec_index(index, "test_env_index")
        command = "SELECT * FROM _environment WHERE `index`={}".format(env_index)
        results = self.benchmark_db.execute_sql_command(command)
        if results:
            results_dict = {
                "vendor": results[0][1],
                "operating_system": results[0][2],
                "ip": results[0][3],
                "capacity": results[0][4],
                "device": results[0][7],
            }
        return results_dict

    def get_real_time_results(self, index):
        real_time_table_name = self.benchmark_db.get_spec_index(index, "real_time_index")
        command = "SELECT * FROM {}".format(real_time_table_name)
        results = self.benchmark_db.execute_sql_command(command)
        results_dict = [{"index":item[0], "time":item[6], "read_iops": item[1], "read_bw":item[2], "write_iops":item[3],
                         "write_bw":item[4], "temperature": item[5]} for item in results]
        return results_dict


if __name__ == '__main__':
    P = PerfDBClient()
    TESTS = P.search(begin_time="20190926", end_time="20190926", project_name="alpha", test_name="32k")
    print(TESTS)
    TEST = TESTS[-1]
    print(P.get_env_by_index(TEST["index"]))
    print(P.get_summary_report_by_index(TEST["index"]))
    print(P.get_real_time_results(TEST["index"]))
