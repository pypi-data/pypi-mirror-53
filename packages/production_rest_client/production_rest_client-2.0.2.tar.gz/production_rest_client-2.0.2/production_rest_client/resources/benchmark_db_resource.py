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
