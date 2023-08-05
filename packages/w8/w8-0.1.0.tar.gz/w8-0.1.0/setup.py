from setuptools import find_packages, setup


setup(
    name='w8',
    version='0.1.0',

    entry_points={
        'console_scripts': [
            'w8 = w8.cli:main',
        ],
    },
    packages=find_packages(),
)
