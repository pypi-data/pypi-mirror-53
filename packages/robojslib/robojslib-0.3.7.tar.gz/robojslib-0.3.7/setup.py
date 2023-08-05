import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robojslib",
    version="0.3.7",
    author="Andrea Gubellini",
    author_email="agubellini@yahoo.com",
    description="A simple RobotFramework keyword library written using Vanilla/Python",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andreagubellini/RoboJSLib",
    packages=["robojslib"],
    install_requires=['robotframework', 'robotframework-seleniumlibrary'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)