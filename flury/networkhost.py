#from pyfiglet import Figlet
import os
import host
import warnings
from pathlib import Path
import subprocess as sp

import flake.src.flake as flake
import flake.src.flake.filters.camflow as camflow


warnings.filterwarnings("ignore", category=DeprecationWarning)

#config options
SAVE_TO_DISK = True

#prov levels
provenance_levels = {
    1 : 'whole system'
}

## Start menu coding
attack_menu_options = {
    'synflood': 'Execute SYN Flood Attack',
    'dataexfil': 'Execute Data Exfiltration Attack',
    'backdoor': 'Execute Remote Code Execution Attack',
    'customattack': 'Use My Own Attack'
}

benign_menu_options = {
    'ping': 'Ping Local Host',
    'fileread': 'read file',
    'localexecution': 'Execute script locally',
    'custombehavior': 'Use My Own Custom Behavior'
}

def main():
    sp.call("./auto_start.sh")
    print("all ok")
    cfg_txt = host.read_input_file()
    cfg_lines = cfg_txt.split("\n")

    # Action getting
    cfg_custom_count = 0
    try:
        if cfg_txt == "":
            host.print_attack_menu(attack_menu_options)
            host.print_benign_menu(benign_menu_options)
            action_str = input('Select one or more attacks to run in a comma-separated list: ')
        else:
            action_str = cfg_lines[0]
            #print(action_str)
        actions = action_str.split(",")
        scripts = []
        term_customs = [] # For writing config files
        for action in actions:
            script = Path("")
            if action == "synflood":
                script = Path(os.getcwd() + "/scripts/synflood.py")
            elif action == "dataexfil":
                script = Path(os.getcwd() + "/scripts/dataexfil.py")
            elif action == "backdoor":
                script = Path(os.getcwd() + "/scripts/backdoor.py")
            elif action == "ping":
                script = Path(os.getcwd() + "/scripts/ping.py")
            elif action == "fileread":
                script = Path(os.getcwd() + "/scripts/fileread.py")
            elif action == "localexecution":
                script = Path(os.getcwd() + "/scripts/localexec.py")
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

    prov_level = 1
    num_loops = host.get_loops(cfg_txt, cfg_lines, cfg_custom_count)

    host.run(scripts, actions, num_loops, prov_level)
    # if cfg_txt == "":
    #     host.save_config(action_str, term_customs, num_loops, prov_level)

main()
