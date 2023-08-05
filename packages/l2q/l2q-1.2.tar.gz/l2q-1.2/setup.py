from setuptools import setup

setup(
    name='l2q',
    keywords='query builder',
    version='1.2',
    author='Sam Holland',
    author_email='sam.h@xewli.com',
    descriptiom='Concatenates a list of terms into a single boolean OR query',
    url='https://github.com/Samuar/l2q',
    license='GPLv3+',
    platforms=['any'],
    packages=['l2q'],
    download_url='https://github.com/Samuar/l2q/archive/v1.2.tar.gz',
    install_requires=[
        'pandas', 'xlrd', 'python-docx'
    ],
    entry_points={
        'console_scripts': [
            'l2q = l2q.__main__:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
)
