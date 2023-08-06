from setuptools import setup, find_packages
from pandoc_compose import version

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as rqrmts:
    requirements = [l for l in rqrmts.readlines() if not l.strip().startswith("#") and len(l.strip()) > 0]

setup(
    name="PandocCompose",
    version=version,
    author="Christophe Henry",
    author_email="contact@c-henry.fr",
    description="PandocCompose lets you manage your documentation base using Pandoc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.feneas.org/christophehenry/pandoc-compose",
    project_urls={
        "Bug Tracker": "https://git.feneas.org/christophehenry/pandoc-compose/issues",
        "Documentation": "https://git.feneas.org/christophehenry/pandoc-compose/blob/master/DOCUMENTATION.md",
        "Source Code": "https://git.feneas.org/christophehenry/pandoc-compose",
    },
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: General",
    ],
    entry_points={"console_scripts": ["pandoc-compose=pandoc_compose.main:main"]},
)
