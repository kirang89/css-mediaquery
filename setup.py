import codecs
import os
import sys

from setuptools import setup

sys.path.append('/Users/CongWeilin/anaconda2/lib/python2.7/site-packages')

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, 'cssmediaquery', '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name='cssmediaquery',
    version=about['__version__'],
    packages=['cssmediaquery'],
    description='CSS Media Query parser and matcher',
    long_description=long_description,
    license='MIT',
    author='Kiran Gangadharan',
    author_email='me@kirang.in',
    url='http://github.com/kirang89/css-mediaquery',
    install_requires=[''],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
    keywords='python, css, media query'
)
