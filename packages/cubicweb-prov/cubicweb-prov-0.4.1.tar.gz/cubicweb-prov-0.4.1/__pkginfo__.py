# pylint: disable=W0622
"""cubicweb-prov application packaging information"""

modname = 'prov'
distname = 'cubicweb-prov'

numversion = (0, 4, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'The PROV Ontology'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {'cubicweb': '>= 3.24.0'}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
