import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EasyModbusSilaaCooling",
    version="1.0.4",
    author=["Alexander Teubert","Stefan Rossmann"],
    packages=["EasyModbusSilaaCooling"],
    description="A modification of the existing EasyModbus-package version 1.2.6 by Stefan Rossmann of Rossmann Engineering",
    url="https://gogs.es-lab.de/SilaaCooling/Simulationsmodell_SilaaCooling/src/master/Helios%20Modbus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
    ],
    python_requires='>=3.5.2',
    install_requires=['pyserial'],
)
