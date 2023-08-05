import ast


class TestResultDTO:
    __run = 'UNDEFINED'
    __test = None
    __status = 'disabled'
    __project = 'UNDEFINED'
    __version = 'UNDEFINED'
    __screenshot = None
    __duration_sec = None
    __exception = None
    __retries = 0
    __test_result_tag_dict = {}
    __test_result_field_dict = {}

    def get_run(self):
        return self.__run

    def set_run(self, run):
        self.__run = run

    def get_test(self):
        return self.__test

    def set_test(self, test):
        self.__test = test

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_project(self):
        return self.__project

    def set_project(self, project):
        self.__project = project

    def get_version(self):
        return self.__version

    def set_version(self, version):
        self.__version = version

    def get_screenshot(self):
        return self.__screenshot

    def set_screenshot(self, screenshot):
        self.__screenshot = screenshot

    def get_duration_sec(self):
        return self.__duration_sec

    def set_duration_sec(self, duration_sec):
        self.__duration_sec = int(duration_sec)

    def get_exception(self):
        return self.__exception

    def set_exception(self, exception):
        self.__exception = exception

    def get_retries(self):
        return self.__retries

    def set_retries(self, retries):
        self.__retries = int(retries)

    def get_test_result_tag_dict(self):
        return TestResultDTO.__test_result_tag_dict

    def get_test_result_field_dict(self):
        return TestResultDTO.__test_result_field_dict

    def set_test_result_tag_dict(self, test_result_tag_dict):
        TestResultDTO.__test_result_tag_dict = test_result_tag_dict

    def set_test_result_field_dict(self, test_result_field_dict):
        TestResultDTO.__test_result_field_dict = test_result_field_dict

    def get_test_json(self, measurement_name):
        json_body = [
            {
                "measurement": measurement_name,
                "tags": {
                    "test": str(self.get_test()),
                    "run": str(self.get_run()),
                    "project": str(self.get_project()),
                    "version": str(self.get_version())
                },
                "fields": {
                    "status": str(self.get_status()),
                    "screenshot": str(self.get_screenshot()),
                    "duration_sec": self.get_duration_sec(),
                    "exception": str(self.get_exception()),
                    "retries": int(self.get_retries())
                }
            }
        ]
        tags_dict_for_all_tests = TestResultDTO.get_test_result_tag_dict(self)
        tags_dict_for_current_test = tags_dict_for_all_tests.get(str(self.get_test()))
        if tags_dict_for_current_test is not None:
            for key in tags_dict_for_current_test:
                json_body[0]['tags'].update({key: tags_dict_for_current_test[key]})
        fields_dict_for_all_tests = TestResultDTO.get_test_result_field_dict(self)
        fields_dict_for_current_test = fields_dict_for_all_tests.get(str(self.get_test()))
        if fields_dict_for_current_test is not None:
            for key in fields_dict_for_current_test:
                json_body[0]['fields'].update({key: fields_dict_for_current_test[key]})
        return json_body

    def get_test_json_for_suite_level(self):
        json_body = {
            "test": str(self.get_test()),
            "status": str(self.get_status()),
            "duration_sec": self.get_duration_sec(),
            "retries": str(self.get_retries()),
            "run": str(self.get_run()),
            "project": str(self.get_project()),
            "version": str(self.get_version())
        }

        return json_body

    def parse_json_to_test_result_dto(self, json_test_result_dto):
        if json_test_result_dto.endswith('\n'):
            json_test_result_dto = json_test_result_dto[:-1]
        json_test_result_dto = ast.literal_eval(json_test_result_dto)
        test_result_dto = TestResultDTO()
        test_result_dto.set_test(json_test_result_dto['test'])
        test_result_dto.set_status(json_test_result_dto['status'])
        test_result_dto.set_duration_sec(json_test_result_dto['duration_sec'])
        test_result_dto.set_retries(json_test_result_dto['retries'])
        test_result_dto.set_run(json_test_result_dto['run'])
        test_result_dto.set_project(json_test_result_dto['project'])
        test_result_dto.set_version(json_test_result_dto['version'])

        return test_result_dto

    def set_tag_values(self, item_nodeid, tags_dict):
        TestResultDTO.get_test_result_tag_dict(self).update({item_nodeid: tags_dict})

    def set_field_values(self, item_nodeid, fields_dict):
        TestResultDTO.get_test_result_field_dict(self).update({item_nodeid: fields_dict})
