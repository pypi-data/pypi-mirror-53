"""Common information for checkers.
"""

import socket
import logging
import os
import typing

from ox_update.checking import noters


class CheckerConfig:
    """Configuration object for ox_update.


    """

    def __init__(self, updated_age_in_days: float = 7,
                 dynamic: dict = None, notifiers: str = 'echo', **kwargs):
        self.updated_age_in_days = updated_age_in_days
        self.dynamic = dynamic if dynamic else {}
        self.notifiers = notifiers.split('/')
        info = self.options()
        for dirty_name, value in kwargs.items():
            name = dirty_name
            if name not in info:
                name = dirty_name.upper().replace('-', '_')
            if name not in info:
                raise ValueError(f'Unknown config "{name}"')
            if name in self.dynamic:
                raise ValueError(f'Duplicate values given for {name}')
            self.dynamic[name] = value

    @staticmethod
    def options() -> typing.Dict[str, typing.Dict]:
        "Return dictionary of options for config."

        info = {
            'notifiers': {
                'default': 'echo',
                'help': ('A slash separated notifiers (e.g., echo/email '
                         'or email/telegram) for notifiers to use.')},
            'age-in-days': {
                'default': 7,
                'type': float,
                'help': ('Age in days allowed since "apt get update". '
                         'Will raise error if too old.')},
            'SENTRY': {
                'default': os.getenv('SENTRY_DSN'),
                'help': ('Optional Sentry DSN if you want error reporting '
                         'via sentry.')
                },
            'OX_UPDATE_EMAIL_TO': {
                'default': None,
                'help': ('Dynamic option for email address to notify. '
                         'Should be a comma separated group of email '
                         'addresses (e.g., foo@examle.com or a@b.c,d@e.f).'
                         'If not set, will lookup from environment.')
                },
            'OX_UPDATE_EMAIL_FROM': {
                'default': None,
                'help': ('Dynamic option for email address to notify from. '
                         'If not set, will lookup from environment.')
                },
            'OX_UPDATE_GMAIL_PASSWD': {
                'default': None,
                'help': ('Dynamic option for gmail password. '
                         'If provided and email notifier is requested, will '
                         'use this to send email via gmail. '
                         'If not set, will lookup from environment.')
                },
            'OX_UPDATE_SES_PROFILE': {
                'default': None,
                'help': ('Dynamic option for AWS SES profile for email. '
                         'If provided and email notifier is requested, will '
                         'use this to send email via AWS SES. '
                         'If not set, will lookup from environment.')
                },
            }

        return info

    def get_config_for(self, name: str, allow_none: bool = False):
        """Get configuration value for given name.

        :param name:     String name for which we want config value for.

        :param allow_none=False:  If True, allow returning None on failure,
                                  otherwise an exception is raised.

        ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

        :return:  Value of desired config option.

        ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

        PURPOSE:  Loookup config option either from self.dynamic or from
                  environment.

        """
        result = self.dynamic.get(name, None)
        if result is not None:
            return result
        result = os.environ.get(name, None)
        if result is not None:
            return result
        if allow_none:
            return None
        raise ValueError('Could not find name %s in config or env' % name)


class GenericPackageInfo:
    """Generic information about a package.
    """

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def __str__(self):
        return '%s: %s' % (self.name, self.version)


class OxUpdateException(Exception):
    """Base class for ox_update exceptions to catch and report.
    """


class NeedAptUpdate(OxUpdateException):
    """Exception for when apt update has not been run recently enough.
    """

    def __init__(self, fname, age_in_days, req_age_in_days, *args, **kwargs):
        msg = 'Apt file has age of %.1f days > required %.1f days: %s' % (
            age_in_days, req_age_in_days, fname)
        super().__init__(msg, *args, **kwargs)


class Checker:
    """Basic checker class.

This is an abstract class which you must-subclass. The main method in
this class is the `check` method which checks if there are pending
security updates to install and notifies based on this.
    """

    def __init__(self, config: CheckerConfig = None):
        self.config = config if config is not None else CheckerConfig()

    def check_repo_updated_recently(self):
        """Check if the package repository has been updated recently.

Should use self.config.age_in_days. Sub-classes must implement.
        """
        raise NotImplementedError

    def check_updates(self):
        """Check if there are packages we need to update.

Sub-classes must implement.
        """
        raise NotImplementedError

    def filter_security_updates(self, update_info) -> typing.List[
            GenericPackageInfo]:
        """Take result of check_updates and filter to security updates.

Returns a list of GenericPackageInfo representing pending security updates.
        """
        raise NotImplementedError

    def check(self):
        """Check if there are security packages to update.

        ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

        PURPOSE:   Check if there are security packages to update.
                   If so, notify based on self.config.notifiers.

        """
        try:
            self.check_repo_updated_recently()
            update_info = self.check_updates()
            pkg_info = self.filter_security_updates(update_info)
            self.warn_uninstalled(pkg_info)
            return update_info
        except OxUpdateException as ox_prob:
            logging.error('Got error: %s; will attempt to notify', ox_prob)
            self.notify('Error: ox_update failed',
                        'Error: ox_update failed:\n%s' % str(ox_prob))
            raise

    def notify(self, subject: str, msg: str):
        """Notify for given subject and message.

        :param subject:   String subject for notification.

        :param msg:       String message for notification.

        ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

        PURPOSE:  Go through all notifiers in self.config.notifiers and
                  send the given notification message.
        """
        for ntype in self.config.notifiers:
            my_noter = noters.make_notifier(ntype, self.config)
            my_noter.send(subject, msg)

    def make_details(self):
        """Make dictionary of details for current system.
        """
        data = {
            'uname': os.uname(),
            'hostname': socket.gethostname(),
            'OX_UPDATE_DETAILS': str(self.config.get_config_for(
                'OX_UPDATE_DETAILS', True)),
            }
        data['ip'] = socket.gethostbyname(data['hostname'])
        return data

    def warn_uninstalled(self, pkg_info: typing.List[
            GenericPackageInfo]) -> str:
        """Warn about uninstalled packages.

        :param pkg_info:   List of GenericPackageInfo to warn about.

        ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

        :return:  String notification message.

        ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

        PURPOSE:  Send notifications for packages in `pkg_info`.

        """
        if not pkg_info:
            return 'No packages need updating.'
        subject = 'Found %i uninstalled packges' % len(pkg_info)
        details = self.make_details()
        msg = 'Found %i uninstalled packges:\n%s\n--------------\n%s' % (
            len(pkg_info), '\n'.join([str(item) for item in pkg_info]),
            details)
        self.notify(subject, msg)
        return msg
