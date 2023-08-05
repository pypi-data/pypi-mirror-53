from setuptools import setup, find_packages

with open('README', 'r') as f:
    long_description = f.read()

test_dependencies = [
        'mock',
        'future',
        ]

setup(
        name='taler-util',
        version='0.6.0rc2',
        license='LGPL3+',
        platforms='any',
        author='Taler Systems SA',
        author_email='ng0@taler.net',
        description='Util library for GNU Taler',
        long_description=long_description,
        url='https://git.taler.net/taler-util.git',
        packages=find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.1',
        test_suite='tests',
        tests_require=test_dependencies,
)
