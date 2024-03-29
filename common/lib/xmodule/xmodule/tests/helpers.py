"""
Utility methods for unit tests.
"""


import filecmp
from unittest.mock import Mock
import pprint

from path import Path as path
from xblock.reference.user_service import UserService, XBlockUser


def directories_equal(directory1, directory2):
    """
    Returns True if the 2 directories have equal content, else false.
    """
    def compare_dirs(dir1, dir2):
        """ Compare directories for equality. """
        comparison = filecmp.dircmp(dir1, dir2)
        if (len(comparison.left_only) > 0) or (len(comparison.right_only) > 0):
            return False
        if (len(comparison.funny_files) > 0) or (len(comparison.diff_files) > 0):
            return False
        for subdir in comparison.subdirs:
            if not compare_dirs(dir1 / subdir, dir2 / subdir):
                return False

        return True

    return compare_dirs(path(directory1), path(directory2))


def mock_render_template(*args, **kwargs):
    """
    Pretty-print the args and kwargs.

    Allows us to not depend on any actual template rendering mechanism,
    while still returning a unicode object
    """
    return pprint.pformat((args, kwargs)).encode().decode()


class StubMakoService:
    """
    Stub MakoService for testing modules that use mako templates.
    """

    def __init__(self, render_template=None):
        self._render_template = render_template or mock_render_template

    def render_template(self, *args, **kwargs):
        """
        Invokes the configured render_template method.
        """
        return self._render_template(*args, **kwargs)


class StubUserService(UserService):
    """
    Stub UserService for testing the sequence module.
    """

    def __init__(self, user=None, user_is_staff=False, anonymous_user_id=None, **kwargs):
        self.user = user or Mock(name='StubUserService.user')
        self.user_is_staff = user_is_staff
        self.anonymous_user_id = anonymous_user_id
        super().__init__(**kwargs)

    def get_current_user(self):
        """
        Implements abstract method for getting the current user.
        """
        user = XBlockUser()
        if self.user.is_authenticated:
            user.opt_attrs['edx-platform.anonymous_user_id'] = self.anonymous_user_id
            user.opt_attrs['edx-platform.user_is_staff'] = self.user_is_staff
            user.opt_attrs['edx-platform.user_id'] = self.user.id
            user.opt_attrs['edx-platform.username'] = self.user.username
        else:
            user.opt_attrs['edx-platform.username'] = 'anonymous'
            user.opt_attrs['edx-platform.is_authenticated'] = False
        return user
