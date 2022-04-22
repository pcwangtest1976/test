# -*- coding: UTF-8 -*-

import os
import xmltodict
import json
import yaml
from urllib.parse import urlparse
import re
import time
import datetime
import subprocess
import traceback


class tools():

    def __init__(self):

        pass

    def get_day_time(self, format):
        if format == '':
            daytime = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            daytime = (datetime.datetime.now() + datetime.timedelta(days=format)).strftime("%Y-%m-%d")
        return daytime

    def get_second_time(self, format):
        if format == '':
            secomdtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            secomdtime = (datetime.datetime.now() + datetime.timedelta(days=format)).strftime("%Y-%m-%d %H:%M:%S")
        return secomdtime

    def get_now_time(self):

        '''
        '''
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return nowtime

    def get_datetime(self, format=''):

        '''
        :return:
        '''
        if format == '':
            time_string = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        else:
            time_string = time.strftime('%Y' + str(format) + '%m' + str(format) + '%d', time.localtime(time.time()))
        return time_string

    def get_currenttime(self, format=''):

        '''
        :param format:
        :return:
        '''
        if format == '':
            current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        else:
            current_time = time.strftime(
                '%Y' + str(format) + '%m' + str(format) + '%d' + str(format) + '%H' + str(format) + '%M' + str(
                    format) + '%S ', time.localtime(time.time()))
        return current_time

    def get_project_path(self, project_name='Test'):

        '''
        :param project_name:
        :return:
        '''
        pro_name = 'Test' if project_name is None else project_name

        project_path = os.path.abspath(os.path.dirname(__file__))

        root_path = project_path[:project_path.find("{}'\\'".format(pro_name)) + len("{}'\\'".format(pro_name))]

        return str(root_path)[:-1]

    def get_current_dir(self):

        '''
        :return:
        '''
        return os.getcwd()

    def get_parent_dir(self):

        '''
        :return:
        '''
        return os.path.abspath(os.path.dirname(self.get_current_dir()))

    def xml_to_json(self, xml_data=''):
        '''
        :param xml_data:
        :return:
        '''
        xmlparse = xmltodict.parse(xml_data)
        json_data = json.dumps(xmlparse, indent=4)
        return json_data

    def dict_to_xml(self, dict_data=None):

        '''
        :param dict_data:
        :return:
        '''
        if dict_data == None:
            dict_data = {}
        xml_data = xmltodict.unparse(dict_data, pretty=1)
        return xml_data

    def xml_to_dict(self, xml_data=''):

        '''
        :param xml_data:
        :return:
        '''
        dict_data = xmltodict.parse(xml_data)
        return dict_data

    def json_to_xml(self, json_data=None):
        '''
        :param json_data:
        :return:
        '''
        if json_data == None:
            json_data = {}
        xml_data = xmltodict.unparse(json_data)
        return xml_data

    def json_to_yaml(self, json_data=None):
        '''
        :param json_data:
        :return:
        '''
        if json_data == None:
            json_data = {}
        yaml_data = yaml.load(json_data, Loader=yaml.FullLoader)
        return yaml_data

    def read_json_file(self, file=''):
        """
        :param file: json file
        :return: json data
        """
        fp = open(file, 'r', encoding='utf-8')
        jsondata = json.load(fp)

        return jsondata

    def write_json_file(self, file='', dict_data=None):
        '''
        :param file:
        :param dict_data:
        :return:
        '''
        if dict_data == None:
            dict_data = {}
        fp = open(file, "w")
        json.dump(dict_data, fp)
        fp.close()

    def read_xml_file(self, file=''):
        '''

        :param file:
        :return:
        '''
        fp = open(file, 'r', encoding='utf-8')
        xmldata = fp.read()
        fp.close()
        return xmldata

    def write_xml_file(self, file_path='', xml_data=''):
        '''

        :param file_path:
        :param xml_data:
        :return:
        '''
        if os.path.exists(file_path):
            fp = open(file_path, "w", encoding='utf-8')
            fp.write(xml_data, indent="\n", addindent="\t")
            fp.close()
        else:
            print(file_path, 'does not exist')

    def read_yaml_file(self, yaml_file=''):
        '''

        :param yaml_file:
        :return:
        '''
        with open(yaml_file, mode='r', encoding='utf-8') as f:
            dict_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return dict_data

    def write_yaml_file(self, file='', yaml_data=''):
        '''
        :param yaml_data:
        :return:
        '''
        fp = open(file, 'w', encoding='utf-8')
        yaml.dump(yaml_data, fp, allow_unicode=True, default_flow_style=False, indent=4)
        fp.close()

    def parse_url(self, url=''):
        '''

        :param url:
        :return:
        '''
        output = {}
        result = urlparse(url)
        output['hostname'] = result.hostname
        if result.port == None or result.port == 'None' or result.port == '':
            output['port'] = 80
        else:
            output['port'] = result.port
        output['base_url'] = result.path.replace('/', '')
        output['protocol'] = result.scheme
        output['username'] = result.username
        output['password'] = result.password
        output['query'] = result.query
        return output

    def yaml_to_dict(self, yaml_data=''):

        '''

        :param yaml_data:
        :return:
        '''
        dict_data = yaml.load(yaml_data, Loader=yaml.FullLoader)
        return dict_data

    def dict_to_yaml(self, dict_data=None):
        '''

        :param dict_data:
        :return:
        '''
        if dict_data == None:
            dict_data = {}
        yaml_data = yaml.dump(dict_data)
        return yaml_data

    def dict_to_json(self, dict_data=None):
        '''

        :param dict_data:
        :return:
        '''
        if dict_data == None:
            dict_data = {}
        json_data = json.dumps(dict_data)

        return json_data

    def json_to_dict(self, json_data=''):
        '''

        :param json_data:
        :return:
        '''
        json_data = json.loads(json_data)

        return json_data

    def dict_merge(self, dict1=None, dict2=None):

        if dict1 == None:
            dict1 = {}
        if dict2 == None:
            dict2 = {}
        if isinstance(dict1, dict) and isinstance(dict2, dict):
            object_dict = dict(dict1, **dict2)
            return object_dict
        else:
            print('please check ' + str(dict1) + ',' + str(dict2) + ' types are dict')
            return {}

    def list_merge(self, list1, list2):

        object_list = list1 + list2
        return object_list


