# pylint: disable=W0622
"""cubicweb-invoice application packaging information"""


modname = 'cubicweb_invoice'
distname = 'cubicweb-invoice'

numversion = (0, 9, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'Logilab'
author_email = 'contact@logilab.fr'
description = 'invoice component for the CubicWeb framework'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {'cubicweb': '>= 3.24.0'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python :: 3',
    'Programming Language :: JavaScript',
]
