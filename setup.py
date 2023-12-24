from setuptools import setup, find_namespace_packages

setup(
    name='bot-helper',
    version='2',
    description='Helper for work with phonebook',
    author='Gena Shpak',
    author_email='gena_shpak@ukr.net',
    license='MIT',
    packages=find_namespace_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['bot-helper2 = bot-helper.main:main']}
)