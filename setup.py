from setuptools import setup, find_namespace_packages

setup(
    name='bot-helper',
    version='2',
    description='Helper for work with phonebook',
    author='Gena Shpak',
    author_email='gena_shpak@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['bot-helper = bot_helper.main:main']}
)