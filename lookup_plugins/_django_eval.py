from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.playbook.conditional import Conditional


class LookupModule(LookupBase):
    '''
    Simple lookup plugin to allow evaluating conditional expressions.
    '''

    def run(self, terms, variables=None, **kwargs):
        vars_copy = variables.copy() if variables else {}
        vars_copy.update(kwargs)
        cond = Conditional(loader=self._loader)
        cond.when = terms
        return [cond.evaluate_conditional(self._templar, vars_copy)]
