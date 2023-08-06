from setuptools import setup, find_packages

setup(
    name='sentinel5dl',
    version='0.2',
    description='Sentinel-5p Downloader',
    author='Emissions API Developers',
    license='MIT',
    url='https://github.com/emissions-api/sentinel5dl',
    packages=find_packages(),
    install_requires=['pycurl>=7.43.0'],
    long_description='This library provides easy access to data from the '
                     'European Space Agency\'s Sentinel 5P sattellite.',
    entry_points={
        'console_scripts': [
            'sentinel5dl = sentinel5dl.__main__:main'
        ]
    }
)
