# -*- coding: UTF-8 -*-


from Utils.tools import *
import traceback

class project_setting():

    def __init__(self, project_file='../Config/configs.yml'):

        self.project_config_file = project_file

    def get_project_configs(self, yaml_file=''):

        '''
        get project config
        '''
        if yaml_file == '':
            try:
                file_path = os.path.abspath(__file__)
                parent_dir = os.path.dirname(file_path)
                project_dir = os.path.abspath(os.path.dirname(parent_dir))
                yaml_file = project_dir + '\\Config\\configs.yml'
                project_configs_data = tools().read_yaml_file(yaml_file=yaml_file)
                project_configs_data['project_setting']['project_dir'] = project_dir
                tools().write_yaml_file(yaml_file, project_configs_data)
                return project_configs_data
            except Exception as e:
                traceback.print_exc()
                print('exception:', e)
            except BaseException as e:
                traceback.print_exc()
                raise ('execption =',e)
            except:
                return None

    def get_project_setting(self):

        project_configs_data = self.get_project_configs()
        if isinstance(project_configs_data, dict):
            project_setting = project_configs_data['project_setting']
            return project_setting
        else:
            return None

    def get_execute_setting(self):

        get_project_setting = self.get_project_setting()
        if isinstance(get_project_setting, dict):
            return get_project_setting['test_case_execute_setting']
        else:
            return None

    def get_hrun_setting(self):

        report_setting = self.get_report_setting()
        if isinstance(report_setting, dict):
            allure_setting = report_setting['hrun_setting']
            return allure_setting
        else:
            return None

    def get_logging_setting(self):

        project_setting = self.get_project_setting()
        if isinstance(project_setting, dict):
            logging_setting = project_setting['logging_setting']
            return logging_setting
        else:
            return None

    def get_pytest_setting(self):

        report_setting = self.get_report_setting()
        if isinstance(report_setting, dict):
            allure_setting = report_setting['pytest_setting']
            return allure_setting
        else:
            return None

    def get_allure_setting(self):

        report_setting = self.get_report_setting()
        if isinstance(report_setting, dict):
            allure_setting = report_setting['allure_setting']
            return allure_setting
        else:
            return None

    def get_test_environment_setting(self):

        project_setting = self.get_project_setting()
        if isinstance(project_setting, dict):
            test_environment_setting = project_setting['test_environment_setting']
            return test_environment_setting
        else:
            return None

    def get_test_case_execute_setting(self):

        project_setting = self.get_project_setting()
        if isinstance(project_setting, dict):
            test_case_execute_setting = project_setting['test_case_execute_setting']
            return test_case_execute_setting
        else:
            return None

    def get_execute_api_yaml_dir(self):

        project_setting = self.get_project_setting()
        if isinstance(project_setting, dict):
            project_dir = self.get_project_dir()
            execute_api_yaml_dir = project_dir + project_setting['execute_api_yaml_dir']
            return execute_api_yaml_dir
        else:
            return None

    def get_api_yaml_dir(self):

        project_setting = self.get_project_setting()
        if isinstance(project_setting, dict):
            project_dir = self.get_project_dir()
            api_yaml_dir = project_dir + project_setting['api_yaml_dir']
            return api_yaml_dir
        else:
            return None

    def get_test_case_dir(self):

        project_setting = self.get_project_setting()
        if isinstance(project_setting, dict):
            project_dir = self.get_project_dir()
            test_case_dir = project_dir + project_setting['test_case_dir']
            return test_case_dir
        else:
            return None

    def get_project_dir(self):

        project_setting = self.get_project_setting()
        if isinstance(project_setting, dict):
            project_dir = project_setting['project_dir']
            return project_dir
        else:
            return None

    def get_report_dir(self):

        report_setting = self.get_report_setting()
        if isinstance(report_setting, dict):
            report_dir = report_setting['report_dir']
            project_dir = self.get_project_dir()
            report_dir = project_dir + report_dir
            return report_dir
        else:
            return None

    def get_report_setting(self):

        project_setting = self.get_project_setting()
        if isinstance(project_setting, dict):
            report_setting = project_setting['report_setting']
            return report_setting
        else:
            return None


class project_vars():

    def __init__(self):

        pass

    #
    project_dir = project_setting().get_project_dir()
    api_dir = project_setting().get_api_yaml_dir()
    exec_dir = project_setting().get_execute_api_yaml_dir()
    cookie = {'SSID': '', 'SCMToken': '', 'PowerTmsCookie': ''}
    #
    https_ignore={'request':{'verify':'false'}}
    #
    report_setting = project_setting().get_report_setting()
    report_dir = project_dir + report_setting['report_dir']

    #
    hrun_setting = project_setting().get_hrun_setting()
    hrun_report_dir = report_dir + hrun_setting['report_dir']
    hrun_report_name = hrun_setting['report_name']
    hrun_report_file = hrun_report_dir + '\\' + hrun_report_name
    hrun_log_name = hrun_setting['report_log_name']
    hrun_log_file = hrun_report_dir + '\\' + hrun_log_name
    #
    pytest_setting = project_setting().get_pytest_setting()
    pytest_report_dir = report_dir + pytest_setting['report_dir']
    pytest_report_name = pytest_setting['report_name']
    pytest_report_file = pytest_report_dir + '\\' + pytest_report_name
    pytest_log_name = pytest_setting['report_log_name']
    pytest_log_file = pytest_report_dir + '\\' + pytest_log_name
    #
    allure_setting = project_setting().get_allure_setting()
    allure_report_dir = report_dir + allure_setting['report_dir']
    #
    logging_setting = project_setting().get_logging_setting()
    logging_config_dir = project_dir + logging_setting['logging_config_dir']
    logging_config_name = logging_setting['logging_config_name']
    log_config_file = logging_config_dir + '\\' + logging_config_name
    #
    test_environment_setting = project_setting().get_test_environment_setting()
    test_environment_config_dir = project_dir + test_environment_setting['test_environment_config_dir']
    test_environment_config_name = test_environment_setting['test_environment_config_name']
    environment_config_file = test_environment_config_dir + '\\' + test_environment_config_name
    #
    config_dir = test_environment_config_dir


