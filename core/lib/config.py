import yaml

def get_config():
    try:
        with open("env-development.yml", 'r') as config_file:
            cfg = yaml.load(config_file)
        return cfg
    except IOError:
        print 'Cannot read config file'
