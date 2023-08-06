
from setuptools import setup, find_packages
from insprdcli.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='insprdcli',
    version=VERSION,
    description='Command-line interface into Inspired Platform',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Jeff Trudeau',
    author_email='jeff.trudeau@gmail.com',
    url='https://github.com/InspiredMember/inspired-cli',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'insprdcli': ['templates/*']},
    include_package_data=True,
    install_requires=[
        'insprd==0.0.2.dev20191004153925',
    ],
    entry_points="""
        [console_scripts]
        insprdcli = insprdcli.main:main
    """,
)
