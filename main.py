import traceback
import time
from datetime import datetime
from appium import webdriver
from appium.common.exceptions import NoSuchContextException

from core_code.common import get_exec_project
from core_code.logger import Logger
from core_code.common import get_config, get_case, get_path, send_email
from core_code.execute_case import ExecuteCase
from core_code.error_aggregate import CaseError, SleepTimeOut, CheckResError
from core_code.check_case import CheckCase
from core_code.generate_simple_report import GenerateSimpleReport
from core_code.generate_html_report import GenerateHtmlReport


def run():
    logger = Logger()  # 实例化日志类
    exec_list = get_exec_project()  # 获取执行项目列表
    logger.info("获取执行的项目列表：{}".format(str(exec_list)))

    for exec_project in exec_list:

        config = get_config(exec_project)  # 根据项目名作为key取对应的配置信息

        # 将配置中指定的驱动文件名转化为对应的路径加载
        config['run_config']['chromedriverExecutable'] = get_path(
            'chromedriver/%s' % config['run_config']['chromedriverExecutable']
            )

        # 获取执行的场景用例，no_run指的是不需要执行的用例编号
        scene_case = get_case(exec_project, config['control_config']['no_run'])
        logger.info("加载项目信息（用例、配置）...：%s" % exec_project)

        if not scene_case:
            logger.info("本次暂无需要执行的用例，停止该项目自动化测试")
            break

        logger.info("项目加载完毕，本次有需要执行的用例，加载驱动...")
        # 根据项目配置以及配置的服务地址端口，加载驱动
        driver = webdriver.Remote(config['control_config']['remote_host'], config['run_config'])

        # 实例化执行用例类
        execute = ExecuteCase(
            exec_project,
            logger,
            driver,
            config
        )

        logger.info("驱动加载完毕，开始执行...")

        # 邮件正文html报告
        simple_report_dict = {
            'project': exec_project,
            'case_count': len(scene_case.keys()),
            'success': 0,
            'fail': 0,
            'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'exec_time': 0,
            'platform': config['run_config']['platformName'],
            'version': config['run_config']['platformVersion'],
            'device_name': config['run_config']['deviceName'],
            'fail_case': [],
            'all_case': [],
        }

        # 邮件附件html报告
        html_report_dict = {
            'fail_case': [],
            'sta_data': [
                {'value': 0, 'name': '用例错误'},
                {'value': 0, 'name': '查找超时'},
                {'value': 0, 'name': '校验失败'},
                {'value': 0, 'name': 'context'},
                {'value': 0, 'name': '未知错误'},
            ]
        }

        # 获取开始时间戳
        start_time = time.time()

        # 获取场景用例文件名，用例内步骤
        for case_name, case_list in scene_case.items():

            # 如果该用例内有步骤，则执行
            if case_list:
                # 每一场景用例执行前都会重新打开app，保证操作独立
                driver.close_app()
                driver.start_activity(config['run_config']['appPackage'], config['run_config']['appActivity'])
                res_type = False  # 默认无报错
                fail_type = '无报错'  # 默认无报错
                fail_children = []  # 错误的步骤列表

                for case in case_list:
                    fail_status = True  # 默认当前步骤成功
                    logger.debug("当前所有的contexts：{}".format(str(driver.contexts)))  # 打印当前环境所有的context

                    # -----报告用-----#
                    case['contexts'] = str(driver.contexts)
                    case['context'] = driver.current_context
                    case['res'] = '暂未执行'
                    case['error'] = '无报错'
                    case['sleep_res'] = 0
                    case['max_sleep'] = 0
                    fail_children.append(case)
                    # -----报告用-----#

                    try:
                        check_case = CheckCase(exec_project, case_name, case, logger)  # 检查用例
                        check_case.check_type()  # 检查用例中的“用例类型”
                        check_case.check_obj()  # 检查用例中的“操作对象”
                        check_case.check_method()  # 检查用例中的“查找方式”

                        execute.case = case  # 初始化执行用例
                        execute.case_name = case_name  # 初始化执行用例名
                        execute.execute()  # 开始执行

                    # 捕获异常，如果是用例编写错误，则报告中对应的类型+1
                    # 类型请查看"html_report_dict"字典定义
                    except CaseError as e:
                        fail_type = '用例错误'
                        case['error'] = str(e)
                        html_report_dict['sta_data'][0]['value'] += 1

                    except SleepTimeOut as e:
                        fail_type = '超时未找到'
                        case['error'] = str(e)
                        html_report_dict['sta_data'][1]['value'] += 1

                    # 这里打印日志是因为，这个异常是appium自带异常，在自定义异常类里打印日志，所以这里需要打印日志
                    except NoSuchContextException:
                        fail_type = '上下文错误'
                        logger.error(
                            "项目名：{}|用例名称：{}|用例编号：{}|用例类型:{}, context切换失败！当前所有context: {}".format(
                                exec_project,
                                case_name,
                                case['case_num'],
                                case['type'],
                                str(driver.contexts)
                            )
                        )
                        case['error'] = "项目名：{}|用例名称：{}|用例编号：{}|用例类型:{}, context切换失败！当前所有context: {}".format(
                                exec_project,
                                case_name,
                                case['case_num'],
                                case['type'],
                                str(driver.contexts)
                            )

                        html_report_dict['sta_data'][3]['value'] += 1

                    except CheckResError as e:
                        fail_type = '校验未通过'
                        case['error'] = str(e)
                        html_report_dict['sta_data'][2]['value'] += 1
                        break

                    except:
                        fail_type = '未知错误'
                        case['error'] = '未知错误'
                        html_report_dict['sta_data'][4]['value'] += 1
                        logger.debug(
                            "项目名：{}|用例名称：{}|用例编号: {}|用例类型: {}".format(
                                exec_project,
                                case_name,
                                case['case_num'],
                                case['type']
                            )
                        )
                        logger.debug(traceback.format_exc())

                    else:
                        case['res'] = '成功'
                        fail_status = False

                    # 如果失败
                    if fail_status:
                        case['res'] = '失败'
                        # 如果用例类型是action，则需要判断是否开启了失败中止运行
                        if case['type'] == 'action':
                            # 如果开启了失败中止运行
                            if case['fail_break']:
                                logger.error("当前步骤开启了失败中断，停止该用例运行...")
                                # 如果该场景用例之前的步骤都没错，则修改报告中的场景用例执行结果
                                if not res_type: res_type = True
                                break
                            # 如果没开启，则判断为该步骤可有可无，默认无报错
                            else:
                                fail_type = '无报错'
                                logger.info("当前用例未开启失败中断，继续运行...")
                        # 如果用例类型是check，为校验步骤，那直接错误
                        else:
                            # 如果该场景用例之前的步骤都没错，则修改报告中的场景用例执行结果
                            if not res_type: res_type = True
                            logger.error("该用例为校验用例,失败则中止场景用例运行...")
                            break
                    # 如果成功了，就打印通过的日志
                    else:
                        logger.info(
                            "项目：{}|用例名：{}|用例编号：{}|用例类型: {},执行成功，执行前等待时间：{}秒".format(
                                exec_project,
                                case_name,
                                case['case_num'],
                                case['type'],
                                execute.sleep_time
                            )
                        )

                # 有报错用例
                if res_type:
                    # 错误+1
                    simple_report_dict['fail'] += 1
                    simple_report_dict['fail_case'].append([case_name, 0, fail_type])
                    simple_report_dict['all_case'].append([case_name, 0, fail_type])

                    html_report_dict['fail_case'].append({
                        'name': case_name, 'children': fail_children
                    })
                # 无报错用例
                else:
                    simple_report_dict['success'] += 1
                    simple_report_dict['all_case'].append([case_name, 1, fail_type])

        # 获取执行时间，四舍五入
        simple_report_dict['exec_time'] = round(time.time() - start_time, 1)

        # 如果需要发送邮件
        if config['mail_config']['send_status']:
            logger.info("该项目测试结束, 生成报告中...")
            simple_report = GenerateSimpleReport(**simple_report_dict)  # 生成邮件正文报告
            html_report = GenerateHtmlReport(simple_report_dict, html_report_dict)  # 生成邮件附件报告

            send_email(
                config['mail_config'],
                simple_report.gen_report(),
                len(simple_report_dict['fail_case']),
                logger,
                html_path=html_report.gen_report()
            )

        driver.quit()


if __name__ == '__main__':
    run()