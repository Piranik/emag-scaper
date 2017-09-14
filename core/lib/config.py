import yaml

def get_config():
    try:
        with open("config-development.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        return cfg
    except IOError:
        print 'Cannot read config file'
