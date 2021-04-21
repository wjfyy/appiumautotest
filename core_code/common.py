import xlrd
import os
import yaml
import re
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



def get_path(file_path):
    """获取路径函数"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../%s' % file_path))


def yaml_get(file_name):
    """
    获取yaml格式的文件数据
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding='utf-8') as fp:
        data = yaml.load(fp, Loader=yaml.FullLoader)
    return data


def get_config(project):
    """获取项目配置文件"""
    return yaml_get(get_path('config/project_conf.yaml'))[project]


def get_exec_project():
    """获取需要执行的项目"""
    return yaml_get(get_path('config/exec_project.yaml'))['exec_project']


def gen_no_run_case(no_run_case):
    """
    生成不运行的用例文件数组
    :param sys_data:
    :return:
    """
    # 获取配置文件的不运行文件数值
    no_run_list = []
    if no_run_case:
        # 分解成数组
        no_run_case_list = str(no_run_case).split(';')
        for data in no_run_case_list:
            # 如果-存在，则判定为范围指定
            if '-' in data:
                no_run_case_section = data.split('-')
                # 分解成数组，利用range函数进行编号添加进数组
                no_run_list.extend(range(int(no_run_case_section[0]), int(no_run_case_section[1]) + 1))
            else:no_run_list.append(int(data))
    return no_run_list


def get_case(project, no_run):
    """获取项目用例"""
    case_dict = {}
    no_run_list = gen_no_run_case(no_run)
    project_case_path = get_path('case/%s' % project)
    path_list = os.listdir(project_case_path)
    num_find = re.compile(r'(\d+)')

    path_list.sort(key=lambda x: int(num_find.match(x).group(0)))
    for path in path_list:
        filename = project_case_path + '/' + path

        if os.path.isdir(filename):
            file_list = os.listdir(filename)
            file_list.sort(key=lambda x: int(num_find.match(x).group(0)))

            for file in file_list:
                case_num = int(num_find.match(file).group(0))
                if not case_num in no_run_list:
                    generate_case(case_dict, file, filename + '/' + file)
        else:
            case_num = int(num_find.match(path).group(0))
            if case_num not in no_run_list:
                generate_case(case_dict, path, filename)

    return case_dict


def generate_case(case_dict, case_name, filename):
    end_list = ['.xls', '.csv', '.xlsx']
    for end in end_list:
        # 校验文件后缀是否为excel
        if filename.endswith(end):
            excel = xlrd.open_workbook(filename)
            case_list = []
            sheet = excel.sheet_by_index(0)
            rows = sheet.nrows
            for row in range(1, rows):
                index = sheet.cell(row, 6).value
                if isinstance(index, str):
                    pass
                else:
                    index = str(int(index))

                case_list.append({
                    'case_num': sheet.cell(row, 0).value,
                    'remark': sheet.cell(row, 1).value,
                    'el': sheet.cell(row, 2).value,
                    'method': sheet.cell(row, 3).value,
                    'obj': sheet.cell(row, 4).value,
                    'action': sheet.cell(row, 5).value,
                    'index': index,
                    'x1': sheet.cell(row, 7).value,
                    'y1': sheet.cell(row, 8).value,
                    'x2': sheet.cell(row, 9).value,
                    'y2': sheet.cell(row, 10).value,
                    'sleep': sheet.cell(row, 11).value,
                    'fail_break': sheet.cell(row, 12).value,
                    'hope': sheet.cell(row, 13).value,
                    'type': sheet.cell(row, 14).value,
                })

            case_dict[case_name.replace(end, '')] = case_list  # 将文件名后缀去除，只保留文件名
            break


def send_email(mail_config, html, fail_count, logger, html_path=None):
    """
    发送邮件功能
    :return:
    """
    msg = MIMEMultipart()
    # 邮件正文内容
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    msg['From'] = mail_config['send_user'] # 发件人
    msg['To'] = mail_config['accept_user'] # 接收人
    if fail_count: msg['Subject'] = mail_config['mail_title'] + '(失败)'
    else: msg['Subject'] = mail_config['mail_title']

    if html_path:
        with open(html_path, 'rb') as f:
            report_part = MIMEApplication(f.read())
            report_part.add_header(
                'Content-Disposition',
                'attachment',
                filename='Mobile UI 自动化测试报告.html'
            )
            msg.attach(report_part)

    server = smtplib.SMTP_SSL(mail_config['mail_server'], 465)
    try:
        server.login(
            user=mail_config['send_user'],
            password=mail_config['password']
        )
        server.sendmail(
            mail_config['send_user'],
            mail_config['accept_user'].split(','), # 多人发送，此处必须为数组形式
            msg.as_string()
        )
        logger.info("邮件发送成功")
    except:
        logger.error("邮件发送失败")
    finally:
        server.quit()