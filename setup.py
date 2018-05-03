from setuptools import setup, find_packages

import os

location = os.path.abspath(os.path.dirname(__file__))

setup(
    name='shadecc',
    version='0.1.0',
    description='Cross-compile GLSL-based shader code to HLSL, MSL, and GLSL byte-code and '
                'source code',
    author='Jacob Milligan',
    author_email='jacobpmilligan@gmail.com',
    packages=find_packages(),
    install_requires=['argparse', 'tqdm'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['shadecc = shadecc:main']
    }
)
