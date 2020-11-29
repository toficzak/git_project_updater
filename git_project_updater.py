#!/usr/bin/python3

import sys
import getopt
import os
import subprocess
import requests
from requests.auth import HTTPBasicAuth
import json
import configparser


def main(argv):

    # reading workdir location
    workingdir = ''
    config_file_location = ''
    try:
        opts, args = getopt.getopt(argv, "w:c:", ["w="])
    except getopt.GetoptError:
        print('git_project_updater.py -w <workingdir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('git_project_updater.py -i <inputfile>')
            sys.exit()
        elif opt in ("-w", "--w"):
            workingdir = arg
        elif opt in ("-c", "--c"):
            config_file_location = arg

    # reading config file
    config = configparser.ConfigParser()
    config.read(config_file_location)
    host = config['Basic']['jira_host']
    api = config['Basic']['api']
    login = config['Basic']['login']
    api_token = config['Basic']['api_token']

    # change working directory to git repo
    os.chdir(workingdir)

    # gather branches
    branches = subprocess.check_output(['git', 'branch']).decode(
        'ascii').replace("*", "").strip().split("\n")

    for branch in branches:
        stripped = branch.strip()
        sb = stripped.replace("feature/", "").replace("_", "-").upper()
        url = host + api + sb

        r = requests.get(url, auth=HTTPBasicAuth(
            login, api_token))
        if r.status_code == 200:
            json_data = json.loads(r.text)
            status = json_data['fields']['status']['name']
            summary = json_data['fields']['summary']
            command = 'git config branch.' + stripped + \
                '.description "' + url + ' | ' + \
                summary + ' [' + status + ']"'
            print(sb)
            os.system(command)


if __name__ == "__main__":
    main(sys.argv[1:])
