from setuptools import setup


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
    entry_points='''
        [console_scripts]
        transcribe=transcribe:cli
    ''',
        )
