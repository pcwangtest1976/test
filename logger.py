import yaml
import logging.config
import os
from Utils.tools import *
from Utils.configs import *


class logger():

    def __init__(self):

        self.project_dir = project_vars().project_dir
        self.log_config = project_vars().log_config_file
        self.log_dir = project_vars().exec_dir
        self.info_log_name = 'info.log'
        self.error_log_name = 'errors.log'
        self.log_level = 'INFO'

    def setup_logging(self, default_path='logging.yaml', default_level=logging.INFO):

        path = default_path
        if not os.path.exists(path):
            path = self.log_config
        self.set_logger_config()
        with open(path, mode='r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logging.config.dictConfig(config)
        if default_level == '':
            logging.basicConfig(level=self.log_level)
        else:
            logging.basicConfig(level=default_level)
        return logging

    def set_logger_config(self):

        yaml_data = tools().read_yaml_file(self.log_config)
        if yaml_data != None and isinstance(yaml_data, dict):
            yaml_data['handlers']['info_file_handler']['filename'] = self.log_dir + '\\' + self.info_log_name
            yaml_data['handlers']['error_file_handler']['filename'] = self.log_dir + '\\' + self.error_log_name
            tools().write_yaml_file(self.log_config, yaml_data)
        else:
            print('can not find yaml file :', self.log_config)


if __name__ == "__main__":
    pass
