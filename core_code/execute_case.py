import time
import traceback
from .webview_el_find import WebViewElFind
from .native_el_find import NativeElFind
from .error_aggregate import NoSuchEl, SleepTimeOut, CheckResError


class ExecuteCase():
    def __init__(self, project, logger, driver, config):
        self.logger = logger
        self.project = project
        self.config = config
        self.driver = driver
        self.case = {}
        self.case_name = ''
        self.default_sleep_time = 0

    def execute(self):
        # 如果用例中填写了等待时间，则默认等待时间以此为准
        if self.case['sleep']:
            self.default_sleep_time = self.case['sleep']
        else:
            self.default_sleep_time = self.config['control_config']['default_sleep_time']

        self.case['sleep_res'] = self.default_sleep_time
        while True:
            try:
                time.sleep(self.default_sleep_time)
                start_time = time.time()

                if self.case['obj'] == 'native' or self.case['obj'] == 'webview':
                    if self.case['obj'] == 'native':
                        context = 'NATIVE_APP'
                        find = NativeElFind(self.driver, self.project, self.case_name, self.case)
                    else:
                        context = self.config['control_config']['webview_context']
                        find = WebViewElFind(self.driver, self.project, self.case_name, self.case)

                    # 如果当前context与要切换的context不同，则切换
                    if self.driver.current_context != context: self.driver._switch_to.context(context)

                    try:
                        obj = find.gen_obj()  # 查找元素，生成对象
                    except:
                        self.logger.debug(traceback.format_exc())
                        raise NoSuchEl(
                            self.project,
                            self.case_name,
                            self.case,
                            self.logger,
                            "查找不到元素, 等待加查找元素时间暂未超过设定的默认等待时间，继续查找..."
                        )
                    if self.case['type'] == 'action':
                        exec("obj.{action}".format(action=self.case['action']))  # 执行元素操作
                    else:
                        # 如果不符合预期
                        if self.case['hope'] and self.case['hope'] != obj.text:
                            raise CheckResError(
                                self.project,
                                self.case_name,
                                self.case,
                                obj.text,
                                self.logger
                            )

                elif self.case['obj'] == 'swipe':
                    self.driver.swipe(
                        start_x=self.case['x1'],
                        start_y=self.case['y1'],
                        end_x=self.case['x2'],
                        end_y=self.case['y2'],
                    )
                break

            # 捕获到没有查找到元素的异常，进行再次查找，超过最大等待时间时，停止查找并报错
            except NoSuchEl as e:

                check_type = self.case['type'].split('-')
                if self.case['type'] == 'action' or int(check_type[-1]):
                    time.sleep(self.config['control_config']['default_sleep_time'])
                    # 查找时间+等待时间
                    self.case['sleep_res'] += (time.time() - start_time) + self.config['control_config']['default_sleep_time']

                    # 如果用例中定义了等待时间
                    if self.case['sleep']:
                        self.case['max_sleep'] = self.case['sleep']
                        raise SleepTimeOut(
                            self.project,
                            self.case_name,
                            self.case,
                            self.case['sleep'],
                            '设定',
                            self.logger
                        )
                    # 如果查找时间+等待时间超过设置的最大等待时间
                    elif self.case['sleep_res'] > self.config['control_config']['max_sleep_time']:
                        self.case['max_sleep'] = self.config['control_config']['max_sleep_time']
                        raise SleepTimeOut(
                            self.project,
                            self.case_name,
                            self.case,
                            self.config['control_config']['max_sleep_time'],
                            '最大',
                            self.logger
                        )
                    else:
                        self.logger.debug(e)
                else:
                    break
        print(self.case['sleep_res'])
        self.case['sleep_res'] = self.case['sleep_res']
