from setuptools import setup

setup(
    name='gdirections',
    version='1.0',
    py_modules=['parse'],
    install_requires=[
        'click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        gdirections=parse:main
    ''',
)
