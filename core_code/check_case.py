from .error_aggregate import CaseError


class CheckCase():
    def __init__(self, project, case_name, case, logger):
        self.project = project
        self.case_name = case_name
        self.case = case
        self.logger = logger

    def check_type(self):
        # 如果操作类型为‘action’，顺便定义好操作对象列表
        if self.case['type'] == 'action':
            self.obj_list = ['native', 'webview', 'touch', 'swipe']
        # 如果操作类型为‘check’，顺便定义好操作对象列表
        elif self.case['type'] == 'check-1' or self.case['type'] == 'check-0':
            self.obj_list = ['native', 'webview']
        # 以上类型都没有，则报错
        else:
            raise CaseError(
                self.project,
                self.case_name,
                self.case,
                "用例中的用例类型只能填写action、check",
                self.logger
            )

    def check_obj(self):
        # 如果操作对象不在定义好的操作对象中，则报错
        if not self.case['obj'] in self.obj_list:
            raise CaseError(
                self.project,
                self.case_name,
                self.case,
                "用例类型为{}，用例中obj只能填写：{}".format(self.case['type'], str(self.obj_list)),
                self.logger
            )
    def check_swipe(self):
        # 如果为swipe，也就是滑动，需要定义x1y1x2y2，必填
        if (self.case['x1'] or self.case['x1'] == 0) and \
                self.case['x2'] or self.case['x2'] == 0 and \
                self.case['y1'] or self.case['y1'] == 0 and \
                self.case['y2'] or self.case['y2'] == 0:
            pass
        else:
            raise CaseError(
                self.project,
                self.case_name,
                self.case,
                "obj为swipe，用例中的x1,y1,x2,y2必填",
                self.logger
            )

    def check_method(self):
        # native，原生元素操作
        if self.case['obj'] == 'native':
            method_list = ['ids', 'xpaths', 'classs', 'names', 'descs']
        # webview，h5元素操作
        elif self.case['obj'] == 'webview':
            method_list = ['ids', 'xpaths', 'classs']

        # 如果是滑动，则不需要检查元素，直接return
        elif self.case['obj'] == 'swipe':
            self.check_swipe()
            return True
        else:
            raise CaseError(
                self.project,
                self.case_name,
                self.case,
                "不支持的obj，用例中的obj应该为native、webview、swipe",
                self.logger
            )

        # 判断是否填写了查找的元素
        if self.case['el']:
            # 判断查找方式是否符合
            if not self.case['method'] in method_list:
                raise CaseError(
                    self.project,
                    self.case_name,
                    self.case,
                    "调用模式为{}，用例中使用的方法应该为:{}".format(
                        self.case['obj'], str(method_list)
                    ),
                    self.logger
                )
        else:
            raise CaseError(
                self.project,
                self.case_name,
                self.case,
                "调用模式为{}，该模式下元素必填".format(self.case['obj']),
                self.logger
            )

    def check_len(self):
        # 组合元素查看，看看即可，用的不多
        method_len = len(self.case['method'].split(';'))
        el_len = len(self.case['el'].split(';'))
        index_len = len(str(self.case['index']).split(';'))

        if not (method_len == el_len == index_len):
            raise CaseError(
                self.project,
                self.case_name,
                self.case,
                "用例中，元素/查找方式/下标如果使用了分号';'进行分隔，则三者都需要拥有同样多的分隔符",
                self.logger
            )