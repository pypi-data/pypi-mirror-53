
from setuptools import setup, find_packages
import aioqs

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="aioqs",
    version=aioqs.__version__,
    author="Oleg Marin",
    author_email="wWolfovich@gmail.com",
    description="Async queue and scheduler with limit for number of simultaneous coroutines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wWolfovich/aioqs",
    packages=find_packages(),
    py_modules=['aioqs'],
    extras_require={
        "async_timeout":["async_timeout"],
        },
    python_requires='>=3.5.2',
    keywords="AIO async queue schedule",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
