# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['runrestic',
 'runrestic.commands',
 'runrestic.config',
 'runrestic.metrics',
 'runrestic.restic',
 'runrestic.runrestic',
 'runrestic.tools']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.0,<3.1', 'toml>=0.10,<0.11']

entry_points = \
{'console_scripts': ['runrestic = runrestic.commands.runrestic:main']}

setup_kwargs = {
    'name': 'runrestic',
    'version': '0.3.5',
    'description': 'A wrapper script for Restic backup software that inits, creates, prunes and checks backups',
    'long_description': '# Overview\n\nrunrestic is a simple Python wrapper script for the\n[Restic](https://restic.net/) backup software that initiates a backup,\nprunes any old backups according to a retention policy, and validates backups\nfor consistency. The script supports specifying your settings in a declarative\nconfiguration file rather than having to put them all on the command-line, and\nhandles common errors.\n\nHere\'s an example config file:\n\n```toml\nrepositories = [\n    "/tmp/restic-repo",\n    "sftp:user@host:/srv/restic-repo",\n    "s3:s3.amazonaws.com/bucket_name"\n    ]\n\n[environment]\nRESTIC_PASSWORD = "CHANGEME"\n\n[backup]\nsources = [\n    "/home",\n    "/var"\n    ]\n\n[prune]\nkeep-last =  3\nkeep-hourly =  5\n```\n\nFor a more comprehensive example see the [example.toml](https://github.com/andreasnuesslein/runrestic/blob/master/example.toml) or check the [schema.json](https://github.com/andreasnuesslein/runrestic/blob/master/runrestic/config/schema.json)\n\n# Getting started\n\nTo get up and running, first [install Restic](https://restic.net/#installation). \n\nTo install runrestic, run the following command to download and install it:\n\n```bash\nsudo pip3 install --upgrade runrestic\n```\n\nNote that your pip binary may have a different name than `pip3`. Make sure\nyou\'re using Python 3, as runrestic does not support Python 2.\n\nOnce you have `restic` and `runrestic` ready, you should put a config file in on of the scanned locations, namely:\n\n- /etc/runrestic.toml\n- /etc/runrestic/*example*.toml\n- ~/.config/runrestic/*example*.toml\n\nAfterwards, run \n\n```bash\nrunrestic init # to initialize all the repos in `repositories`\n\nrunrestic  # without actions will do: runrestic backup prune check\n# or\nrunrestic [action]\n```\n\n# Autopilot\n\nIf you want to run runrestic automatically, say once a day, the you can\nconfigure a job runner to invoke it periodically.\n\n### cron\n\nIf you\'re using cron, download the [sample cron file](https://raw.githubusercontent.com/andreasnuesslein/runrestic/master/sample/cron/runrestic).\nThen, from the directory where you downloaded it:\n\n```bash\nsudo mv runrestic /etc/cron.d/runrestic\nsudo chmod +x /etc/cron.d/runrestic\n```\n\n\n### systemd\n\nIf you\'re using systemd instead of cron to run jobs, download the [sample systemd service file](https://raw.githubusercontent.com/andreasnuesslein/runrestic/master/sample/systemd/runrestic.service)\nand the [sample systemd timer file](https://raw.githubusercontent.com/andreasnuesslein/runrestic/master/sample/systemd/runrestic.timer).\nThen, from the directory where you downloaded them:\n\n```bash\nsudo mv runrestic.service runrestic.timer /etc/systemd/system/\nsudo systemctl enable runrestic.timer\nsudo systemctl start runrestic.timer\n```\n\n\n# Thanks\nMuch of this project is copy and paste from [borgmatic](https://github.com/witten/borgmatic/).\n',
    'author': 'Andreas Nüßlein',
    'author_email': 'andreas@nuessle.in',
    'url': 'https://github.com/andreasnuesslein/runrestic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
