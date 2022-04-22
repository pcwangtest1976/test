import sys

from Utils.tools import tools,ops_tools
import os
from Utils.collects import *
from Utils.configs import *
from collections import Counter


class process():

    service_name='Wms'

    def __init__(self):

        pass

    class read_ops():

        def __init__(self):

            pass

        def get_yaml_data(self,yaml_file):

            '''
            get yaml file content
            '''
            if os.path.exists(yaml_file):
                yaml_data = tools().read_yaml_file(yaml_file)
                if yaml_data!=None:
                    return yaml_data
                else:
                    return None
            else:
                raise('can not find file :',yaml_file)

        def get_config_info(self,yaml_data):

            '''
            get config info
            '''
            if yaml_data!=None:
                if 'config' in yaml_data.keys():
                    config_info = yaml_data['config']
                    return config_info
                else:
                    return None
            else:
                return None

        def get_api_info(self,yaml_data):

            '''
            get api info
            '''
            if yaml_data!=None:
                if 'teststeps' in yaml_data.keys():
                    apis_info = yaml_data['teststeps']
                    return apis_info
                else:
                    return None
            else:
                return None

    class write_ops():

        def __init__(self):

            pass

        def set_test_folder(self,file_path,folder_name='test'):

            '''
            prepare test folder
            '''
            if os.path.exists(file_path):
                if folder_name != 'test':
                    folder_name = os.path.basename(file_path)
                dir_path = os.path.dirname(file_path)
                # print('dir_path=',dir_path)
                test_path= dir_path+'\\'+folder_name
                if not os.path.exists(test_path):
                    os.mkdir(test_path)
                # print('test_path=',test_path)
                return test_path
            else:
                return None

        def set_api_yaml(self,yaml_file):

            '''
            prepare yaml file for every api
            '''
            test_path = self.set_test_folder(yaml_file)
            if test_path!=None:
                yaml_data = process().read_ops().get_yaml_data(yaml_file)
                config_info = process().read_ops().get_config_info(yaml_data)
                api_info = process().read_ops().get_api_info(yaml_data)
                api_info = self.reset_api_info(api_info)
                for i in range(len(api_info)):
                    api_name = api_info[i]['name']
                    # for j in range(i,len(api_info_1)):
                    api_file_name = self.set_file_name(api_name)
                    api_file_path= test_path+'\\'+api_file_name
                    yaml_data={}
                    yaml_data['config'] = config_info
                    yaml_data['teststeps'] = []
                    yaml_data['teststeps'].append(api_info[i])
                    yaml_data['teststeps'][0]['name']=str(api_name).split('_')[0]
                    self.write_yaml_file(api_file_path,yaml_data)
            else:
                raise('can not set folder path with :',yaml_file)

        def write_yaml_file(self,file_name,yaml_data):

            '''
            write yaml files
            '''
            return tools().write_yaml_file(file_name, yaml_data)

        def set_file_name(self,api_name,end_with='.yml'):

            '''
            get api yaml file name
            '''
            api_name_split = str(api_name).strip().split('/')
            # #2_#3 = api file name
            if len(api_name_split) == 4:
                file_name = api_name_split[2] + '_' + api_name_split[3] + end_with
            elif len(api_name_split) == 3:
                file_name = api_name_split[1] + '_' + api_name_split[2] + end_with
            else:
                file_name = api_name_split[0] + '_' + api_name_split[1] + end_with
            return file_name

        def delete_file(self,file_path):

            '''
            remove file
            '''
            if os.path.exists(file_path):
                os.remove(file_path)

        def set_api_py(self,yaml_file):

            '''
            set api py file
            '''
            yaml_data = process().read_ops().get_yaml_data(yaml_file)
            api_info = process().read_ops().get_api_info(yaml_data)
            file_name = os.path.split(yaml_file)[-1].split(".")[0]
            base_dir_path = os.path.dirname(yaml_file)
            file_path = base_dir_path + '\\' + file_name + '.py'
            #
            if os.path.exists(file_path):
                self.delete_file(file_path)
            #
            api_name_list = self.get_api_name(api_info)
            self.set_api_header(file_path)
            self.set_api_content(api_name_list,file_path)

        def get_api_name(self, api_info):

            '''
            get api name
            '''
            for i in api_info:
                api_name = i['name']
                api_name_split = str(api_name).strip().split('/')
                if len(api_name_split) == 4:
                    api_short_name = api_name_split[2] + '_' + api_name_split[3]
                elif len(api_name_split) == 3:
                    api_short_name = api_name_split[1] + '_' + api_name_split[2]
                else:
                    api_short_name = api_name_split[0] + '_' + api_name_split[1]
                i['name']= api_short_name
            api_names_list = self.reset_api_info(api_info)
            return api_names_list

        def set_tab_space(self,tab=''):

            '''
            create tab space
            '''
            if tab == '':
                return '    '
            else:
                return tab

        def set_api_header(self,file_name=''):

            '''
            set api header info 
            '''
            if os.path.exists(file_name):
                self.delete_file(file_name)
            fs = open(file_name, 'w', encoding='utf-8')
            #
            _tab_space = self.set_tab_space()
            _2tab_space = _tab_space + _tab_space
            class_name = os.path.basename(file_name).split('.')[0]
            #
            lines_content=[]
            line = 'from Utils.tools import * \n'
            lines_content.append(line)
            line = 'from Utils.collects import * \n'
            lines_content.append(line)
            line = 'from Utils.executes import *\n'
            lines_content.append(line)
            line = 'from Common.Api_Common.Scm_Api import *\n'
            lines_content.append(line)
            line = 'import traceback\n'
            lines_content.append(line)
            line = 'from requests.exceptions import RequestException'
            lines_content.append(line)
            lines_content.append('\n')
            lines_content.append('\n')
            line ='cookie = Scm_Api().get_cookie()\n'
            lines_content.append(line)
            lines_content.append('\n')
            lines_content.append('\n')
            line = 'class ' + class_name + '():\n'
            lines_content.append(line)
            lines_content.append('\n')
            fs.writelines(lines_content)
            fs.close()

        def set_api_content(self,api_name_list,file_name,key_name='name'):

            '''
            create api .py file
            '''
            fs = open(file_name, 'a', encoding='utf-8')
            #
            _tab_space = self.set_tab_space()
            _2tab_space = _tab_space + _tab_space
            _3tab_space = _tab_space + _tab_space+ _tab_space
            #
            service_path = project_vars().project_dir + '\\API\\' + process().service_name
            dir_name=os.path.dirname(file_name)
            relative_path = str(dir_name).replace(service_path,'')
            for i in range(len(api_name_list)):
                #
                lines_content = []
                api_name = str(api_name_list[i][key_name])
                #
                line = _tab_space + 'def ' + api_name + '(self, update_content={}):\n'
                lines_content.append(line)
                lines_content.append('\n')
                line = _2tab_space + 'yaml_file_name = ' + "'" + relative_path+'\\'+api_name + ".yml'\n"
                lines_content.append(line)
                line = _2tab_space + 'try:\n'
                lines_content.append(line)
                line = _3tab_space+'update_content = tools().dict_merge(update_content, cookie)\n'
                lines_content.append(line)
                line = _3tab_space+"result = execute().execute_process(yaml_file=yaml_file_name,update_content=update_content,folder_name='"+relative_path+"')\n"
                lines_content.append(line)
                line = _3tab_space+'status_code = response().get_response_status_code(result)\n'
                lines_content.append(line)
                line = _3tab_space+'assert status_code == 200\n'
                lines_content.append(line)
                line = _3tab_space+'body = response().get_response_body(result)\n'
                lines_content.append(line)
                line = _3tab_space+'body = json.loads(body)\n'
                lines_content.append(line)
                line = _3tab_space+'return body\n'
                lines_content.append(line)
                line = _2tab_space + 'except Exception as e:\n'
                lines_content.append(line)
                line = _3tab_space+'traceback.print_exc()\n'
                lines_content.append(line)
                line = _3tab_space+"raise ('execption =' + e)\n"
                lines_content.append(line)
                line = _2tab_space +'except BaseException as e:\n'
                lines_content.append(line)
                line = _3tab_space + 'traceback.print_exc()\n'
                lines_content.append(line)
                line = _3tab_space+"raise ('execption =' + e)\n"
                lines_content.append(line)
                line = _2tab_space + 'except RequestException as e:\n'
                lines_content.append(line)
                line = _3tab_space + 'traceback.print_exc()\n'
                lines_content.append(line)
                line = _3tab_space+"raise ('execption =' + e)\n"
                lines_content.append(line)
                line = _2tab_space +'except:\n'
                lines_content.append(line)
                line = _3tab_space + "return None\n"
                lines_content.append(line)
                lines_content.append('\n')
                lines_content.append('\n')
                fs.writelines(lines_content)
            fs.close()

        def set_process_header(self,file_name,process_name='process',prefix='test'):

            '''
            set process header info 
            '''
            post_fix = '_'+process_name
            base_name = os.path.basename(file_name)
            api_py_name= base_name.split('.')[0].replace(post_fix,'')
            class_name = prefix + '_' + base_name.split('.')[0]
            fs = open(file_name, 'w', encoding='utf-8')
            #
            _tab_space = self.set_tab_space()
            _2tab_space = _tab_space + _tab_space
            #import part
            lines_content=[]
            line = 'from Utils.tools import * \n'
            lines_content.append(line)
            line = 'from Utils.collects import * \n'
            lines_content.append(line)
            line = 'from Utils.executes import *\n'
            lines_content.append(line)
            line = 'from '+api_py_name +' import *\n'
            lines_content.append(line)
            lines_content.append('\n')
            lines_content.append('\n')

            # class part
            line = 'class ' + class_name + '():\n'
            lines_content.append(line)
            lines_content.append('\n')
            fs.writelines(lines_content)
            fs.close()

        def set_process_content(self,file_name,api_name_list,process_name='process',perfix='test',key_name='name'):

            '''
            set process content info for process.py
            '''
            if os.path.exists(file_name):

                base_name = os.path.basename(file_name)
                post_fix='_'+process_name
                api_class_name = api_py_name = base_name.split('.')[0].replace(post_fix,'')
                report_name = api_py_name + '_' + process_name + '.html'
                function_name =perfix+'_'+process_name
                fs = open(file_name, 'a', encoding='utf-8')
                _tab_space = self.set_tab_space()
                _2tab_space= _tab_space + _tab_space
                _3tab_space= _tab_space + _tab_space+ _tab_space
                lines_content=[]

                # process name
                line = _tab_space + 'def ' + function_name + '(self):\n'
                lines_content.append(line)
                lines_content.append('\n')

                line = _2tab_space + 'try:\n'
                lines_content.append(line)

                # test step
                for i in range(len(api_name_list)):
                    api_name = str(api_name_list[i][key_name])
                    line = _3tab_space+ api_class_name+'().'+api_name+'()\n'
                    lines_content.append(line)

                line = _2tab_space + 'except Exception as e:\n'
                lines_content.append(line)
                line = _3tab_space+'traceback.print_exc()\n'
                lines_content.append(line)
                line = _3tab_space+"raise ('execption =' + e)\n"
                lines_content.append(line)
                lines_content.append('\n')
                lines_content.append('\n')

                # main step
                line = 'if __name__ == "__main__":\n'
                lines_content.append(line)
                lines_content.append('\n')
                line =_tab_space+"execute().run_test('"+base_name+"', runner='pytest', pytest_report_name='"+report_name+"')\n"
                lines_content.append(line)
                fs.writelines(lines_content)
                fs.close()
            else:
                raise('can not find yaml file :',file_name)


        def set_process_py(self,yaml_file,process_name='process',yaml_folder_name='test'):

            '''
            set process py file
            '''
            yaml_data = process().read_ops().get_yaml_data(yaml_file)
            api_info = process().read_ops().get_api_info(yaml_data)
            api_name_list = self.get_api_name(api_info)
            #
            dir_path = os.path.dirname(yaml_file)
            file_name = os.path.basename(yaml_file).strip().split('.')[0]
            file_path= dir_path+'\\'+file_name+'_'+process_name+'.py'
            if os.path.exists(file_path):
                self.delete_file(file_path)
            #
            self.set_process_header(file_path,process_name)
            self.set_process_content(file_path,api_name_list,process_name)

        def get_count_dict(self, test_list):

            ''' 
            count list duplicate element info 
            '''
            if isinstance(test_list, list) and test_list != []:
                obj_count = Counter(test_list)
                test = {}
                for key, value in obj_count.items():
                    test[key] = value
                return test
            else:
                print(test_list + ' type is invalid')
                return None

        def set_api_info(self,yaml_data):

            '''
            set api info for apis in apy py file 
            '''
            api_info =process().read_ops().get_api_info(yaml_data)
            api_name_list=[]
            for api in api_info:
                api_name_list.append(api['name'])
            #
            api_count_info = self.reset_count_dict(api_name_list)
            #
            for i in api_info:
                if i['name'] in api_count_info.keys():
                    key = i['name']
                    total_num = api_count_info[key][0]
                    index_num= api_count_info[key][1]
                    if  index_num< total_num:
                        i['name']=i['name']+'_'+str(index_num)
                        api_count_info[key][1] = index_num+1
                else:
                    continue
            return api_info

        def reset_count_dict(self,test_list):
            
            '''
            get list count info 
            '''
            api_count_info = self.get_count_dict(test_list)
            result_list_count_info={}
            for key in api_count_info.keys():
                count_info = []
                count_info.append(api_count_info[key])
                count_info.append(0)
                result_list_count_info[key] = count_info
            return result_list_count_info

        def reset_list_info(self,test_list,postfix='_'):

            '''
            reset list by douplicate element count
            '''
            list_info = self.reset_count_dict(test_list)
            new_list_info = []
            for i in test_list:
                if i in list_info.keys():
                    key = i
                    total_num = list_info[key][0]
                    index_num = list_info[key][1]
                    if index_num < total_num:
                        test_i = i + str(postfix) + str(index_num)
                        list_info[key][1] = index_num + 1
                        new_list_info.append(test_i)
                else:
                    continue
            return new_list_info

        def reset_api_info(self,api_info,key_name='name'):

            '''
            reset api info by key_name
            '''
            key_name_list =[]
            for i in api_info:
                key_name_list.append(i[key_name])
            reset_api_name = process().write_ops().reset_list_info(key_name_list)

            for i in range(len(api_info)):
                api_info[i][key_name] = reset_api_name[i]

            return api_info

