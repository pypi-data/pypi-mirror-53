from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lvs',
    version='1.0',
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=['opencv-python', 'click', 'toml', 'flask'],
    python_requires='>=3.7',
    entry_points='''
            [console_scripts]
            lvs=lvs.cli:cli
        ''',
    url='https://github.com/ksharshveer/lvs',
    license='MIT',
    author='Harshveer Singh',
    author_email='ksharshveer@gmail.com',
    description='Stream video from camera or video file to devices on your local network',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
