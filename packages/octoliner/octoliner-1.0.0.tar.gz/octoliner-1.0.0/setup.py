import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="octoliner",
    version="1.0.0",
    description="Raspberry Pi library for working with Amperka Octoliner "
                "line sensor board",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/amperka/OctolinerPi/",
    author="Amperka LLC",
    author_email="dev@amperka.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["octoliner"],
    include_package_data=True,
    entry_points={"console_scripts": ["octoliner=octoliner.example:main"]},
)
