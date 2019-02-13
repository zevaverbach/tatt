from setuptools import setup, find_packages


with open('README.md') as file:
    long_description = file.read()

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
    description=('Tatt creates a uniform API for multiple speech-to-text '
                 '(STT) services.'),
    long_description=long_description,
    entry_points='''
        [console_scripts]
        transcribe=tatt.transcribe:cli
    ''',
        )
