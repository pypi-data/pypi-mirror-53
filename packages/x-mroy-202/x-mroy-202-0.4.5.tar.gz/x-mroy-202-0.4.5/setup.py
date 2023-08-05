from setuptools import setup, find_packages


setup(name='x-mroy-202',
    version='0.4.5',
    description='a data cache extend',
    url='https://github.com/Qingluan/x-mroy-1.git',
    author='Qing luan',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[ 'mroylib-min', "aiohttp_socks","asyncssh"],
    entry_points={
        'console_scripts': ['fshare=ashares.cmd:main']
    },

)
