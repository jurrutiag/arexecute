from setuptools import setup, find_packages

setup(
    name="arexecute",
    version="0.0.1",
    description="Record and execute actions",
    long_description=README,
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