class ops_tools():

    def __init__(self):

        pass

    def run_command(self, cmd=''):

        outputs, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE).communicate()
        output = outputs.decode("utf-8")
        print('cmd 命令执行成功！')
        return output

    def update_yaml_field(self, yaml_file='', field=None):

        '''
        :param yaml_file:
        :param field:
        :return:
        '''
        if field == None:
            field = {}
        self.replace_yaml_file(yaml_file, field)

    def get_xml_content(self, file=''):
        '''
        :param file:
        :return:
        '''

        xml_str = tools().read_xml_file(file)
        test_dict = tools().xml_to_json(xml_str)
        return test_dict

    def get_yaml_content(self, file_name=''):

        '''
        :param file_name:
        :return:
        '''
        if os.path.exists(file_name):
            yaml_file = open(file_name, 'r', encoding="utf-8")
            yaml_content = yaml_file.readlines()
            return yaml_content
        else:
            message = file_name + ' does not exist'
            # print(message)
            return None

    def get_replace_str(self, string='', dict_vars=None):
        '''
        替换一个字符串中间的变量，用这个变量的值来替换，
        for an example: {'$test',['$abc'],'abc$test$abc'},使用一个对应的字典来做替换，比如 {'test':'12344','abc':'ok'}
        :param string:
        :param dict_vars:
        :return:
        '''
        if dict_vars == None:
            dict_vars = {}
        if isinstance(dict_vars, dict):
            for key in dict_vars:
                if string.find(key) != -1:
                    string = string.replace(key, str(dict_vars[key]))
                else:
                    continue
            return string
        else:
            message = string + ' or ' + str(dict_vars) + 'are invalid'
            # print(message)
            return None

    def replace_yaml_file(self, file_name='', dict_vars=None):
        '''
        :param file_name: yaml file
        :param dict_vars: vars dict,for an example {'message': test}
        :return:
        '''
        if dict_vars == None:
            dict_vars = {}
        if os.path.exists(file_name) and isinstance(dict_vars, dict):
            yaml_content = self.get_yaml_content(file_name)
            new_yaml_content = []
            for line in yaml_content:
                new_yaml_content.append(self.get_replace_str(line, dict_vars))
            # rewrite update content
            yaml_file = open(file_name, "w", encoding="utf-8")
            for line in new_yaml_content:
                yaml_file.write(line)
            yaml_file.close()
        else:
            raise ('do nothing as ' + file_name + ',' + str(dict_vars) + 'types are invalid')

    def copy_yaml(self, source_yaml_path='', target_yaml_path=''):

        '''
        :param source_yaml_path:
        :param target_yaml_path:
        :return:
        '''
        # print('source_yaml_path=', source_yaml_path, 'target_yaml_path=', target_yaml_path)
        if os.path.exists(target_yaml_path):
            command = 'del ' + target_yaml_path
            # print('command =', command)
            os.system(command)
        if os.path.exists(source_yaml_path):
            command = 'copy ' + source_yaml_path + ' ' + target_yaml_path
            # print('command =', command)
            os.system(command)
        else:
            # print('source_yaml_path======',source_yaml_path)
            raise (source_yaml_path + ' does not exists')

    def replace_str(self, line='', old_str='', new_str=''):

        '''
        :param line:
        :param old_str:
        :param new_str:
        :return:
        '''
        line = re.sub(old_str, new_str, line)
        return line

    def update_dict_v0(self, dict_data=None, dict_set=None):

        if dict_data == None:
            dict_data = {}
        if dict_set == None:
            dict_set = {}
        if isinstance(dict_data, list):
            for i in range(len(dict_data)):
                if isinstance(dict_data[i], list) or isinstance(dict_data[i], dict):
                    dict_data[i] = self.update_dict_v0(dict_data[i], dict_set)
        elif isinstance(dict_data, dict):
            for test_key, test_value in dict_data.items():
                if isinstance(test_value, dict):
                    dict_data[test_key] = self.update_dict_v0(test_value, dict_set)
                elif (dict_set.get(test_key) != None):
                    dict_data[test_key] = dict_set[test_key]
                elif isinstance(test_value, list):
                    dict_data[test_key] = self.update_dict_v0(test_value, dict_set)
        return dict_data


    def update_dict_v1(self,dict_data=None,dict_set=None):

        if dict_data == None:
            dict_data = {}
        if dict_set == None:
            dict_set = {}
        for test_key in dict_set.keys():
            if test_key in dict_data.keys():
                if isinstance(dict_data, list):
                    for i in range(len(dict_data)):
                        if isinstance(dict_data[i], list) or isinstance(dict_data[i], dict):
                            dict_data[i] = self.update_dict_v1(dict_data[i], dict_set)
                elif isinstance(dict_data, dict):
                    for test_key, test_value in dict_data.items():
                        if isinstance(test_value, dict):
                            dict_data[test_key] = self.update_dict_v1(test_value, dict_set)
                        elif (dict_set.get(test_key) != None):
                            dict_data[test_key] = dict_set[test_key]
                        elif isinstance(test_value, list):
                            dict_data[test_key] = self.update_dict_v1(test_value, dict_set)
            else:

                test_dict = {test_key: dict_set[test_key]}
                dict_data.update(test_dict) # 添加到第一层（如果都没有没替换掉就添加到第一层，如果用到了就不添加）
        return dict_data

    def update_yaml_by_dict(self, yaml_file='', update_content=None):

        '''
        :param yaml_file:
        :param update_content:
        :return:
        '''
        # without set url ,need to set in update content
        # message = '[update_yaml_by_dict]: yaml_file=', yaml_file, 'update_content=', str(update_content)
        # print(message)
        if update_content == None:
            update_content = {}
        try:
            yaml_data = tools().read_yaml_file(yaml_file)
            if 'config' in yaml_data.keys():
                config_data = yaml_data['config']
                config_data = self.update_dict_v0(config_data, update_content)
                yaml_data['config'] = config_data
            if 'teststeps' in yaml_data.keys() and isinstance(yaml_data['teststeps'], list):
                if 'validate' in yaml_data['teststeps'][0]:
                    validate_data = yaml_data['teststeps'][0]['validate']  # does not replace
                if 'name' in yaml_data['teststeps'][0]:
                    teststep_name_data = yaml_data['teststeps'][0]['name']  # does not replace
                if 'request' in yaml_data['teststeps'][0]:
                    teststep_name_request = yaml_data['teststeps'][0]['request']  # depend on the selection exists
                    if isinstance(teststep_name_request, dict):
                        teststep_name_request = self.update_dict_v0(teststep_name_request, update_content)
                    yaml_data['teststeps'][0]['request'] = teststep_name_request

            # write yaml file
            tools().write_yaml_file(yaml_file, yaml_data)
        except Exception as e:
            print('exception:', e)
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

    def parse_url(self, url=''):
        '''
        :param url:
        :return:
        '''
        output = {}
        result = urlparse(url)
        output['hostname'] = result.hostname
        if result.port == None or result.port == 'None' or result.port == '':
            output['port'] = 80
        else:
            output['port'] = result.port
        output['base_url'] = result.path.replace('/', '')
        output['protocol'] = result.scheme
        output['username'] = result.username
        output['password'] = result.password
        output['query'] = result.query
        return output

    def get_url_root(self, url=''):

        url_result = ops_tools().parse_url(url)
        port = url_result['port']
        protocol = url_result['protocol']
        hostname = url_result['hostname']
        if port == 80 or port == '80':
            url_root = protocol + '://' + hostname
        else:
            url_root = protocol + '://' + hostname + ':' + str(port)
        return url_root

    def update_values_dict_v1(self, original_dict, future_dict, old_value, new_value):

        if isinstance(original_dict, dict):
            tmp_dict = {}
            for key, value in original_dict.items():
                tmp_dict[key] = self.update_values_dict_v1(value, future_dict, old_value, new_value)
            return tmp_dict
        elif isinstance(original_dict, list):
            tmp_list = []
            for i in original_dict:
                tmp_list.append(self.update_values_dict_v1(i, future_dict, old_value, new_value))
            return tmp_list
        else:
            return original_dict if original_dict != old_value else new_value

    def update_values_dict_v2(self, original_dict, future_dict, old_value, new_value):

        return str(original_dict).replace(old_value, new_value)



