# coding=utf-8
# pylint: disable=import-error, broad-except
from resources.models.database import SqlConnection


class BenchmarkDBResource(object):

    def __init__(self, db_name="performance_test"):
        self.sql = SqlConnection(db_name=db_name)

    def get_search_match_string(self, project_name=None, begin_time=None, end_time=None, test_name=None):
        search_str = "SELECT * FROM _tests"
        is_first_filter = True
        if project_name is not None:
            match_string = self.get_project_name_match_string(project_name)
            search_str = self.generate_filter_string(search_str, match_string, is_first_filter)
            is_first_filter = False
        if begin_time is not None and end_time is not None:
            match_string = self.get_search_date_match_string(begin_time, end_time)
            search_str = self.generate_filter_string(search_str, match_string, is_first_filter)
            is_first_filter = False
        if test_name is not None:
            match_string = self.get_test_name_match_string(test_name)
            search_str = self.generate_filter_string(search_str, match_string, is_first_filter)
        return search_str

    @staticmethod
    def get_project_name_match_string(project_name):
        match_str = "project_name like '%{}%'".format(project_name)
        return match_str

    @staticmethod
    def get_search_date_match_string(begin_time, end_time):
        match_string = "DATE_FORMAT(start_time,'%Y%m%d') BETWEEN '{}' and '{}'".format(begin_time, end_time)
        return match_string

    @staticmethod
    def get_test_name_match_string(test_name):
        match_str = "test_name like '%{}%'".format(test_name)
        return match_str

    @staticmethod
    def generate_filter_string(base_string, new_filter, is_first_filter):
        if is_first_filter:
            base_string = "{} WHERE ".format(base_string)
        else:
            base_string = "{} AND ".format(base_string)
        search_string = "{} {}".format(base_string, new_filter)
        return search_string

    def get_spec_index(self, main_index, get_index_name):
        command = "SELECT `{}` FROM _tests WHERE `index`={}".format(get_index_name, main_index)
        self.sql.cursor.execute(command)
        tests = self.sql.cursor.fetchall()
        env_index = tests[0][0] if tests else None
        return env_index

    def execute_sql_command(self, command):
        results = list()
        try:
            self.sql.cursor.execute(command)
            results = self.sql.cursor.fetchall()
        except BaseException as message:
            print(message)
        return results

    def get_test_config(self, index):
        results_dict = dict()
        config_index = self.get_spec_index(index, "config_index")
        command = "SELECT * FROM _configuration WHERE `index`={}".format(config_index)
        results = self.execute_sql_command(command)
        if results:
            results_dict = {
                "type": results[0][1],
                "ioengine": results[0][3],
                "blocksize": results[0][4],
                "iodepth": results[0][5],
                "numjobs": results[0][6],
                "rw": results[0][7],
                "rwmixread": results[0][8],
                "size": results[0][9],
                "runtime": results[0][10],
            }
        return results_dict

    def get_env_by_index(self, index):
        results_dict = dict()
        env_index = self.get_spec_index(index, "test_env_index")
        command = "SELECT * FROM _environment WHERE `index`={}".format(env_index)
        results = self.execute_sql_command(command)
        if results:
            results_dict = {
                "vendor": results[0][1],
                "operating_system": results[0][2],
                "ip": results[0][3],
                "capacity": results[0][4],
                "device": results[0][7],
            }
        return results_dict

    def get_summary_report_by_index(self, index):
        result_dict = dict()
        report_index = self.get_spec_index(index, "summary_report_index")
        command = "SELECT * FROM _summary_test_results WHERE `index`={}".format(report_index)
        results = self.execute_sql_command(command)
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

    @staticmethod
    def get_duration(start_time, end_time):
        duration = 0
        if start_time is not None and end_time is not None:
            duration = end_time - start_time
        return duration

    def get_test_state(self, index):
        result = None
        command = "SELECT state FROM _tests WHERE `index`={}".format(index)
        results = self.execute_sql_command(command)
        if results:
            result = results[0][0]
        return result
