# Считывание настроек DialogFlow
import json


def config():
    NAME_CONFIG_FILE = 'dialogflow_config.json'

    def read_config():
        with open(NAME_CONFIG_FILE, 'r') as read_file:
            config = json.load(read_file)
        return config
    
    def cons_config():
        return read_config()

    return cons_config


def token(config):
    return config()['connection']['token']


def session_id(config):
    return config()['connection']['session_id']


def lang(config):
    return config()['language']['lang']