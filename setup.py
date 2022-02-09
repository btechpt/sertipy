from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sertipy",  # Replace with your own username
    version="1.1.0",
    author="Boer Technology",
    author_email="dev@btech.id",
    description="Python library for the Sertiva Web API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/btechpt/sertipy",
    project_urls={
        "Bug Tracker": "https://github.com/btechpt/sertipy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires=">=3.6",
    packages=['sertipy'],
)
