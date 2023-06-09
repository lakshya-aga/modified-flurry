import configparser
import os
import sys

configp = configparser.ConfigParser()
config_path = '/home/shah/flurry/flake/src/flake/flake.ini'
configp.read(config_path)

# check if the path is to a valid file
if not os.path.isfile(config_path):
    print("Invalid configuration path provided.")
    sys.exit()

def initFromConfig(param):
    for section in configp.sections():
        if configp.has_option(section, param):
            return configp[section][param]
    print("Error initializing " + str(param) + "from config. Parameter not found.")
    sys.exit()
