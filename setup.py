from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="arexecute",
    version="1.0.0",
    description="Record and execute actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jurrutiag/arexecute",
    author="Juan Urrutia",
    author_email="juan.urrutia.gandolfo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    install_requires=[
        "pynput", "pyautogui"
    ],
    entry_points={"console_scripts": ["arexecute=arexecute.__main__:main"]},
)
