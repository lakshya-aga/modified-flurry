import os
import sys
import argparse
import subprocess
from pathlib import Path
from termcolor import colored
import flake.src.flake as flake
import flake.src.flake.filters.camflow as camflow
import time

def print_provenance_menu(menu):
    for key in menu.keys():
        print(colored(str(str(key) + '--' + menu[key]), 'magenta'))

def print_attack_menu(menu):
    for key in menu.keys():
        print(colored(str(key + '--' + menu[key]), 'red'))

def print_benign_menu(menu):
    for key in menu.keys():
        print(colored(str(key + '--' + menu[key]), 'green'))

def read_input_file():
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", help="file path to automation script with arguments")
    args = parser.parse_args()
    cfg_txt = ""
    if args.script is not None:
        cfg_path = Path(os.getcwd() + "/" + args.script)
        if not cfg_path.is_file():
            print("Could not find the automation file; try again.")
            sys.exit()
        cfg_txt = open(cfg_path).read()
    return cfg_txt

def get_level(cfg_txt, cfg_lines, cfg_custom_count):
    prov_level = 1
    if cfg_txt == "":
        prov_level = int(input("Select provenance capture granularity: "))
        while prov_level < 1 or prov_level > 4:
            prov_level = int(input("Invalid option selected. Try again."))
    else:
        prov_level = int(cfg_lines[2 + cfg_custom_count])
        print(prov_level)
    return prov_level

def get_loops(cfg_txt, cfg_lines, cfg_custom_count):
    num_loops = 1
    if cfg_txt == "":
        num_loops = int(input("How many iterations would you like to make? "))
    else:
        num_loops = int(cfg_lines[1 + cfg_custom_count])
        print(num_loops)
    return num_loops

def run(scripts, actions, num_loops, level):
    i = 0
  
    filter = camflow.W3CFilter()
    database = flake.Bank(filter)
    time.sleep(3)
    
    while i < num_loops:
        '''
            Runs a list of scripts and gathers provenance on each one
        '''
        # time.sleep(2)
        graph = database.make_flake(actions)
        database.connect_mqtt_client(graph)
        
        if level == 1:
            subprocess.run(["sudo", "camflow", "-a", "true"])
        elif level == 2:
            subprocess.run(["sudo", "camflow", "--track-file", "/opt/lampp/bin/httpd", "true"])
        elif level == 3:
            subprocess.run(["sudo", "camflow", "--track-file", "/opt/google/chrome/chrome", "true"])
        elif level == 4:
            subprocess.run(["sudo", "camflow", "--track-file", "/opt/lampp/sbin/mysqld", "true"])
            subprocess.run(["sudo", "camflow", "--track-file", "/opt/lampp/bin/mysqld_safe", "true"])
        
        for script in scripts:
            try:
                print("running " + str(script))
                fileRead = open(script).read()
                exec(fileRead)
            except FileNotFoundError as e:
                print(e)
                print("Can't open " + str(script))
        
        time.sleep(2)
        database.disconnect_mqtt_client(graph)

        i += 1

def save_config(action_str, term_customs, num_loops, prov_level):
    fn = input("Enter filename to save this configuration (cwd = " + os.getcwd() + "; leave blank to not save config): ")
    fn=""
    if (fn != ""):
        f = open(fn, "w")
        f.write(action_str + "\n")
        for tc in term_customs:
            f.write(tc)
        f.write(str(num_loops) + "\n" + str(prov_level))
        f.close()
