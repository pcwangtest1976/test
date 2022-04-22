from Utils.configs import *


def get_yaml_api(file_dir=''):
    '''
    get api yaml file list
    '''
    if os.path.exists(file_dir):
        # list *.yml
        yaml_file_list = []
        file_names = os.listdir(file_dir)
        for name in file_names:
            if name.endswith('.yml'):
                yaml_file_list.append(name)
        return yaml_file_list
    else:
        raise ('can not get files list as file dir' + file_dir + ' does not exist')


def create_api_file(file_name='', yaml_file_list=None):
    '''
    create api .py file
    '''
    # clean/create an empty file
    if yaml_file_list == None:
        yaml_file_list = []
    clean_file_content(file_name)
    #
    fs = open(file_name, 'a', encoding='utf-8')
    #
    _tab_space = get_tab_space()
    _2tab_space = _tab_space + _tab_space
    for i in range(len(yaml_file_list)):
        lines_content = []
        api_name = str(yaml_file_list[i])[:-4]
        line = _tab_space + 'def ' + api_name + '(self, update_content={}):\n'
        lines_content.append(line)
        lines_content.append('\n')
        line = _2tab_space + 'yaml_file_name = ' + "'" + api_name + ".yml'\n"
        lines_content.append(line)
        line = _2tab_space + 'update_content = tools().dict_merge(update_content, cookie)\n'
        lines_content.append(line)
        line = _2tab_space + 'result = execute().execute_process(yaml_file=yaml_file_name,update_content=update_content,folder_name=self.service_dir_name)\n'
        lines_content.append(line)
        line = _2tab_space + 'status_code = response().get_response_status_code(result)\n'
        lines_content.append(line)
        line = _2tab_space + 'assert status_code == 200\n'
        lines_content.append(line)
        line = _2tab_space + 'body = response().get_response_body(result)\n'
        lines_content.append(line)
        line = _2tab_space + 'body = json.loads(body)\n'
        lines_content.append(line)
        line = _2tab_space + 'return body\n'
        lines_content.append(line)
        lines_content.append('\n')
        lines_content.append('\n')
        fs.writelines(lines_content)
    fs.close()


def get_tab_space(tab=''):
    '''
    create tab space
    '''
    if tab == '':
        return '    '
    else:
        return tab


def clean_file_content(file_name):
    # clean api.py file
    if os.path.exists(file_name):
        print(file_name + 'does not exist and create a empty file now')
    fs = open(file_name, 'w', encoding='utf-8')
    fs.write('')
    fs.close()


if __name__ == "__main__":
    # example
    project_dir = project_vars().project_dir
    yaml_file_dir = 'C:\\Users\\user\\PycharmProjects\\python_api_test\\API\\Wms\\Test_TC1811290001'
    api_yaml_list = get_yaml_api(yaml_file_dir)
    file_name = project_dir+'/API/Wms/Test_TC1811290001/Test_TC1811290001_Api.py'
    create_api_file(file_name, api_yaml_list)
