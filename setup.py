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
    # dependency_links=['https://github.com/zevaverbach/tatt#egg=package-0.1'],
    packages=['tatt'],
    entry_points='''
        [console_scripts]
        transcribe=tatt.transcribe:cli
    ''',
        )
