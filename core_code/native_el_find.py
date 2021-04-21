class NativeElFind():
    def __init__(self, driver, project, case_name, case):
        self.project = project
        self.case_name = case_name
        self.case_num = case['case_num']
        self.driver = driver
        self.case = case

    def gen_obj(self):
        function_text = ''
        method_list = self.case['method'].split(';')
        el_list = self.case['el'].split(';')
        index_list = self.case['index'].split(';')

        for idx in range(len(method_list)):
            method = method_list[idx]
            el = el_list[idx]
            index = index_list[idx]

            # 查找方法及元素拼接
            function_text += eval("self.el_{method}('{el}', {index})".format(
                method=method,
                el=el,
                index=int(index)
            ))

        return eval("self.driver" + function_text)  # 返回查找的元素对应

    def el_ids(self, el, index):
        return ".find_elements_by_id('{el}')[{index}]".format(el=el, index=index)

    def el_xpaths(self, el, index):
        return ".find_elements_by_xpath('{el}')[{index}]".format(el=el, index=index)

    def el_classs(self, el, index):
        return ".find_elements_by_class_name('{el}')[{index}]".format(el=el, index=index)

    def el_names(self, el, index):
        return ".find_elements_by_android_uiautomator" \
               "('new UiSelector().text(\"{el}\")')[{index}]".format(el=el, index=index)

    def el_descs(self, el, index):
        return ".find_elements_by_android_uiautomator" \
               "('new UiSelector().description(\"{el}\")')[{index}]".format(el=el, index=index)