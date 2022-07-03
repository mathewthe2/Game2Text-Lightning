from configparser import ConfigParser

class Config():
    def __init__(self, appctxt):
        self.config_file = appctxt.get_resource('config.ini')
        self.config_object = ConfigParser()

    def read(self, section_name, key):
        self.config_object.read(self.config_file, encoding='utf-8')
        section = self.config_object[section_name]
        return section[key]

    def write(self, section_name, to_update_dict):
        self.config_object.read(self.config_file, encoding='utf-8')
        section = self.config_object[section_name]

        # Update the key value
        for key, value in to_update_dict.items():
            section[key] = value

        # Write changes back to file
        with open(self.config_file, 'w', encoding='utf-8') as conf:
           self.config_object.write(conf)