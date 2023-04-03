#from pyfiglet import Figlet
import os
import host
import warnings
from pathlib import Path
import util.driversetup as ds
import subprocess as sp
import flake.src.flake as flake
import flake.src.flake.filters.camflow as camflow
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

#config options
SAVE_TO_DISK = True

#prov levels
provenance_levels = {
    1 : 'whole system',
    2 : 'HTTP server',
    3 : 'MySQL database',
    4 : 'Chrome browser',
}

## Start menu coding
attack_menu_options = {
    'xssstored': 'Execute XSS Stored Attack',
    'xssreflected': 'Execute XSS Reflected Attack',
    'xssdom': 'Execute XSS DOM Attack',
    'commandinjection': 'Execute Command Injection Attack',
    'sqlinjection': 'Execute SQL Injection Attack',
    'bruteforce': 'Execute Brute Force Attack',
    'customattack': 'Use My Own Attack'
}

benign_menu_options = {
    'message': 'Message Board Post (Benign version of XSS stored)',
    'submit': 'Complete a Questionnaire (Benign version of XSS reflected)',
    'query': 'Query a Webpage (Benign version of XSS DOM)',
    'ping': 'Ping Local Host (Benign version of command injection)',
    'databaseentry': 'Create a User ID (Benign version of SQL injection)',
    'login': 'Enter Username and Password (Benign version of brute force)',
    'custombehavior': 'Use My Own Custom Behavior'
}

def main():
    sp.call("./auto_start.sh")
    print("all ok")
    cfg_txt = host.read_input_file()
    cfg_lines = cfg_txt.split("\n")


    cfg_custom_count = 0
    try:
        if cfg_txt == "":
            host.print_attack_menu(attack_menu_options)
            host.print_benign_menu(benign_menu_options)
            action_str = input('Select one or more attacks to run in a comma-separated list: ')
        else:
            action_str = cfg_lines[0]
            print(action_str)
        actions = action_str.split(",")
        scripts = []
        term_customs = [] # For writing config files
        for action in actions:
            script = Path("")
            if action == "xssstored":
                script = Path(os.getcwd() + "/scripts/xssstored.py")
            elif action == "xssreflected":
                script = Path(os.getcwd() + "/scripts/xssreflected.py")
            elif action == "xssdom":
                script = Path(os.getcwd() + "/scripts/xssdom.py")
            elif action == "commandinjection":
                script = Path(os.getcwd() + "/scripts/commandinjection.py")
            elif action == "sqlinjection":
                script = Path(os.getcwd() + "/scripts/sqlinjection.py")
            elif action == "bruteforce":
                script = Path(os.getcwd() + "/scripts/bruteforce.py")
            elif action == "message":
                script = Path(os.getcwd() + "/scripts/messageboard.py")
            elif action == "submit":
                script = Path(os.getcwd() + "/scripts/questionnaire.py")
            elif action == "query":
                script = Path(os.getcwd() + "/scripts/pagequery.py")
            elif action == "ping":
                script = Path(os.getcwd() + "/scripts/commandlineping.py")
            elif action == "databaseentry":
                script = Path(os.getcwd() + "/scripts/databaseentry.py")
            elif action == "login":
                script = Path(os.getcwd() + "/scripts/singlelogin.py")
            elif action == "customattack" or action == "custombehavior":
                if cfg_txt == "":
                    local_path = ""
                    while (not script.is_file()):
                        local_path = input('Provide the local path to your custom script: ')
                        script = Path(os.getcwd() + "/" + local_path)
                        if (not script.is_file()):
                            print('Invalid file path provided. Try again.')
                    term_customs.append(local_path)
                    #action = str(input("Provide a single word identifier for this custom execution (i.e. \'bruteforce\')")).split(" ")[0]
                else:
                    cfg_custom_count += 1
                    script = Path(os.getcwd() + "/" + cfg_lines[cfg_custom_count])
            else:
                print('Invalid option ' + action + ' provided.')
            if script.is_file():
                scripts.append(script)
    except Exception as e:
        print(e)

    # Other options
    #host.print_provenance_menu(provenance_levels)
    prov_level = 1 #host.get_level(cfg_txt, cfg_lines, cfg_custom_count)
    num_loops = host.get_loops(cfg_txt, cfg_lines, cfg_custom_count)

    DRIVER = ds.setupDriver()

    host.run(scripts, actions, num_loops, prov_level)
    DRIVER.close()
    #if cfg_txt == "":
    #    host.save_config(action_str, term_customs, num_loops, prov_level)

main()
