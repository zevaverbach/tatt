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
    include_package_data=True,
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        transcribe=tatt.transcribe:cli
    ''',
        )
