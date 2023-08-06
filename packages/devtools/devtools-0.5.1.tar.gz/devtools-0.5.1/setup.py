from importlib.machinery import SourceFileLoader
from pathlib import Path
from setuptools import setup

THIS_DIR = Path(__file__).resolve().parent
long_description = THIS_DIR.joinpath('README.rst').read_text()

# avoid loading the package before requirements are installed:
version = SourceFileLoader('version', 'devtools/version.py').load_module()

setup(
    name='devtools',
    version=str(version.VERSION),
    description='Dev tools for python',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Environment :: MacOS X',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author='Samuel Colvin',
    author_email='s@muelcolvin.com',
    url='https://github.com/samuelcolvin/python-devtools',
    license='MIT',
    packages=['devtools'],
    python_requires='>=3.5',
    extras_require={
        'pygments': ['Pygments>=2.2.0'],
    },
    zip_safe=True,
)
