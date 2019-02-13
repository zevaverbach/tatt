from setuptools import setup, find_packages


setup(
    name="tatt",
    version="0.1",
    py_modules=['tatt'],
    install_requires=[
        'Click',
        'awscli',
        'boto3',
        'requests',
        ],
    dependency_links=['https://github.com/zevaverbach/tatt#egg=package-0.1'],
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        transcribe=transcribe:cli
    ''',
        )
