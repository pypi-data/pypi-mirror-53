import unittest
from cubicweb.devtools.testlib import AutomaticWebTest


class AutomaticWebTest(AutomaticWebTest):

    def to_test_etypes(self):
        return set(('Invoice', 'Account',))

    def list_startup_views(self):
        return ()


if __name__ == '__main__':
    unittest.main()
