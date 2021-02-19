from setuptools import find_packages
from distutils.core import setup

setup(
    name='adminpanel',
    version="1.0.0",
    author='Moritz Finke',
    author_email='moritz.finke@uni-wuerzburg.de',
    description=('Administrator panel and chat for enterprise-wide issue handling'),
    license='© 2021',
    include_package_data=True,
    packages=['adminpanel'], #find_packages(),
    entry_points={'console_scripts': [
        'cross-secrecy-servers=adminpanel.server:main',
    ]},
    install_requires=['tornado', 'apscheduler', 'python-lorem', 'pycairo', 'py-avataaars', 'names', 'pillow', 'markdown']
)
