from setuptools import setup, find_packages


with open('README.md') as file:
    long_description = file.read()

setup(
    name="tatt",
    version="0.958",
    py_modules=['tatt'],
    url='https://github.com/zevaverbach/tatt',
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
    long_description_content_type='text/markdown',
    long_description=long_description,
    entry_points='''
        [console_scripts]
        transcribe=tatt.transcribe:cli
    ''',
        )
