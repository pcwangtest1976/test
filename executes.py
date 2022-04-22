# -*- coding: UTF-8 -*-
import traceback

import pytest

'''
reference
#https:\\v2.hrun.org\\development\\dev-api\\
#http:\\testerhome.com\\opensource_projects\\hrun

'''
from httprunner.api import HttpRunner
from Utils.collects import *
from httprunner import report
from Utils.configs import *
from Utils.logger import logger
from Utils.customizes import customize
import requests


class execute():

    def __init__(self):

        #
        self.project_dir = project_vars().project_dir
        self.exec_dir = project_vars().exec_dir
        self.api_dir = project_vars().api_dir
        self.cookie = project_vars().cookie
        # hrun
        self.hrun_report_dir = project_vars().hrun_report_dir
        self.hrun_report_name = project_vars().hrun_report_name
        self.hrun_report_file = project_vars().hrun_report_dir + '\\' + self.hrun_report_name
        self.hrun_log_name = project_vars().hrun_log_name
        self.hrun_log_file = self.hrun_report_dir + '\\' + self.hrun_log_name
        # pytest
        self.pytest_report_dir = project_vars().pytest_report_dir  # pytest/hrun test report dir
        self.pytest_report_name = project_vars().pytest_report_name
        # self.allure_report_dir = project_vars().allure_report_dir
        self.allure_report_dir = self.project_dir+ '\\Report\\allure_report'
        self.allure_report_file = self.project_dir+ '\\Report\\allure_file'
        # logger
        self.logger = logger().setup_logging()

    def execute_yaml_general(self, yaml_file='', log_file=''):
        '''
        another method to execute yaml file by request
        reference : https://blog.51cto.com/u_6315133/3122768
                    https://blog.csdn.net/xc_zhou/article/details/81021496
        '''
        if os.path.exists(yaml_file):
            try:
                yaml_data = tools().read_yaml_file(yaml_file)
                request = yaml_data['teststeps'][0]['request']
                request_data = request['data']
                request_headers = request['headers']
                request_url = request['url']
                request_method = request['method']
                request_params = request['params']
                request_cookies = request['cookies']
                data = {'cookies': request_cookies, 'params': request_params, 'data': request_data,
                        'headers': request_headers}
                res = requests.request(method=request_method, url=request_url, params=data)
                if res != None:
                    return res
                else:
                    return None
            except Exception as e:
                traceback.print_exc()
                self.logger.exception('exception:' ,e)
            except BaseException as e:
                traceback.print_exc()
                raise ('execption =' , e)
            except:
                return None
        else:
            raise ('can not find yaml file =', yaml_file)

    def execute_yaml(self, yaml_file='', hrun_log_file=''):

        '''
        execute yaml file
        ××××可以使用hrun来达到相同的目的
        #reference https://blog.csdn.net/qq_27371025/article/details/117398085
        # hrun yaml_file --save-tests
        #demo_login.io.json ： io读写文件相关的数据
        #demo_login.loaded.json： 加载到的测试用例生成的json数据文件
        #demo_login.parsed.json： 解析yaml文件生成json数据
        #demo_login.summary.json：运行用例后生成的报告总结---get summary
        #hrun yaml_file --save=tests --html=report_dir or file --self-contained-html(内嵌报告格式）
        1. $ hrun --alluredir allure-results --clean-alluredir     # 当用例格式为py文件时，可以用“pytest”替换“hrun”，作用相同
        --alluredir：生成allure报告的原始数据
        allure-results：原始数据的保存位置
        --clean-alluredir：清除allure-results历史数据
        2.调用allure 生成报告
        allure generate allure-results -o allure-report
        '''
        message='[execute_yaml]:'+yaml_file
        self.logger.info(message)
        if hrun_log_file == '' or hrun_log_file == None:
            hrun_log_file = os.path.dirname(yaml_file) + '\\' + self.hrun_log_name
            if not os.path.exists(hrun_log_file):
                hrun_log_file = self.hrun_log_file
        if os.path.exists(yaml_file):
            try:
                runner = HttpRunner(failfast=True, save_tests=False, log_level='ERROR', log_file=hrun_log_file)
                result = runner.run(yaml_file)
                return result
            except Exception as e:
                traceback.print_exc()
                self.logger.exception('exception:',e)
                raise ('please check input parameters for execute_yaml()')
            except BaseException as e:
                traceback.print_exc()
                raise ('execption =',e)
            except:
                return None
        else:
            raise (yaml_file + ' does not exist ')

    def pytest_allure(self,testcase_dir,num=1):
        #num 线程数
        allure_report_dir = self.project_dir + '\\Report\\allure_report'
        allure_report_file = self.project_dir + '\\Report\\allure_file'
        try:
            cmd_1 = 'del /Q ' + allure_report_file
            ops_tools().run_command(cmd_1)
        except Exception as e:
            traceback.print_exc()
            self.logger.info('exception:' ,e)
            raise ('Failed del ' + allure_report_file)
        except BaseException as e:
            traceback.print_exc()
            raise ('execption =', e)
        except:
            return None
        if num > 1:
            parameters = ["-s",'-v', testcase_dir, "-n " + str(num), '--reruns', '3', '--reruns-delay', '2', "--alluredir",
                          allure_report_file]
        else:
            parameters = ["-s",'-v', testcase_dir, "--alluredir", allure_report_file]
        pytest.main(parameters)
        command = 'allure generate %s -o %s --clean' % (allure_report_file, allure_report_dir)
        ops_tools().run_command(command)


    def get_allure_report(self, source_report_dir='', allure_report_dir=''):

        '''
        generate allure report via pytest result
        :param source_report_dir(hrun/pytest report dir):
        :param allure_report_dir:
        :return:
        '''
        if source_report_dir == '':
            source_report_dir = self.pytest_report_dir
        if allure_report_dir == '':
            allure_report_dir = self.allure_report_dir
        command = 'allure generate --clean ' + source_report_dir + ' -o ' + allure_report_dir
        exe_result = ops_tools().run_command(command)
        #check result
        if 'successfully' in str(exe_result):
            raise ('get test report successfully')
        else:
            raise ('fail to get test report')

    def run_test(self, script_name='', runner='pytest', pytest_report_name='', pytest_report_dir='', keyword='',
                 maxfail=100, parallel=1,reruns=3,reruns_delay=1):

        '''
        run test cases via pytest command
        :param script_name:
        :param runner:
        :param keyword:
        :param maxfail:
        :param parallel: pip install pytest-xdist,pip install pytest-rerunfailures
        :return:
        Note:  mulitple asserts:  pip3 install pytest-assume
        '''
        message = 'run test '+script_name+'runner='+runner+',pytest_report_name='+pytest_report_name+'pytest_report_dir='+pytest_report_dir
        self.logger.info(message)
        #
        if pytest_report_dir == '':
            pytest_report_dir = self.pytest_report_dir
        if pytest_report_name == '':
            pytest_report_name = self.pytest_report_name
        pytest_report_file = pytest_report_dir + '\\' + pytest_report_name
        #
        if os.path.exists(pytest_report_dir) and os.path.exists(script_name):
            parameters_init = ['-s', '-v', script_name, "--capture=sys"]
            if runner == 'pytest':
                #disable reruns
                if keyword == '':
                    if parallel == 1:
                        parameters = parameters_init + ['--maxfail=' + str(maxfail), '--html='+pytest_report_file,'--alluredir='+pytest_report_dir]
                    else:
                        parameters = parameters_init + ['-n '+str(parallel), '--maxfail='+str(maxfail),'--html='+pytest_report_file,'--alluredir='+pytest_report_dir]
                else:
                    if pytest_report_dir == '' and parallel == 1:
                        parameters = parameters_init + ['--maxfail='+str(maxfail), '--html='+pytest_report_file]
                    else:
                        parameters = parameters_init + ['-n '+str(parallel), '--maxfail='+str(maxfail),'--html='+pytest_report_file]
                # enable reruns
                if reruns != None and reruns_delay != None:
                    reruns_setting=['--reruns', str(reruns), '--reruns-delay', str(reruns_delay)]
                    parameters =parameters+reruns_setting
                try:
                    pytest.main(parameters)
                    #get allure report
                    #self.get_allure_report()
                except Exception as e:
                    #traceback.print_exc()
                    self.logger.exception('exception:' ,e)
                    raise('can not get report for script name:',script_name)
            else:
                pass
                # 遗留待补充
        else:
            raise('can not find pytest_report_dir=',pytest_report_dir,' and ',script_name)

    def execute_process(self, yaml_file='', update_content=None, source_dir='', target_dir='', folder_name='',
                        hrun_report_dir='', hrun_log_file=''):
        """
        execute whole process
        1>.copy yaml file from api to tests/temp
        2>.customize yaml file with update content(url/key/value...)
        3>.execute customized yaml file via hrun api
        4>.collect resulta and get hrun report
        """
        if update_content is None:
            update_content = {}
        if source_dir == '':
            source_dir = self.api_dir
        if target_dir == '':
            target_dir = self.exec_dir
        if hrun_report_dir == '':
            hrun_report_dir = target_dir + '\\' + folder_name + '\\report'
        if hrun_log_file == '':
            hrun_log_file = hrun_report_dir + '\\' + self.hrun_log_name
        #
        file_name = yaml_file
        yaml_file = target_dir + '\\' + folder_name + '\\' + yaml_file
        try:
            # step 1
            customize().prepare_yaml(source_dir, target_dir, folder_name, file_name)
            # step 2
            customize().customize_yaml(yaml_file, update_content, folder_name)
            # step 3
            summary = self.execute_yaml(yaml_file, hrun_log_file)
            # step 4
            result = collect().get_result(summary)
            request = collect().get_request(result)
            response = collect().get_response(result)
            self.logger.info('request='+self.get_request_info_format(request))
            self.logger.info('response='+self.get_request_info_format(response))
            if isinstance(result, dict) and result != {}:
                return result
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('exception:', e)
            raise ('check inputs for execute_process()')
        except BaseException as e:
            traceback.print_exc()
            raise ('execption =', e)
        except:
            return None

    def get_report(self, summary=None, report_template='', hrun_report_dir='', hrun_report_file=''):

        """
        get hrun report via summary
        """
        if summary is None:
            summary = {}
        if hrun_report_dir != '' and hrun_report_file == '' and not os.path.exists(hrun_report_dir):
            hrun_report_dir = self.hrun_report_dir
        if hrun_report_dir == '' and hrun_report_file != '' and not os.path.exists(hrun_report_file):
            hrun_report_file = self.hrun_report_file
        if hrun_report_dir == '' and hrun_report_file == '':
            hrun_report_dir = self.hrun_report_dir

        if report_template == '':
            return report.gen_html_report(summary, report_dir=hrun_report_dir,
                                          report_file=hrun_report_file)
        else:
            return report.gen_html_report(summary, report_template=report_template, report_dir=hrun_report_dir,
                                          report_file=hrun_report_file)

    def string_convert(self,data):

        if data==None:
           data='null'
        else:
            data = "'''" + data + "'''"
            if '&#34' in data:
                data = data.replace('&#34', '"')
            if 'Markup' in data:
                data = data.replace('Markup', '')
            if '(' in data:
                data = data.replace('(', '')
            if ')' in data:
                data = data.replace(')', '')
            if '\\n' in data:
                data = data.replace('\\n', '')
            if '...' in data:
                data = data.replace('...', '"')
            if ';' in data:
                data = data.replace(';', '')
            if 'true' in data:
                data = data.replace('true', 'True')
            if 'false' in data:
                data = data.replace('false', 'False')
            if '\\' in data:
                data = data.replace('\\', '')
            if "'''" in data:
                data = data.replace("'''", '')
            if '"' in data:
                data = data.replace('"', "'")
            if "'{" in data:
                data = data.replace("'{", '{')
            if "}'" in data:
                data = data.replace("}'", '}')
        return data

    def get_request_info_format(self,request_info):

        request_info= json.dumps(self.string_convert(json.dumps(request_info)), indent=4)
        return request_info

    def get_request_info(self,request_info):

        request_info= eval(str(self.string_convert(json.dumps(request_info))))
        return request_info


if __name__ == "__main__":

    pass
