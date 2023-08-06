from setuptools import setup

setup(
    name='jarbas_house',
    version='0.1.3',
    packages=['jarbas_house', 'jarbas_house.colors', 'jarbas_house.devices', 'jarbas_house.devices.tplink',
              'jarbas_house.devices.ewelink', 'jarbas_house.devices.magic_home'],
    url='',
    install_requires=[
        "webcolors",
        "simpleKasa",
        "requests",
        "websocket-client==0.54.0",
        "python-nmap",
        "pybluez"
    ],
    license='MIT',
    author='jarbasai',
    author_email='jarbasai@mailfence.com',
    description='tools to control my iot devices'
)
