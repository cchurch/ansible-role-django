# Ansible
from ansible.plugins.filter.core import combine
from ansible.plugins.filter.mathstuff import zip


def _django_zipmerge(*args, **kwargs):
    return map(lambda x: combine(*x, **kwargs), zip(*args))


class FilterModule(object):

    def filters(self):
        return {
            '_django_zipmerge': _django_zipmerge,
        }
