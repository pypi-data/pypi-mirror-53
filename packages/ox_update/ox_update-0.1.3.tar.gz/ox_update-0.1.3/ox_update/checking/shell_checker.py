"""Module for checking things using shell commands.

The following illustrates some example usage:

>>> from ox_update.checking import shell_checker
>>> chk = shell_checker.SimpleShellChecker()
>>> chk.config.notifiers = ['loginfo']  # so doctest works better
>>> data = chk.check()  # run the checks
>>> data.returncode     # verify return code succesful
0
"""

import logging
import time
import os
import re
import subprocess

from ox_update.checking import common


class SimpleShellChecker(common.Checker):
    """Version of checker using shell commands.
    """

    sec_re = re.compile('^Inst.*securi')
    update_success_file = '/var/lib/apt/periodic/update-success-stamp'

    def filter_security_updates(self, update_info):
        result = []
        lines = update_info.stdout.decode('utf8').split('\n')
        for item in lines:
            if not self.sec_re.match(item):
                logging.debug('"%s" since not security update; skip', item)
                continue
            sitem = item.split(' ')
            result.append(common.GenericPackageInfo(
                sitem[1], sitem[2].lstrip('[').rstrip(']')))
        return result

    def check_repo_updated_recently(self):
        info = os.stat(self.update_success_file)
        age_in_seconds = time.time() - info.st_mtime
        age_in_days = age_in_seconds / 86400.0
        if age_in_days > float(self.config.updated_age_in_days):
            raise common.NeedAptUpdate(self.update_success_file, age_in_days,
                                       self.config.updated_age_in_days)

    def check_updates(self):

        cmd = ['apt-get', '-s', 'dist-upgrade']
        proc = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        return proc
