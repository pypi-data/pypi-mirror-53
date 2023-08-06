import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Automunge",
    version="2.67",
    author="Nicholas Teague",
    author_email="pitg888@gmail.com",
    description="A tool for automated data wrangling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Automunge/AutoMunge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
