# importing stuff for python launch file
import os
from glob import glob 

from setuptools import find_packages, setup

package_name = 'launch_substitution'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # tells python to take the files inside the launch folder and copy them to the install folder so that the launch files can be executed
        (os.path.join('share',package_name,'launch'),glob('launch/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='avi',
    maintainer_email='example@gmail.com',
    description='creating launch file with substitution',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
