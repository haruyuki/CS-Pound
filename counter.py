from datetime import datetime
from git import Repo
import json
import os
import re
import sys


def write_update():
    new_version = f'{data["version"]}.{data["build"]}'

    g = open('constants.py', 'r')
    lines = g.readlines()
    g.close()

    with open('constants.py', 'w') as g:
        version = re.findall(r'\d{1,4}\.\d{1,4}\.\d{1,3}', lines[10])
        if version:
            lines[10] = lines[10].replace(version[0], new_version)
        for line in lines:
            g.write(line)

    f.seek(0)
    json.dump(data, f, indent=2)
    return new_version


def add_and_commit(version):
    repo = Repo(os.getcwd())
    repo.git.add('constants.py')
    repo.git.add('counter.json')
    repo.git.add('counter.py')
    repo.git.commit('-S', '-m', f'Updated to version {version}')


if sys.argv[1] == 'startup':
    with open('counter.json', 'r+') as f:
        data = json.load(f)

        if data['version'] != datetime.today().strftime('%Y.%m%d'):
            changes_made = True
            data['version'] = datetime.today().strftime('%Y.%m%d')
            data['build'] = 0
        else:
            changes_made = False

        new_version = write_update()
        f.truncate()
        if changes_made:
            add_and_commit(new_version)

if sys.argv[1] == 'update':
    with open('counter.json', 'r+') as f:
        data = json.load(f)
        data['build'] += 1
        new_version = write_update()
        f.truncate()
        add_and_commit(new_version)
