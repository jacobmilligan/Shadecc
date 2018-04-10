from setuptools import setup, find_packages, Extension
from setuptools.command.install import install

import os
import shutil
import subprocess

location = os.path.abspath(os.path.dirname(__file__))


class CMakeBuild(install):
    def run(self):
        print('Installing with CMake')
        build_dir = os.path.join(location, 'cmake-build-release')
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.mkdir(build_dir)
        subprocess.call(['cmake', '..', '-DCMAKE_BUILD_TYPE=Release'], cwd=build_dir)
        subprocess.call(['cmake', '--build', '.', '--', '-j4'], cwd=build_dir)
        super().run()


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
    cmdclass=dict(install=CMakeBuild),
    entry_points={
        'console_scripts': ['shadecc = shadecc:main']
    }
)
