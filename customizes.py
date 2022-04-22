# coding:utf-8
import traceback

from Utils.configs import *
from Utils.tools import ops_tools, tools
from Utils.logger import logger

class customize():

    def __init__(self):

        self.project_dir = project_vars().project_dir
        self.exec_dir = project_vars().exec_dir
        self.api_dir = project_vars().api_dir
        self.cookie = project_vars().cookie
        self.logger = logger().setup_logging()
        # self.folder_name = ''

    def customize_yaml(self, yaml_file='', update_content=None, folder_name=''):

        """
        customize yaml with update content
        """
        if update_content == None:
            update_content = {}
        message = 'yaml_file:' + yaml_file + ',' + 'update_content: ' + str(
            update_content) + ',' + 'folder_name=' + folder_name
        self.logger.info('[' + self.customize_yaml.__name__ + ']:' + message)
        if os.path.exists(yaml_file) and isinstance(update_content, dict):
            try:
                # update yaml file with environment
                self.update_yaml_by_dict(yaml_file, update_content, folder_name)
                #
            except Exception as e:
                traceback.print_exc()
                self.logger.exception('exception:', e)
                raise ('please check input parameters for ' + message)
            except BaseException as e:
                traceback.print_exc()
                raise ('execption =',e)
            except:
                return None
        else:
            raise (yaml_file + ' does not exist')

    def update_yaml_by_dict(self, yaml_file='', update_content=None, folder_name=''):

        '''
        update yaml file with environment and set headers(refer/host... to null)
        :param yaml_file:
        :param update_content:
        :return:
        '''
        if update_content == None:
            update_content = {}
        try:
            service_name = folder_name.split("\\", 1)[0]
            web_url = envirment().get_url(service_name=service_name)
            yaml_data = tools().read_yaml_file(yaml_file)
            #print('yaml_data0=', yaml_data)
            if 'config' in yaml_data.keys():
                config_data = yaml_data['config']
                config_data = ops_tools().update_dict_v0(config_data, update_content)
                yaml_data['config'] = config_data
            if 'teststeps' in yaml_data.keys() and isinstance(yaml_data['teststeps'], list):
                if 'validate' in yaml_data['teststeps'][0]:
                    validate_data = yaml_data['teststeps'][0]['validate']  # does not replace
                if 'name' in yaml_data['teststeps'][0]:
                    api_name = yaml_data['teststeps'][0]['name']  # does not replace
                    if 'request' in yaml_data['teststeps'][0]:
                        teststep_name_request = yaml_data['teststeps'][0]['request']  # depend on the selection exists
                        if isinstance(teststep_name_request, dict):
                            for key in teststep_name_request.keys():
                                if key == 'headers':
                                    content = teststep_name_request[key]
                                    teststep_name_request[key] = self.reset_headers(content)
                                elif key == 'url':
                                    teststep_name_request[key] = web_url + api_name
                                else:
                                    continue
                            # ignore https
                            if 'verify' not in teststep_name_request.keys():
                                teststep_name_request['verify'] = False
                        # add cookies
                        if 'cookies' not in teststep_name_request.keys():
                            teststep_name_request['cookies'] = project_vars().cookie
                        else:
                            if 'SSID' not in teststep_name_request['cookies'].keys():
                                teststep_name_request['cookies'] = project_vars().cookie
                        # update yaml data
                        teststep_name_request = ops_tools().update_dict_v0(teststep_name_request, update_content)
                        #
                        #print('teststep_name_request=',teststep_name_request)
                        yaml_data['teststeps'][0]['request'] = teststep_name_request
            #print('yaml_data1=',yaml_data)
            # write yaml file
            tools().write_yaml_file(yaml_file, yaml_data)
        except Exception as e:
            traceback.print_exc()
            self.logger.exception('exception:', e)
            raise ('can not update yaml_file' + str(yaml_file) + ' with ' + str(update_content))
        except BaseException as e:
            traceback.print_exc()
            raise ('execption =', e)
        except:
            return None

    def reset_headers(self, headers=None):

        # reset host,Referer,Origin,Cookie value =None
        # remove the key of host,Referer,Origin,Cookie also work well

        if headers == None:
            headers = {}
        reset_keys = ['Host', 'Referer', 'Origin', 'Cookie']
        for key in headers.keys():
            if key in reset_keys:
                headers[key] = None
            else:
                continue
        return headers

    def prepare_yaml(self, source_dir='', target_dir='', folder_name='', file_name=''):
        """
        copy api/yaml file to tests/temp dictionary
        """

        if source_dir == '':
            source_dir = self.api_dir
        if target_dir == '':
            target_dir = self.exec_dir
        if os.path.exists(source_dir) and os.path.exists(target_dir) and folder_name != '' and file_name != '':

            source_yaml_file = source_dir + '\\' + folder_name + '\\' + file_name
            target_yaml_file = target_dir + '\\' + folder_name + '\\' + file_name
            ops_tools().copy_yaml(source_yaml_file, target_yaml_file)
        else:
            raise ('please check input parameters')

    def get_yaml_api_name(self, yaml_file_path):

        '''
        get api name from yaml file
        '''
        self.logger.info('yaml_file_path=' + yaml_file_path)
        if isinstance(yaml_file_path, str):
            try:
                yaml_content = tools().read_yaml_file(yaml_file_path)
                api_name = yaml_content['teststeps'][0]['name']
                if api_name != '' and isinstance(api_name, str):
                    return api_name
                else:
                    return None
            except Exception as e:
                self.logger.info('exception:', e)
                raise ('can not get yaml url from ', str(yaml_file_path))
            except BaseException as e:
                traceback.print_exc()
                raise ('execption =',e)
            except:
                return None
        else:
            raise ('can not read file ' ,yaml_file_path)


if __name__ == "__main__":

    pass