class test():

    def __init__(self):

        pass

    def test_01(self):

        a= {'a':1,'b':243,'c':1323,'d':[{'a':21,'b':'def'}],'e':[{'d':[{'a':21,'b':'def'}]}]}
        b= {'a':2,'b':24322,'c':1323223,'d':[{'a':21,'b':'def'}],'e':'hello','f':[{'a':21,'b':'def'}]}
        new_a = self.update_dict(a,b)
        print('new_a=',new_a)
        new_a = self.update_dict2(a, b)
        print('new_a=', new_a)

    def update_dict(self, dict_data=None, dict_set=None):

        if dict_data == None:
            dict_data = {}
        if dict_set == None:
            dict_set = {}
        if isinstance(dict_data, list):
            for i in range(len(dict_data)):
                if isinstance(dict_data[i], list) or isinstance(dict_data[i], dict):
                    dict_data[i] = self.update_dict(dict_data[i], dict_set)
        elif isinstance(dict_data, dict):
            for test_key, test_value in dict_data.items():
                if isinstance(test_value, dict):
                    dict_data[test_key] = self.update_dict(test_value, dict_set)
                elif (dict_set.get(test_key) != None):
                    dict_data[test_key] = dict_set[test_key]
                elif isinstance(test_value, list):
                    dict_data[test_key] = self.update_dict(test_value, dict_set)
        return dict_data

    def update_dict2(self,dict_data=None,dict_set=None):

        if dict_data == None:
            dict_data = {}
        if dict_set == None:
            dict_set = {}
        for test_key in dict_set.keys():
            if test_key in dict_data.keys():
                if isinstance(dict_data, list):
                    for i in range(len(dict_data)):
                        if isinstance(dict_data[i], list) or isinstance(dict_data[i], dict):
                            dict_data[i] = self.update_dict(dict_data[i], dict_set)
                elif isinstance(dict_data, dict):
                    for test_key, test_value in dict_data.items():
                        if isinstance(test_value, dict):
                            dict_data[test_key] = self.update_dict(test_value, dict_set)
                        elif (dict_set.get(test_key) != None):
                            dict_data[test_key] = dict_set[test_key]
                        elif isinstance(test_value, list):
                            dict_data[test_key] = self.update_dict(test_value, dict_set)
            else:
                test_dict = {test_key: dict_set[test_key]}
                dict_data.update(test_dict)
        return dict_data

if __name__ == "__main__":


    test().test_01()
    pass

