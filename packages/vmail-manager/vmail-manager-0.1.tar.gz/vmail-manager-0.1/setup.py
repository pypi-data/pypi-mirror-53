from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='vmail-manager',
    version='0.1',
    author='Dominik Rimpf',
    author_email='dev@d-rimpf.de',
    description='Handy cli interface to manage an vmail-sql-db.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/domrim/vmail-manager/',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'click',
        'sqlalchemy',
        'pymysql',
        'tabulate',
        'argon2_cffi',
        'confuse',
    ],
    entry_points='''
    [console_scripts]
    vmail-manager=vmail_manager:cli
    ''',
)