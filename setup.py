import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name="robotarm", # Replace with your username

    version="0.0.3",

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

    install_requires=['gunicorn', 'flask', 'pyyaml', 'python-decouple', 'requests'],
    package_dir={"": "robotarm"},
    packages=setuptools.find_packages(
        where='.',
        include=['robotarm*'],  # ["*"] by default
        exclude=['robotarm.tests'],  # empty by default
    ),

    python_requires=">=3.6",

    py_modules=['arm', 'robotarm', 'controllers', 'handlers', 'armservice'],

    entry_points={
    'console_scripts': [
        'arm=Robot-Arm.robotarm.arm:main',
    ],
},

)

