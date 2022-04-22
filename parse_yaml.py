from Utils.tools import *
import os
from Utils.configs import *

def get_yaml_data(file_name):
    '''
    get yaml data content
    '''
    yaml_data = tools().read_yaml_file(file_name)
    return yaml_data


def filter_api(yaml_data):
    '''
    remove duplicate api by api name
    '''
    new_yaml_data = {}
    name_init = ''
    data_length_init=0
    new_yaml_data['config'] = yaml_data['config']
    new_yaml_data['teststeps'] = []
    total_items = len(yaml_data['teststeps'])
    print('total_items=', total_items)
    for i in range(total_items):
        name = yaml_data['teststeps'][i]['name']
        if 'data' in yaml_data['teststeps'][i]['request']:
            # by getting max length data and api name not duplicate
            data_length = len(yaml_data['teststeps'][i]['request']['data'])
            if name != name_init and data_length>=data_length_init:
                new_yaml_data['teststeps'].append(yaml_data['teststeps'][i])
                name_init = name
            else:
                continue
        else:
            #by name not duplicate
            # remove duplicate api name
            if name != name_init:
                new_yaml_data['teststeps'].append(yaml_data['teststeps'][i])
                name_init = name
            else:
                continue
    return new_yaml_data


def write_yaml_file(filename, yaml_data):
    '''
    write yaml data into yaml file
    '''
    return tools().write_yaml_file(filename, yaml_data)


def generate_yaml_files(yaml_file_path):
    '''
    generate yaml files
    '''
    config_info = {}
    child_file_dir = get_file_dir(yaml_file_path)
    # get yaml data content
    yaml_data = get_yaml_data(yaml_file_path)
    # remove duplicate apis from yaml data content
    yaml_data = filter_api(yaml_data)
    # prepare child yaml files
    config_info['config'] = yaml_data['config']
    total_items = len(yaml_data['teststeps'])
    for i in range(total_items):
        # child yaml data content
        child_yaml_data = {}
        api_name = yaml_data['teststeps'][i]['name']
        api_name_split = str(api_name).strip().split('/')
        # #2_#3 = api file name
        if len(api_name_split) == 4:
            child_file_name = api_name_split[2] + '_' + api_name_split[3] + '.yml'
        elif len(api_name_split) == 3:
            child_file_name = api_name_split[1] + '_' + api_name_split[2] + '.yml'
        else:
            child_file_name = api_name_split[0] + '_' + api_name_split[1] + '.yml'
        child_yaml_file_path = child_file_dir + '\\' + child_file_name
        child_yaml_data['config'] = config_info['config']
        child_yaml_data['teststeps'] = []
        # add cookies
        if 'cookies' not in yaml_data['teststeps'][i]['request'].keys():
            yaml_data['teststeps'][i]['request']['cookies'] = project_vars().cookie
        else:
            if 'SSID' not in yaml_data['teststeps'][i]['request']['cookies'].keys():
                yaml_data['teststeps'][i]['request']['cookies'] = project_vars().cookie
        child_yaml_data['teststeps'].append(yaml_data['teststeps'][i])
        # just save first validate data item
        child_yaml_data = save_first_validate(child_yaml_data)
        # write child yaml data into yaml files
        write_yaml_file(child_yaml_file_path, child_yaml_data)



def add_cookies(yaml_data):


    if 'cookies' not in yaml_data['teststeps'][0]['request'].keys():
        yaml_data['teststeps'][0]['request']['cookies']=project_vars().cookie
    else:
        if 'SSID' not in yaml_data['teststeps'][0]['request']['cookies'].keys():
            yaml_data['teststeps'][0]['request']['cookies']=project_vars().cookie
    #ignore https
    if 'verify' not in yaml_data['teststeps'][0]['request'].keys():
        yaml_data['teststeps'][0]['request']['verify']='false'

    return yaml_data

def get_file_dir(file_path):
    '''
    get files dir
    '''
    file_dir = os.path.dirname(os.path.realpath(file_path))

    return file_dir


def save_first_validate(yaml_data):
    '''
    remove validaters and just save status code
    '''
    target_validate_data = []
    source_validate_data = yaml_data['teststeps'][0]['validate']
    # just save first validate data item
    for i in range(1):
        target_validate_data.append(source_validate_data[i])
    yaml_data['teststeps'][0]['validate'] = target_validate_data
    return yaml_data


if __name__ == "__main__":
    # example
    yaml_file_path = 'C:\\Users\\user\\Downloads\\Test_TC1811290001_test\\Test_TC1811290001.yml'
    generate_yaml_files(yaml_file_path)
