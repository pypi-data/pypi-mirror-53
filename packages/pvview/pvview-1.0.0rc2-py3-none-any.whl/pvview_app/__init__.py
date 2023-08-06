__package_name__        = u'pvview'
__description__         = u"display one or more EPICS PVs in a PyDM GUI window as a table"
__long_description__    = __description__

__author__              = u'Pete R. Jemian'
__email__               = u'jemian@anl.gov'
__institution__         = u"Advanced Photon Source"
__author_name__         = __author__
__author_email__        = __email__

__copyright__           = u'2009-2019, UChicago Argonne, LLC'
# __license_url__         = u''
__license__             = u'OPEN SOURCE LICENSE'
__url__                 = u'https://github.com/BCDA-APS/pvview/'
__download_url__        = __url__
__keywords__            = ['Python', 'Qt5', 'PyDM', 'EPICS']

from ._requirements import learn_requirements
__install_requires__ = learn_requirements()
del learn_requirements

__classifiers__ = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Science/Research',
            'License :: Free To Use But Restricted',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
                     ]

# as shown in the About box ...
__credits__ = u'author: ' + __author__
__credits__ += u'\nemail: ' + __email__
__credits__ += u'\ninstitution: ' + __institution__
__credits__ += u'\nURL: ' + __url__

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
