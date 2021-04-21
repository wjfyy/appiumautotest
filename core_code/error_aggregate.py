# 报错集合
# 需要继承python自带标准异常类：Exception

class CaseError(Exception):
    def __init__(self, project, case_name, case, error_msg, logger):
        self.project = project
        self.case_name = case_name
        self.case = case
        self.error_msg = error_msg
        self.logger = logger

    def __str__(self):
        """
        返回的异常信息
        :return:
        """
        msg = "用例编写错误！项目：{project}|用例名：{case_name}|" \
              "编号：{case_num}|用例类型: {case_type}，报错信息：{error_msg}".format(
            project=self.project,
            case_name=self.case_name,
            case_num=self.case['case_num'],
            case_type=self.case['type'],
            error_msg=self.error_msg
        )
        self.logger.error(msg)
        return self.error_msg


class NoSuchEl(Exception):
    def __init__(self, project, case_name, case, error_msg, logger):
        self.project = project
        self.case_name = case_name
        self.case = case
        self.error_msg = error_msg
        self.logger = logger

    def __str__(self):
        msg = "项目：{project}|用例名：{case_name}|编号：{case_num}|用例类型: {case_type}, " \
              "查找方式：{method}|元素：{el}，报错信息：{error_msg}".format(
            project=self.project,
            case_name=self.case_name,
            case_num=self.case['case_num'],
            case_type=self.case['type'],
            method=self.case['method'],
            el=self.case['el'],
            error_msg=self.error_msg
        )
        self.logger.error(msg)
        return self.error_msg


class SleepTimeOut(Exception):
    def __init__(self, project, case_name, case, max_sleep_time, time_type, logger):
        self.project = project
        self.case_name = case_name
        self.case = case
        self.max_sleep_time = max_sleep_time
        self.time_type = time_type
        self.logger = logger

    def __str__(self):
        self.logger.error(
            "项目：{project}|用例名：{case_name}|编号：{case_num}|用例类型: {case_type}|查找方式：{method}|元素：{el}，" \
            "报错信息：超过{time_type}等待时间{max_sleep_time}秒，查找不到元素".format(
                project=self.project,
                case_name=self.case_name,
                case_num=self.case['case_num'],
                case_type=self.case['type'],
                method=self.case['method'],
                el=self.case['el'],
                max_sleep_time=self.max_sleep_time,
                time_type=self.time_type)
        )
        return "超过{time_type}等待时间{max_sleep_time}秒，查找不到元素".format(
            max_sleep_time=self.max_sleep_time,
            time_type=self.time_type
        )


class CheckResError(Exception):
    def __init__(self, project, case_name, case, res_text, logger):
        self.project = project
        self.case_name = case_name
        self.case = case
        self.res_text = res_text
        self.logger = logger

    def __str__(self):
        self.logger.error(
            "项目：{project}|用例名：{case_name}|编号：{case_num}|" \
            "预期结果: {hope_res}, 实际结果: {res_text}, 校验不通过，中止该场景用例运行...".format(
            project=self.project,
            case_name=self.case_name,
            case_num=self.case['case_num'],
            hope_res=self.case['hope'],
            res_text=self.res_text
        ))
        return "预期结果: {hope_res}, 实际结果: {res_text}, 校验不通过，中止该场景用例运行...".format(
            hope_res=self.case['hope'],
            res_text=self.res_text
        )