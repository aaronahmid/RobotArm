import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(

    name="robotarm", # Replace with your username

    version="0.1.1",

    author="<Aaron Ahmid Balogun>",

    author_email="<amidbidee@gmail.com>",

    description="<Template Setup.py package>",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="<https://github.com/AmidBidee/RobotArm>",

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    install_requires=['gunicorn', 'flask', 'pyyaml', 'python-decouple', 'requests', 'psutil', 'tabulate'],
    package_dir={},
    packages=find_packages(
        where='.',
        include=['robotarm*'],  # ["*"] by default
        exclude=['robotarm.tests'],  # empty by default
    ),

    python_requires=">=3.6",

    py_modules=['arm'],

    entry_points={
    'console_scripts': [
        'arm=arm:main',
        #'start_arm=start_arm_api:main'
    ],
    },
    scripts=['robotarm/arm',
    #'robotarm/scripts/start_arm_api.py',
   ]

)

