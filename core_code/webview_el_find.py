class WebViewElFind():
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

            function_text += eval("self.el_{method}('{el}', {index})".format(
                method=method,
                el=el,
                index=int(index)
            ))

        return eval("self.driver" + function_text)

    def el_ids(self, el, index):
        selector = '[id="{id}"]'.format(id=el)
        return ".find_elements_by_css_selector('{selector}')[{index}]".format(
            selector=selector,
            index=index
        )

    def el_xpaths(self, el, index):
        return ".find_elements_by_xpath('{xpath}')[{index}]".format(xpath=el, index=index)

    def el_classs(self, el, index):
        selector = '[class="{class_name}"]'.format(class_name=el)
        return ".find_elements_by_css_selector('{selector}')[{index}]".format(
            selector=selector,
            index=index
        )