class test():

    def __init__(self):

        pass

    def test_yaml_data(self):


        file_name = 'C:\\Users\\user\\PycharmProjects\\python_api_test\\API\\Wms\\test\\Allocation_AutoAllocate.yml'
        test_process = process()
        yaml_data =  test_process.read_ops().get_yaml_data(file_name)
        print('yaml_data=',yaml_data)

    def test_set_test_folder(self):

        file_name = 'C:\\Users\\user\\PycharmProjects\\python_api_test\\API\\Wms\\test\\Allocation_AutoAllocate.yml'
        test_process = process()
        folder_path = test_process.write_ops().set_test_folder(file_name)
        print('folder_path=', folder_path)


    def test_set_api_yaml(self):

        file_name = 'C:\\Users\\user\\PycharmProjects\\python_api_test\\API\\Wms\\test\\Allocation_AutoAllocate.yml'
        test_process = process()
        test_process.write_ops().set_api_yaml(file_name)


    def test_set_api_py(self):

        file_name = 'C:\\Users\\user\\PycharmProjects\\python_api_test\\API\\Wms\\test\\Allocation_AutoAllocate.yml'
        test_process = process()
        test_process.write_ops().set_api_py(file_name)

    def test_prepare_process(self):

        file_name = 'C:\\Users\\user\\PycharmProjects\\python_api_test\\API\\Wms\\test\\Allocation_AutoAllocate.yml'
        test_process = process()
        test_process.write_ops().set_test_folder(file_name)
        test_process.write_ops().set_api_yaml(file_name)
        test_process.write_ops().set_api_py(file_name)
        test_process.write_ops().set_process_py(file_name)

    def test_list(self):

        list1 = ['1', '1', '2', '3', '4', '4', '5', '6', '6', '6', '6', '2', '1', '6', '4', '1']

        new_list_info= process().write_ops().reset_list_info(list1)
        print('new_list_info=',new_list_info)

    def example_2(self):

        api_info = [{'name': 'test1', 'info': 'test13'}, {'name': 'test', 'info': 'test232324'},
                    {'name': 'test1', 'info': 'ererfedsfdf'}, {'name': 'test2', 'info': 'ererfedsfdf'},
                    {'name': 'test', 'info': 'test13'}]
        print('api_info==',api_info)
        api_info_2 = process().write_ops().reset_api_info(api_info)
        print('api_info_2===',api_info_2)


if __name__ == "__main__":


    # test().example_2()
    # test().test_yaml_data()
    # test().test_set_test_folder()
    # test().test_set_api_yaml()
    # test().test_set_api_py()
    test().test_prepare_process()