class envirment():

    def __init__(self, env_file='../Config/environment.yml'):

        if os.path.exists(env_file):
            self.env_config_file = env_file
        else:
            self.env_config_file = project_vars().config_dir + '\\' + 'environment.yml'
        #print('self.env_config_file=',self.env_config_file)

    def fromat_configs(self):

        env_config_data = tools().read_yaml_file(self.env_config_file)
        #print('env_config_data=',env_config_data)
        tools().write_yaml_file(self.env_config_file,env_config_data)

    def get_env_configs(self):

        env_config_data = tools().read_yaml_file(self.env_config_file)
        return env_config_data

    def get_runtime_envname(self):

        env_data = self.get_env_configs()
        if env_data != None and isinstance(env_data, dict):
            return env_data['environments']['runTimeSettings']['Environment']
        else:
            return None

    def get_runtime_envsettings(self):

        env_data = self.get_env_configs()
        runtime_env_name = str(env_data['environments']['runTimeSettings']['Environment']).strip()
        env_list = env_data['environments']['environment']
        run_time_env=None
        for env in env_list:
            if str(env['name']).strip() == str(runtime_env_name).strip():
                run_time_env= env['customSettings']
            else:
                continue
        return run_time_env

    def get_user_name(self):

        runtime_env = self.get_runtime_envsettings()
        if isinstance(runtime_env, dict):
            return runtime_env['setting']['SCM.Username']
        else:
            return None

    def get_password(self):

        runtime_env = self.get_runtime_envsettings()
        if isinstance(runtime_env, dict):
            return runtime_env['setting']['SCM.Password']
        else:
            return None

    def get_api_key(self):

        runtime_env = self.get_runtime_envsettings()
        if isinstance(runtime_env, dict):
            return runtime_env['setting']['SCM.Apikey']
        else:
            return None

    def get_service_url(self, key_name):

        if key_name!=None:
            runtime_env = self.get_runtime_envsettings()
            if isinstance(runtime_env, dict):
                return runtime_env['apps'][key_name]
            else:
                return None
        else:
            return None

    def get_tms_url(self, key_name='SCM.TMS.URL'):

        return self.get_service_url(key_name)

    def get_oms_url(self, key_name='SCM.URL'):

        return self.get_service_url(key_name)

    def get_wms_url(self, key_name='SCM.WMS.URL'):

        return self.get_service_url(key_name)

    def get_rf_url(self, key_name='SCM.RF.URL'):

        return self.get_service_url(key_name)

    def get_ams_url(self, key_name='SCM.URL'):

        return self.get_service_url(key_name)

    def get_scm_url(self, key_name='SCM.URL'):

        return self.get_service_url(key_name)

    def get_url(self, service_name):

        if service_name == 'Oms':
            return envirment().get_oms_url()
        elif service_name == 'Tms':
            return envirment().get_tms_url()
        elif service_name == 'Wms':
            return envirment().get_wms_url()
        elif service_name == 'Ams':
            return envirment().get_ams_url()
        elif service_name == 'Rf':
            return envirment().get_rf_url()
        elif service_name == 'Scm':
            return envirment().get_scm_url()
        else:
            print('input invalid service name:',service_name)
            return None


class test():

    def __init__(self):
        pass

    def test_01(self):

        envirment().fromat_configs()
        print(
            'get_runtime_envsettings=', envirment().get_runtime_envsettings(),
            '\nproject_dir=', project_vars().project_dir,
            '\napi_dir=', project_vars().api_dir,
            '\nexec_dir=', project_vars().exec_dir,
            '\ncookie=', str(project_vars().cookie),
            '\nreport_setting=', project_vars().report_setting,
            '\nreport_dir=', project_vars().report_dir,
            #
            '\nhrun_report_dir=', project_vars().hrun_report_dir,
            '\nhrun_report_name=', project_vars().hrun_report_name,
            '\nhrun_log_name=', project_vars().hrun_log_name,
            '\nhrun_log_file=', project_vars().hrun_log_file,
            #
            '\npytest_report_dir=', project_vars().pytest_report_dir,
            '\npytest_report_name=', project_vars().pytest_report_name,
            '\npytest_log_name=', project_vars().pytest_log_name,
            '\npytest_log_file=', project_vars().pytest_log_file,
            #
            '\nallure_setting=', project_vars().allure_setting,
            '\nallure_report_dir=', project_vars().allure_report_dir,
            #
            '\nlogging_config_dir=', project_vars().logging_config_dir,
            '\nlogging_config_name=', project_vars().logging_config_name,
            '\nlog_config_file=', project_vars().log_config_file,
            #
            '\ntest_environment_config_dir=', project_vars().test_environment_config_dir,
            '\ntest_environment_config_name=', project_vars().test_environment_config_name,
            '\nenvironment_config_file=', project_vars().environment_config_file
        )
        tms_url = envirment().get_tms_url()
        print('tms_url=', tms_url)


if __name__ == "__main__":

    test().test_01()
    pass

    # test().test_01()
